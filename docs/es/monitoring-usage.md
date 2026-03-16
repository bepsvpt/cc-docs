> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoreo

> Aprende cómo habilitar y configurar OpenTelemetry para Claude Code.

Claude Code admite métricas y eventos de OpenTelemetry (OTel) para monitoreo y observabilidad.

Todas las métricas son datos de series temporales exportados a través del protocolo estándar de métricas de OpenTelemetry, y los eventos se exportan a través del protocolo de registros/eventos de OpenTelemetry. Es responsabilidad del usuario asegurar que sus backends de métricas y registros estén correctamente configurados y que la granularidad de agregación cumpla con sus requisitos de monitoreo.

## Inicio rápido

Configura OpenTelemetry usando variables de entorno:

```bash  theme={null}
# 1. Habilitar telemetría
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Elegir exportadores (ambos son opcionales - configura solo lo que necesites)
export OTEL_METRICS_EXPORTER=otlp       # Opciones: otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # Opciones: otlp, console

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

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

<Note>
  Los ajustes administrados pueden distribuirse a través de MDM (Mobile Device Management) u otras soluciones de gestión de dispositivos. Las variables de entorno definidas en el archivo de configuración administrada tienen alta precedencia y no pueden ser anuladas por los usuarios.
</Note>

## Detalles de configuración

### Variables de configuración comunes

| Variable de Entorno                             | Descripción                                                                              | Valores de Ejemplo                        |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                  | Habilita la recopilación de telemetría (requerido)                                       | `1`                                       |
| `OTEL_METRICS_EXPORTER`                         | Tipo(s) de exportador de métricas (separados por comas)                                  | `console`, `otlp`, `prometheus`           |
| `OTEL_LOGS_EXPORTER`                            | Tipo(s) de exportador de registros/eventos (separados por comas)                         | `console`, `otlp`                         |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                   | Protocolo para exportador OTLP (todas las señales)                                       | `grpc`, `http/json`, `http/protobuf`      |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                   | Punto final del recopilador OTLP (todas las señales)                                     | `http://localhost:4317`                   |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`           | Protocolo para métricas (anula el general)                                               | `grpc`, `http/json`, `http/protobuf`      |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`           | Punto final de métricas OTLP (anula el general)                                          | `http://localhost:4318/v1/metrics`        |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`              | Protocolo para registros (anula el general)                                              | `grpc`, `http/json`, `http/protobuf`      |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`              | Punto final de registros OTLP (anula el general)                                         | `http://localhost:4318/v1/logs`           |
| `OTEL_EXPORTER_OTLP_HEADERS`                    | Encabezados de autenticación para OTLP                                                   | `Authorization=Bearer token`              |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`         | Clave de cliente para autenticación mTLS                                                 | Ruta al archivo de clave de cliente       |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | Certificado de cliente para autenticación mTLS                                           | Ruta al archivo de certificado de cliente |
| `OTEL_METRIC_EXPORT_INTERVAL`                   | Intervalo de exportación en milisegundos (predeterminado: 60000)                         | `5000`, `60000`                           |
| `OTEL_LOGS_EXPORT_INTERVAL`                     | Intervalo de exportación de registros en milisegundos (predeterminado: 5000)             | `1000`, `10000`                           |
| `OTEL_LOG_USER_PROMPTS`                         | Habilitar registro del contenido del mensaje del usuario (predeterminado: deshabilitado) | `1` para habilitar                        |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`   | Intervalo para actualizar encabezados dinámicos (predeterminado: 1740000ms / 29 minutos) | `900000`                                  |

### Control de cardinalidad de métricas

Las siguientes variables de entorno controlan qué atributos se incluyen en las métricas para gestionar la cardinalidad:

| Variable de Entorno                 | Descripción                                     | Valor Predeterminado | Ejemplo para Deshabilitar |
| ----------------------------------- | ----------------------------------------------- | -------------------- | ------------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Incluir atributo session.id en métricas         | `true`               | `false`                   |
| `OTEL_METRICS_INCLUDE_VERSION`      | Incluir atributo app.version en métricas        | `false`              | `true`                    |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Incluir atributo user.account\_uuid en métricas | `true`               | `false`                   |

Estas variables ayudan a controlar la cardinalidad de las métricas, lo que afecta los requisitos de almacenamiento y el rendimiento de las consultas en tu backend de métricas. Una cardinalidad más baja generalmente significa mejor rendimiento y costos de almacenamiento más bajos, pero datos menos granulares para el análisis.

### Encabezados dinámicos

