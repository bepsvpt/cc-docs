> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Uso de datos

> Conozca las políticas de uso de datos de Anthropic para Claude

## Políticas de datos

### Política de entrenamiento de datos

**Usuarios de consumidor (planes Free, Pro y Max)**:
Le damos la opción de permitir que sus datos se utilicen para mejorar futuros modelos de Claude. Entrenaremos nuevos modelos utilizando datos de cuentas Free, Pro y Max cuando esta configuración esté activada (incluso cuando utiliza Claude Code desde estas cuentas).

**Usuarios comerciales**: (planes Team y Enterprise, API, plataformas de terceros y Claude Gov) mantienen políticas existentes: Anthropic no entrena modelos generativos utilizando código o indicaciones enviados a Claude Code bajo términos comerciales, a menos que el cliente haya elegido proporcionarnos sus datos para mejorar el modelo (por ejemplo, el [Development Partner Program](https://support.claude.com/es/articles/11174108-about-the-development-partner-program)).

### Development Partner Program

Si opta explícitamente por métodos para proporcionarnos materiales para entrenar, como a través del [Development Partner Program](https://support.claude.com/es/articles/11174108-about-the-development-partner-program), podemos utilizar esos materiales proporcionados para entrenar nuestros modelos. Un administrador de la organización puede optar explícitamente por el Development Partner Program para su organización. Tenga en cuenta que este programa está disponible solo para API de primera parte de Anthropic, y no para usuarios de Bedrock o Vertex.

### Comentarios usando el comando `/bug`

Si elige enviarnos comentarios sobre Claude Code usando el comando `/bug`, podemos utilizar sus comentarios para mejorar nuestros productos y servicios. Las transcripciones compartidas a través de `/bug` se retienen durante 5 años.

### Encuestas de calidad de sesión

Cuando ve el mensaje "¿Cómo está funcionando Claude en esta sesión?" en Claude Code, responder a esta encuesta (incluyendo seleccionar "Descartar"), solo se registra su calificación numérica (1, 2, 3 o descartar). No recopilamos ni almacenamos transcripciones de conversación, entradas, salidas u otros datos de sesión como parte de esta encuesta. A diferencia de los comentarios de pulgar hacia arriba/abajo o los informes `/bug`, esta encuesta de calidad de sesión es una métrica simple de satisfacción del producto. Sus respuestas a esta encuesta no afectan sus preferencias de entrenamiento de datos y no se pueden utilizar para entrenar nuestros modelos de IA.

Para desactivar estas encuestas, establezca `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. La encuesta también se desactiva automáticamente cuando se utilizan proveedores de terceros (Bedrock, Vertex, Foundry) o cuando la telemetría está desactivada.

### Retención de datos

Anthropic retiene datos de Claude Code según su tipo de cuenta y preferencias.

**Usuarios de consumidor (planes Free, Pro y Max)**:

* Usuarios que permiten el uso de datos para mejorar el modelo: período de retención de 5 años para apoyar el desarrollo del modelo y mejoras de seguridad
* Usuarios que no permiten el uso de datos para mejorar el modelo: período de retención de 30 días
* La configuración de privacidad se puede cambiar en cualquier momento en [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Usuarios comerciales (Team, Enterprise y API)**:

* Estándar: período de retención de 30 días
* [Zero data retention](/es/zero-data-retention): disponible para Claude Code en Claude for Enterprise. ZDR se habilita por organización; cada nueva organización debe tener ZDR habilitado por separado por su equipo de cuenta
* Almacenamiento en caché local: los clientes de Claude Code pueden almacenar sesiones localmente hasta 30 días para permitir la reanudación de sesiones (configurable)

Puede eliminar sesiones individuales de Claude Code en la web en cualquier momento. Eliminar una sesión elimina permanentemente los datos de eventos de la sesión. Para obtener instrucciones sobre cómo eliminar sesiones, consulte [Managing sessions](/es/claude-code-on-the-web#managing-sessions).

Obtenga más información sobre las prácticas de retención de datos en nuestro [Privacy Center](https://privacy.anthropic.com/).

Para obtener todos los detalles, consulte nuestros [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (para usuarios de Team, Enterprise y API) o [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (para usuarios de Free, Pro y Max) y [Privacy Policy](https://www.anthropic.com/legal/privacy).

## Acceso a datos

Para todos los usuarios de primera parte, puede obtener más información sobre qué datos se registran para [Claude Code local](#local-claude-code-data-flow-and-dependencies) y [Claude Code remoto](#cloud-execution-data-flow-and-dependencies). Las sesiones de [Remote Control](/es/remote-control) siguen el flujo de datos local ya que toda la ejecución ocurre en su máquina. Tenga en cuenta que para Claude Code remoto, Claude accede al repositorio donde inicia su sesión de Claude Code. Claude no accede a repositorios que ha conectado pero en los que no ha iniciado una sesión.

## Local Claude Code: Flujo de datos y dependencias

El diagrama a continuación muestra cómo Claude Code se conecta a servicios externos durante la instalación y operación normal. Las líneas sólidas indican conexiones requeridas, mientras que las líneas punteadas representan flujos de datos opcionales o iniciados por el usuario.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/claude-code-data-flow.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=b3f71c69d743bff63343207dfb7ad6ce" alt="Diagrama que muestra las conexiones externas de Claude Code: instalar/actualizar se conecta a NPM, y las solicitudes del usuario se conectan a servicios de Anthropic incluyendo autenticación de consola, API pública, y opcionalmente Statsig, Sentry e informes de errores" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code se instala desde [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code se ejecuta localmente. Para interactuar con el LLM, Claude Code envía datos a través de la red. Estos datos incluyen todos los indicadores del usuario y salidas del modelo. Los datos se cifran en tránsito a través de TLS y no se cifran en reposo. Claude Code es compatible con la mayoría de VPN y proxies LLM populares.

Claude Code se construye sobre las API de Anthropic. Para obtener detalles sobre los controles de seguridad de nuestra API, incluidos nuestros procedimientos de registro de API, consulte los artefactos de cumplimiento ofrecidos en el [Anthropic Trust Center](https://trust.anthropic.com).

### Cloud execution: Flujo de datos y dependencias

Cuando se utiliza [Claude Code en la web](/es/claude-code-on-the-web), las sesiones se ejecutan en máquinas virtuales administradas por Anthropic en lugar de localmente. En entornos en la nube:

* **Almacenamiento de código y datos:** Su repositorio se clona en una VM aislada. El código y los datos de sesión están sujetos a las políticas de retención y uso para su tipo de cuenta (consulte la sección Retención de datos anterior)
* **Credenciales:** La autenticación de GitHub se maneja a través de un proxy seguro; sus credenciales de GitHub nunca ingresan al sandbox
* **Tráfico de red:** Todo el tráfico saliente pasa a través de un proxy de seguridad para registro de auditoría y prevención de abuso
* **Datos de sesión:** Los indicadores, cambios de código y salidas siguen las mismas políticas de datos que el uso local de Claude Code

Para obtener detalles de seguridad sobre la ejecución en la nube, consulte [Security](/es/security#cloud-execution-security).

## Servicios de telemetría

Claude Code se conecta desde las máquinas de los usuarios al servicio Statsig para registrar métricas operativas como latencia, confiabilidad y patrones de uso. Este registro no incluye ningún código o ruta de archivo. Los datos se cifran en tránsito usando TLS y en reposo usando cifrado AES de 256 bits. Lea más en la [documentación de seguridad de Statsig](https://www.statsig.com/trust/security). Para optar por no participar en la telemetría de Statsig, establezca la variable de entorno `DISABLE_TELEMETRY`.

Claude Code se conecta desde las máquinas de los usuarios a Sentry para el registro de errores operativos. Los datos se cifran en tránsito usando TLS y en reposo usando cifrado AES de 256 bits. Lea más en la [documentación de seguridad de Sentry](https://sentry.io/security/). Para optar por no participar en el registro de errores, establezca la variable de entorno `DISABLE_ERROR_REPORTING`.

Cuando los usuarios ejecutan el comando `/bug`, se envía una copia de su historial de conversación completo incluyendo código a Anthropic. Los datos se cifran en tránsito y en reposo. Opcionalmente, se crea un problema de Github en nuestro repositorio público. Para optar por no participar en los informes de errores, establezca la variable de entorno `DISABLE_BUG_COMMAND`.

## Comportamientos predeterminados por proveedor de API

De forma predeterminada, deshabilitamos todo el tráfico no esencial (incluyendo informes de errores, telemetría, funcionalidad de informes de errores y encuestas de calidad de sesión) cuando se utiliza Bedrock, Vertex o Foundry. También puede optar por no participar en todos estos a la vez estableciendo la variable de entorno `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Aquí están los comportamientos predeterminados completos:

| Servicio                           | Claude API                                                                                      | Vertex API                                                                     | Bedrock API                                                                     | Foundry API                                                                     |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Statsig (Métricas)**             | Activado de forma predeterminada.<br />`DISABLE_TELEMETRY=1` para desactivar.                   | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_FOUNDRY` debe ser 1. |
| **Sentry (Errores)**               | Activado de forma predeterminada.<br />`DISABLE_ERROR_REPORTING=1` para desactivar.             | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_FOUNDRY` debe ser 1. |
| **Claude API (informes `/bug`)**   | Activado de forma predeterminada.<br />`DISABLE_BUG_COMMAND=1` para desactivar.                 | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_FOUNDRY` debe ser 1. |
| **Encuestas de calidad de sesión** | Activado de forma predeterminada.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` para desactivar. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. | Desactivado de forma predeterminada.<br />`CLAUDE_CODE_USE_FOUNDRY` debe ser 1. |

Todas las variables de entorno se pueden verificar en `settings.json` ([leer más](/es/settings)).
