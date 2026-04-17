> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ejecutar prompts en un horario

> Utilice /loop y las herramientas de programación cron para ejecutar prompts repetidamente, sondear el estado o establecer recordatorios únicos dentro de una sesión de Claude Code.

<Note>
  Las tareas programadas requieren Claude Code v2.1.72 o posterior. Verifique su versión con `claude --version`.
</Note>

Las tareas programadas permiten que Claude vuelva a ejecutar un prompt automáticamente en un intervalo. Úselas para sondear una implementación, supervisar un PR, verificar una compilación de larga duración o recordarse a sí mismo que debe hacer algo más adelante en la sesión. Para reaccionar a eventos a medida que ocurren en lugar de sondear, consulte [Channels](/es/channels): su CI puede insertar el error directamente en la sesión.

Las tareas tienen alcance de sesión: viven en el proceso actual de Claude Code y desaparecen cuando sale. Para la programación duradera que sobrevive a los reinicios, utilice [Routines](/es/routines), [tareas programadas de Desktop](/es/desktop-scheduled-tasks) o [GitHub Actions](/es/github-actions).

## Comparar opciones de programación

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Ejecutar un prompt repetidamente con /loop

El `/loop` [bundled skill](/es/commands) es la forma más rápida de ejecutar un prompt repetidamente mientras la sesión permanece abierta. Tanto el intervalo como el prompt son opcionales, y lo que proporcione determina cómo se comporta el bucle.

