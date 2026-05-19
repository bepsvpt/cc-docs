> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuración del modelo

> Aprenda sobre la configuración del modelo Claude Code, incluidos los alias de modelo como `opusplan`

## Modelos disponibles

Para la configuración de `model` en Claude Code, puede configurar:

* Un **alias de modelo**
* Un **nombre de modelo**
  * API de Anthropic: Un **[nombre de modelo](https://platform.claude.com/docs/es/about-claude/models/overview)** completo
  * Bedrock: un ARN de perfil de inferencia
  * Foundry: un nombre de implementación
  * Vertex: un nombre de versión

<Note>
  `ANTHROPIC_BASE_URL` cambia dónde se envían las solicitudes, no qué modelo las responde. Para enrutar Claude a través de una puerta de enlace LLM, consulte [configuración de puerta de enlace LLM](/es/llm-gateway).
</Note>

### Alias de modelo

Los alias de modelo proporcionan una forma conveniente de seleccionar configuraciones de modelo sin necesidad de recordar números de versión exactos:

| Alias de modelo  | Comportamiento                                                                                                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Valor especial que borra cualquier anulación de modelo y revierte al modelo recomendado para su tipo de cuenta. No es en sí mismo un alias de modelo                                   |
| **`best`**       | Utiliza el modelo disponible más capaz, actualmente equivalente a `opus`                                                                                                               |
| **`sonnet`**     | Utiliza el último modelo Sonnet para tareas de codificación diaria                                                                                                                     |
| **`opus`**       | Utiliza el último modelo Opus para tareas de razonamiento complejo                                                                                                                     |
| **`haiku`**      | Utiliza el modelo Haiku rápido y eficiente para tareas simples                                                                                                                         |
| **`sonnet[1m]`** | Utiliza Sonnet con una [ventana de contexto de 1 millón de tokens](https://platform.claude.com/docs/es/build-with-claude/context-windows#1m-token-context-window) para sesiones largas |
| **`opus[1m]`**   | Utiliza Opus con una [ventana de contexto de 1 millón de tokens](https://platform.claude.com/docs/es/build-with-claude/context-windows#1m-token-context-window) para sesiones largas   |
| **`opusplan`**   | Modo especial que utiliza `opus` durante el modo de plan, luego cambia a `sonnet` para la ejecución                                                                                    |

En la API de Anthropic y [Claude Platform on AWS](/es/claude-platform-on-aws), `opus` se resuelve a Opus 4.7 y `sonnet` se resuelve a Sonnet 4.6. En Bedrock, Vertex y Foundry, `opus` se resuelve a Opus 4.6 y `sonnet` se resuelve a Sonnet 4.5; hay modelos más nuevos disponibles en esos proveedores seleccionando el nombre de modelo completo explícitamente o estableciendo `ANTHROPIC_DEFAULT_OPUS_MODEL` o `ANTHROPIC_DEFAULT_SONNET_MODEL`.

Los alias siempre apuntan a la versión recomendada para su proveedor y se actualizan con el tiempo. Para fijar una versión específica, utilice el nombre de modelo completo (por ejemplo, `claude-opus-4-7`) o establezca la variable de entorno correspondiente como `ANTHROPIC_DEFAULT_OPUS_MODEL`.

<Note>
  Opus 4.7 requiere Claude Code v2.1.111 o posterior. Ejecute `claude update` para actualizar.
</Note>

### Configurar su modelo

Puede configurar su modelo de varias formas, enumeradas en orden de prioridad:

1. **Durante la sesión** - Utilice `/model <alias|name>` para cambiar inmediatamente, o ejecute `/model` sin argumentos para abrir el selector. El selector solicita confirmación cuando la conversación tiene salida anterior, ya que la siguiente respuesta relee el historial completo sin contexto en caché
2. **Al inicio** - Inicie con `claude --model <alias|name>`
3. **Variable de entorno** - Establezca `ANTHROPIC_MODEL=<alias|name>`
4. **Configuración** - Configure permanentemente en su archivo de configuración utilizando el campo `model`.

Su selección de `/model` se guarda en la configuración del usuario y persiste entre reinicios. A partir de v2.1.117, si el archivo `.claude/settings.json` del proyecto fija un modelo diferente, Claude Code también escribe su selección en `.claude/settings.local.json` para que continúe aplicándose en ese proyecto después de un reinicio. La configuración administrada tiene prioridad y se reaplicará en el siguiente lanzamiento.

Cuando el modelo activo al inicio proviene de la configuración del proyecto o administrada en lugar de su propia selección, el encabezado de inicio muestra qué archivo de configuración lo estableció. Ejecute `/model` para anular la selección de la sesión actual.

Ejemplo de uso:

```bash theme={null}
# Iniciar con Opus
claude --model opus

# Cambiar a Sonnet durante la sesión
/model sonnet
```

Archivo de configuración de ejemplo:

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Restringir la selección de modelo

Los administradores empresariales pueden utilizar `availableModels` en [configuración administrada o de política](/es/settings#settings-files) para restringir qué modelos pueden seleccionar los usuarios.

Cuando se establece `availableModels`, los usuarios no pueden cambiar a modelos que no estén en la lista a través de `/model`, la bandera `--model`, o la variable de entorno `ANTHROPIC_MODEL`.

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportamiento del modelo predeterminado

La opción Predeterminado en el selector de modelo no se ve afectada por `availableModels`. Siempre permanece disponible y representa el valor predeterminado de tiempo de ejecución del sistema [basado en el nivel de suscripción del usuario](#default-model-setting).

Incluso con `availableModels: []`, los usuarios aún pueden usar Claude Code con el modelo Predeterminado para su nivel.

### Controlar el modelo en el que se ejecutan los usuarios

La configuración de `model` es una selección inicial, no una aplicación. Establece qué modelo está activo cuando comienza una sesión, pero los usuarios aún pueden abrir `/model` y elegir Predeterminado, que se resuelve al valor predeterminado del sistema para su nivel independientemente de lo que esté configurado en `model`.

Para controlar completamente la experiencia del modelo, combine tres configuraciones:

* **`availableModels`**: restringe a qué modelos nombrados pueden cambiar los usuarios
* **`model`**: establece la selección de modelo inicial cuando comienza una sesión
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**: controlan a qué se resuelven la opción Predeterminado y los alias `sonnet`, `opus` y `haiku`

Este ejemplo inicia a los usuarios en Sonnet 4.5, limita el selector a Sonnet y Haiku, y fija Predeterminado para que se resuelva a Sonnet 4.5 en lugar de la versión más reciente:

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Sin el bloque `env`, un usuario que seleccione Predeterminado en el selector obtendría la versión más reciente de Sonnet, omitiendo la fijación de versión en `model` y `availableModels`.

### Comportamiento de fusión

Cuando `availableModels` se establece en múltiples niveles, como configuración de usuario y configuración de proyecto, los arrays se fusionan y se desduplican. Para aplicar una lista de permitidos estricta, establezca `availableModels` en configuración administrada o de política que tenga la máxima prioridad.

### IDs de modelo Mantle

Cuando el [punto final Bedrock Mantle](/es/amazon-bedrock#use-the-mantle-endpoint) está habilitado, las entradas en `availableModels` que comienzan con `anthropic.` se agregan al selector `/model` como opciones personalizadas y se enrutan al punto final Mantle. Esta es una excepción a la coincidencia solo de alias descrita en [Fijar modelos para implementaciones de terceros](#pin-models-for-third-party-deployments). La configuración aún restringe el selector a las entradas enumeradas, así que incluya los alias estándar junto con cualquier ID de Mantle.

## Comportamiento especial del modelo

### Configuración del modelo `default`

El comportamiento de `default` depende del tipo de cuenta:

* **Max y Team Premium**: por defecto Opus 4.7
* **Pro, Team Standard, Enterprise y API de Anthropic**: por defecto Sonnet 4.6
* **Bedrock, Vertex y Foundry**: por defecto Sonnet 4.5

Claude Code puede retroceder automáticamente a Sonnet si alcanza un umbral de uso con Opus.

<Note>
  El 23 de abril de 2026, el modelo predeterminado para usuarios de Enterprise de pago por uso y API de Anthropic cambiará a Opus 4.7. Para mantener un predeterminado diferente, establezca `ANTHROPIC_MODEL` o el campo `model` en [configuración administrada por servidor](/es/server-managed-settings).
</Note>

### Configuración del modelo `opusplan`

El alias de modelo `opusplan` proporciona un enfoque híbrido automatizado:

* **En Plan Mode** - Utiliza `opus` para razonamiento complejo y decisiones de arquitectura
* **En modo de ejecución** - Cambia automáticamente a `sonnet` para generación de código e implementación

Esto le da lo mejor de ambos mundos: el razonamiento superior de Opus para la planificación y la eficiencia de Sonnet para la ejecución.

La fase Opus en Plan Mode se ejecuta con la ventana de contexto estándar de 200K. La actualización automática de 1M descrita en [Contexto extendido](#extended-context) se aplica a la configuración del modelo `opus` y no se extiende a `opusplan`.

### Ajustar el nivel de esfuerzo

[Los niveles de esfuerzo](https://platform.claude.com/docs/es/build-with-claude/effort) controlan el razonamiento adaptativo, que permite que el modelo decida si y cuánto pensar en cada paso basado en la complejidad de la tarea. El esfuerzo menor es más rápido y económico para tareas directas, mientras que el esfuerzo mayor proporciona un razonamiento más profundo para problemas complejos.

El esfuerzo es compatible con Opus 4.7, Opus 4.6 y Sonnet 4.6. Los niveles disponibles dependen del modelo:

| Modelo                | Niveles                                 |
| :-------------------- | :-------------------------------------- |
| Opus 4.7              | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 y Sonnet 4.6 | `low`, `medium`, `high`, `max`          |

Si establece un nivel que el modelo activo no admite, Claude Code retrocede al nivel más alto admitido en o por debajo del que estableció. Por ejemplo, `xhigh` se ejecuta como `high` en Opus 4.6.

A partir de v2.1.117, el esfuerzo predeterminado es `xhigh` en Opus 4.7 y `high` en Opus 4.6 y Sonnet 4.6.

Cuando ejecuta Opus 4.7 por primera vez, Claude Code aplica `xhigh` incluso si estableció anteriormente un nivel de esfuerzo diferente para Opus 4.6 o Sonnet 4.6. Ejecute `/effort` nuevamente para elegir un nivel diferente después de cambiar.

`low`, `medium`, `high` y `xhigh` persisten entre sesiones. `max` proporciona el razonamiento más profundo sin restricción en el gasto de tokens y se aplica solo a la sesión actual, excepto cuando se establece a través de la variable de entorno `CLAUDE_CODE_EFFORT_LEVEL`.

#### Elegir un nivel de esfuerzo

Cada nivel intercambia gasto de tokens contra capacidad. El predeterminado es adecuado para la mayoría de tareas de codificación; ajuste cuando desee un equilibrio diferente.

| Nivel    | Cuándo usarlo                                                                                                                                                       |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `low`    | Reserve para tareas cortas, limitadas y sensibles a la latencia que no son sensibles a la inteligencia                                                              |
| `medium` | Reduce el uso de tokens para trabajo sensible a costos que puede intercambiar algo de inteligencia                                                                  |
| `high`   | Equilibra el uso de tokens e inteligencia. Utilice como mínimo para trabajo sensible a la inteligencia, o para reducir el gasto de tokens en relación con `xhigh`   |
| `xhigh`  | Mejores resultados para la mayoría de tareas de codificación y agentes. Predeterminado recomendado en Opus 4.7                                                      |
| `max`    | Puede mejorar el rendimiento en tareas exigentes pero puede mostrar rendimientos decrecientes y es propenso a pensar demasiado. Pruebe antes de adoptar ampliamente |

La escala de esfuerzo se calibra por modelo, por lo que el mismo nombre de nivel no representa el mismo valor subyacente en todos los modelos.

#### Utilizar ultrathink para razonamiento profundo único

Incluya `ultrathink` en cualquier lugar de su indicación para solicitar un razonamiento más profundo en ese turno sin cambiar su configuración de esfuerzo de sesión. Claude Code reconoce la palabra clave y añade una instrucción en contexto. El nivel de esfuerzo enviado a la API no cambia. Otras frases como "think", "think hard" y "think more" se pasan como texto de indicación ordinario y no se reconocen como palabras clave.

#### Establecer el nivel de esfuerzo

Puede cambiar el esfuerzo a través de cualquiera de los siguientes:

* **`/effort`**: ejecute `/effort` sin argumentos para abrir un control deslizante interactivo, `/effort` seguido de un nombre de nivel para establecerlo directamente, o `/effort auto` para restablecer el predeterminado del modelo
* **En `/model`**: utilice las teclas de flecha izquierda/derecha para ajustar el control deslizante de esfuerzo al seleccionar un modelo
* **Bandera `--effort`**: pase un nombre de nivel para establecerlo para una única sesión al iniciar Claude Code
* **Variable de entorno**: establezca `CLAUDE_CODE_EFFORT_LEVEL` en un nombre de nivel o `auto`
* **Configuración**: establezca `effortLevel` en `low`, `medium`, `high` o `xhigh` en su archivo de configuración. `max` es [solo de sesión](#adjust-effort-level) y no se acepta aquí
* **Frontmatter de skill y subagent**: establezca `effort` en un archivo markdown de [skill](/es/skills#frontmatter-reference) o [subagent](/es/sub-agents#supported-frontmatter-fields) para anular el nivel de esfuerzo cuando ese skill o subagent se ejecuta

La variable de entorno tiene precedencia sobre todos los demás métodos, luego su nivel configurado, luego el predeterminado del modelo. El esfuerzo de frontmatter se aplica cuando ese skill o subagent está activo, anulando el nivel de sesión pero no la variable de entorno.

El control deslizante de esfuerzo aparece en `/model` cuando se selecciona un modelo compatible. El nivel de esfuerzo actual también se muestra junto al logotipo y al indicador, por ejemplo "with low effort", para que pueda confirmar qué configuración está activa sin abrir `/model`.

#### Razonamiento adaptativo y presupuestos de pensamiento fijo

El razonamiento adaptativo hace que el pensamiento sea opcional en cada paso, por lo que Claude puede responder más rápido a indicaciones rutinarias y reservar un pensamiento más profundo para pasos que se benefician de él. Si desea que Claude piense más o menos a menudo de lo que produce el nivel actual, puede decirlo directamente en su indicación o en `CLAUDE.md`; el modelo responde a esa orientación dentro de su configuración de esfuerzo.

Opus 4.7 siempre utiliza razonamiento adaptativo. El modo de presupuesto de pensamiento fijo y `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` no se aplican a él.

En Opus 4.6 y Sonnet 4.6, puede establecer `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` para revertir al presupuesto de pensamiento fijo anterior controlado por `MAX_THINKING_TOKENS`. Consulte [variables de entorno](/es/env-vars).

### Pensamiento extendido

El pensamiento extendido es el razonamiento que Claude emite antes de responder. En modelos que admiten [razonamiento adaptativo](#adjust-effort-level), el nivel de esfuerzo es el control principal de cuánto pensamiento ocurre; la configuración a continuación activa o desactiva el pensamiento y controla cómo se muestra.

| Control                                    | Cómo configurarlo                                                                                                                                                          |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alternar para la sesión actual             | Presione `Option+T` en macOS o `Alt+T` en Windows y Linux                                                                                                                  |
| Establecer el predeterminado global        | Ejecute `/config` y alterne el modo de pensamiento. Se guarda como `alwaysThinkingEnabled` en `~/.claude/settings.json`                                                    |
| Desactivar independientemente del esfuerzo | Establezca [`MAX_THINKING_TOKENS=0`](/es/env-vars). Otros valores se aplican solo con un [presupuesto de pensamiento fijo](#adaptive-reasoning-and-fixed-thinking-budgets) |

La salida de pensamiento se colapsa de forma predeterminada. Presione `Ctrl+O` para alternar el modo detallado y ver el razonamiento como texto gris en cursiva. Las sesiones interactivas en la API de Anthropic reciben bloques de pensamiento redactados de forma predeterminada, por lo que establezca `showThinkingSummaries: true` en [configuración](/es/settings) si desea que los resúmenes completos estén disponibles cuando se expandan. Se le cobra por todos los tokens de pensamiento generados, incluso cuando se colapsan o se redactan.

### Contexto extendido

Opus 4.7, Opus 4.6 y Sonnet 4.6 admiten una [ventana de contexto de 1 millón de tokens](https://platform.claude.com/docs/es/build-with-claude/context-windows#1m-token-context-window) para sesiones largas con bases de código grandes.

La disponibilidad varía según el modelo y el plan. En los planes Max, Team y Enterprise, Opus se actualiza automáticamente a contexto de 1M sin configuración adicional. Esto se aplica tanto a los asientos de Team Standard como de Team Premium. Sonnet con contexto de 1M no es parte de la actualización automática y requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) en todos los planes de suscripción, incluido Max.

| Plan                   | Opus con contexto de 1M                                                                                     | Sonnet con contexto de 1M                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Max, Team y Enterprise | Incluido en la suscripción                                                                                  | Requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                    | Requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) | Requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) |
| API y pago por uso     | Acceso completo                                                                                             | Acceso completo                                                                                             |

Para desactivar completamente el contexto de 1M, establezca `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Esto elimina variantes de modelo de 1M del selector de modelo. Consulte [variables de entorno](/es/env-vars).

La ventana de contexto de 1M utiliza precios de modelo estándar sin prima para tokens más allá de 200K. Para planes donde el contexto extendido está incluido en su suscripción, el uso permanece cubierto por su suscripción. Para planes que acceden al contexto extendido a través de uso adicional, los tokens se facturan al uso adicional.

Si su cuenta admite contexto de 1M, la opción aparece en el selector de modelo (`/model`) en las últimas versiones de Claude Code. Si no la ve, intente reiniciar su sesión.

También puede utilizar el sufijo `[1m]` con alias de modelo o nombres de modelo completos:

```bash theme={null}
# Utilizar el alias opus[1m] o sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# O añadir [1m] a un nombre de modelo completo
/model claude-opus-4-7[1m]
```

## Verificar su modelo actual

Puede ver qué modelo está utilizando actualmente de varias formas:

1. En [línea de estado](/es/statusline) (si está configurada)
2. En `/status`, que también muestra la información de su cuenta.

## Agregar una opción de modelo personalizado

Utilice `ANTHROPIC_CUSTOM_MODEL_OPTION` para agregar una única entrada personalizada al selector `/model` sin reemplazar los alias integrados. Esto es útil para probar IDs de modelo que Claude Code no enumera de forma predeterminada. Para implementaciones de puerta de enlace LLM, Claude Code puede completar automáticamente el selector desde el punto final `/v1/models` de la puerta de enlace cuando se establece `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`, por lo que esta variable solo es necesaria cuando el descubrimiento está deshabilitado o no devuelve el modelo que desea. Consulte [Selección de modelo de puerta de enlace LLM](/es/llm-gateway#model-selection).

Este ejemplo establece las tres variables para hacer que una implementación de Opus enrutada por puerta de enlace sea seleccionable:

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-7"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

La entrada personalizada aparece en la parte inferior del selector `/model`. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` y `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` son opcionales. Si se omiten, el ID de modelo se utiliza como nombre y la descripción tiene como valor predeterminado `Custom model (<model-id>)`.

Claude Code omite la validación para el ID de modelo establecido en `ANTHROPIC_CUSTOM_MODEL_OPTION`, por lo que puede utilizar cualquier cadena que su punto final de API acepte.

## Variables de entorno

Puede utilizar las siguientes variables de entorno, que deben ser **nombres de modelo** completos (o equivalentes para su proveedor de API), para controlar los nombres de modelo a los que se asignan los alias.

| Variable de entorno              | Descripción                                                                                                                                                                               |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | El modelo a utilizar para `opus`, o para `opusplan` cuando Plan Mode está activo.                                                                                                         |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | El modelo a utilizar para `sonnet`, o para `opusplan` cuando Plan Mode no está activo.                                                                                                    |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | El modelo a utilizar para `haiku`, o [funcionalidad de fondo](/es/costs#background-token-usage)                                                                                           |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | El modelo a utilizar para todos los [subagents](/es/sub-agents#choose-a-model). Anula tanto el parámetro `model` por invocación como el frontmatter `model` de la definición del subagent |

Nota: `ANTHROPIC_SMALL_FAST_MODEL` está deprecado en favor de `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Fijar modelos para implementaciones de terceros

Al implementar Claude Code a través de [Bedrock](/es/amazon-bedrock), [Vertex AI](/es/google-vertex-ai), [Foundry](/es/microsoft-foundry), o [Claude Platform on AWS](/es/claude-platform-on-aws), fije versiones de modelo antes de implementar para usuarios.

Sin fijar, Claude Code utiliza alias de modelo (`sonnet`, `opus`, `haiku`) que se resuelven a la versión más reciente. Cuando Anthropic lanza un nuevo modelo que aún no está habilitado en la cuenta de un usuario, los usuarios de Bedrock y Vertex AI ven un aviso y retroceden a la versión anterior para esa sesión, mientras que los usuarios de Foundry ven errores porque Foundry no tiene ninguna verificación de inicio equivalente.

<Warning>
  Establezca las tres variables de entorno de modelo en IDs de versión específicos como parte de su configuración inicial. Fijar le permite controlar cuándo sus usuarios se mueven a un nuevo modelo.
</Warning>

Utilice las siguientes variables de entorno con IDs de modelo específicos de versión para su proveedor:

| Proveedor | Ejemplo                                                              |
| :-------- | :------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |

Aplique el mismo patrón para `ANTHROPIC_DEFAULT_SONNET_MODEL` y `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Para IDs de modelo actuales y heredados en todos los proveedores, consulte [Descripción general de modelos](https://platform.claude.com/docs/es/about-claude/models/overview). Para actualizar usuarios a una nueva versión de modelo, actualice estas variables de entorno e implemente nuevamente.

Para habilitar [contexto extendido](#extended-context) para un modelo fijo, añada `[1m]` al ID de modelo en `ANTHROPIC_DEFAULT_OPUS_MODEL` o `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7[1m]'
```

El sufijo `[1m]` aplica la ventana de contexto de 1M a todo el uso de ese alias, incluido `opusplan`. Claude Code elimina el sufijo antes de enviar el ID de modelo a su proveedor. Solo añada `[1m]` cuando el modelo subyacente admita contexto de 1M, como Opus 4.7 o Sonnet 4.6.

<Note>
  La lista de permitidos `settings.availableModels` aún se aplica cuando se utilizan proveedores de terceros. El filtrado coincide con el alias de modelo (`opus`, `sonnet`, `haiku`), no con el ID de modelo específico del proveedor.
</Note>

### Personalizar la visualización y capacidades del modelo fijo

Cuando fija un modelo en un proveedor de terceros, el ID específico del proveedor aparece tal cual en el selector `/model` y Claude Code puede no reconocer qué características admite el modelo. Puede anular el nombre de visualización y declarar capacidades con variables de entorno complementarias para cada modelo fijo.

Estas variables tienen efecto en proveedores de terceros como Bedrock, Vertex AI y Foundry. Las variables `_NAME` y `_DESCRIPTION` también tienen efecto cuando `ANTHROPIC_BASE_URL` apunta a una [puerta de enlace LLM](/es/llm-gateway). No tienen efecto cuando se conecta directamente a `api.anthropic.com`.

| Variable de entorno                                   | Descripción                                                                                                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Nombre de visualización para el modelo Opus fijo en el selector `/model`. Por defecto al ID de modelo cuando no está configurado            |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Descripción de visualización para el modelo Opus fijo en el selector `/model`. Por defecto a `Custom Opus model` cuando no está configurado |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Lista separada por comas de capacidades que admite el modelo Opus fijo                                                                      |

Los mismos sufijos `_NAME`, `_DESCRIPTION` y `_SUPPORTED_CAPABILITIES` están disponibles para `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` y `ANTHROPIC_CUSTOM_MODEL_OPTION`.

Claude Code habilita características como [niveles de esfuerzo](#adjust-effort-level) y [pensamiento extendido](#extended-thinking) haciendo coincidir el ID de modelo con patrones conocidos. Los IDs específicos del proveedor como ARNs de Bedrock o nombres de implementación personalizados a menudo no coinciden con estos patrones, dejando las características compatibles deshabilitadas. Establezca `_SUPPORTED_CAPABILITIES` para indicar a Claude Code qué características admite realmente el modelo:

| Valor de capacidad     | Habilita                                                                                             |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| `effort`               | [Niveles de esfuerzo](#adjust-effort-level) y el comando `/effort`                                   |
| `xhigh_effort`         | {/* min-version: 2.1.111 */}El nivel de esfuerzo `xhigh`                                             |
| `max_effort`           | El nivel de esfuerzo `max`                                                                           |
| `thinking`             | [Pensamiento extendido](#extended-thinking)                                                          |
| `adaptive_thinking`    | Razonamiento adaptativo que asigna dinámicamente el pensamiento basado en la complejidad de la tarea |
| `interleaved_thinking` | Pensamiento entre llamadas de herramientas                                                           |

Cuando se establece `_SUPPORTED_CAPABILITIES`, las capacidades enumeradas se habilitan y las capacidades no enumeradas se deshabilitan para el modelo fijo coincidente. Cuando la variable no está configurada, Claude Code vuelve a la detección integrada basada en el ID de modelo.

Este ejemplo fija Opus a un ARN de modelo personalizado de Bedrock, establece un nombre amigable y declara sus capacidades:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Anular IDs de modelo por versión

Las variables de entorno a nivel de familia anteriores configuran un ID de modelo por alias de familia. Si necesita asignar varias versiones dentro de la misma familia a IDs de proveedor distintos, utilice la configuración `modelOverrides` en su lugar.

`modelOverrides` asigna IDs de modelo individuales de Anthropic a las cadenas específicas del proveedor que Claude Code envía a la API de su proveedor. Cuando un usuario selecciona un modelo asignado en el selector `/model`, Claude Code utiliza su valor configurado en lugar del predeterminado integrado.

Esto permite a los administradores empresariales enrutar cada versión de modelo a un ARN de perfil de inferencia de Bedrock específico, nombre de versión de Vertex AI o nombre de implementación de Foundry para gobernanza, asignación de costos o enrutamiento regional.

Establezca `modelOverrides` en su [archivo de configuración](/es/settings#settings-files):

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Las claves deben ser IDs de modelo de Anthropic como se enumeran en la [Descripción general de modelos](https://platform.claude.com/docs/es/about-claude/models/overview). Para IDs de modelo con fecha, incluya el sufijo de fecha exactamente como aparece allí. Las claves desconocidas se ignoran.

Las anulaciones reemplazan los IDs de modelo integrados que respaldan cada entrada en el selector `/model`. En Bedrock, las anulaciones tienen precedencia sobre cualquier perfil de inferencia que Claude Code descubra automáticamente al inicio. Los valores que proporciona directamente a través de `ANTHROPIC_MODEL`, `--model`, o las variables de entorno `ANTHROPIC_DEFAULT_*_MODEL` se pasan al proveedor tal como están y no se transforman por `modelOverrides`.

`modelOverrides` funciona junto con `availableModels`. La lista de permitidos se evalúa contra el ID de modelo de Anthropic, no el valor de anulación, por lo que una entrada como `"opus"` en `availableModels` continúa coincidiendo incluso cuando las versiones de Opus se asignan a ARNs.

### Configuración de almacenamiento en caché de indicaciones

Claude Code utiliza automáticamente [almacenamiento en caché de indicaciones](https://platform.claude.com/docs/es/build-with-claude/prompt-caching) para optimizar el rendimiento y reducir costos. Puede desactivar el almacenamiento en caché de indicaciones globalmente o para niveles de modelo específicos:

| Variable de entorno             | Descripción                                                                                                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Establezca en `1` para desactivar el almacenamiento en caché de indicaciones para todos los modelos (tiene precedencia sobre configuraciones por modelo) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Establezca en `1` para desactivar el almacenamiento en caché de indicaciones solo para modelos Haiku                                                     |
| `DISABLE_PROMPT_CACHING_SONNET` | Establezca en `1` para desactivar el almacenamiento en caché de indicaciones solo para modelos Sonnet                                                    |
| `DISABLE_PROMPT_CACHING_OPUS`   | Establezca en `1` para desactivar el almacenamiento en caché de indicaciones solo para modelos Opus                                                      |

Estas variables de entorno le dan control granular sobre el comportamiento del almacenamiento en caché de indicaciones. La configuración global `DISABLE_PROMPT_CACHING` tiene precedencia sobre las configuraciones específicas del modelo, permitiéndole desactivar rápidamente todo el almacenamiento en caché cuando sea necesario. Las configuraciones por modelo son útiles para control selectivo, como cuando se depura modelos específicos o se trabaja con proveedores de nube que pueden tener diferentes implementaciones de almacenamiento en caché.