Para entornos empresariales que requieren autenticación dinámica, puedes configurar un script para generar encabezados dinámicamente:

#### Configuración de ajustes

Agrega a tu `.claude/settings.json`:

```json  theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Requisitos del script

El script debe generar JSON válido con pares clave-valor de cadena que representen encabezados HTTP:

```bash  theme={null}
#!/bin/bash
# Ejemplo: Múltiples encabezados
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Comportamiento de actualización

El script auxiliar de encabezados se ejecuta al inicio y periódicamente después para admitir la actualización de tokens. Por defecto, el script se ejecuta cada 29 minutos. Personaliza el intervalo con la variable de entorno `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Soporte de organización multi-equipo

Las organizaciones con múltiples equipos o departamentos pueden agregar atributos personalizados para distinguir entre diferentes grupos usando la variable de entorno `OTEL_RESOURCE_ATTRIBUTES`:

```bash  theme={null}
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

  La variable de entorno `OTEL_RESOURCE_ATTRIBUTES` sigue la [especificación W3C Baggage](https://www.w3.org/TR/baggage/), que tiene requisitos de formato estrictos:

  * **No se permiten espacios**: Los valores no pueden contener espacios. Por ejemplo, `user.organizationName=My Company` es inválido
  * **Formato**: Debe ser pares clave=valor separados por comas: `key1=value1,key2=value2`
  * **Caracteres permitidos**: Solo caracteres US-ASCII excluyendo caracteres de control, espacios en blanco, comillas dobles, comas, puntos y comas, y barras invertidas
  * **Caracteres especiales**: Los caracteres fuera del rango permitido deben estar codificados en porcentaje

  **Ejemplos:**

  ```bash  theme={null}
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

```bash  theme={null}
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
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

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

| Atributo            | Descripción                                                             | Controlado Por                                             |
| ------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------- |
| `session.id`        | Identificador único de sesión                                           | `OTEL_METRICS_INCLUDE_SESSION_ID` (predeterminado: true)   |
| `app.version`       | Versión actual de Claude Code                                           | `OTEL_METRICS_INCLUDE_VERSION` (predeterminado: false)     |
| `organization.id`   | UUID de organización (cuando está autenticado)                          | Siempre incluido cuando está disponible                    |
| `user.account_uuid` | UUID de cuenta (cuando está autenticado)                                | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (predeterminado: true) |
| `terminal.type`     | Tipo de terminal (por ejemplo, `iTerm.app`, `vscode`, `cursor`, `tmux`) | Siempre incluido cuando se detecta                         |

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

#### Contador de sesión

Se incrementa al inicio de cada sesión.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)

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
* `model`: Identificador de modelo (por ejemplo, "claude-sonnet-4-5-20250929")

#### Contador de tokens

Se incrementa después de cada solicitud de API.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Identificador de modelo (por ejemplo, "claude-sonnet-4-5-20250929")

#### Contador de decisión de herramienta de edición de código

Se incrementa cuando el usuario acepta o rechaza el uso de herramientas Edit, Write o NotebookEdit.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `tool`: Nombre de la herramienta (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Decisión del usuario (`"accept"`, `"reject"`)
* `language`: Lenguaje de programación del archivo editado (por ejemplo, `"TypeScript"`, `"Python"`, `"JavaScript"`, `"Markdown"`). Devuelve `"unknown"` para extensiones de archivo no reconocidas.

#### Contador de tiempo activo

Rastrea el tiempo real dedicado a usar activamente Claude Code (no tiempo inactivo). Esta métrica se incrementa durante interacciones del usuario como escribir mensajes o recibir respuestas.

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)

### Eventos

Claude Code exporta los siguientes eventos a través de registros/eventos de OpenTelemetry (cuando `OTEL_LOGS_EXPORTER` está configurado):

#### Evento de mensaje del usuario

Se registra cuando un usuario envía un mensaje.

**Nombre del Evento**: `claude_code.user_prompt`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `prompt_length`: Longitud del mensaje
* `prompt`: Contenido del mensaje (redactado por defecto, habilitar con `OTEL_LOG_USER_PROMPTS=1`)

#### Evento de resultado de herramienta

Se registra cuando una herramienta completa la ejecución.