| Lo que proporciona     | Ejemplo                     | Qué sucede                                                                                                            |
| :--------------------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| Intervalo y prompt     | `/loop 5m check the deploy` | Su prompt se ejecuta en un [horario fijo](#run-on-a-fixed-interval)                                                   |
| Solo prompt            | `/loop check the deploy`    | Su prompt se ejecuta en un [intervalo que Claude elige](#let-claude-choose-the-interval) en cada iteración            |
| Solo intervalo, o nada | `/loop`                     | El [prompt de mantenimiento integrado](#run-the-built-in-maintenance-prompt) se ejecuta, o su `loop.md` si existe uno |

También puede pasar otro comando como el prompt, por ejemplo `/loop 20m /review-pr 1234`, para volver a ejecutar un flujo de trabajo empaquetado en cada iteración.

### Ejecutar en un intervalo fijo

Cuando proporciona un intervalo, Claude lo convierte en una expresión cron, programa el trabajo y confirma la cadencia y el ID del trabajo.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

El intervalo puede encabezar el prompt como un token simple como `30m`, o seguirlo como una cláusula como `every 2 hours`. Las unidades admitidas son `s` para segundos, `m` para minutos, `h` para horas y `d` para días.

Los segundos se redondean al minuto más cercano ya que cron tiene una granularidad de un minuto. Los intervalos que no se asignan a un paso cron limpio, como `7m` o `90m`, se redondean al intervalo más cercano que sí lo hace y Claude le dice cuál eligió.

### Dejar que Claude elija el intervalo

Cuando omite el intervalo, Claude elige uno dinámicamente en lugar de ejecutarse en un horario cron fijo. Después de cada iteración, elige un retraso entre un minuto y una hora según lo que observó: esperas cortas mientras una compilación se está terminando o un PR está activo, esperas más largas cuando no hay nada pendiente. El retraso elegido y la razón del mismo se imprimen al final de cada iteración.

El ejemplo a continuación verifica CI y comentarios de revisión, con Claude esperando más tiempo entre iteraciones una vez que el PR se queda en silencio:

```text theme={null}
/loop check whether CI passed and address any review comments
```

Cuando solicita un horario `/loop` dinámico, Claude puede usar la [herramienta Monitor](/es/tools-reference#monitor-tool) directamente. Monitor ejecuta un script de fondo y transmite cada línea de salida, lo que evita el sondeo por completo y a menudo es más eficiente en tokens y más receptivo que volver a ejecutar un prompt en un intervalo.

Un bucle programado dinámicamente aparece en su [lista de tareas programadas](#manage-scheduled-tasks) como cualquier otra tarea, por lo que puede enumerarla o cancelarla de la misma manera. Las [reglas de jitter](#jitter) no se aplican a ella, pero el [vencimiento de siete días](#seven-day-expiry) sí: el bucle termina automáticamente siete días después de iniciarlo.

<Note>
  En Bedrock, Vertex AI y Microsoft Foundry, un prompt sin intervalo se ejecuta en un horario fijo de 10 minutos en su lugar.
</Note>

### Ejecutar el prompt de mantenimiento integrado

Cuando omite el prompt, Claude usa un prompt de mantenimiento integrado en lugar de uno que proporcione. En cada iteración, trabaja a través de lo siguiente, en orden:

* continuar cualquier trabajo inacabado de la conversación
* cuidar el pull request de la rama actual: comentarios de revisión, ejecuciones de CI fallidas, conflictos de fusión
* ejecutar pasadas de limpieza como búsquedas de errores o simplificación cuando no hay nada más pendiente

Claude no inicia nuevas iniciativas fuera de ese alcance, y las acciones irreversibles como insertar o eliminar solo proceden cuando continúan algo que la transcripción ya autorizó.

```text theme={null}
/loop
```

Un `/loop` simple ejecuta este prompt en un [intervalo elegido dinámicamente](#let-claude-choose-the-interval). Agregue un intervalo, por ejemplo `/loop 15m`, para ejecutarlo en un horario fijo en su lugar. Para reemplazar el prompt integrado con el suyo propio, consulte [Personalizar el prompt predeterminado con loop.md](#customize-the-default-prompt-with-loop-md).

<Note>
  En Bedrock, Vertex AI y Microsoft Foundry, `/loop` sin prompt imprime el mensaje de uso en lugar de iniciar el bucle de mantenimiento.
</Note>

### Personalizar el prompt predeterminado con loop.md

Un archivo `loop.md` reemplaza el prompt de mantenimiento integrado con sus propias instrucciones. Define un único prompt predeterminado para `/loop` simple, no una lista de tareas programadas separadas, e se ignora siempre que proporcione un prompt en la línea de comandos. Para programar prompts adicionales junto a él, use `/loop <prompt>` o [pida a Claude directamente](#manage-scheduled-tasks).

Claude busca el archivo en dos ubicaciones y usa el primero que encuentra.

| Ruta                | Alcance                                                                         |
| :------------------ | :------------------------------------------------------------------------------ |
| `.claude/loop.md`   | Nivel de proyecto. Tiene precedencia cuando ambos archivos existen.             |
| `~/.claude/loop.md` | Nivel de usuario. Se aplica en cualquier proyecto que no defina el suyo propio. |

El archivo es Markdown simple sin estructura requerida. Escríbalo como si estuviera escribiendo el prompt `/loop` directamente. El siguiente ejemplo mantiene una rama de lanzamiento saludable:

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

Las ediciones a `loop.md` tienen efecto en la siguiente iteración, por lo que puede refinar las instrucciones mientras un bucle se está ejecutando. Cuando no existe `loop.md` en ninguna ubicación, el bucle vuelve al prompt de mantenimiento integrado. Mantenga el archivo conciso: el contenido más allá de 25,000 bytes se trunca.

## Establecer un recordatorio único

Para recordatorios únicos, describa lo que desea en lenguaje natural en lugar de usar `/loop`. Claude programa una tarea de un solo disparo que se elimina a sí misma después de ejecutarse.

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude fija la hora de disparo a un minuto y hora específicos usando una expresión cron y confirma cuándo se ejecutará.

## Gestionar tareas programadas

Pida a Claude en lenguaje natural que enumere o cancele tareas, o haga referencia directamente a las herramientas subyacentes.

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

Bajo el capó, Claude utiliza estas herramientas:

| Herramienta  | Propósito                                                                                                                        |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `CronCreate` | Programar una nueva tarea. Acepta una expresión cron de 5 campos, el prompt a ejecutar y si se repite o se ejecuta una sola vez. |
| `CronList`   | Enumerar todas las tareas programadas con sus IDs, horarios y prompts.                                                           |
| `CronDelete` | Cancelar una tarea por ID.                                                                                                       |

Cada tarea programada tiene un ID de 8 caracteres que puede pasar a `CronDelete`. Una sesión puede contener hasta 50 tareas programadas a la vez.

## Cómo se ejecutan las tareas programadas

El programador verifica cada segundo si hay tareas vencidas y las encola con baja prioridad. Un prompt programado se ejecuta entre sus turnos, no mientras Claude está en medio de una respuesta. Si Claude está ocupado cuando vence una tarea, el prompt espera hasta que termine el turno actual.

Todos los tiempos se interpretan en su zona horaria local. Una expresión cron como `0 9 * * *` significa las 9am donde está ejecutando Claude Code, no UTC.

### Jitter

Para evitar que cada sesión golpee la API en el mismo momento de reloj de pared, el programador agrega un pequeño desplazamiento determinista a los tiempos de disparo:

* Las tareas recurrentes se ejecutan hasta un 10% de su período tarde, limitado a 15 minutos. Un trabajo por hora podría ejecutarse en cualquier momento desde `:00` hasta `:06`.
* Las tareas únicas programadas para la parte superior o inferior de la hora se ejecutan hasta 90 segundos antes.

El desplazamiento se deriva del ID de la tarea, por lo que la misma tarea siempre obtiene el mismo desplazamiento. Si el tiempo exacto es importante, elija un minuto que no sea `:00` o `:30`, por ejemplo `3 9 * * *` en lugar de `0 9 * * *`, y el jitter único no se aplicará.

### Vencimiento de siete días

Las tareas recurrentes expiran automáticamente 7 días después de su creación. La tarea se ejecuta una última vez y luego se elimina a sí misma. Esto limita cuánto tiempo puede ejecutarse un bucle olvidado. Si necesita que una tarea recurrente dure más, cancele y recree antes de que expire, o utilice [Routines](/es/routines) o [tareas programadas de Desktop](/es/desktop-scheduled-tasks) para programación duradera.

## Referencia de expresión cron

`CronCreate` acepta expresiones cron estándar de 5 campos: `minute hour day-of-month month day-of-week`. Todos los campos admiten comodines (`*`), valores únicos (`5`), pasos (`*/15`), rangos (`1-5`) y listas separadas por comas (`1,15,30`).

| Ejemplo        | Significado                    |
| :------------- | :----------------------------- |
| `*/5 * * * *`  | Cada 5 minutos                 |
| `0 * * * *`    | Cada hora en punto             |
| `7 * * * *`    | Cada hora a los 7 minutos      |
| `0 9 * * *`    | Todos los días a las 9am local |
| `0 9 * * 1-5`  | Días de semana a las 9am local |
| `30 14 15 3 *` | 15 de marzo a las 2:30pm local |

El día de la semana usa `0` o `7` para domingo hasta `6` para sábado. La sintaxis extendida como `L`, `W`, `?` y alias de nombres como `MON` o `JAN` no se admiten.

Cuando tanto el día del mes como el día de la semana están restringidos, una fecha coincide si cualquiera de los campos coincide. Esto sigue la semántica estándar de vixie-cron.

## Deshabilitar tareas programadas

Establezca `CLAUDE_CODE_DISABLE_CRON=1` en su entorno para deshabilitar completamente el programador. Las herramientas cron y `/loop` dejan de estar disponibles, y cualquier tarea ya programada deja de ejecutarse. Consulte [Variables de entorno](/es/env-vars) para la lista completa de banderas de deshabilitación.

## Limitaciones

La programación con alcance de sesión tiene limitaciones inherentes:

* Las tareas solo se ejecutan mientras Claude Code está ejecutándose e inactivo. Cerrar la terminal o dejar que la sesión salga cancela todo.
* Sin recuperación de disparos perdidos. Si el tiempo programado de una tarea pasa mientras Claude está ocupado en una solicitud de larga duración, se ejecuta una vez cuando Claude queda inactivo, no una vez por intervalo perdido.
* Sin persistencia entre reinicios. Reiniciar Claude Code borra todas las tareas con alcance de sesión.

Para la automatización impulsada por cron que necesita ejecutarse sin supervisión:

* [Routines](/es/routines): se ejecutan en infraestructura administrada por Anthropic en un horario, mediante llamada a API o en eventos de GitHub
* [GitHub Actions](/es/github-actions): utilice un disparador `schedule` en CI
* [tareas programadas de Desktop](/es/desktop-scheduled-tasks): se ejecutan localmente en su máquina
