> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoreo

> Aprende cómo habilitar y configurar OpenTelemetry para Claude Code.

Rastrea el uso de Claude Code, costos y actividad de herramientas en toda tu organización exportando datos de telemetría a través de OpenTelemetry (OTel). Claude Code exporta métricas como datos de series temporales a través del protocolo estándar de métricas, eventos a través del protocolo de registros/eventos, y opcionalmente trazas distribuidas a través del [protocolo de trazas](#traces-beta). Configura tus backends de métricas, registros y trazas para que coincidan con tus requisitos de monitoreo.

## Inicio rápido

Configura OpenTelemetry usando variables de entorno:

```bash theme={null}
# 1. Habilitar telemetría
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Elegir exportadores (ambos son opcionales - configura solo lo que necesites)
export OTEL_METRICS_EXPORTER=otlp       # Opciones: otlp, prometheus, console, none
export OTEL_LOGS_EXPORTER=otlp          # Opciones: otlp, console, none

# 3. Configurar punto final OTLP (para exportador OTLP)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Establecer autenticación (si es requerida)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Para depuración: reducir intervalos de exportación
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 segundos (predeterminado: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 segundos (predeterminado: 5000ms)

# 6. Ejecutar Claude Code
claude
```

<Note>
  Los intervalos de exportación predeterminados son 60 segundos para métricas y 5 segundos para registros. Durante la configuración, es posible que desees usar intervalos más cortos para propósitos de depuración. Recuerda restablecer estos valores para uso en producción.
</Note>

Para opciones de configuración completas, consulta la [especificación de OpenTelemetry](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Configuración del administrador

Los administradores pueden configurar los ajustes de OpenTelemetry para todos los usuarios a través del [archivo de configuración administrada](/es/settings#settings-files). Esto permite el control centralizado de los ajustes de telemetría en toda una organización. Consulta la [precedencia de configuración](/es/settings#settings-precedence) para obtener más información sobre cómo se aplican los ajustes.

Ejemplo de configuración de ajustes administrados:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  Los ajustes administrados pueden distribuirse a través de MDM (Mobile Device Management) u otras soluciones de gestión de dispositivos. Las variables de entorno definidas en el archivo de configuración administrada tienen alta precedencia y no pueden ser anuladas por los usuarios.
</Note>

## Detalles de configuración

### Variables de configuración comunes

| Variable de Entorno                                 | Descripción                                                                                                                                                                                                                                                                                                                                                                                          | Valores de Ejemplo                                                                                                                    |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Habilita la recopilación de telemetría (requerido)                                                                                                                                                                                                                                                                                                                                                   | `1`                                                                                                                                   |
| `OTEL_METRICS_EXPORTER`                             | Tipos de exportador de métricas, separados por comas. Usa `none` para deshabilitar                                                                                                                                                                                                                                                                                                                   | `console`, `otlp`, `prometheus`, `none`                                                                                               |
| `OTEL_LOGS_EXPORTER`                                | Tipos de exportador de registros/eventos, separados por comas. Usa `none` para deshabilitar                                                                                                                                                                                                                                                                                                          | `console`, `otlp`, `none`                                                                                                             |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protocolo para exportador OTLP, se aplica a todas las señales                                                                                                                                                                                                                                                                                                                                        | `grpc`, `http/json`, `http/protobuf`                                                                                                  |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | Punto final del recopilador OTLP para todas las señales                                                                                                                                                                                                                                                                                                                                              | `http://localhost:4317`                                                                                                               |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protocolo para métricas, anula la configuración general                                                                                                                                                                                                                                                                                                                                              | `grpc`, `http/json`, `http/protobuf`                                                                                                  |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | Punto final de métricas OTLP, anula la configuración general                                                                                                                                                                                                                                                                                                                                         | `http://localhost:4318/v1/metrics`                                                                                                    |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protocolo para registros, anula la configuración general                                                                                                                                                                                                                                                                                                                                             | `grpc`, `http/json`, `http/protobuf`                                                                                                  |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | Punto final de registros OTLP, anula la configuración general                                                                                                                                                                                                                                                                                                                                        | `http://localhost:4318/v1/logs`                                                                                                       |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Encabezados de autenticación para OTLP                                                                                                                                                                                                                                                                                                                                                               | `Authorization=Bearer token`                                                                                                          |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Clave de cliente para autenticación mTLS                                                                                                                                                                                                                                                                                                                                                             | Ruta al archivo de clave de cliente                                                                                                   |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Certificado de cliente para autenticación mTLS                                                                                                                                                                                                                                                                                                                                                       | Ruta al archivo de certificado de cliente                                                                                             |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Intervalo de exportación en milisegundos (predeterminado: 60000)                                                                                                                                                                                                                                                                                                                                     | `5000`, `60000`                                                                                                                       |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Intervalo de exportación de registros en milisegundos (predeterminado: 5000)                                                                                                                                                                                                                                                                                                                         | `1000`, `10000`                                                                                                                       |
| `OTEL_LOG_USER_PROMPTS`                             | Habilitar registro del contenido del mensaje del usuario (predeterminado: deshabilitado)                                                                                                                                                                                                                                                                                                             | `1` para habilitar                                                                                                                    |
| `OTEL_LOG_TOOL_DETAILS`                             | Habilitar registro de parámetros de herramientas e argumentos de entrada en eventos de herramientas y atributos de span de traza: comandos Bash, nombres de servidor MCP y herramienta, nombres de habilidades, e entrada de herramienta. También habilita nombres de comandos personalizados, de plugin y MCP en eventos `user_prompt` (predeterminado: deshabilitado)                              | `1` para habilitar                                                                                                                    |
| `OTEL_LOG_TOOL_CONTENT`                             | Habilitar registro de contenido de entrada y salida de herramientas en eventos de span (predeterminado: deshabilitado). Requiere [trazas](#traces-beta). El contenido se trunca en 60 KB                                                                                                                                                                                                             | `1` para habilitar                                                                                                                    |
| `OTEL_LOG_RAW_API_BODIES`                           | Emitir el cuerpo completo de solicitud y respuesta JSON de la API de Mensajes de Anthropic como eventos de registro `api_request_body` / `api_response_body` (predeterminado: deshabilitado). Los cuerpos incluyen el historial de conversación completo. Habilitar esto implica consentimiento a todo lo que `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, y `OTEL_LOG_TOOL_CONTENT` revelarían | `1` para cuerpos en línea truncados en 60 KB, o `file:<dir>` para cuerpos sin truncar en disco con un puntero `body_ref` en el evento |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Preferencia de temporalidad de métricas (predeterminado: `delta`). Establece en `cumulative` si tu backend espera temporalidad acumulativa                                                                                                                                                                                                                                                           | `delta`, `cumulative`                                                                                                                 |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Intervalo para actualizar encabezados dinámicos (predeterminado: 1740000ms / 29 minutos)                                                                                                                                                                                                                                                                                                             | `900000`                                                                                                                              |

### Control de cardinalidad de métricas

Las siguientes variables de entorno controlan qué atributos se incluyen en las métricas para gestionar la cardinalidad:

| Variable de Entorno                 | Descripción                                                         | Valor Predeterminado | Ejemplo para Deshabilitar |
| ----------------------------------- | ------------------------------------------------------------------- | -------------------- | ------------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Incluir atributo session.id en métricas                             | `true`               | `false`                   |
| `OTEL_METRICS_INCLUDE_VERSION`      | Incluir atributo app.version en métricas                            | `false`              | `true`                    |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Incluir atributos user.account\_uuid y user.account\_id en métricas | `true`               | `false`                   |

Estas variables ayudan a controlar la cardinalidad de las métricas, lo que afecta los requisitos de almacenamiento y el rendimiento de las consultas en tu backend de métricas. Una cardinalidad más baja generalmente significa mejor rendimiento y costos de almacenamiento más bajos, pero datos menos granulares para el análisis.

### Trazas (beta)

Las trazas distribuidas exportan spans que vinculan cada mensaje del usuario a las solicitudes de API y ejecuciones de herramientas que desencadena, para que puedas ver una solicitud completa como una única traza en tu backend de trazas.

Las trazas están deshabilitadas por defecto. Para habilitarlas, establece tanto `CLAUDE_CODE_ENABLE_TELEMETRY=1` como `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, luego establece `OTEL_TRACES_EXPORTER` para elegir dónde se envían los spans. Las trazas reutilizan la [configuración OTLP común](#common-configuration-variables) para punto final, protocolo y encabezados.

| Variable de Entorno                   | Descripción                                                                              | Valores de Ejemplo                   |
| ------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Habilitar trazas de span (requerido). `ENABLE_ENHANCED_TELEMETRY_BETA` también se acepta | `1`                                  |
| `OTEL_TRACES_EXPORTER`                | Tipos de exportador de trazas, separados por comas. Usa `none` para deshabilitar         | `console`, `otlp`, `none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | Protocolo para trazas, anula `OTEL_EXPORTER_OTLP_PROTOCOL`                               | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | Punto final de trazas OTLP, anula `OTEL_EXPORTER_OTLP_ENDPOINT`                          | `http://localhost:4318/v1/traces`    |
| `OTEL_TRACES_EXPORT_INTERVAL`         | Intervalo de exportación de lote de span en milisegundos (predeterminado: 5000)          | `1000`, `10000`                      |

Los spans redactan el texto del mensaje del usuario, los detalles de entrada de herramientas y el contenido de herramientas por defecto. Establece `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1`, y `OTEL_LOG_TOOL_CONTENT=1` para incluirlos.

Cuando el trazado está activo, los subprocesos de Bash y PowerShell heredan automáticamente una variable de entorno `TRACEPARENT` que contiene el contexto de traza W3C del span de ejecución de herramienta activo. Esto permite que cualquier subproceso que lea `TRACEPARENT` padre sus propios spans bajo la misma traza, habilitando trazado distribuido de extremo a extremo a través de scripts y comandos que Claude ejecuta.

En sesiones del SDK de Agent y no interactivas iniciadas con `-p`, Claude Code también lee `TRACEPARENT` y `TRACESTATE` de su propio entorno cuando inicia cada span de interacción. Esto permite que un proceso de incrustación pase su contexto de traza W3C activo al subproceso para que los spans de Claude Code aparezcan como hijos de la traza distribuida del llamador. Las sesiones interactivas ignoran `TRACEPARENT` entrante para evitar heredar accidentalmente valores ambientes de entornos de CI o contenedor.

#### Jerarquía de spans

Cada mensaje del usuario inicia un span raíz `claude_code.interaction`. Las llamadas de API, llamadas de herramientas y ejecuciones de hooks se registran como sus hijos. Los spans de herramientas tienen dos spans hijos propios: uno para el tiempo dedicado a esperar una decisión de permiso y otro para la ejecución en sí. Cuando la herramienta Task genera un subagenteagente, los spans de API y herramienta del subagenteagente se anidan bajo el span `claude_code.tool` del padre.

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (requiere trazado beta detallado)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (herramienta Task) spans de claude_code.llm_request / claude_code.tool del subagenteagente
```

En sesiones del SDK de Agent y `claude -p`, `claude_code.interaction` en sí se convierte en un hijo del span del llamador cuando `TRACEPARENT` se establece en el entorno.

#### Atributos de spans

Cada span lleva los [atributos estándar](#standard-attributes) más un atributo `span.type` que coincide con su nombre. Las tablas a continuación enumeran los atributos adicionales establecidos en cada span. Los spans `llm_request`, `tool.execution`, y `hook` establecen el estado de OpenTelemetry `ERROR` cuando registran una falla; los otros spans siempre terminan con estado `UNSET`.

**`claude_code.interaction`**

| Atributo                  | Descripción                                                                        | Controlado Por          |
| ------------------------- | ---------------------------------------------------------------------------------- | ----------------------- |
| `user_prompt`             | Texto del mensaje. El valor es `<REDACTED>` a menos que la puerta esté establecida | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length`      | Longitud del mensaje en caracteres                                                 |                         |
| `interaction.sequence`    | Contador basado en 1 de interacciones en esta sesión                               |                         |
| `interaction.duration_ms` | Duración de pared del turno                                                        |                         |

**`claude_code.llm_request`**

| Atributo                 | Descripción                                                                                | Controlado Por |
| ------------------------ | ------------------------------------------------------------------------------------------ | -------------- |
| `model`                  | Identificador de modelo                                                                    |                |
| `gen_ai.system`          | Siempre `anthropic`. Convención semántica de GenAI de OpenTelemetry                        |                |
| `gen_ai.request.model`   | Mismo valor que `model`. Convención semántica de GenAI de OpenTelemetry                    |                |
| `query_source`           | Subsistema que emitió la solicitud, como `repl_main_thread` o un nombre de subagenteagente |                |
| `speed`                  | `fast` o `normal`                                                                          |                |
| `llm_request.context`    | `interaction`, `tool`, o `standalone` dependiendo del span padre                           |                |
| `duration_ms`            | Duración de pared incluyendo reintentos                                                    |                |
| `ttft_ms`                | Tiempo al primer token en milisegundos                                                     |                |
| `input_tokens`           | Recuento de tokens de entrada del bloque de uso de API                                     |                |
| `output_tokens`          | Recuento de tokens de salida                                                               |                |
| `cache_read_tokens`      | Tokens leídos del caché de mensaje                                                         |                |
| `cache_creation_tokens`  | Tokens escritos en el caché de mensaje                                                     |                |
| `request_id`             | ID de solicitud de API de Anthropic del encabezado de respuesta `request-id`               |                |
| `gen_ai.response.id`     | Mismo valor que `request_id`. Convención semántica de GenAI de OpenTelemetry               |                |
| `client_request_id`      | `x-client-request-id` generado por cliente del intento final                               |                |
| `attempt`                | Intentos totales realizados para esta solicitud                                            |                |
| `success`                | `true` o `false`                                                                           |                |
| `status_code`            | Código de estado HTTP cuando la solicitud falló                                            |                |
| `error`                  | Mensaje de error cuando la solicitud falló                                                 |                |
| `response.has_tool_call` | `true` cuando la respuesta contenía bloques de uso de herramientas                         |                |

Cada intento de reintento también se registra como un evento de span `gen_ai.request.attempt` con atributos `attempt` e `client_request_id`.

**`claude_code.tool`**

| Atributo        | Descripción                                                      | Controlado Por          |
| --------------- | ---------------------------------------------------------------- | ----------------------- |
| `tool_name`     | Nombre de la herramienta                                         |                         |
| `duration_ms`   | Duración de pared incluyendo espera de permiso y ejecución       |                         |
| `result_tokens` | Tamaño aproximado de token del resultado de la herramienta       |                         |
| `file_path`     | Ruta de archivo de destino para herramientas Read, Edit, y Write | `OTEL_LOG_TOOL_DETAILS` |
| `full_command`  | Cadena de comando para la herramienta Bash                       | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name`    | Nombre de habilidad para la herramienta Skill                    | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Tipo de subagenteagente para la herramienta Task                 | `OTEL_LOG_TOOL_DETAILS` |

Cuando `OTEL_LOG_TOOL_CONTENT=1`, este span también registra un evento de span `tool.output` cuyos atributos contienen los cuerpos de entrada y salida de la herramienta, truncados en 60 KB por atributo.

**`claude_code.tool.blocked_on_user`**

| Atributo      | Descripción                                                    | Controlado Por |
| ------------- | -------------------------------------------------------------- | -------------- |
| `duration_ms` | Tiempo dedicado a esperar la decisión de permiso               |                |
| `decision`    | `accept` o `reject`                                            |                |
| `source`      | Fuente de decisión, coincidiendo con el evento `tool_decision` |                |

**`claude_code.tool.execution`**

| Atributo      | Descripción                                                                                                                                                                     | Controlado Por          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `duration_ms` | Tiempo dedicado a ejecutar el cuerpo de la herramienta                                                                                                                          |                         |
| `success`     | `true` o `false`                                                                                                                                                                |                         |
| `error`       | Cadena de categoría de error cuando la ejecución falló, como `Error:ENOENT` o `ShellError`. Contiene el mensaje de error completo en su lugar cuando la puerta está establecida | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**

Este span se emite solo cuando el trazado beta detallado está activo, lo que requiere `ENABLE_BETA_TRACING_DETAILED=1` y `BETA_TRACING_ENDPOINT` además de la configuración del exportador de trazas anterior. En sesiones de CLI interactivas, esto también requiere que tu organización esté en la lista de permitidos para la característica. Las sesiones del SDK de Agent y no interactivas `-p` no están controladas. No se emite cuando solo `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` está establecido.

| Atributo                 | Descripción                                               | Controlado Por          |
| ------------------------ | --------------------------------------------------------- | ----------------------- |
| `hook_event`             | Tipo de evento de hook, como `PreToolUse`                 |                         |
| `hook_name`              | Nombre completo del hook, como `PreToolUse:Write`         |                         |
| `num_hooks`              | Número de comandos de hook coincidentes ejecutados        |                         |
| `hook_definitions`       | Configuración de hook serializada en JSON                 | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms`            | Duración de pared de todos los hooks coincidentes         |                         |
| `num_success`            | Recuento de hooks que se completaron exitosamente         |                         |
| `num_blocking`           | Recuento de hooks que devolvieron una decisión de bloqueo |                         |
| `num_non_blocking_error` | Recuento de hooks que fallaron sin bloquear               |                         |
| `num_cancelled`          | Recuento de hooks cancelados antes de completarse         |                         |

<Note>
  Atributos adicionales que contienen contenido como `new_context`, `system_prompt_preview`, `tool_input`, y `response.model_output` se emiten solo cuando el trazado beta detallado está activo. No son parte del esquema de span estable.
</Note>

### Encabezados dinámicos

Para entornos empresariales que requieren autenticación dinámica, puedes configurar un script para generar encabezados dinámicamente:

#### Configuración de ajustes

Agrega a tu `.claude/settings.json`:

```json theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Requisitos del script

El script debe generar JSON válido con pares clave-valor de cadena que representen encabezados HTTP:

```bash theme={null}
#!/bin/bash
# Ejemplo: Múltiples encabezados
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Comportamiento de actualización

El script auxiliar de encabezados se ejecuta al inicio y periódicamente después para admitir la actualización de tokens. Por defecto, el script se ejecuta cada 29 minutos. Personaliza el intervalo con la variable de entorno `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Soporte de organización multi-equipo

Las organizaciones con múltiples equipos o departamentos pueden agregar atributos personalizados para distinguir entre diferentes grupos usando la variable de entorno `OTEL_RESOURCE_ATTRIBUTES`:

```bash theme={null}
# Agregar atributos personalizados para identificación de equipo
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Estos atributos personalizados se incluirán en todas las métricas y eventos, permitiéndote:

* Filtrar métricas por equipo o departamento
* Rastrear costos por centro de costos
* Crear paneles específicos del equipo
* Configurar alertas para equipos específicos

<Warning>
  **Requisitos de formato importantes para OTEL\_RESOURCE\_ATTRIBUTES:**

  La variable de entorno `OTEL_RESOURCE_ATTRIBUTES` utiliza pares clave=valor separados por comas con requisitos de formato estrictos:

  * **No se permiten espacios**: Los valores no pueden contener espacios. Por ejemplo, `user.organizationName=My Company` es inválido
  * **Formato**: Debe ser pares clave=valor separados por comas: `key1=value1,key2=value2`
  * **Caracteres permitidos**: Solo caracteres US-ASCII excluyendo caracteres de control, espacios en blanco, comillas dobles, comas, puntos y comas, y barras invertidas
  * **Caracteres especiales**: Los caracteres fuera del rango permitido deben estar codificados en porcentaje

  **Ejemplos:**

  ```bash theme={null}
  # ❌ Inválido - contiene espacios
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Válido - usar guiones bajos o camelCase en su lugar
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Válido - codificar en porcentaje caracteres especiales si es necesario
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Nota: envolver valores entre comillas no escapa espacios. Por ejemplo, `org.name="My Company"` resulta en el valor literal `"My Company"` (con comillas incluidas), no `My Company`.
</Warning>

### Configuraciones de ejemplo

Establece estas variables de entorno antes de ejecutar `claude`. Cada bloque muestra una configuración completa para un exportador diferente o escenario de implementación:

```bash theme={null}
# Depuración de consola (intervalos de 1 segundo)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Múltiples exportadores
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Diferentes puntos finales/backends para métricas y registros
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Solo métricas (sin eventos/registros)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Solo eventos/registros (sin métricas)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Métricas y eventos disponibles

### Atributos estándar

Todas las métricas y eventos comparten estos atributos estándar:

| Atributo            | Descripción                                                                                                                                   | Controlado Por                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `session.id`        | Identificador único de sesión                                                                                                                 | `OTEL_METRICS_INCLUDE_SESSION_ID` (predeterminado: true)   |
| `app.version`       | Versión actual de Claude Code                                                                                                                 | `OTEL_METRICS_INCLUDE_VERSION` (predeterminado: false)     |
| `organization.id`   | UUID de organización (cuando está autenticado)                                                                                                | Siempre incluido cuando está disponible                    |
| `user.account_uuid` | UUID de cuenta (cuando está autenticado)                                                                                                      | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (predeterminado: true) |
| `user.account_id`   | ID de cuenta en formato etiquetado que coincide con las API de administrador de Anthropic (cuando está autenticado), como `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (predeterminado: true) |
| `user.id`           | Identificador anónimo de dispositivo/instalación, generado por instalación de Claude Code                                                     | Siempre incluido                                           |
| `user.email`        | Dirección de correo electrónico del usuario (cuando está autenticado a través de OAuth)                                                       | Siempre incluido cuando está disponible                    |
| `terminal.type`     | Tipo de terminal, como `iTerm.app`, `vscode`, `cursor`, o `tmux`                                                                              | Siempre incluido cuando se detecta                         |

Los eventos incluyen adicionalmente los siguientes atributos. Estos nunca se adjuntan a las métricas porque causarían cardinalidad ilimitada:

* `prompt.id`: UUID que correlaciona un mensaje del usuario con todos los eventos posteriores hasta el siguiente mensaje. Consulta [Atributos de correlación de eventos](#event-correlation-attributes).
* `workspace.host_paths`: directorios de espacio de trabajo del host seleccionados en la aplicación de escritorio, como una matriz de cadenas

### Métricas

Claude Code exporta las siguientes métricas:

| Nombre de Métrica                     | Descripción                                                            | Unidad |
| ------------------------------------- | ---------------------------------------------------------------------- | ------ |
| `claude_code.session.count`           | Recuento de sesiones CLI iniciadas                                     | count  |
| `claude_code.lines_of_code.count`     | Recuento de líneas de código modificadas                               | count  |
| `claude_code.pull_request.count`      | Número de solicitudes de extracción creadas                            | count  |
| `claude_code.commit.count`            | Número de confirmaciones de git creadas                                | count  |
| `claude_code.cost.usage`              | Costo de la sesión de Claude Code                                      | USD    |
| `claude_code.token.usage`             | Número de tokens utilizados                                            | tokens |
| `claude_code.code_edit_tool.decision` | Recuento de decisiones de permisos de herramienta de edición de código | count  |
| `claude_code.active_time.total`       | Tiempo activo total en segundos                                        | s      |

### Detalles de métricas

Cada métrica incluye los atributos estándar enumerados anteriormente. Las métricas con atributos adicionales específicos del contexto se indican a continuación.

#### Contador de sesión

Se incrementa al inicio de cada sesión.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `start_type`: Cómo se inició la sesión. Uno de `"fresh"`, `"resume"`, o `"continue"`

#### Contador de líneas de código

Se incrementa cuando se agrega o se elimina código.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `type`: (`"added"`, `"removed"`)

#### Contador de solicitud de extracción

Se incrementa al crear solicitudes de extracción a través de Claude Code.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)

#### Contador de confirmación

Se incrementa al crear confirmaciones de git a través de Claude Code.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)

#### Contador de costo

Se incrementa después de cada solicitud de API.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `model`: Identificador de modelo (por ejemplo, "claude-sonnet-4-6")
* `query_source`: Categoría del subsistema que emitió la solicitud. Uno de `"main"`, `"subagent"`, o `"auxiliary"`
* `speed`: `"fast"` cuando la solicitud utilizó modo rápido. Ausente de otra manera
* `effort`: [Nivel de esfuerzo](/es/model-config#adjust-effort-level) aplicado a la solicitud: `"low"`, `"medium"`, `"high"`, `"xhigh"`, o `"max"`. Ausente cuando el modelo no admite esfuerzo.

#### Contador de tokens

Se incrementa después de cada solicitud de API.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Identificador de modelo (por ejemplo, "claude-sonnet-4-6")
* `query_source`: Categoría del subsistema que emitió la solicitud. Uno de `"main"`, `"subagent"`, o `"auxiliary"`
* `speed`: `"fast"` cuando la solicitud utilizó modo rápido. Ausente de otra manera
* `effort`: [Nivel de esfuerzo](/es/model-config#adjust-effort-level) aplicado a la solicitud. Consulta [Contador de costo](#cost-counter) para detalles.

#### Contador de decisión de herramienta de edición de código

Se incrementa cuando el usuario acepta o rechaza el uso de herramientas Edit, Write, o NotebookEdit.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `tool_name`: Nombre de la herramienta (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Decisión del usuario (`"accept"`, `"reject"`)
* `source`: Fuente de decisión - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`
* `language`: Lenguaje de programación del archivo editado, como `"TypeScript"`, `"Python"`, `"JavaScript"`, o `"Markdown"`. Devuelve `"unknown"` para extensiones de archivo no reconocidas.

#### Contador de tiempo activo

Rastrea el tiempo real dedicado a usar activamente Claude Code, excluyendo tiempo inactivo. Esta métrica se incrementa durante interacciones del usuario (escribir, leer respuestas) y durante procesamiento de CLI (ejecución de herramientas, generación de respuestas de IA).

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `type`: `"user"` para interacciones de teclado, `"cli"` para ejecución de herramientas y respuestas de IA

### Eventos

Claude Code exporta los siguientes eventos a través de registros/eventos de OpenTelemetry (cuando `OTEL_LOGS_EXPORTER` está configurado):

#### Atributos de correlación de eventos

Cuando un usuario envía un mensaje, Claude Code puede hacer múltiples llamadas de API y ejecutar varias herramientas. El atributo `prompt.id` te permite vincular todos esos eventos al único mensaje que los desencadenó.

| Atributo    | Descripción                                                                                                     |
| ----------- | --------------------------------------------------------------------------------------------------------------- |
| `prompt.id` | Identificador UUID v4 que vincula todos los eventos producidos mientras se procesa un único mensaje del usuario |

Para rastrear toda la actividad desencadenada por un único mensaje, filtra tus eventos por un valor específico de `prompt.id`. Esto devuelve el evento user\_prompt, cualquier evento api\_request, y cualquier evento tool\_result que ocurrió mientras se procesaba ese mensaje.

<Note>
  `prompt.id` se excluye intencionalmente de las métricas porque cada mensaje genera un ID único, lo que crearía un número siempre creciente de series temporales. Úsalo solo para análisis a nivel de evento y auditoría.
</Note>

#### Evento de mensaje del usuario

Se registra cuando un usuario envía un mensaje.

**Nombre del Evento**: `claude_code.user_prompt`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `prompt_length`: Longitud del mensaje
* `prompt`: Contenido del mensaje (redactado por defecto, habilitar con `OTEL_LOG_USER_PROMPTS=1`)
* `command_name`: Nombre del comando cuando el mensaje invoca uno. Los nombres de comandos integrados y agrupados como `compact` o `debug` se emiten tal cual; los alias como `reset` se emiten como se escribieron en lugar del nombre canónico. Los nombres de comandos personalizados, de plugin y MCP se contraen a `custom` o `mcp` a menos que `OTEL_LOG_TOOL_DETAILS=1` esté establecido
* `command_source`: Origen del comando cuando está presente: `builtin`, `custom`, o `mcp`. Los comandos proporcionados por plugins reportan como `custom`

#### Evento de resultado de herramienta

Se registra cuando una herramienta completa la ejecución.

**Nombre del Evento**: `claude_code.tool_result`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `tool_name`: Nombre de la herramienta
* `tool_use_id`: Identificador único para esta invocación de herramienta. Coincide con el `tool_use_id` pasado a hooks, permitiendo correlación entre eventos OTel y datos capturados por hooks.
* `success`: `"true"` o `"false"`
* `duration_ms`: Tiempo de ejecución en milisegundos
* `error_type`: Cadena de categoría de error cuando la herramienta falló, como `"Error:ENOENT"` o `"ShellError"`
* `error` (cuando `OTEL_LOG_TOOL_DETAILS=1`): Mensaje de error completo cuando la herramienta falló
* `decision_type`: Ya sea `"accept"` o `"reject"`
* `decision_source`: Fuente de decisión - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`
* `tool_input_size_bytes`: Tamaño de la entrada de herramienta serializada en JSON en bytes
* `tool_result_size_bytes`: Tamaño del resultado de la herramienta en bytes
* `mcp_server_scope`: Identificador de alcance del servidor MCP (para herramientas MCP)
* `tool_parameters` (cuando `OTEL_LOG_TOOL_DETAILS=1`): Cadena JSON que contiene parámetros específicos de la herramienta:
  * Para herramienta Bash: incluye `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox`, y `git_commit_id` (el SHA del commit, cuando un comando `git commit` tiene éxito)
  * Para herramientas MCP: incluye `mcp_server_name`, `mcp_tool_name`
  * Para herramienta Skill: incluye `skill_name`
  * Para herramienta Task: incluye `subagent_type`
* `tool_input` (cuando `OTEL_LOG_TOOL_DETAILS=1`): Argumentos de herramienta serializados en JSON. Los valores individuales superiores a 512 caracteres se truncan, y la carga útil completa está limitada a aproximadamente 4 K caracteres. Se aplica a todas las herramientas, incluidas las herramientas MCP.

#### Evento de solicitud de API

Se registra para cada solicitud de API a Claude.

**Nombre del Evento**: `claude_code.api_request`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `model`: Modelo utilizado (por ejemplo, "claude-sonnet-4-6")
* `cost_usd`: Costo estimado en USD
* `duration_ms`: Duración de la solicitud en milisegundos
* `input_tokens`: Número de tokens de entrada
* `output_tokens`: Número de tokens de salida
* `cache_read_tokens`: Número de tokens leídos del caché
* `cache_creation_tokens`: Número de tokens utilizados para la creación del caché
* `request_id`: ID de solicitud de API de Anthropic del encabezado `request-id` de la respuesta, como `"req_011..."`. Presente solo cuando la API devuelve uno.
* `speed`: `"fast"` o `"normal"`, indicando si el modo rápido estaba activo
* `query_source`: Subsistema que emitió la solicitud, como `"repl_main_thread"`, `"compact"`, o un nombre de subagenteagente
* `effort`: [Nivel de esfuerzo](/es/model-config#adjust-effort-level) aplicado a la solicitud: `"low"`, `"medium"`, `"high"`, `"xhigh"`, o `"max"`. Ausente cuando el modelo no admite esfuerzo.

#### Evento de error de API

Se registra cuando una solicitud de API a Claude falla.

**Nombre del Evento**: `claude_code.api_error`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `model`: Modelo utilizado (por ejemplo, "claude-sonnet-4-6")
* `error`: Mensaje de error
* `status_code`: Código de estado HTTP como cadena, o `"undefined"` para errores no HTTP
* `duration_ms`: Duración de la solicitud en milisegundos
* `attempt`: Número total de intentos realizados, incluyendo la solicitud inicial (`1` significa que no ocurrieron reintentos)
* `request_id`: ID de solicitud de API de Anthropic del encabezado `request-id` de la respuesta, como `"req_011..."`. Presente solo cuando la API devuelve uno.
* `speed`: `"fast"` o `"normal"`, indicando si el modo rápido estaba activo
* `query_source`: Subsistema que emitió la solicitud, como `"repl_main_thread"`, `"compact"`, o un nombre de subagenteagente
* `effort`: [Nivel de esfuerzo](/es/model-config#adjust-effort-level) aplicado a la solicitud. Ausente cuando el modelo no admite esfuerzo.

#### Evento de cuerpo de solicitud de API

Se registra para cada intento de solicitud de API cuando `OTEL_LOG_RAW_API_BODIES` está establecido. Se emite un evento por intento, por lo que los reintentos con parámetros ajustados producen cada uno su propio evento.

**Nombre del Evento**: `claude_code.api_request_body`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_request_body"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `body`: Parámetros de solicitud de API de Mensajes serializados en JSON (mensaje del sistema, mensajes, herramientas, etc.), truncados en 60 KB. El contenido de pensamiento extendido en turnos de asistente anteriores se redacta. Se emite solo en modo en línea (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Ruta absoluta a un archivo `<dir>/<uuid>.request.json` que contiene el cuerpo sin truncar. Se emite solo en modo de archivo (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Longitud del cuerpo sin truncar. Bytes UTF-8 cuando `OTEL_LOG_RAW_API_BODIES=file:<dir>`, o unidades de código UTF-16 cuando `=1`
* `body_truncated`: `"true"` cuando ocurrió truncamiento en línea. Ausente en modo de archivo y cuando no ocurrió truncamiento.
* `model`: Identificador de modelo de los parámetros de solicitud
* `query_source`: Subsistema que emitió la solicitud (por ejemplo, `"compact"`)

#### Evento de cuerpo de respuesta de API

Se registra para cada respuesta de API exitosa cuando `OTEL_LOG_RAW_API_BODIES` está establecido.

**Nombre del Evento**: `claude_code.api_response_body`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_response_body"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `body`: Respuesta de API de Mensajes serializada en JSON (id, bloques de contenido, uso, razón de parada), truncada en 60 KB. El contenido de pensamiento extendido se redacta. Se emite solo en modo en línea (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Ruta absoluta a un archivo `<dir>/<request_id>.response.json` que contiene el cuerpo sin truncar. Se emite solo en modo de archivo (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Longitud del cuerpo sin truncar. Bytes UTF-8 cuando `OTEL_LOG_RAW_API_BODIES=file:<dir>`, o unidades de código UTF-16 cuando `=1`
* `body_truncated`: `"true"` cuando ocurrió truncamiento en línea. Ausente en modo de archivo y cuando no ocurrió truncamiento.
* `model`: Identificador de modelo
* `query_source`: Subsistema que emitió la solicitud
* `request_id`: ID de solicitud de API de Anthropic del encabezado `request-id` de la respuesta, como `"req_011..."`. Presente solo cuando la API devuelve uno.

#### Evento de decisión de herramienta

Se registra cuando se toma una decisión de permiso de herramienta (aceptar/rechazar).

**Nombre del Evento**: `claude_code.tool_decision`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `tool_name`: Nombre de la herramienta (por ejemplo, "Read", "Edit", "Write", "NotebookEdit")
* `tool_use_id`: Identificador único para esta invocación de herramienta. Coincide con el `tool_use_id` pasado a hooks, permitiendo correlación entre eventos OTel y datos capturados por hooks.
* `decision`: Ya sea `"accept"` o `"reject"`
* `source`: Fuente de decisión - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`

#### Evento de cambio de modo de permiso

Se registra cuando el modo de permiso cambia, por ejemplo al ciclar con Shift+Tab, salir del modo de plan, o una verificación de puerta de modo automático.

**Nombre del Evento**: `claude_code.permission_mode_changed`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"permission_mode_changed"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `from_mode`: El modo de permiso anterior, por ejemplo `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, o `"bypassPermissions"`
* `to_mode`: El nuevo modo de permiso
* `trigger`: Qué causó el cambio. Uno de `"shift_tab"`, `"exit_plan_mode"`, `"auto_gate_denied"`, o `"auto_opt_in"`. Ausente cuando la transición se origina del SDK o puente

#### Evento de autenticación

Se registra cuando `/login` o `/logout` se completa.

**Nombre del Evento**: `claude_code.auth`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"auth"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `action`: `"login"` o `"logout"`
* `success`: `"true"` o `"false"`
* `auth_method`: Método de autenticación, como `"oauth"`
* `error_category`: Tipo de error categórico cuando la acción falló. El mensaje de error sin procesar nunca se incluye
* `status_code`: Código de estado HTTP como cadena cuando la acción falló con un error HTTP

#### Evento de conexión del servidor MCP

Se registra cuando un servidor MCP se conecta, desconecta o falla al conectarse.

**Nombre del Evento**: `claude_code.mcp_server_connection`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"mcp_server_connection"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `status`: `"connected"`, `"failed"`, o `"disconnected"`
* `transport_type`: Transporte del servidor, como `"stdio"`, `"sse"`, o `"http"`
* `server_scope`: Alcance en el que está configurado el servidor, como `"user"`, `"project"`, o `"local"`
* `duration_ms`: Duración del intento de conexión en milisegundos
* `error_code`: Código de error cuando la conexión falló
* `server_name` (cuando `OTEL_LOG_TOOL_DETAILS=1`): Nombre del servidor configurado
* `error` (cuando `OTEL_LOG_TOOL_DETAILS=1`): Mensaje de error completo cuando la conexión falló

#### Evento de error interno

Se registra cuando Claude Code captura un error interno inesperado. Solo se registran el nombre de la clase de error y un código de estilo errno. El mensaje de error y el seguimiento de pila nunca se incluyen. Este evento no se emite cuando se ejecuta contra Bedrock, Vertex, o Foundry, o cuando `DISABLE_ERROR_REPORTING` está establecido.

**Nombre del Evento**: `claude_code.internal_error`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"internal_error"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `error_name`: Nombre de la clase de error, como `"TypeError"` o `"SyntaxError"`
* `error_code`: Código errno de Node.js como `"ENOENT"` cuando está presente en el error

#### Evento de plugin instalado

Se registra cuando un plugin termina de instalarse, tanto desde el comando CLI `claude plugin install` como desde la interfaz de usuario interactiva `/plugin`.

**Nombre del Evento**: `claude_code.plugin_installed`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"plugin_installed"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `marketplace.is_official`: `"true"` si el mercado es un mercado oficial de Anthropic, `"false"` de otra manera
* `install.trigger`: `"cli"` o `"ui"`
* `plugin.name`: Nombre del plugin instalado. Para mercados de terceros esto se incluye solo cuando `OTEL_LOG_TOOL_DETAILS=1`
* `plugin.version`: Versión del plugin cuando se declara en la entrada del mercado. Para mercados de terceros esto se incluye solo cuando `OTEL_LOG_TOOL_DETAILS=1`
* `marketplace.name`: Mercado desde el que se instaló el plugin. Para mercados de terceros esto se incluye solo cuando `OTEL_LOG_TOOL_DETAILS=1`

#### Evento de habilidad activada

Se registra cuando se invoca una habilidad.

**Nombre del Evento**: `claude_code.skill_activated`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"skill_activated"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `skill.name`: Nombre de la habilidad. Para habilidades definidas por el usuario y de plugin de terceros el valor es el marcador de posición `"custom_skill"` a menos que `OTEL_LOG_TOOL_DETAILS=1`
* `skill.source`: De dónde se cargó la habilidad (por ejemplo, `"bundled"`, `"userSettings"`, `"projectSettings"`, `"plugin"`)
* `plugin.name` (cuando `OTEL_LOG_TOOL_DETAILS=1` o el plugin es de un mercado oficial): Nombre del plugin propietario cuando la habilidad es proporcionada por un plugin
* `marketplace.name` (cuando `OTEL_LOG_TOOL_DETAILS=1` o el plugin es de un mercado oficial): Mercado del plugin propietario fue instalado desde, cuando la habilidad es proporcionada por un plugin

#### Evento de reintentos de API agotados

Se registra una vez cuando una solicitud de API falla después de más de un intento. Se emite junto con el evento `api_error` final.

**Nombre del Evento**: `claude_code.api_retries_exhausted`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_retries_exhausted"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `model`: Modelo utilizado
* `error`: Mensaje de error final
* `status_code`: Código de estado HTTP como cadena
* `total_attempts`: Número total de intentos realizados
* `total_retry_duration_ms`: Tiempo total de pared en todos los intentos
* `speed`: `"fast"` o `"normal"`

#### Evento de inicio de ejecución de hook

Se registra cuando uno o más hooks comienzan a ejecutarse para un evento de hook.

**Nombre del Evento**: `claude_code.hook_execution_start`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"hook_execution_start"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `hook_event`: Tipo de evento de hook, como `"PreToolUse"` o `"PostToolUse"`
* `hook_name`: Nombre completo del hook incluyendo coincidencia, como `"PreToolUse:Write"`
* `num_hooks`: Número de comandos de hook coincidentes
* `managed_only`: `"true"` cuando solo se permiten hooks de política administrada
* `hook_source`: `"policySettings"` o `"merged"`
* `hook_definitions`: Configuración de hook serializada en JSON. Se incluye solo cuando tanto el trazado beta detallado como `OTEL_LOG_TOOL_DETAILS=1` están habilitados

#### Evento de ejecución de hook completado

Se registra cuando todos los hooks para un evento de hook han terminado.

**Nombre del Evento**: `claude_code.hook_execution_complete`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"hook_execution_complete"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `hook_event`: Tipo de evento de hook
* `hook_name`: Nombre completo del hook incluyendo coincidencia
* `num_hooks`: Número de comandos de hook coincidentes
* `num_success`: Recuento que se completó exitosamente
* `num_blocking`: Recuento que devolvió una decisión de bloqueo
* `num_non_blocking_error`: Recuento que falló sin bloquear
* `num_cancelled`: Recuento cancelado antes de completarse
* `total_duration_ms`: Duración de pared de todos los hooks coincidentes
* `managed_only`: `"true"` cuando solo se permiten hooks de política administrada
* `hook_source`: `"policySettings"` o `"merged"`
* `hook_definitions`: Configuración de hook serializada en JSON. Se incluye solo cuando tanto el trazado beta detallado como `OTEL_LOG_TOOL_DETAILS=1` están habilitados

#### Evento de compactación

Se registra cuando la compactación de conversación se completa.

**Nombre del Evento**: `claude_code.compaction`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"compaction"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `event.sequence`: Contador monotónicamente creciente para ordenar eventos dentro de una sesión
* `trigger`: `"auto"` o `"manual"`
* `success`: `"true"` o `"false"`
* `duration_ms`: Duración de compactación
* `pre_tokens`: Recuento aproximado de tokens antes de compactación
* `post_tokens`: Recuento aproximado de tokens después de compactación
* `error`: Mensaje de error cuando la compactación falló

## Interpretar datos de métricas y eventos

Las métricas y eventos exportados admiten una variedad de análisis:

### Monitoreo de uso

| Métrica                                                       | Oportunidad de Análisis                                          |
| ------------------------------------------------------------- | ---------------------------------------------------------------- |
| `claude_code.token.usage`                                     | Desglosar por `type` (entrada/salida), usuario, equipo o modelo  |
| `claude_code.session.count`                                   | Rastrear adopción y compromiso a lo largo del tiempo             |
| `claude_code.lines_of_code.count`                             | Medir productividad rastreando adiciones/eliminaciones de código |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Entender el impacto en los flujos de trabajo de desarrollo       |

### Monitoreo de costos

La métrica `claude_code.cost.usage` ayuda con:

* Rastrear tendencias de uso entre equipos o individuos
* Identificar sesiones de alto uso para optimización

<Note>
  Las métricas de costo son aproximaciones. Para datos de facturación oficiales, consulta tu proveedor de API (Claude Console, AWS Bedrock, o Google Cloud Vertex).
</Note>

### Alertas y segmentación

Alertas comunes a considerar:

* Picos de costo
* Consumo inusual de tokens
* Alto volumen de sesiones de usuarios específicos

Todas las métricas pueden segmentarse por `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model`, y `app.version`.

### Detectar agotamiento de reintentos

Claude Code reintenta solicitudes de API fallidas internamente y emite un único evento `claude_code.api_error` solo después de rendirse, por lo que el evento en sí es la señal terminal para esa solicitud. Los intentos de reintento intermedios no se registran como eventos separados.

El atributo `attempt` en el evento registra cuántos intentos se realizaron en total. Un valor mayor que `CLAUDE_CODE_MAX_RETRIES` (predeterminado `10`) indica que la solicitud agotó todos los reintentos en un error transitorio. Un valor más bajo indica un error no reintentable como una respuesta `400`.

Para distinguir una sesión que se recuperó de una que se estancó, agrupa eventos por `session.id` y verifica si existe un evento `api_request` posterior después del error.

### Análisis de eventos

Los datos de eventos proporcionan información detallada sobre las interacciones de Claude Code:

**Patrones de Uso de Herramientas**: analizar eventos de resultado de herramientas para identificar:

* Herramientas más utilizadas frecuentemente
* Tasas de éxito de herramientas
* Tiempos de ejecución promedio de herramientas
* Patrones de error por tipo de herramienta

**Monitoreo de Rendimiento**: rastrear duraciones de solicitudes de API y tiempos de ejecución de herramientas para identificar cuellos de botella de rendimiento.

## Consideraciones de backend

Tu elección de backends de métricas, registros y trazas determina los tipos de análisis que puedes realizar:

### Para métricas

* **Bases de datos de series temporales (por ejemplo, Prometheus)**: Cálculos de tasa, métricas agregadas
* **Almacenes columnares (por ejemplo, ClickHouse)**: Consultas complejas, análisis de usuario único
* **Plataformas de observabilidad completas (por ejemplo, Honeycomb, Datadog)**: Consultas avanzadas, visualización, alertas

### Para eventos/registros

* **Sistemas de agregación de registros (por ejemplo, Elasticsearch, Loki)**: Búsqueda de texto completo, análisis de registros
* **Almacenes columnares (por ejemplo, ClickHouse)**: Análisis de eventos estructurados
* **Plataformas de observabilidad completas (por ejemplo, Honeycomb, Datadog)**: Correlación entre métricas y eventos

### Para trazas

Elige un backend que admita almacenamiento de trazas distribuidas y correlación de spans:

* **Sistemas de trazas distribuidas (por ejemplo, Jaeger, Zipkin, Grafana Tempo)**: Visualización de spans, cascadas de solicitudes, análisis de latencia
* **Plataformas de observabilidad completas (por ejemplo, Honeycomb, Datadog)**: Búsqueda de trazas y correlación con métricas y registros

Para organizaciones que requieren métricas de Usuarios Activos Diarios/Semanales/Mensuales (DAU/WAU/MAU), considera backends que admitan consultas de valores únicos eficientes.

## Información del servicio

Todas las métricas y eventos se exportan con los siguientes atributos de recurso:

* `service.name`: `claude-code`
* `service.version`: Versión actual de Claude Code
* `os.type`: Tipo de sistema operativo (por ejemplo, `linux`, `darwin`, `windows`)
* `os.version`: Cadena de versión del sistema operativo
* `host.arch`: Arquitectura del host (por ejemplo, `amd64`, `arm64`)
* `wsl.version`: Número de versión de WSL (solo presente cuando se ejecuta en Windows Subsystem for Linux)
* Nombre del Medidor: `com.anthropic.claude_code`

## Recursos de medición de ROI

Para una guía completa sobre cómo medir el retorno de inversión para Claude Code, incluyendo configuración de telemetría, análisis de costos, métricas de productividad e informes automatizados, consulta la [Guía de Medición de ROI de Claude Code](https://github.com/anthropics/claude-code-monitoring-guide). Este repositorio proporciona configuraciones de Docker Compose listas para usar, configuraciones de Prometheus y OpenTelemetry, y plantillas para generar informes de productividad integrados con herramientas como Linear.

## Seguridad y privacidad

* La telemetría es opcional y requiere configuración explícita
* Los contenidos de archivos sin procesar y fragmentos de código no se incluyen en métricas o eventos. Las trazas de span son una ruta de datos separada: consulta la viñeta `OTEL_LOG_TOOL_CONTENT` a continuación
* Cuando está autenticado a través de OAuth, `user.email` se incluye en atributos de telemetría. Si esto es una preocupación para tu organización, trabaja con tu backend de telemetría para filtrar o redactar este campo
* El contenido del mensaje del usuario no se recopila por defecto. Solo se registra la longitud del mensaje. Para incluir contenido del mensaje, establece `OTEL_LOG_USER_PROMPTS=1`
* Los argumentos de entrada de herramientas y parámetros no se registran por defecto. Para incluirlos, establece `OTEL_LOG_TOOL_DETAILS=1`. Cuando está habilitado, los eventos `tool_result` incluyen un atributo `tool_parameters` con comandos Bash, nombres de servidor MCP y herramienta, y nombres de habilidades, más un atributo `tool_input` con rutas de archivo, URLs, patrones de búsqueda y otros argumentos. Los eventos `user_prompt` incluyen el `command_name` verbatim para comandos personalizados, de plugin y MCP. Los spans de traza incluyen el mismo atributo `tool_input` y atributos derivados de entrada como `file_path`. Los valores individuales superiores a 512 caracteres se truncan y el total está limitado a aproximadamente 4 K caracteres, pero los argumentos aún pueden contener valores sensibles. Configura tu backend de telemetría para filtrar o redactar estos atributos según sea necesario
* El contenido de entrada y salida de herramientas no se registra en spans de trazas por defecto. Para incluirlo, establece `OTEL_LOG_TOOL_CONTENT=1`. Cuando está habilitado, los eventos de span incluyen contenido completo de entrada y salida de herramientas truncado en 60 KB por span. Esto puede incluir contenidos de archivo sin procesar de resultados de herramienta Read y salida de comandos Bash. Configura tu backend de telemetría para filtrar o redactar estos atributos según sea necesario
* Los cuerpos de solicitud y respuesta de la API de Mensajes de Anthropic sin procesar no se registran por defecto. Para incluirlos, establece `OTEL_LOG_RAW_API_BODIES`. Con `=1`, cada llamada de API emite eventos de registro `api_request_body` y `api_response_body` cuyo atributo `body` es la carga útil serializada en JSON, truncada en 60 KB. Con `=file:<dir>`, los cuerpos sin truncar se escriben en archivos `.request.json` y `.response.json` bajo ese directorio y los eventos llevan una ruta `body_ref` en su lugar del cuerpo en línea. Envía el directorio con un recopilador de registros o sidecar en lugar de a través del flujo de telemetría. En ambos modos, los cuerpos contienen el historial de conversación completo (mensaje del sistema, cada turno anterior de usuario y asistente, resultados de herramientas), por lo que habilitar esto implica consentimiento a todo lo que las otras banderas de contenido `OTEL_LOG_*` revelarían. El contenido de pensamiento extendido de Claude siempre se redacta de estos cuerpos independientemente de otras configuraciones

## Monitorear Claude Code en Amazon Bedrock

Para orientación detallada sobre monitoreo de uso de Claude Code para Amazon Bedrock, consulta [Implementación de Monitoreo de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
