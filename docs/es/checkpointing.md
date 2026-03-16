> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# checkpoint

> Realiza un seguimiento automático y revierte los cambios de Claude para recuperarse rápidamente de cambios no deseados.

Claude Code realiza un seguimiento automático de los cambios de archivos de Claude mientras trabaja, permitiéndole deshacer rápidamente cambios y revertir a estados anteriores si algo se sale del camino.

## Cómo funciona checkpoint

Mientras trabaja con Claude, checkpoint captura automáticamente el estado de su código antes de cada edición. Esta red de seguridad le permite realizar tareas ambiciosas y a gran escala sabiendo que siempre puede volver a un estado de código anterior.

### Seguimiento automático

Claude Code realiza un seguimiento de todos los cambios realizados por sus herramientas de edición de archivos:

* Cada mensaje del usuario crea un nuevo checkpoint
* Los checkpoints persisten entre sesiones, por lo que puede acceder a ellos en conversaciones reanudadas
* Se limpian automáticamente junto con las sesiones después de 30 días (configurable)

### Revertir cambios

Presione `Esc` dos veces (`Esc` + `Esc`) o use el comando `/rewind` para abrir el menú de rewind. Puede elegir restaurar:

* **Solo conversación**: Revertir a un mensaje del usuario manteniendo los cambios de código
* **Solo código**: Revertir cambios de archivo manteniendo la conversación
* **Tanto código como conversación**: Restaurar ambos a un punto anterior en la sesión

## Casos de uso comunes

Los checkpoints son particularmente útiles cuando:

* **Explorar alternativas**: Pruebe diferentes enfoques de implementación sin perder su punto de partida
* **Recuperarse de errores**: Deshaga rápidamente cambios que introdujeron errores o rompieron funcionalidad
* **Iterar en características**: Experimente con variaciones sabiendo que puede revertir a estados que funcionan

## Limitaciones

### Los cambios de comando Bash no se rastrean

checkpoint no rastrea archivos modificados por comandos bash. Por ejemplo, si Claude Code ejecuta:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Estas modificaciones de archivo no se pueden deshacer a través de rewind. Solo se rastrean las ediciones de archivo directo realizadas a través de las herramientas de edición de archivos de Claude.

### Los cambios externos no se rastrean

checkpoint solo rastrea archivos que han sido editados dentro de la sesión actual. Los cambios manuales que realiza en archivos fuera de Claude Code y las ediciones de otras sesiones concurrentes normalmente no se capturan, a menos que modifiquen los mismos archivos que la sesión actual.

### No es un reemplazo para control de versiones

Los checkpoints están diseñados para recuperación rápida a nivel de sesión. Para historial de versiones permanente y colaboración:

* Continúe usando control de versiones (ej. Git) para commits, ramas e historial a largo plazo
* Los checkpoints complementan pero no reemplazan el control de versiones adecuado
* Piense en los checkpoints como "deshacer local" y Git como "historial permanente"

## Ver también

* [Modo interactivo](/es/interactive-mode) - Atajos de teclado y controles de sesión
* [Comandos integrados](/es/interactive-mode#built-in-commands) - Acceso a checkpoints usando `/rewind`
* [Referencia CLI](/es/cli-reference) - Opciones de línea de comandos
