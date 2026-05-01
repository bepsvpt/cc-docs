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

* **Lanzamiento rápido**: utiliza `Cmd+Esc` (Mac) o `Ctrl+Esc` (Windows/Linux) para abrir Claude Code directamente desde tu editor, o haz clic en el botón de Claude Code en la interfaz
* **Visualización de diferencias**: los cambios de código se pueden mostrar directamente en el visor de diferencias del IDE en lugar de la terminal
* **Contexto de selección**: la selección actual o pestaña en el IDE se comparte automáticamente con Claude Code
* **Atajos de referencia de archivos**: utiliza `Cmd+Option+K` (Mac) o `Alt+Ctrl+K` (Linux/Windows) para insertar referencias de archivos como `@src/auth.ts#L1-99`
* **Compartición de diagnósticos**: los errores de diagnóstico del IDE, como errores de lint y sintaxis, se comparten automáticamente con Claude mientras trabajas

## Instalación

### Instalación desde Marketplace

Busca e instala el [plugin de Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) desde el marketplace de JetBrains y reinicia tu IDE.

Si aún no has instalado Claude Code, consulta la [guía de inicio rápido](/es/quickstart) para obtener instrucciones de instalación.

<Note>
  Después de instalar el plugin, es posible que necesites reiniciar completamente tu IDE para que surta efecto.
</Note>

## Uso

### Desde tu IDE

Ejecuta `claude` desde la terminal integrada de tu IDE, y todas las características de integración estarán activas.

### Desde terminales externos

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
3. Establece la herramienta de diferencias en `auto` para mostrar diferencias en el IDE, o `terminal` para mantenerlas en la terminal

### Configuración del Plugin

Configura el plugin de Claude Code yendo a **Settings → Tools → Claude Code \[Beta]**:

#### Configuración general

* **Comando Claude**: especifica un comando personalizado para ejecutar Claude, por ejemplo `claude`, `/usr/local/bin/claude`, o `npx @anthropic-ai/claude-code`
* **Suprimir notificación para comando Claude no encontrado**: omite notificaciones sobre no encontrar el comando Claude
* **Habilitar usar Option+Enter para indicadores de varias líneas**: solo en macOS. Cuando está habilitado, Option+Enter inserta nuevas líneas en los indicadores de Claude Code. Desactívalo si la tecla Option se captura inesperadamente. Requiere reinicio de terminal.
* **Habilitar actualizaciones automáticas**: verifica automáticamente e instala actualizaciones del plugin, aplicadas al reiniciar

<Tip>
  Para usuarios de WSL: establece `wsl -d Ubuntu -- bash -lic "claude"` como tu comando Claude (reemplaza `Ubuntu` con el nombre de tu distribución WSL)
</Tip>

#### Configuración de la tecla ESC

Si la tecla ESC no interrumpe las operaciones de Claude Code en terminales de JetBrains:

1. Ve a **Settings → Tools → Terminal**
2. Cualquiera de:
   * Desactiva "Move focus to the editor with Escape", o
   * Haz clic en "Configure terminal keybindings" y elimina el atajo "Switch focus to Editor"
3. Aplica los cambios

Esto permite que la tecla ESC interrumpa correctamente las operaciones de Claude Code.

## Configuraciones especiales

### Desarrollo remoto

<Warning>
  Cuando utilices JetBrains Remote Development, debes instalar el plugin en el host remoto a través de **Settings → Plugin (Host)**.
</Warning>

El plugin debe instalarse en el host remoto, no en tu máquina cliente local.

### Configuración de WSL

Si estás utilizando Claude Code en WSL2 con un JetBrains IDE y ves "No available IDEs detected", la causa generalmente es el enrutamiento NAT de WSL2 o el Firewall de Windows bloqueando la conexión entre WSL2 y el IDE ejecutándose en el host de Windows. WSL1 utiliza la red del host directamente y no se ve afectado.

#### Permitir tráfico de WSL2 a través del Firewall de Windows

Esta es la solución recomendada porque mantiene tu modo de red WSL2 existente.

<Steps>
  <Step title="Encuentra tu dirección IP de WSL2">
    Desde dentro de tu shell de WSL, ejecuta:

    ```bash theme={null}
    hostname -I
    ```

    Anota la subred, por ejemplo `172.21.123.45` está en `172.21.0.0/16`.
  </Step>

  <Step title="Crea una regla de firewall">
    Abre PowerShell como Administrador y ejecuta lo siguiente, ajustando el rango de IP para que coincida con tu subred:

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="Reinicia tu IDE y Claude Code">
    Cierra y reabre ambos para que la nueva regla surta efecto.
  </Step>
</Steps>

#### Cambiar WSL2 a redes espejadas

Las redes espejadas requieren Windows 11 22H2 o posterior. Si estás en Windows 10, utiliza la regla de firewall anterior.

Añade esto a `.wslconfig` en tu directorio de usuario de Windows:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Luego reinicia WSL con `wsl --shutdown` desde PowerShell.

## Solución de problemas

### Plugin no funciona

Si el plugin está instalado pero las características de Claude Code no aparecen en tu IDE:

* Asegúrate de que estés ejecutando Claude Code desde el directorio raíz del proyecto
* Verifica que el plugin de JetBrains esté habilitado en la configuración del IDE
* Reinicia completamente el IDE (es posible que necesites hacerlo varias veces)
* Para Desarrollo Remoto, asegúrate de que el plugin esté instalado en el host remoto

### IDE no detectado

Si ejecutar `claude` muestra "No available IDEs detected":

* Verifica que el plugin esté instalado y habilitado
* Reinicia completamente el IDE
* Comprueba que estés ejecutando Claude Code desde la terminal integrada
* Para usuarios de WSL, consulta la [configuración de WSL](#wsl-configuration) anterior

### Comando no encontrado

Si hacer clic en el icono de Claude muestra "command not found":

1. Verifica que Claude Code esté instalado ejecutando `claude --version` en una terminal
2. Configura la ruta del comando Claude en la configuración del plugin
3. Para usuarios de WSL, utiliza el formato de comando WSL mencionado en la sección de configuración

## Consideraciones de seguridad

Cuando Claude Code se ejecuta en un JetBrains IDE con permisos de edición automática habilitados, puede ser capaz de modificar archivos de configuración del IDE que pueden ser ejecutados automáticamente por tu IDE. Esto puede aumentar el riesgo de ejecutar Claude Code en modo de edición automática y permitir eludir los indicadores de permiso de Claude Code para la ejecución de bash.

Cuando se ejecuta en JetBrains IDEs, considera:

* Usar el modo de aprobación manual para ediciones
* Tener especial cuidado para asegurar que Claude solo se use con indicadores de confianza
* Ser consciente de qué archivos Claude Code tiene acceso para modificar

Para problemas de instalación o inicio de sesión de Claude Code fuera del IDE, consulta [Solucionar problemas de instalación e inicio de sesión](/es/troubleshoot-install).