**Nombre del Evento**: `claude_code.tool_result`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `tool_name`: Nombre de la herramienta
* `success`: `"true"` o `"false"`
* `duration_ms`: Tiempo de ejecución en milisegundos
* `error`: Mensaje de error (si falló)
* `decision`: Ya sea `"accept"` o `"reject"`
* `source`: Fuente de decisión - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`
* `tool_parameters`: Cadena JSON que contiene parámetros específicos de la herramienta (cuando está disponible)
  * Para herramienta Bash: incluye `bash_command`, `full_command`, `timeout`, `description`, `sandbox`

#### Evento de solicitud de API

Se registra para cada solicitud de API a Claude.

**Nombre del Evento**: `claude_code.api_request`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `model`: Modelo utilizado (por ejemplo, "claude-sonnet-4-5-20250929")
* `cost_usd`: Costo estimado en USD
* `duration_ms`: Duración de la solicitud en milisegundos
* `input_tokens`: Número de tokens de entrada
* `output_tokens`: Número de tokens de salida
* `cache_read_tokens`: Número de tokens leídos del caché
* `cache_creation_tokens`: Número de tokens utilizados para la creación del caché

#### Evento de error de API

Se registra cuando una solicitud de API a Claude falla.

**Nombre del Evento**: `claude_code.api_error`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `model`: Modelo utilizado (por ejemplo, "claude-sonnet-4-5-20250929")
* `error`: Mensaje de error
* `status_code`: Código de estado HTTP (si aplica)
* `duration_ms`: Duración de la solicitud en milisegundos
* `attempt`: Número de intento (para solicitudes reintentadas)

#### Evento de decisión de herramienta

Se registra cuando se toma una decisión de permiso de herramienta (aceptar/rechazar).

**Nombre del Evento**: `claude_code.tool_decision`

**Atributos**:

* Todos los [atributos estándar](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Marca de tiempo ISO 8601
* `tool_name`: Nombre de la herramienta (por ejemplo, "Read", "Edit", "Write", "NotebookEdit")
* `decision`: Ya sea `"accept"` o `"reject"`
* `source`: Fuente de decisión - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`

## Interpretación de datos de métricas y eventos

Las métricas exportadas por Claude Code proporcionan información valiosa sobre patrones de uso y productividad. Aquí hay algunas visualizaciones y análisis comunes que puedes crear:

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
  Las métricas de costo son aproximaciones. Para datos de facturación oficiales, consulta tu proveedor de API (Claude Console, AWS Bedrock o Google Cloud Vertex).
</Note>

### Alertas y segmentación

Alertas comunes a considerar:

* Picos de costo
* Consumo inusual de tokens
* Alto volumen de sesiones de usuarios específicos

Todas las métricas pueden segmentarse por `user.account_uuid`, `organization.id`, `session.id`, `model` y `app.version`.

### Análisis de eventos

Los datos de eventos proporcionan información detallada sobre las interacciones de Claude Code:

**Patrones de Uso de Herramientas**: analizar eventos de resultado de herramientas para identificar:

* Herramientas más utilizadas frecuentemente
* Tasas de éxito de herramientas
* Tiempos de ejecución promedio de herramientas
* Patrones de error por tipo de herramienta

**Monitoreo de Rendimiento**: rastrear duraciones de solicitudes de API y tiempos de ejecución de herramientas para identificar cuellos de botella de rendimiento.

## Consideraciones de backend

Tu elección de backends de métricas y registros determina los tipos de análisis que puedes realizar:

### Para métricas

* **Bases de datos de series temporales (por ejemplo, Prometheus)**: Cálculos de tasa, métricas agregadas
* **Almacenes columnares (por ejemplo, ClickHouse)**: Consultas complejas, análisis de usuario único
* **Plataformas de observabilidad completas (por ejemplo, Honeycomb, Datadog)**: Consultas avanzadas, visualización, alertas

### Para eventos/registros

* **Sistemas de agregación de registros (por ejemplo, Elasticsearch, Loki)**: Búsqueda de texto completo, análisis de registros
* **Almacenes columnares (por ejemplo, ClickHouse)**: Análisis de eventos estructurados
* **Plataformas de observabilidad completas (por ejemplo, Honeycomb, Datadog)**: Correlación entre métricas y eventos

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

## Consideraciones de seguridad/privacidad

* La telemetría es opcional y requiere configuración explícita
* La información sensible como claves de API o contenidos de archivos nunca se incluye en métricas o eventos
* El contenido del mensaje del usuario se redacta por defecto - solo se registra la longitud del mensaje. Para habilitar el registro de mensajes del usuario, establece `OTEL_LOG_USER_PROMPTS=1`

## Monitoreo de Claude Code en Amazon Bedrock

Para orientación detallada sobre monitoreo de uso de Claude Code para Amazon Bedrock, consulta [Implementación de Monitoreo de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
