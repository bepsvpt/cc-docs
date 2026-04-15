> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Realiza un seguimiento, revierte y resume las ediciones y conversaciones de Claude para gestionar el estado de la sesión.

Claude Code realiza un seguimiento automático de las ediciones de archivos de Claude mientras trabaja, permitiéndole deshacer rápidamente cambios y revertir a estados anteriores si algo se sale de control.

## Cómo funciona el checkpointing

Mientras trabaja con Claude, el checkpointing captura automáticamente el estado de su código antes de cada edición. Esta red de seguridad le permite realizar tareas ambiciosas y a gran escala sabiendo que siempre puede volver a un estado de código anterior.

### Seguimiento automático

Claude Code realiza un seguimiento de todos los cambios realizados por sus herramientas de edición de archivos:

* Cada solicitud del usuario crea un nuevo checkpoint
* Los checkpoints persisten entre sesiones, por lo que puede acceder a ellos en conversaciones reanudadas
* Se limpian automáticamente junto con las sesiones después de 30 días (configurable)

### Revertir y resumir

Presione `Esc` dos veces (`Esc` + `Esc`) o use el comando `/rewind` para abrir el menú de rewind. Una lista desplazable muestra cada una de sus solicitudes de la sesión. Seleccione el punto en el que desea actuar y luego elija una acción:

* **Restaurar código y conversación**: revierte tanto el código como la conversación a ese punto
* **Restaurar conversación**: revierte a ese mensaje mientras mantiene el código actual
* **Restaurar código**: revierte los cambios de archivo mientras mantiene la conversación
* **Resumir desde aquí**: comprime la conversación desde este punto en adelante en un resumen, liberando espacio de context window
* **Cancelar**: regresa a la lista de mensajes sin hacer cambios

Después de restaurar la conversación o resumir, la solicitud original del mensaje seleccionado se restaura en el campo de entrada para que pueda reenviarlo o editarlo.

#### Restaurar vs. resumir

Las tres opciones de restauración revierten el estado: deshacen cambios de código, historial de conversación, o ambos. "Resumir desde aquí" funciona de manera diferente:

* Los mensajes anteriores al mensaje seleccionado permanecen intactos
* El mensaje seleccionado y todos los mensajes posteriores se reemplazan con un resumen compacto generado por IA
* No se cambian archivos en el disco
* Los mensajes originales se conservan en la transcripción de la sesión, por lo que Claude puede hacer referencia a los detalles si es necesario

Esto es similar a `/compact`, pero dirigido: en lugar de resumir toda la conversación, mantiene el contexto inicial en detalle completo y solo comprime las partes que están usando espacio. Puede escribir instrucciones opcionales para guiar en qué se enfoca el resumen.

<Note>
  Resumir lo mantiene en la misma sesión y comprime el contexto. Si desea ramificarse e intentar un enfoque diferente mientras preserva la sesión original intacta, use [fork](/es/how-claude-code-works#resume-or-fork-sessions) en su lugar (`claude --continue --fork-session`).
</Note>

## Casos de uso comunes

Los checkpoints son particularmente útiles cuando:

* **Explorar alternativas**: pruebe diferentes enfoques de implementación sin perder su punto de partida
* **Recuperarse de errores**: deshaga rápidamente cambios que introdujeron errores o rompieron la funcionalidad
* **Iterar en características**: experimente con variaciones sabiendo que puede revertir a estados que funcionan
* **Liberar espacio de contexto**: resuma una sesión de depuración detallada desde el punto medio en adelante, manteniendo sus instrucciones iniciales intactas

## Limitaciones

### Los cambios de comandos Bash no se rastrean

El checkpointing no rastrea archivos modificados por comandos bash. Por ejemplo, si Claude Code ejecuta:

```bash theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Estas modificaciones de archivo no se pueden deshacer a través de rewind. Solo se rastrean las ediciones de archivo directo realizadas a través de las herramientas de edición de archivos de Claude.

### Los cambios externos no se rastrean

El checkpointing solo rastrea archivos que han sido editados dentro de la sesión actual. Los cambios manuales que realiza en archivos fuera de Claude Code y las ediciones de otras sesiones concurrentes normalmente no se capturan, a menos que modifiquen los mismos archivos que la sesión actual.

### No es un reemplazo para el control de versiones

Los checkpoints están diseñados para recuperación rápida a nivel de sesión. Para historial de versiones permanente y colaboración:

* Continúe usando control de versiones (por ejemplo, Git) para commits, ramas e historial a largo plazo
* Los checkpoints complementan pero no reemplazan el control de versiones adecuado
* Piense en los checkpoints como "deshacer local" y Git como "historial permanente"

## Ver también

* [Modo interactivo](/es/interactive-mode) - Atajos de teclado y controles de sesión
* [Comandos integrados](/es/commands) - Acceso a checkpoints usando `/rewind`
* [Referencia de CLI](/es/cli-reference) - Opciones de línea de comandos
