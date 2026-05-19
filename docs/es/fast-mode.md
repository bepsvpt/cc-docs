> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Acelera las respuestas con el modo rápido

> Obtén respuestas más rápidas de Opus en Claude Code al activar el modo rápido.

<Note>
  El modo rápido está en [vista previa de investigación](#research-preview). La función, los precios y la disponibilidad pueden cambiar según los comentarios.
</Note>

El modo rápido es una configuración de alta velocidad para Claude Opus, haciendo que el modelo sea 2.5x más rápido a un costo más alto por token. Actívalo con `/fast` cuando necesites velocidad para trabajo interactivo como iteración rápida o depuración en vivo, y desactívalo cuando el costo sea más importante que la latencia.

El modo rápido no es un modelo diferente. Utiliza Claude Opus con una configuración de API diferente que prioriza la velocidad sobre la eficiencia de costos. Obtienes la misma calidad y capacidades con respuestas más rápidas. El modo rápido es compatible con Opus 4.7 y Opus 4.6. No está disponible en Sonnet, Haiku u otros modelos.

<Note>
  El modo rápido requiere Claude Code v2.1.36 o posterior. Verifica tu versión con `claude --version`.
</Note>

Lo que debes saber:

* Usa `/fast` para activar o desactivar el modo rápido en Claude Code CLI. También disponible a través de `/fast` en la Extensión Claude Code VS Code.
* Los precios del modo rápido son $30/$150 MTok tanto en Opus 4.7 como en Opus 4.6.
* Disponible para todos los usuarios de Claude Code en planes de suscripción (Pro/Max/Team/Enterprise) y Claude Console.
* Para los usuarios de Claude Code en planes de suscripción (Pro/Max/Team/Enterprise), el modo rápido está disponible solo a través de créditos de uso y no está incluido en los límites de velocidad de la suscripción.

Esta página cubre cómo [activar el modo rápido](#toggle-fast-mode), su [compensación de costos](#understand-the-cost-tradeoff), [cuándo usarlo](#decide-when-to-use-fast-mode), [requisitos](#requirements), [opción de participación por sesión](#require-per-session-opt-in), y [comportamiento de límite de velocidad](#handle-rate-limits).

## Activar el modo rápido

Activa el modo rápido de cualquiera de estas formas:

* Escribe `/fast` y presiona Tab para activar o desactivar
* Establece `"fastMode": true` en tu [archivo de configuración de usuario](/es/settings)

De forma predeterminada, el modo rápido persiste entre sesiones. Los administradores pueden configurar el modo rápido para que se reinicie cada sesión. Consulta [opción de participación por sesión](#require-per-session-opt-in) para obtener más detalles.

Para la mejor eficiencia de costos, habilita el modo rápido al inicio de una sesión en lugar de cambiar a mitad de la conversación. Consulta [comprender la compensación de costos](#understand-the-cost-tradeoff) para obtener más detalles.

Cuando habilitas el modo rápido:

* Si estás en un modelo diferente, Claude Code cambia automáticamente a Opus
* Verás un mensaje de confirmación: "Fast mode ON"
* Un pequeño icono `↯` aparece junto al prompt mientras el modo rápido está activo
* Ejecuta `/fast` nuevamente en cualquier momento para verificar si el modo rápido está activado o desactivado

Cuando desactivas el modo rápido con `/fast` nuevamente, permaneces en Opus. El modelo no revierte a tu modelo anterior. Para cambiar a un modelo diferente, usa `/model`.

Opus 4.7 es el valor predeterminado del modo rápido en Claude Code v2.1.142 y posterior. Para fijar el modo rápido a Opus 4.6 en su lugar, establece `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`.

## Comprender la compensación de costos

El modo rápido tiene precios por token más altos que el Opus estándar:

| Modo        | Entrada (MTok) | Salida (MTok) |
| ----------- | -------------- | ------------- |
| Modo rápido | \$30           | \$150         |

Los precios del modo rápido son fijos en toda la ventana de contexto de 1M tokens.

Cuando cambias al modo rápido a mitad de la conversación, pagas el precio completo del token de entrada sin caché del modo rápido para todo el contexto de la conversación. Esto cuesta más que si hubieras habilitado el modo rápido desde el inicio.

## Decidir cuándo usar el modo rápido

El modo rápido es mejor para trabajo interactivo donde la latencia de respuesta es más importante que el costo:

* Iteración rápida en cambios de código
* Sesiones de depuración en vivo
* Trabajo sensible al tiempo con plazos ajustados

El modo estándar es mejor para:

* Tareas autónomas largas donde la velocidad importa menos
* Procesamiento por lotes o canalizaciones CI/CD
* Cargas de trabajo sensibles al costo

### Modo rápido versus nivel de esfuerzo

El modo rápido y el nivel de esfuerzo afectan la velocidad de respuesta, pero de manera diferente:

| Configuración                  | Efecto                                                                                                   |
| ------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **Modo rápido**                | Misma calidad de modelo, latencia más baja, costo más alto                                               |
| **Nivel de esfuerzo más bajo** | Menos tiempo de pensamiento, respuestas más rápidas, calidad potencialmente más baja en tareas complejas |

Puedes combinar ambos: usa el modo rápido con un [nivel de esfuerzo](/es/model-config#adjust-effort-level) más bajo para máxima velocidad en tareas sencillas.

## Requisitos

El modo rápido requiere todos los siguientes:

* **No disponible en proveedores de nube de terceros**: el modo rápido no está disponible en Amazon Bedrock, Google Vertex AI o Microsoft Azure Foundry. El modo rápido está disponible a través de la API de Anthropic Console y para planes de suscripción de Claude usando créditos de uso.
* **Créditos de uso activados**: tu cuenta debe tener los créditos de uso activados, lo que permite facturación más allá del uso incluido en tu plan. Para cuentas individuales, activa esto en tu [configuración de facturación de Console](https://platform.claude.com/settings/organization/billing). Para Teams y Enterprise, un administrador debe activar los créditos de uso para la organización.

<Note>
  El uso del modo rápido se extrae directamente de los créditos de uso, incluso si tienes uso restante en tu plan. Esto significa que los tokens del modo rápido no cuentan contra el uso incluido en tu plan y se cobran a la tarifa del modo rápido desde el primer token.
</Note>

* **Habilitación del administrador para Teams y Enterprise**: el modo rápido está deshabilitado de forma predeterminada para organizaciones Teams y Enterprise. Un administrador debe [habilitar explícitamente el modo rápido](#enable-fast-mode-for-your-organization) antes de que los usuarios puedan acceder a él.

<Note>
  Si tu administrador no ha habilitado el modo rápido para tu organización, el comando `/fast` mostrará "Fast mode has been disabled by your organization."
</Note>

### Habilitar el modo rápido para tu organización

Los administradores pueden habilitar el modo rápido en:

* **Console** (clientes de API): [Preferencias de Claude Code](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Teams y Enterprise): [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

Otra opción para desactivar completamente el modo rápido es establecer `CLAUDE_CODE_DISABLE_FAST_MODE=1`. Consulta [Variables de entorno](/es/env-vars).

### Opción de participación por sesión

De forma predeterminada, el modo rápido persiste entre sesiones: si un usuario habilita el modo rápido, permanece activado en futuras sesiones. Los administradores en planes [Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) o [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) pueden evitar esto estableciendo `fastModePerSessionOptIn` en `true` en [configuración administrada](/es/settings#settings-files) o [configuración administrada por servidor](/es/server-managed-settings). Esto hace que cada sesión comience con el modo rápido desactivado, requiriendo que los usuarios lo habiliten explícitamente con `/fast`.

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

Esto es útil para controlar costos en organizaciones donde los usuarios ejecutan múltiples sesiones concurrentes. Los usuarios aún pueden habilitar el modo rápido con `/fast` cuando necesiten velocidad, pero se reinicia al inicio de cada nueva sesión. La preferencia del modo rápido del usuario aún se guarda, por lo que eliminar esta configuración restaura el comportamiento persistente predeterminado.

## Manejar límites de velocidad

El modo rápido tiene límites de velocidad separados del Opus estándar. El modo rápido para Opus 4.7 y Opus 4.6 comparten el mismo grupo de límite de velocidad: el uso en cualquiera de los modelos se extrae de los mismos límites. Cuando alcanzas el límite de velocidad del modo rápido o se agotan tus créditos de uso:

1. El modo rápido automáticamente vuelve a velocidad estándar
2. El icono `↯` se vuelve gris para indicar enfriamiento
3. Continúas trabajando a velocidad y precios estándar
4. Cuando expira el enfriamiento, el modo rápido se vuelve a habilitar automáticamente

Para desactivar el modo rápido manualmente en lugar de esperar el enfriamiento, ejecuta `/fast` nuevamente.

## Vista previa de investigación

El modo rápido es una función de vista previa de investigación. Esto significa:

* La función puede cambiar según los comentarios
* La disponibilidad y los precios están sujetos a cambios
* La configuración de API subyacente puede evolucionar

Reporta problemas o comentarios a través de tus canales de soporte habituales de Anthropic.

## Ver también

* [Configuración de modelo](/es/model-config): cambiar modelos y ajustar niveles de esfuerzo
* [Gestionar costos de manera efectiva](/es/costs): rastrear el uso de tokens y reducir costos
* [Configuración de línea de estado](/es/statusline): mostrar información de modelo y contexto
