> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Utiliza Claude Code con JetBrains IDEs incluyendo IntelliJ, PyCharm, WebStorm y más

Claude Code se integra con JetBrains IDEs a través de un plugin dedicado, proporcionando características como visualización de diferencias interactivas, compartición de contexto de selección y más.

## IDEs Compatibles

El plugin de Claude Code funciona con la mayoría de JetBrains IDEs, incluyendo:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Características

* **Lanzamiento rápido**: Utiliza `Cmd+Esc` (Mac) o `Ctrl+Esc` (Windows/Linux) para abrir Claude Code directamente desde tu editor, o haz clic en el botón de Claude Code en la interfaz
* **Visualización de diferencias**: Los cambios de código se pueden mostrar directamente en el visor de diferencias del IDE en lugar de la terminal
* **Contexto de selección**: La selección/pestaña actual en el IDE se comparte automáticamente con Claude Code
* **Atajos de referencia de archivos**: Utiliza `Cmd+Option+K` (Mac) o `Alt+Ctrl+K` (Linux/Windows) para insertar referencias de archivos (por ejemplo, @File#L1-99)
* **Compartición de diagnósticos**: Los errores de diagnóstico (lint, sintaxis, etc.) del IDE se comparten automáticamente con Claude mientras trabajas

## Instalación

### Instalación desde Marketplace

Busca e instala el [plugin de Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) desde el marketplace de JetBrains y reinicia tu IDE.

Si aún no has instalado Claude Code, consulta [nuestra guía de inicio rápido](/es/quickstart) para obtener instrucciones de instalación.

<Note>
  Después de instalar el plugin, es posible que necesites reiniciar completamente tu IDE para que surta efecto.
</Note>

## Uso

### Desde tu IDE

Ejecuta `claude` desde la terminal integrada de tu IDE, y todas las características de integración estarán activas.

### Desde Terminales Externos

Utiliza el comando `/ide` en cualquier terminal externo para conectar Claude Code a tu JetBrains IDE y activar todas las características:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Si deseas que Claude tenga acceso a los mismos archivos que tu IDE, inicia Claude Code desde el mismo directorio que la raíz del proyecto de tu IDE.

## Configuración

### Configuración de Claude Code

Configura la integración del IDE a través de la configuración de Claude Code:

1. Ejecuta `claude`
2. Ingresa el comando `/config`
3. Establece la herramienta de diferencias en `auto` para la detección automática del IDE

### Configuración del Plugin

Configura el plugin de Claude Code yendo a **Settings → Tools → Claude Code \[Beta]**:

#### Configuración General

* **Comando Claude**: Especifica un comando personalizado para ejecutar Claude (por ejemplo, `claude`, `/usr/local/bin/claude`, o `npx @anthropic/claude`)
* **Suprimir notificación para comando Claude no encontrado**: Omite notificaciones sobre no encontrar el comando Claude
* **Habilitar usar Option+Enter para indicadores de varias líneas** (solo macOS): Cuando está habilitado, Option+Enter inserta nuevas líneas en los indicadores de Claude Code. Desactívalo si experimentas problemas con la tecla Option siendo capturada inesperadamente (requiere reinicio de terminal)
* **Habilitar actualizaciones automáticas**: Verifica automáticamente e instala actualizaciones del plugin (se aplica al reiniciar)

<Tip>
  Para usuarios de WSL: Establece `wsl -d Ubuntu -- bash -lic "claude"` como tu comando Claude (reemplaza `Ubuntu` con el nombre de tu distribución WSL)
</Tip>

#### Configuración de la Tecla ESC

Si la tecla ESC no interrumpe las operaciones de Claude Code en terminales de JetBrains:

1. Ve a **Settings → Tools → Terminal**
2. Cualquiera de:
   * Desactiva "Move focus to the editor with Escape", o
   * Haz clic en "Configure terminal keybindings" y elimina el atajo "Switch focus to Editor"
3. Aplica los cambios

Esto permite que la tecla ESC interrumpa correctamente las operaciones de Claude Code.

## Configuraciones Especiales

### Desarrollo Remoto

<Warning>
  Cuando utilices JetBrains Remote Development, debes instalar el plugin en el host remoto a través de **Settings → Plugin (Host)**.
</Warning>

El plugin debe instalarse en el host remoto, no en tu máquina cliente local.

### Configuración de WSL

<Warning>
  Los usuarios de WSL pueden necesitar configuración adicional para que la detección del IDE funcione correctamente. Consulta nuestra [guía de solución de problemas de WSL](/es/troubleshooting#jetbrains-ide-not-detected-on-wsl2) para obtener instrucciones de configuración detalladas.
</Warning>

La configuración de WSL puede requerir:

* Configuración adecuada de la terminal
* Ajustes del modo de red
* Actualizaciones de configuración del firewall

## Solución de Problemas

### Plugin No Funciona

* Asegúrate de que estés ejecutando Claude Code desde el directorio raíz del proyecto
* Verifica que el plugin de JetBrains esté habilitado en la configuración del IDE
* Reinicia completamente el IDE (es posible que necesites hacerlo varias veces)
* Para Desarrollo Remoto, asegúrate de que el plugin esté instalado en el host remoto

### IDE No Detectado

* Verifica que el plugin esté instalado y habilitado
* Reinicia completamente el IDE
* Comprueba que estés ejecutando Claude Code desde la terminal integrada
* Para usuarios de WSL, consulta la [guía de solución de problemas de WSL](/es/troubleshooting#jetbrains-ide-not-detected-on-wsl2)

### Comando No Encontrado

Si hacer clic en el icono de Claude muestra "command not found":

1. Verifica que Claude Code esté instalado: `npm list -g @anthropic-ai/claude-code`
2. Configura la ruta del comando Claude en la configuración del plugin
3. Para usuarios de WSL, utiliza el formato de comando WSL mencionado en la sección de configuración

## Consideraciones de Seguridad

Cuando Claude Code se ejecuta en un JetBrains IDE con permisos de edición automática habilitados, puede ser capaz de modificar archivos de configuración del IDE que pueden ser ejecutados automáticamente por tu IDE. Esto puede aumentar el riesgo de ejecutar Claude Code en modo de edición automática y permitir eludir los indicadores de permiso de Claude Code para la ejecución de bash.

Cuando se ejecuta en JetBrains IDEs, considera:

* Usar el modo de aprobación manual para ediciones
* Tener especial cuidado para asegurar que Claude solo se use con indicadores de confianza
* Ser consciente de qué archivos Claude Code tiene acceso para modificar

Para obtener ayuda adicional, consulta nuestra [guía de solución de problemas](/es/troubleshooting).
