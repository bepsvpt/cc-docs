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

### Alias de modelo

Los alias de modelo proporcionan una forma conveniente de seleccionar configuraciones de modelo sin necesidad de recordar números de versión exactos:

| Alias de modelo  | Comportamiento                                                                                                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Configuración de modelo recomendada, según el tipo de cuenta                                                                                                                           |
| **`sonnet`**     | Utiliza el último modelo Sonnet (actualmente Sonnet 4.6) para tareas de codificación diaria                                                                                            |
| **`opus`**       | Utiliza el último modelo Opus (actualmente Opus 4.6) para tareas de razonamiento complejo                                                                                              |
| **`haiku`**      | Utiliza el modelo Haiku rápido y eficiente para tareas simples                                                                                                                         |
| **`sonnet[1m]`** | Utiliza Sonnet con una [ventana de contexto de 1 millón de tokens](https://platform.claude.com/docs/es/build-with-claude/context-windows#1m-token-context-window) para sesiones largas |
| **`opus[1m]`**   | Utiliza Opus con una [ventana de contexto de 1 millón de tokens](https://platform.claude.com/docs/es/build-with-claude/context-windows#1m-token-context-window) para sesiones largas   |
| **`opusplan`**   | Modo especial que utiliza `opus` durante el modo de plan, luego cambia a `sonnet` para la ejecución                                                                                    |

Los alias siempre apuntan a la versión más reciente. Para fijar una versión específica, utilice el nombre de modelo completo (por ejemplo, `claude-opus-4-6`) o establezca la variable de entorno correspondiente como `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Configurar su modelo

Puede configurar su modelo de varias formas, enumeradas en orden de prioridad:

1. **Durante la sesión** - Utilice `/model <alias|name>` para cambiar modelos durante la sesión
2. **Al inicio** - Inicie con `claude --model <alias|name>`
3. **Variable de entorno** - Establezca `ANTHROPIC_MODEL=<alias|name>`
4. **Configuración** - Configure permanentemente en su archivo de configuración utilizando el campo `model`.

Ejemplo de uso:

```bash  theme={null}
# Iniciar con Opus
claude --model opus

# Cambiar a Sonnet durante la sesión
/model sonnet
```

Archivo de configuración de ejemplo:

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Restringir la selección de modelo

Los administradores empresariales pueden utilizar `availableModels` en [configuración administrada o de política](/es/settings#settings-files) para restringir qué modelos pueden seleccionar los usuarios.

Cuando se establece `availableModels`, los usuarios no pueden cambiar a modelos que no estén en la lista a través de `/model`, la bandera `--model`, la herramienta Config o la variable de entorno `ANTHROPIC_MODEL`.

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportamiento del modelo predeterminado

La opción Predeterminado en el selector de modelo no se ve afectada por `availableModels`. Siempre permanece disponible y representa el valor predeterminado de tiempo de ejecución del sistema [basado en el nivel de suscripción del usuario](#default-model-setting).

Incluso con `availableModels: []`, los usuarios aún pueden usar Claude Code con el modelo Predeterminado para su nivel.

### Controlar el modelo en el que se ejecutan los usuarios

Para controlar completamente la experiencia del modelo, utilice `availableModels` junto con la configuración `model`:

* **availableModels**: restringe a qué pueden cambiar los usuarios
* **model**: establece la anulación de modelo explícita, tomando precedencia sobre el Predeterminado

Este ejemplo asegura que todos los usuarios ejecuten Sonnet 4.6 y solo puedan elegir entre Sonnet y Haiku:

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportamiento de fusión

Cuando `availableModels` se establece en múltiples niveles, como configuración de usuario y configuración de proyecto, los arrays se fusionan y se desduplican. Para aplicar una lista de permitidos estricta, establezca `availableModels` en configuración administrada o de política que tenga la máxima prioridad.

## Comportamiento especial del modelo

### Configuración del modelo `default`

El comportamiento de `default` depende del tipo de cuenta:

* **Max y Team Premium**: por defecto Opus 4.6
* **Pro y Team Standard**: por defecto Sonnet 4.6
* **Enterprise**: Opus 4.6 está disponible pero no es el predeterminado

Claude Code puede retroceder automáticamente a Sonnet si alcanza un umbral de uso con Opus.

### Configuración del modelo `opusplan`

El alias de modelo `opusplan` proporciona un enfoque híbrido automatizado:

* **En modo de plan** - Utiliza `opus` para razonamiento complejo y decisiones de arquitectura
* **En modo de ejecución** - Cambia automáticamente a `sonnet` para generación de código e implementación

Esto le da lo mejor de ambos mundos: el razonamiento superior de Opus para la planificación y la eficiencia de Sonnet para la ejecución.

### Ajustar el nivel de esfuerzo

[Los niveles de esfuerzo](https://platform.claude.com/docs/es/build-with-claude/effort) controlan el razonamiento adaptativo, que asigna dinámicamente el pensamiento basado en la complejidad de la tarea. El esfuerzo menor es más rápido y económico para tareas directas, mientras que el esfuerzo mayor proporciona un razonamiento más profundo para problemas complejos.

Tres niveles persisten entre sesiones: **low**, **medium** y **high**. Un cuarto nivel, **max**, proporciona el razonamiento más profundo sin restricción en el gasto de tokens, por lo que las respuestas son más lentas y cuestan más que en `high`. `max` está disponible solo en Opus 4.6 y se aplica a la sesión actual sin persistir. Opus 4.6 tiene un esfuerzo medio predeterminado para suscriptores de Max y Team.

**Configurar esfuerzo:**

* **`/effort`**: ejecute `/effort low`, `/effort medium`, `/effort high` o `/effort max` para cambiar el nivel, o `/effort auto` para restablecer el valor predeterminado del modelo
* **En `/model`**: utilice las teclas de flecha izquierda/derecha para ajustar el control deslizante de esfuerzo al seleccionar un modelo
* **Bandera `--effort`**: pase `low`, `medium`, `high` o `max` para establecer el nivel para una única sesión al iniciar Claude Code
* **Variable de entorno**: establezca `CLAUDE_CODE_EFFORT_LEVEL` en `low`, `medium`, `high`, `max` o `auto`
* **Configuración**: establezca `effortLevel` en su archivo de configuración en `"low"`, `"medium"` o `"high"`

La variable de entorno tiene precedencia, luego su nivel configurado, luego el valor predeterminado del modelo.

El esfuerzo es compatible con Opus 4.6 y Sonnet 4.6. El control deslizante de esfuerzo aparece en `/model` cuando se selecciona un modelo compatible. El nivel de esfuerzo actual también se muestra junto al logotipo y al indicador, por ejemplo "with low effort", para que pueda confirmar qué configuración está activa sin abrir `/model`.

Para desactivar el razonamiento adaptativo en Opus 4.6 y Sonnet 4.6 y revertir al presupuesto de pensamiento fijo anterior, establezca `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Cuando está desactivado, estos modelos utilizan el presupuesto fijo controlado por `MAX_THINKING_TOKENS`. Consulte [variables de entorno](/es/env-vars).

### Contexto extendido

Opus 4.6 y Sonnet 4.6 admiten una [ventana de contexto de 1 millón de tokens](https://platform.claude.com/docs/es/build-with-claude/context-windows#1m-token-context-window) para sesiones largas con bases de código grandes.

La disponibilidad varía según el modelo y el plan. En los planes Max, Team y Enterprise, Opus se actualiza automáticamente a contexto de 1M sin configuración adicional. Esto se aplica tanto a los asientos de Team Standard como de Team Premium.

| Plan                   | Opus 4.6 con contexto de 1M                                                                                 | Sonnet 4.6 con contexto de 1M                                                                               |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Max, Team y Enterprise | Incluido en la suscripción                                                                                  | Requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                    | Requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) | Requiere [uso adicional](https://support.claude.com/es/articles/12429409-extra-usage-for-paid-claude-plans) |
| API y pago por uso     | Acceso completo                                                                                             | Acceso completo                                                                                             |

Para desactivar completamente el contexto de 1M, establezca `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Esto elimina variantes de modelo de 1M del selector de modelo. Consulte [variables de entorno](/es/env-vars).

La ventana de contexto de 1M utiliza precios de modelo estándar sin prima para tokens más allá de 200K. Para planes donde el contexto extendido está incluido en su suscripción, el uso permanece cubierto por su suscripción. Para planes que acceden al contexto extendido a través de uso adicional, los tokens se facturan al uso adicional.

Si su cuenta admite contexto de 1M, la opción aparece en el selector de modelo (`/model`) en las últimas versiones de Claude Code. Si no la ve, intente reiniciar su sesión.

También puede utilizar el sufijo `[1m]` con alias de modelo o nombres de modelo completos:

```bash  theme={null}
# Utilizar el alias opus[1m] o sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# O añadir [1m] a un nombre de modelo completo
/model claude-opus-4-6[1m]
```

## Verificar su modelo actual

Puede ver qué modelo está utilizando actualmente de varias formas:

1. En [línea de estado](/es/statusline) (si está configurada)
2. En `/status`, que también muestra la información de su cuenta.

## Variables de entorno

Puede utilizar las siguientes variables de entorno, que deben ser **nombres de modelo** completos (o equivalentes para su proveedor de API), para controlar los nombres de modelo a los que se asignan los alias.

| Variable de entorno              | Descripción                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | El modelo a utilizar para `opus`, o para `opusplan` cuando Plan Mode está activo.               |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | El modelo a utilizar para `sonnet`, o para `opusplan` cuando Plan Mode no está activo.          |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | El modelo a utilizar para `haiku`, o [funcionalidad de fondo](/es/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | El modelo a utilizar para [subagents](/es/sub-agents)                                           |

Nota: `ANTHROPIC_SMALL_FAST_MODEL` está deprecado en favor de `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Fijar modelos para implementaciones de terceros

Al implementar Claude Code a través de [Bedrock](/es/amazon-bedrock), [Vertex AI](/es/google-vertex-ai), o [Foundry](/es/microsoft-foundry), fije versiones de modelo antes de implementar para usuarios.

Sin fijar, Claude Code utiliza alias de modelo (`sonnet`, `opus`, `haiku`) que se resuelven a la versión más reciente. Cuando Anthropic lanza un nuevo modelo, los usuarios cuyas cuentas no tienen la nueva versión habilitada se romperán silenciosamente.

<Warning>
  Establezca las tres variables de entorno de modelo en IDs de versión específicos como parte de su configuración inicial. Omitir este paso significa que una actualización de Claude Code puede romper sus usuarios sin ninguna acción de su parte.
</Warning>

Utilice las siguientes variables de entorno con IDs de modelo específicos de versión para su proveedor:

| Proveedor | Ejemplo                                                                 |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Aplique el mismo patrón para `ANTHROPIC_DEFAULT_SONNET_MODEL` y `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Para IDs de modelo actuales y heredados en todos los proveedores, consulte [Descripción general de modelos](https://platform.claude.com/docs/es/about-claude/models/overview). Para actualizar usuarios a una nueva versión de modelo, actualice estas variables de entorno e implemente nuevamente.

Para habilitar [contexto extendido](#extended-context) para un modelo fijo, añada `[1m]` al ID de modelo en `ANTHROPIC_DEFAULT_OPUS_MODEL` o `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

El sufijo `[1m]` aplica la ventana de contexto de 1M a todo el uso de ese alias, incluido `opusplan`. Claude Code elimina el sufijo antes de enviar el ID de modelo a su proveedor. Solo añada `[1m]` cuando el modelo subyacente admita contexto de 1M, como Opus 4.6 o Sonnet 4.6.

<Note>
  La lista de permitidos `settings.availableModels` aún se aplica cuando se utilizan proveedores de terceros. El filtrado coincide con el alias de modelo (`opus`, `sonnet`, `haiku`), no con el ID de modelo específico del proveedor.
</Note>

### Anular IDs de modelo por versión

Las variables de entorno a nivel de familia anteriores configuran un ID de modelo por alias de familia. Si necesita asignar varias versiones dentro de la misma familia a IDs de proveedor distintos, utilice la configuración `modelOverrides` en su lugar.

`modelOverrides` asigna IDs de modelo individuales de Anthropic a las cadenas específicas del proveedor que Claude Code envía a la API de su proveedor. Cuando un usuario selecciona un modelo asignado en el selector `/model`, Claude Code utiliza su valor configurado en lugar del predeterminado integrado.

Esto permite a los administradores empresariales enrutar cada versión de modelo a un ARN de perfil de inferencia de Bedrock específico, nombre de versión de Vertex AI o nombre de implementación de Foundry para gobernanza, asignación de costos o enrutamiento regional.

Establezca `modelOverrides` en su [archivo de configuración](/es/settings#settings-files):

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
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
