> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Personalizar atajos de teclado

> Personaliza atajos de teclado en Claude Code con un archivo de configuración de keybindings.

<Note>
  Los atajos de teclado personalizables requieren Claude Code v2.1.18 o posterior. Verifique su versión con `claude --version`.
</Note>

Claude Code admite atajos de teclado personalizables. Ejecute `/keybindings` para crear o abrir su archivo de configuración en `~/.claude/keybindings.json`.

## Archivo de configuración

El archivo de configuración de keybindings es un objeto con un array `bindings`. Cada bloque especifica un contexto y un mapa de pulsaciones de teclas a acciones.

<Note>Los cambios en el archivo de keybindings se detectan y aplican automáticamente sin reiniciar Claude Code.</Note>

| Campo      | Descripción                                                 |
| :--------- | :---------------------------------------------------------- |
| `$schema`  | URL de esquema JSON opcional para autocompletado del editor |
| `$docs`    | URL de documentación opcional                               |
| `bindings` | Array de bloques de vinculación por contexto                |

Este ejemplo vincula `Ctrl+E` para abrir un editor externo en el contexto de chat, y desvincula `Ctrl+U`:

```json theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/es/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## Contextos

Cada bloque de vinculación especifica un **contexto** donde se aplican los atajos:

| Contexto          | Descripción                                                                   |
| :---------------- | :---------------------------------------------------------------------------- |
| `Global`          | Se aplica en todas partes de la aplicación                                    |
| `Chat`            | Área principal de entrada de chat                                             |
| `Autocomplete`    | Menú de autocompletado está abierto                                           |
| `Settings`        | Menú de configuración                                                         |
| `Confirmation`    | Diálogos de permiso y confirmación                                            |
| `Tabs`            | Componentes de navegación de pestañas                                         |
| `Help`            | Menú de ayuda es visible                                                      |
| `Transcript`      | Visor de transcripción                                                        |
| `HistorySearch`   | Modo de búsqueda de historial (Ctrl+R)                                        |
| `Task`            | Tarea de fondo está en ejecución                                              |
| `ThemePicker`     | Diálogo de selector de tema                                                   |
| `Attachments`     | Navegación de adjunto de imagen en diálogos de selección                      |
| `Footer`          | Navegación de indicador de pie de página (tareas, equipos, diff)              |
| `MessageSelector` | Selección de mensaje de diálogo de rebobinado y resumen                       |
| `DiffDialog`      | Navegación del visor de diff                                                  |
| `ModelPicker`     | Nivel de esfuerzo del selector de modelo                                      |
| `Select`          | Componentes genéricos de selección/lista                                      |
| `Plugin`          | Diálogo de plugin (examinar, descubrir, administrar)                          |
| `Scroll`          | Desplazamiento de conversación y selección de texto en modo pantalla completa |
| `Doctor`          | Pantalla de diagnósticos `/doctor`                                            |

## Acciones disponibles

Las acciones siguen un formato `namespace:action`, como `chat:submit` para enviar un mensaje o `app:toggleTodos` para mostrar la lista de tareas. Cada contexto tiene acciones específicas disponibles.

### Acciones de aplicación

Acciones disponibles en el contexto `Global`:

| Acción                 | Predeterminado | Descripción                             |
| :--------------------- | :------------- | :-------------------------------------- |
| `app:interrupt`        | Ctrl+C         | Cancelar operación actual               |
| `app:exit`             | Ctrl+D         | Salir de Claude Code                    |
| `app:redraw`           | (sin vincular) | Forzar redibujo de terminal             |
| `app:toggleTodos`      | Ctrl+T         | Alternar visibilidad de lista de tareas |
| `app:toggleTranscript` | Ctrl+O         | Alternar transcripción detallada        |

### Acciones de historial

Acciones para navegar por el historial de comandos:

| Acción             | Predeterminado | Descripción                     |
| :----------------- | :------------- | :------------------------------ |
| `history:search`   | Ctrl+R         | Abrir búsqueda de historial     |
| `history:previous` | Arriba         | Elemento de historial anterior  |
| `history:next`     | Abajo          | Siguiente elemento de historial |

### Acciones de chat

Acciones disponibles en el contexto `Chat`:

| Acción                | Predeterminado            | Descripción                                                                                                                                                                                                     |
| :-------------------- | :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chat:cancel`         | Escape                    | Cancelar entrada actual                                                                                                                                                                                         |
| `chat:clearInput`     | Ctrl+L                    | Forzar un redibujo de pantalla completa, preservando la entrada. En [renderizado de pantalla completa](/es/fullscreen#clear-the-conversation), presione dos veces dentro de dos segundos para ejecutar `/clear` |
| `chat:clearScreen`    | Cmd+K                     | En [renderizado de pantalla completa](/es/fullscreen#clear-the-conversation), presione dos veces dentro de dos segundos para ejecutar `/clear`                                                                  |
| `chat:killAgents`     | Ctrl+X Ctrl+K             | Matar todos los agentes de fondo                                                                                                                                                                                |
| `chat:cycleMode`      | Shift+Tab\*               | Ciclar modos de permiso                                                                                                                                                                                         |
| `chat:modelPicker`    | Meta+P                    | Abrir selector de modelo                                                                                                                                                                                        |
| `chat:fastMode`       | Meta+O                    | Alternar modo rápido                                                                                                                                                                                            |
| `chat:thinkingToggle` | Meta+T                    | Alternar pensamiento extendido                                                                                                                                                                                  |
| `chat:submit`         | Enter                     | Enviar mensaje                                                                                                                                                                                                  |
| `chat:newline`        | Ctrl+J                    | Insertar una nueva línea sin enviar                                                                                                                                                                             |
| `chat:undo`           | Ctrl+\_, Ctrl+Shift+-     | Deshacer última acción                                                                                                                                                                                          |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E     | Abrir en editor externo                                                                                                                                                                                         |
| `chat:stash`          | Ctrl+S                    | Guardar indicación actual                                                                                                                                                                                       |
| `chat:imagePaste`     | Ctrl+V (Alt+V en Windows) | Pegar imagen                                                                                                                                                                                                    |

\*En Windows sin modo VT (Node \<24.2.0/\<22.17.0, Bun \<1.2.23), el valor predeterminado es Meta+M.

### Acciones de autocompletado

Acciones disponibles en el contexto `Autocomplete`:

| Acción                  | Predeterminado | Descripción          |
| :---------------------- | :------------- | :------------------- |
| `autocomplete:accept`   | Tab            | Aceptar sugerencia   |
| `autocomplete:dismiss`  | Escape         | Descartar menú       |
| `autocomplete:previous` | Arriba         | Sugerencia anterior  |
| `autocomplete:next`     | Abajo          | Siguiente sugerencia |

### Acciones de confirmación

Acciones disponibles en el contexto `Confirmation`:

| Acción                      | Predeterminado | Descripción                     |
| :-------------------------- | :------------- | :------------------------------ |
| `confirm:yes`               | Y, Enter       | Confirmar acción                |
| `confirm:no`                | N, Escape      | Rechazar acción                 |
| `confirm:previous`          | Arriba         | Opción anterior                 |
| `confirm:next`              | Abajo          | Siguiente opción                |
| `confirm:nextField`         | Tab            | Siguiente campo                 |
| `confirm:previousField`     | (sin vincular) | Campo anterior                  |
| `confirm:toggle`            | Espacio        | Alternar selección              |
| `confirm:cycleMode`         | Shift+Tab      | Ciclar modos de permiso         |
| `confirm:toggleExplanation` | Ctrl+E         | Alternar explicación de permiso |

### Acciones de permiso

Acciones disponibles en el contexto `Confirmation` para diálogos de permiso:

| Acción                   | Predeterminado | Descripción                                   |
| :----------------------- | :------------- | :-------------------------------------------- |
| `permission:toggleDebug` | Ctrl+D         | Alternar información de depuración de permiso |

### Acciones de transcripción

Acciones disponibles en el contexto `Transcript`:

| Acción                     | Predeterminado    | Descripción                        |
| :------------------------- | :---------------- | :--------------------------------- |
| `transcript:toggleShowAll` | Ctrl+E            | Alternar mostrar todo el contenido |
| `transcript:exit`          | q, Ctrl+C, Escape | Salir de vista de transcripción    |

### Acciones de búsqueda de historial

Acciones disponibles en el contexto `HistorySearch`:

| Acción                     | Predeterminado | Descripción                                       |
| :------------------------- | :------------- | :------------------------------------------------ |
| `historySearch:next`       | Ctrl+R         | Siguiente coincidencia                            |
| `historySearch:accept`     | Escape, Tab    | Aceptar selección                                 |
| `historySearch:cancel`     | Ctrl+C         | Cancelar búsqueda                                 |
| `historySearch:execute`    | Enter          | Ejecutar comando seleccionado                     |
| `historySearch:cycleScope` | Ctrl+S         | Ciclar alcance: sesión, proyecto, en todas partes |

### Acciones de tarea

Acciones disponibles en el contexto `Task`:

| Acción            | Predeterminado | Descripción           |
| :---------------- | :------------- | :-------------------- |
| `task:background` | Ctrl+B         | Tarea de fondo actual |

### Acciones de tema

Acciones disponibles en el contexto `ThemePicker`:

| Acción                           | Predeterminado | Descripción                    |
| :------------------------------- | :------------- | :----------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T         | Alternar resaltado de sintaxis |

### Acciones de ayuda

Acciones disponibles en el contexto `Help`:

| Acción         | Predeterminado | Descripción          |
| :------------- | :------------- | :------------------- |
| `help:dismiss` | Escape         | Cerrar menú de ayuda |

### Acciones de pestañas

Acciones disponibles en el contexto `Tabs`:

| Acción          | Predeterminado       | Descripción       |
| :-------------- | :------------------- | :---------------- |
| `tabs:next`     | Tab, Derecha         | Siguiente pestaña |
| `tabs:previous` | Shift+Tab, Izquierda | Pestaña anterior  |

### Acciones de adjuntos

Acciones disponibles en el contexto `Attachments`:

| Acción                 | Predeterminado      | Descripción                     |
| :--------------------- | :------------------ | :------------------------------ |
| `attachments:next`     | Derecha             | Siguiente adjunto               |
| `attachments:previous` | Izquierda           | Adjunto anterior                |
| `attachments:remove`   | Retroceso, Suprimir | Eliminar adjunto seleccionado   |
| `attachments:exit`     | Abajo, Escape       | Salir de navegación de adjuntos |

### Acciones de pie de página

Acciones disponibles en el contexto `Footer`:

| Acción                  | Predeterminado | Descripción                                                               |
| :---------------------- | :------------- | :------------------------------------------------------------------------ |
| `footer:next`           | Derecha        | Siguiente elemento de pie de página                                       |
| `footer:previous`       | Izquierda      | Elemento de pie de página anterior                                        |
| `footer:up`             | Arriba         | Navegar hacia arriba en pie de página (deselecciona en la parte superior) |
| `footer:down`           | Abajo          | Navegar hacia abajo en pie de página                                      |
| `footer:openSelected`   | Enter          | Abrir elemento de pie de página seleccionado                              |
| `footer:clearSelection` | Escape         | Limpiar selección de pie de página                                        |

### Acciones del selector de mensajes

Acciones disponibles en el contexto `MessageSelector`:

| Acción                   | Predeterminado                                  | Descripción                    |
| :----------------------- | :---------------------------------------------- | :----------------------------- |
| `messageSelector:up`     | Arriba, K, Ctrl+P                               | Mover hacia arriba en la lista |
| `messageSelector:down`   | Abajo, J, Ctrl+N                                | Mover hacia abajo en la lista  |
| `messageSelector:top`    | Ctrl+Arriba, Shift+Arriba, Meta+Arriba, Shift+K | Saltar al inicio               |
| `messageSelector:bottom` | Ctrl+Abajo, Shift+Abajo, Meta+Abajo, Shift+J    | Saltar al final                |
| `messageSelector:select` | Enter                                           | Seleccionar mensaje            |

### Acciones de diff

Acciones disponibles en el contexto `DiffDialog`:

| Acción                | Predeterminado            | Descripción                   |
| :-------------------- | :------------------------ | :---------------------------- |
| `diff:dismiss`        | Escape                    | Cerrar visor de diff          |
| `diff:previousSource` | Izquierda                 | Fuente de diff anterior       |
| `diff:nextSource`     | Derecha                   | Siguiente fuente de diff      |
| `diff:previousFile`   | Arriba                    | Archivo anterior en diff      |
| `diff:nextFile`       | Abajo                     | Siguiente archivo en diff     |
| `diff:viewDetails`    | Enter                     | Ver detalles de diff          |
| `diff:back`           | (específico del contexto) | Volver atrás en visor de diff |

### Acciones del selector de modelo

Acciones disponibles en el contexto `ModelPicker`:

| Acción                       | Predeterminado | Descripción                 |
| :--------------------------- | :------------- | :-------------------------- |
| `modelPicker:decreaseEffort` | Izquierda      | Disminuir nivel de esfuerzo |
| `modelPicker:increaseEffort` | Derecha        | Aumentar nivel de esfuerzo  |

### Acciones de selección

Acciones disponibles en el contexto `Select`:

| Acción            | Predeterminado    | Descripción        |
| :---------------- | :---------------- | :----------------- |
| `select:next`     | Abajo, J, Ctrl+N  | Siguiente opción   |
| `select:previous` | Arriba, K, Ctrl+P | Opción anterior    |
| `select:accept`   | Enter             | Aceptar selección  |
| `select:cancel`   | Escape            | Cancelar selección |

### Acciones de plugin

Acciones disponibles en el contexto `Plugin`:

| Acción            | Predeterminado | Descripción                                                                                                       |
| :---------------- | :------------- | :---------------------------------------------------------------------------------------------------------------- |
| `plugin:toggle`   | Espacio        | Alternar selección de plugin                                                                                      |
| `plugin:install`  | I              | Instalar plugins seleccionados                                                                                    |
| `plugin:favorite` | F              | Marcar como favorito el plugin seleccionado para que se ordene cerca de la parte superior de la pestaña Instalado |

### Acciones de configuración

Acciones disponibles en el contexto `Settings`:

| Acción            | Predeterminado | Descripción                                                                          |
| :---------------- | :------------- | :----------------------------------------------------------------------------------- |
| `settings:search` | /              | Entrar en modo de búsqueda                                                           |
| `settings:retry`  | R              | Reintentar carga de datos de uso (en caso de error)                                  |
| `settings:close`  | Enter          | Guardar cambios y cerrar el panel de configuración. Escape descarta cambios y cierra |

### Acciones de doctor

Acciones disponibles en el contexto `Doctor`:

| Acción       | Predeterminado | Descripción                                                                                                                   |
| :----------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `doctor:fix` | F              | Enviar el informe de diagnósticos a Claude para corregir los problemas reportados. Solo activo cuando se encuentran problemas |

### Acciones de voz

Acciones disponibles en el contexto `Chat` cuando [dictado de voz](/es/voice-dictation) está habilitado:

| Acción             | Predeterminado | Descripción                                                               |
| :----------------- | :------------- | :------------------------------------------------------------------------ |
| `voice:pushToTalk` | Espacio        | Dictar una indicación. Mantener presionado o tocar según el modo `/voice` |

### Acciones de desplazamiento

Acciones disponibles en el contexto `Scroll` cuando [renderizado de pantalla completa](/es/fullscreen) está habilitado:

| Acción                      | Predeterminado       | Descripción                                                                                                                                              |
| :-------------------------- | :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scroll:lineUp`             | (sin vincular)       | Desplazarse hacia arriba una línea. El desplazamiento de rueda de ratón activa esta acción                                                               |
| `scroll:lineDown`           | (sin vincular)       | Desplazarse hacia abajo una línea. El desplazamiento de rueda de ratón activa esta acción                                                                |
| `scroll:pageUp`             | Av Pág               | Desplazarse hacia arriba la mitad de la altura de la ventana gráfica                                                                                     |
| `scroll:pageDown`           | Re Pág               | Desplazarse hacia abajo la mitad de la altura de la ventana gráfica                                                                                      |
| `scroll:top`                | Ctrl+Inicio          | Saltar al inicio de la conversación                                                                                                                      |
| `scroll:bottom`             | Ctrl+Fin             | Saltar al mensaje más reciente y reactivar el seguimiento automático                                                                                     |
| `scroll:halfPageUp`         | (sin vincular)       | Desplazarse hacia arriba la mitad de la altura de la ventana gráfica. Mismo comportamiento que `scroll:pageUp`, proporcionado para rebinds de estilo vi  |
| `scroll:halfPageDown`       | (sin vincular)       | Desplazarse hacia abajo la mitad de la altura de la ventana gráfica. Mismo comportamiento que `scroll:pageDown`, proporcionado para rebinds de estilo vi |
| `scroll:fullPageUp`         | (sin vincular)       | Desplazarse hacia arriba la altura completa de la ventana gráfica                                                                                        |
| `scroll:fullPageDown`       | (sin vincular)       | Desplazarse hacia abajo la altura completa de la ventana gráfica                                                                                         |
| `selection:copy`            | Ctrl+Shift+C / Cmd+C | Copiar el texto seleccionado al portapapeles                                                                                                             |
| `selection:clear`           | (sin vincular)       | Limpiar la selección de texto activa                                                                                                                     |
| `selection:extendLeft`      | Shift+Izquierda      | Extender la selección activa una columna hacia la izquierda                                                                                              |
| `selection:extendRight`     | Shift+Derecha        | Extender la selección activa una columna hacia la derecha                                                                                                |
| `selection:extendUp`        | Shift+Arriba         | Extender la selección activa una fila hacia arriba. Desplaza la ventana gráfica cuando la selección alcanza el borde superior                            |
| `selection:extendDown`      | Shift+Abajo          | Extender la selección activa una fila hacia abajo. Desplaza la ventana gráfica cuando la selección alcanza el borde inferior                             |
| `selection:extendLineStart` | Shift+Inicio         | Extender la selección activa al inicio de la línea                                                                                                       |
| `selection:extendLineEnd`   | Shift+Fin            | Extender la selección activa al final de la línea                                                                                                        |

## Sintaxis de pulsación de tecla

### Modificadores

Use teclas modificadoras con el separador `+`:

* `ctrl` o `control` - Tecla Control
* `shift` - Tecla Shift
* `alt`, `opt`, `option`, o `meta` - Tecla Alt en Windows y Linux, tecla Opción en macOS
* `cmd`, `command`, `super`, o `win` - Tecla Comando en macOS, tecla Windows en Windows, tecla Super en Linux

El grupo `cmd` solo se detecta en terminales que reportan el modificador Super, como aquellos que soportan el protocolo de teclado Kitty o el modo `modifyOtherKeys` de xterm. La mayoría de terminales no lo envían, así que use `ctrl` o `meta` para atajos de teclado que desee que funcionen en todas partes.

Por ejemplo:

```text theme={null}
ctrl+k          Ctrl + K
shift+tab       Shift + Tab
meta+p          Opción + P en macOS, Alt + P en otros lugares
ctrl+shift+c    Múltiples modificadores
```

### Letras mayúsculas

Una letra mayúscula independiente implica Shift. Por ejemplo, `K` es equivalente a `shift+k`. Esto es útil para atajos de teclado de estilo vim donde las teclas mayúsculas y minúsculas tienen significados diferentes.

Las letras mayúsculas con modificadores (por ejemplo, `ctrl+K`) se tratan como estilísticas y **no** implican Shift: `ctrl+K` es lo mismo que `ctrl+k`.

### Acordes

Los acordes son secuencias de pulsaciones de teclas separadas por espacios:

```text theme={null}
ctrl+k ctrl+s   Presione Ctrl+K, suelte, luego Ctrl+S
```

### Teclas especiales

* `escape` o `esc` - Tecla Escape
* `enter` o `return` - Tecla Enter
* `tab` - Tecla Tab
* `space` - Barra espaciadora
* `up`, `down`, `left`, `right` - Teclas de flecha
* `backspace`, `delete` - Teclas de eliminación

## Desvinculación de atajos predeterminados

Establezca una acción en `null` para desvinculación de un atajo predeterminado:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

Esto también funciona para vinculaciones de acordes. Desvinculación de cada acorde que comparte un prefijo libera ese prefijo para su uso como una vinculación de tecla única:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

Si desvincula algunos pero no todos los acordes en un prefijo, presionar el prefijo aún entra en modo de espera de acorde para las vinculaciones restantes.

## Atajos reservados

Estos atajos no se pueden reasignar:

| Atajo     | Razón                                            |
| :-------- | :----------------------------------------------- |
| Ctrl+C    | Interrupción/cancelación codificada              |
| Ctrl+D    | Salida codificada                                |
| Ctrl+M    | Idéntico a Enter en terminales (ambos envían CR) |
| Caps Lock | No se entrega a las aplicaciones de terminal     |

## Conflictos de terminal

Algunos atajos pueden entrar en conflicto con multiplexores de terminal:

| Atajo  | Conflicto                                        |
| :----- | :----------------------------------------------- |
| Ctrl+B | Prefijo de tmux (presione dos veces para enviar) |
| Ctrl+A | Prefijo de GNU screen                            |
| Ctrl+Z | Suspensión de proceso Unix (SIGTSTP)             |

## Interacción del modo Vim

Cuando el modo vim está habilitado mediante `/config` → Editor mode, los keybindings y el modo vim funcionan de forma independiente:

* **Modo Vim** maneja la entrada a nivel de entrada de texto (movimiento del cursor, modos, movimientos)
* **Keybindings** manejan acciones a nivel de componente (alternar tareas, enviar, etc.)
* La tecla Escape en modo vim cambia de modo INSERT a NORMAL; no activa `chat:cancel`
* La mayoría de los atajos Ctrl+tecla pasan a través del modo vim al sistema de keybindings
* En modo NORMAL de vim, `?` muestra el menú de ayuda (comportamiento de vim)

## Validación

Claude Code valida sus keybindings y muestra advertencias para:

* Errores de análisis (JSON o estructura inválida)
* Nombres de contexto inválidos
* Conflictos de atajos reservados
* Conflictos de multiplexor de terminal
* Vinculaciones duplicadas en el mismo contexto

Ejecute `/doctor` para ver cualquier advertencia de keybindings.
