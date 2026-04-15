> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Solución de problemas

> Descubre soluciones para problemas comunes con la instalación y el uso de Claude Code.

## Solucionar problemas de instalación

<Tip>
  Si prefieres evitar la terminal por completo, la [aplicación de escritorio Claude Code](/es/desktop-quickstart) te permite instalar y usar Claude Code a través de una interfaz gráfica. Descárgala para [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) o [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) y comienza a codificar sin ninguna configuración de línea de comandos.
</Tip>

Encuentra el mensaje de error o síntoma que estás viendo:

| Lo que ves                                                               | Solución                                                                                                                 |
| :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `command not found: claude` o `'claude' is not recognized`               | [Corrige tu PATH](#command-not-found-claude-after-installation)                                                          |
| `syntax error near unexpected token '<'`                                 | [El script de instalación devuelve HTML](#install-script-returns-html-instead-of-a-shell-script)                         |
| `curl: (56) Failure writing output to destination`                       | [Descarga el script primero, luego ejecútalo](#curl-56-failure-writing-output-to-destination)                            |
| `Killed` durante la instalación en Linux                                 | [Añade espacio de intercambio para servidores con poca memoria](#install-killed-on-low-memory-linux-servers)             |
| `TLS connect error` o `SSL/TLS secure channel`                           | [Actualiza los certificados CA](#tls-or-ssl-connection-errors)                                                           |
| `Failed to fetch version` o no se puede alcanzar el servidor de descarga | [Verifica la conectividad de red y la configuración del proxy](#check-network-connectivity)                              |
| `irm is not recognized` o `&& is not valid`                              | [Usa el comando correcto para tu shell](#windows-irm-or--not-recognized)                                                 |
| `Claude Code on Windows requires git-bash`                               | [Instala o configura Git Bash](#windows-claude-code-on-windows-requires-git-bash)                                        |
| `Error loading shared library`                                           | [Variante binaria incorrecta para tu sistema](#linux-wrong-binary-variant-installed-muslglibc-mismatch)                  |
| `Illegal instruction` en Linux                                           | [Desajuste de arquitectura](#illegal-instruction-on-linux)                                                               |
| `dyld: cannot load` o `Abort trap` en macOS                              | [Incompatibilidad binaria](#dyld-cannot-load-on-macos)                                                                   |
| `Invoke-Expression: Missing argument in parameter list`                  | [El script de instalación devuelve HTML](#install-script-returns-html-instead-of-a-shell-script)                         |
| `App unavailable in region`                                              | Claude Code no está disponible en tu país. Consulta [países compatibles](https://www.anthropic.com/supported-countries). |
| `unable to get local issuer certificate`                                 | [Configura certificados CA corporativos](#tls-or-ssl-connection-errors)                                                  |
| `OAuth error` o `403 Forbidden`                                          | [Corrige la autenticación](#authentication-issues)                                                                       |

Si tu problema no está listado, trabaja a través de estos pasos de diagnóstico.

## Depurar problemas de instalación

### Verifica la conectividad de red

El instalador descarga desde `storage.googleapis.com`. Verifica que puedas alcanzarlo:

```bash theme={null}
curl -sI https://storage.googleapis.com
```

Si esto falla, tu red puede estar bloqueando la conexión. Las causas comunes incluyen:

* Firewalls corporativos o proxies bloqueando Google Cloud Storage
* Restricciones de red regional: intenta usar una VPN o una red alternativa
* Problemas de TLS/SSL: actualiza los certificados CA de tu sistema, o verifica si `HTTPS_PROXY` está configurado

Si estás detrás de un proxy corporativo, establece `HTTPS_PROXY` y `HTTP_PROXY` a la dirección de tu proxy antes de instalar. Pregunta a tu equipo de TI por la URL del proxy si no la conoces, o verifica la configuración del proxy en tu navegador.

Este ejemplo establece ambas variables de proxy, luego ejecuta el instalador a través de tu proxy:

```bash theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### Verifica tu PATH

Si la instalación fue exitosa pero obtienes un error `command not found` o `not recognized` al ejecutar `claude`, el directorio de instalación no está en tu PATH. Tu shell busca programas en directorios listados en PATH, y el instalador coloca `claude` en `~/.local/bin/claude` en macOS/Linux o `%USERPROFILE%\.local\bin\claude.exe` en Windows.

Verifica si el directorio de instalación está en tu PATH listando tus entradas de PATH y filtrando por `local/bin`:

<Tabs>
  <Tab title="macOS/Linux">
    ```bash theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    Si no hay salida, el directorio falta. Añádelo a tu configuración de shell:

    ```bash theme={null}
    # Zsh (macOS por defecto)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux por defecto)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    Alternativamente, cierra y reabre tu terminal.

    Verifica que la corrección funcionó:

    ```bash theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    Si no hay salida, añade el directorio de instalación a tu PATH de usuario:

    ```powershell theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    Reinicia tu terminal para que el cambio surta efecto.

    Verifica que la corrección funcionó:

    ```powershell theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    Si no hay salida, abre Configuración del Sistema, ve a Variables de Entorno, y añade `%USERPROFILE%\.local\bin` a tu variable PATH de usuario. Reinicia tu terminal.

    Verifica que la corrección funcionó:

    ```batch theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### Verifica instalaciones conflictivas

Múltiples instalaciones de Claude Code pueden causar desajustes de versión o comportamiento inesperado. Verifica qué está instalado:

<Tabs>
  <Tab title="macOS/Linux">
    Lista todos los binarios `claude` encontrados en tu PATH:

    ```bash theme={null}
    which -a claude
    ```

    Verifica si las versiones del instalador nativo y npm están presentes:

    ```bash theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

Si encuentras múltiples instalaciones, mantén solo una. La instalación nativa en `~/.local/bin/claude` es recomendada. Elimina cualquier instalación adicional:

Desinstala una instalación global de npm:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

Elimina una instalación de Homebrew en macOS:

```bash theme={null}
brew uninstall --cask claude-code
```

### Verifica permisos de directorio

El instalador necesita acceso de escritura a `~/.local/bin/` y `~/.claude/`. Si la instalación falla con errores de permisos, verifica si estos directorios son escribibles:

```bash theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

Si alguno de los directorios no es escribible, crea el directorio de instalación y establece tu usuario como propietario:

```bash theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### Verifica que el binario funciona

Si `claude` está instalado pero se bloquea o cuelga al iniciar, ejecuta estas comprobaciones para reducir la causa.

Confirma que el binario existe y es ejecutable:

```bash theme={null}
ls -la $(which claude)
```

En Linux, verifica si hay bibliotecas compartidas faltantes. Si `ldd` muestra bibliotecas faltantes, es posible que necesites instalar paquetes del sistema. En Alpine Linux y otras distribuciones basadas en musl, consulta [Configuración de Alpine Linux](/es/setup#alpine-linux-and-musl-based-distributions).

```bash theme={null}
ldd $(which claude) | grep "not found"
```

Ejecuta una comprobación rápida de cordura de que el binario puede ejecutarse:

```bash theme={null}
claude --version
```

## Problemas comunes de instalación

Estos son los problemas de instalación más frecuentemente encontrados y sus soluciones.

### El script de instalación devuelve HTML en lugar de un script de shell

Al ejecutar el comando de instalación, puedes ver uno de estos errores:

```text theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

En PowerShell, el mismo problema aparece como:

```text theme={null}
Invoke-Expression: Missing argument in parameter list.
```

Esto significa que la URL de instalación devolvió una página HTML en lugar del script de instalación. Si la página HTML dice "App unavailable in region," Claude Code no está disponible en tu país. Consulta [países compatibles](https://www.anthropic.com/supported-countries).

De lo contrario, esto puede ocurrir debido a problemas de red, enrutamiento regional, o una interrupción temporal del servicio.

**Soluciones:**

1. **Usa un método de instalación alternativo**:

   En macOS o Linux, instala a través de Homebrew:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   En Windows, instala a través de WinGet:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **Reintentar después de unos minutos**: el problema es a menudo temporal. Espera e intenta el comando original nuevamente.

### `command not found: claude` después de la instalación

La instalación terminó pero `claude` no funciona. El error exacto varía según la plataforma:

| Plataforma  | Mensaje de error                                                       |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

Esto significa que el directorio de instalación no está en la ruta de búsqueda de tu shell. Consulta [Verifica tu PATH](#verify-your-path) para la corrección en cada plataforma.

### `curl: (56) Failure writing output to destination`

El comando `curl ... | bash` descarga el script y lo pasa directamente a Bash para su ejecución usando una tubería (`|`). Este error significa que la conexión se rompió antes de que el script terminara de descargar. Las causas comunes incluyen interrupciones de red, la descarga siendo bloqueada a mitad de camino, o límites de recursos del sistema.

**Soluciones:**

1. **Verifica la estabilidad de la red**: Los binarios de Claude Code se alojan en Google Cloud Storage. Prueba que puedas alcanzarlo:
   ```bash theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   Si el comando se completa silenciosamente, tu conexión está bien y el problema es probablemente intermitente. Reintentar el comando de instalación. Si ves un error, tu red puede estar bloqueando la descarga.

2. **Intenta un método de instalación alternativo**:

   En macOS o Linux:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   En Windows:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Errores de conexión TLS o SSL

Errores como `curl: (35) TLS connect error`, `schannel: next InitializeSecurityContext failed`, o el `Could not establish trust relationship for the SSL/TLS secure channel` de PowerShell indican fallos en el apretón de manos TLS.

**Soluciones:**

1. **Actualiza tus certificados CA del sistema**:

   En Ubuntu/Debian:

   ```bash theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   En macOS a través de Homebrew:

   ```bash theme={null}
   brew install ca-certificates
   ```

2. **En Windows, habilita TLS 1.2** en PowerShell antes de ejecutar el instalador:
   ```powershell theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **Verifica la interferencia de proxy o firewall**: los proxies corporativos que realizan inspección TLS pueden causar estos errores, incluyendo `unable to get local issuer certificate`. Establece `NODE_EXTRA_CA_CERTS` a tu paquete de certificados CA corporativos:
   ```bash theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   Pregunta a tu equipo de TI por el archivo de certificado si no lo tienes. También puedes intentar en una conexión directa para confirmar que el proxy es la causa.

### `Failed to fetch version from storage.googleapis.com`

El instalador no pudo alcanzar el servidor de descarga. Esto típicamente significa que `storage.googleapis.com` está bloqueado en tu red.

**Soluciones:**

1. **Prueba la conectividad directamente**:
   ```bash theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **Si estás detrás de un proxy**, establece `HTTPS_PROXY` para que el instalador pueda enrutarse a través de él. Consulta [configuración de proxy](/es/network-config#proxy-configuration) para detalles.
   ```bash theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **Si estás en una red restringida**, intenta una red diferente o VPN, o usa un método de instalación alternativo:

   En macOS o Linux:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   En Windows:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows: `irm` o `&&` no reconocido

Si ves `'irm' is not recognized` o `The token '&&' is not valid`, estás ejecutando el comando incorrecto para tu shell.

* **`irm` no reconocido**: estás en CMD, no en PowerShell. Tienes dos opciones:

  Abre PowerShell buscando "PowerShell" en el menú Inicio, luego ejecuta el comando de instalación original:

  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  O quédate en CMD y usa el instalador de CMD en su lugar:

  ```batch theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` no válido**: estás en PowerShell pero ejecutaste el comando del instalador de CMD. Usa el instalador de PowerShell:
  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### Instalación eliminada en servidores Linux con poca memoria

Si ves `Killed` durante la instalación en un VPS o instancia en la nube:

```text theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

El asesino de OOM de Linux terminó el proceso porque el sistema se quedó sin memoria. Claude Code requiere al menos 4 GB de RAM disponible.

**Soluciones:**

1. **Añade espacio de intercambio** si tu servidor tiene RAM limitada. El intercambio usa espacio en disco como memoria de desbordamiento, permitiendo que la instalación se complete incluso con RAM física baja.

   Crea un archivo de intercambio de 2 GB y habilítalo:

   ```bash theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   Luego reintentar la instalación:

   ```bash theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Cierra otros procesos** para liberar memoria antes de instalar.

3. **Usa una instancia más grande** si es posible. Claude Code requiere al menos 4 GB de RAM.

### La instalación se cuelga en Docker

Al instalar Claude Code en un contenedor Docker, instalar como root en `/` puede causar cuelgues.

**Soluciones:**

1. **Establece un directorio de trabajo** antes de ejecutar el instalador. Cuando se ejecuta desde `/`, el instalador escanea todo el sistema de archivos, lo que causa un uso excesivo de memoria. Establecer `WORKDIR` limita el escaneo a un pequeño directorio:
   ```dockerfile theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Aumenta los límites de memoria de Docker** si usas Docker Desktop:
   ```bash theme={null}
   docker build --memory=4g .
   ```

### Windows: Claude Desktop anula el comando CLI `claude`

Si instalaste una versión anterior de Claude Desktop, puede registrar un `Claude.exe` en el directorio `WindowsApps` que toma prioridad en PATH sobre Claude Code CLI. Ejecutar `claude` abre la aplicación de escritorio en lugar de la CLI.

Actualiza Claude Desktop a la última versión para corregir este problema.

### Windows: "Claude Code on Windows requires git-bash"

Claude Code en Windows nativo necesita [Git para Windows](https://git-scm.com/downloads/win), que incluye Git Bash.

**Si Git no está instalado**, descárgalo e instálalo desde [git-scm.com/downloads/win](https://git-scm.com/downloads/win). Durante la configuración, selecciona "Add to PATH." Reinicia tu terminal después de instalar.

**Si Git ya está instalado** pero Claude Code aún no puede encontrarlo, establece la ruta en tu [archivo settings.json](/es/settings):

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Si tu Git está instalado en otro lugar, encuentra la ruta ejecutando `where.exe git` en PowerShell y usa la ruta `bin\bash.exe` de ese directorio.

### Linux: variante binaria incorrecta instalada (desajuste musl/glibc)

Si ves errores sobre bibliotecas compartidas faltantes como `libstdc++.so.6` o `libgcc_s.so.1` después de la instalación, el instalador puede haber descargado la variante binaria incorrecta para tu sistema.

```text theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

Esto puede ocurrir en sistemas basados en glibc que tienen paquetes de compilación cruzada musl instalados, causando que el instalador detecte incorrectamente el sistema como musl.

**Soluciones:**

1. **Verifica qué libc usa tu sistema**:
   ```bash theme={null}
   ldd /bin/ls | head -1
   ```
   Si muestra `linux-vdso.so` o referencias a `/lib/x86_64-linux-gnu/`, estás en glibc. Si muestra `musl`, estás en musl.

2. **Si estás en glibc pero obtuviste el binario musl**, elimina la instalación y reinstala. También puedes descargar manualmente el binario correcto desde el bucket de GCS en `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Abre un [problema en GitHub](https://github.com/anthropics/claude-code/issues) con la salida de `ldd /bin/ls` y `ls /lib/libc.musl*`.

3. **Si realmente estás en musl** (Alpine Linux), instala los paquetes requeridos:
   ```bash theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### `Illegal instruction` en Linux

Si el instalador imprime `Illegal instruction` en lugar del mensaje `Killed` de OOM, el binario descargado no coincide con la arquitectura de tu CPU. Esto ocurre comúnmente en servidores ARM que reciben un binario x86, o en CPUs más antiguas que carecen de conjuntos de instrucciones requeridos.

```text theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**Soluciones:**

1. **Verifica tu arquitectura**:
   ```bash theme={null}
   uname -m
   ```
   `x86_64` significa 64-bit Intel/AMD, `aarch64` significa ARM64. Si el binario no coincide, [abre un problema en GitHub](https://github.com/anthropics/claude-code/issues) con la salida.

2. **Intenta un método de instalación alternativo** mientras se resuelve el problema de arquitectura:
   ```bash theme={null}
   brew install --cask claude-code
   ```

### `dyld: cannot load` en macOS

Si ves `dyld: cannot load` o `Abort trap: 6` durante la instalación, el binario es incompatible con tu versión de macOS o hardware.

```text theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**Soluciones:**

1. **Verifica tu versión de macOS**: Claude Code requiere macOS 13.0 o posterior. Abre el menú Apple y selecciona About This Mac para verificar tu versión.

2. **Actualiza macOS** si estás en una versión anterior. El binario usa comandos de carga que las versiones anteriores de macOS no soportan.

3. **Intenta Homebrew** como método de instalación alternativo:
   ```bash theme={null}
   brew install --cask claude-code
   ```

### Problemas de instalación en Windows: errores en WSL

Podrías encontrar los siguientes problemas en WSL:

**Problemas de detección de SO/plataforma**: si recibes un error durante la instalación, WSL puede estar usando `npm` de Windows. Intenta:

* Ejecuta `npm config set os linux` antes de la instalación
* Instala con `npm install -g @anthropic-ai/claude-code --force --no-os-check`. No uses `sudo`.

**Errores de Node no encontrado**: si ves `exec: node: not found` al ejecutar `claude`, tu entorno WSL puede estar usando una instalación de Windows de Node.js. Puedes confirmar esto con `which npm` y `which node`, que deberían apuntar a rutas de Linux que comienzan con `/usr/` en lugar de `/mnt/c/`. Para corregir esto, intenta instalar Node a través del gestor de paquetes de tu distribución de Linux o a través de [`nvm`](https://github.com/nvm-sh/nvm).

**Conflictos de versión de nvm**: si tienes nvm instalado tanto en WSL como en Windows, puedes experimentar conflictos de versión al cambiar versiones de Node en WSL. Esto ocurre porque WSL importa el PATH de Windows por defecto, causando que npm/nvm de Windows tenga prioridad sobre la instalación de WSL.

Puedes identificar este problema por:

* Ejecutar `which npm` y `which node` - si apuntan a rutas de Windows (comenzando con `/mnt/c/`), se están usando versiones de Windows
* Experimentar funcionalidad rota después de cambiar versiones de Node con nvm en WSL

Para resolver este problema, corrige tu PATH de Linux para asegurar que las versiones de node/npm de Linux tengan prioridad:

**Solución principal: Asegúrate de que nvm se carga correctamente en tu shell**

La causa más común es que nvm no se carga en shells no interactivos. Añade lo siguiente a tu archivo de configuración de shell (`~/.bashrc`, `~/.zshrc`, etc.):

```bash theme={null}
# Carga nvm si existe
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

O ejecuta directamente en tu sesión actual:

```bash theme={null}
source ~/.nvm/nvm.sh
```

**Alternativa: Ajusta el orden de PATH**

Si nvm se carga correctamente pero las rutas de Windows aún tienen prioridad, puedes prepender explícitamente tus rutas de Linux a PATH en tu configuración de shell:

```bash theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  Evita desabilitar la importación de PATH de Windows a través de `appendWindowsPath = false` ya que esto rompe la capacidad de llamar ejecutables de Windows desde WSL. De manera similar, evita desinstalar Node.js de Windows si lo usas para desarrollo de Windows.
</Warning>

### Configuración de sandbox WSL2

[Sandboxing](/es/sandboxing) es compatible en WSL2 pero requiere instalar paquetes adicionales. Si ves un error como "Sandbox requires socat and bubblewrap" al ejecutar `/sandbox`, instala las dependencias:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

WSL1 no soporta sandboxing. Si ves "Sandboxing requires WSL2", necesitas actualizar a WSL2 o ejecutar Claude Code sin sandboxing.

### Errores de permisos durante la instalación

Si el instalador nativo falla con errores de permisos, el directorio de destino puede no ser escribible. Consulta [Verifica permisos de directorio](#check-directory-permissions).

Si instalaste previamente con npm y estás teniendo errores específicos de permisos de npm, cambia al instalador nativo:

```bash theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## Permisos y autenticación

Estas secciones abordan fallos de inicio de sesión, problemas de tokens, y comportamiento de solicitudes de permisos.

### Solicitudes de permisos repetidas

Si te encuentras aprobando repetidamente los mismos comandos, puedes permitir que herramientas específicas se ejecuten sin aprobación usando el comando `/permissions`. Consulta [documentación de Permisos](/es/permissions#manage-permissions).

### Problemas de autenticación

Si estás experimentando problemas de autenticación:

1. Ejecuta `/logout` para cerrar sesión completamente
2. Cierra Claude Code
3. Reinicia con `claude` y completa el proceso de autenticación nuevamente

Si el navegador no se abre automáticamente durante el inicio de sesión, presiona `c` para copiar la URL de OAuth a tu portapapeles, luego pégala en tu navegador manualmente.

### Error OAuth: Código inválido

Si ves `OAuth error: Invalid code. Please make sure the full code was copied`, el código de inicio de sesión expiró o fue truncado durante la copia-pega.

**Soluciones:**

* Presiona Enter para reintentar y completa el inicio de sesión rápidamente después de que se abra el navegador
* Escribe `c` para copiar la URL completa si el navegador no se abre automáticamente
* Si usas una sesión remota/SSH, el navegador puede abrirse en la máquina incorrecta. Copia la URL mostrada en la terminal y ábrela en tu navegador local en su lugar.

### 403 Forbidden después del inicio de sesión

Si ves `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}` después de iniciar sesión:

* **Usuarios de Claude Pro/Max**: verifica que tu suscripción esté activa en [claude.ai/settings](https://claude.ai/settings)
* **Usuarios de Console**: confirma que tu cuenta tiene el rol "Claude Code" o "Developer" asignado por tu administrador
* **Detrás de un proxy**: los proxies corporativos pueden interferir con solicitudes de API. Consulta [configuración de red](/es/network-config) para configuración de proxy.

### El inicio de sesión OAuth falla en WSL2

El inicio de sesión basado en navegador en WSL2 puede fallar si WSL no puede abrir tu navegador de Windows. Establece la variable de entorno `BROWSER`:

```bash theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

O copia la URL manualmente: cuando aparezca la solicitud de inicio de sesión, presiona `c` para copiar la URL de OAuth, luego pégala en tu navegador de Windows.

### "Not logged in" o token expirado

Si Claude Code te solicita iniciar sesión nuevamente después de una sesión, tu token de OAuth puede haber expirado.

Ejecuta `/login` para re-autenticarte. Si esto ocurre frecuentemente, verifica que tu reloj del sistema sea preciso, ya que la validación de tokens depende de marcas de tiempo correctas.

## Ubicaciones de archivos de configuración

Claude Code almacena la configuración en varias ubicaciones:

| Archivo                       | Propósito                                                                                                                              |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| `~/.claude/settings.json`     | Configuración de usuario (permisos, hooks, anulaciones de modelo)                                                                      |
| `.claude/settings.json`       | Configuración de proyecto (registrada en control de fuente)                                                                            |
| `.claude/settings.local.json` | Configuración de proyecto local (no confirmada)                                                                                        |
| `~/.claude.json`              | Estado global (tema, OAuth, servidores MCP)                                                                                            |
| `.mcp.json`                   | Servidores MCP de proyecto (registrados en control de fuente)                                                                          |
| `managed-mcp.json`            | [Servidores MCP administrados](/es/mcp#managed-mcp-configuration)                                                                      |
| Configuración administrada    | [Configuración administrada](/es/settings#settings-files) (administrada por servidor, políticas MDM/nivel de SO, o basada en archivos) |

En Windows, `~` se refiere a tu directorio de inicio de usuario, como `C:\Users\TuNombre`.

Para detalles sobre la configuración de estos archivos, consulta [Configuración](/es/settings) y [MCP](/es/mcp).

### Restablecimiento de configuración

Para restablecer Claude Code a la configuración predeterminada, puedes eliminar los archivos de configuración:

```bash theme={null}
# Restablece toda la configuración de usuario y estado
rm ~/.claude.json
rm -rf ~/.claude/

# Restablece la configuración específica del proyecto
rm -rf .claude/
rm .mcp.json
```

<Warning>
  Esto eliminará toda tu configuración, configuraciones de servidores MCP, e historial de sesiones.
</Warning>

## Rendimiento y estabilidad

Estas secciones cubren problemas relacionados con el uso de recursos, capacidad de respuesta, y comportamiento de búsqueda.

### Alto uso de CPU o memoria

Claude Code está diseñado para funcionar con la mayoría de entornos de desarrollo, pero puede consumir recursos significativos al procesar bases de código grandes. Si estás experimentando problemas de rendimiento:

1. Usa `/compact` regularmente para reducir el tamaño del contexto
2. Cierra y reinicia Claude Code entre tareas principales
3. Considera añadir directorios de compilación grandes a tu archivo `.gitignore`

### El comando se cuelga o congela

Si Claude Code parece no responder:

1. Presiona Ctrl+C para intentar cancelar la operación actual
2. Si no responde, es posible que necesites cerrar la terminal y reiniciar

### Problemas de búsqueda y descubrimiento

Si la herramienta Search, menciones `@file`, agentes personalizados, y skills personalizados no funcionan, instala el sistema `ripgrep`:

```bash theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Luego establece `USE_BUILTIN_RIPGREP=0` en tu [entorno](/es/env-vars).

### Resultados de búsqueda lentos o incompletos en WSL

Las penalizaciones de rendimiento de lectura de disco al [trabajar entre sistemas de archivos en WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) pueden resultar en menos coincidencias de las esperadas al usar Claude Code en WSL. La búsqueda aún funciona, pero devuelve menos resultados que en un sistema de archivos nativo.

<Note>
  `/doctor` mostrará Search como OK en este caso.
</Note>

**Soluciones:**

1. **Envía búsquedas más específicas**: reduce el número de archivos buscados especificando directorios o tipos de archivo: "Search for JWT validation logic in the auth-service package" o "Find use of md5 hash in JS files".

2. **Mueve el proyecto al sistema de archivos de Linux**: si es posible, asegúrate de que tu proyecto esté ubicado en el sistema de archivos de Linux (`/home/`) en lugar del sistema de archivos de Windows (`/mnt/c/`).

3. **Usa Windows nativo en su lugar**: considera ejecutar Claude Code nativamente en Windows en lugar de a través de WSL, para mejor rendimiento del sistema de archivos.

## Problemas de integración de IDE

Si Claude Code no se conecta a tu IDE o se comporta inesperadamente dentro de una terminal de IDE, intenta las soluciones a continuación.

### IDE de JetBrains no detectado en WSL2

Si estás usando Claude Code en WSL2 con IDEs de JetBrains y obteniendo errores "No available IDEs detected", esto es probablemente debido a la configuración de red de WSL2 o Windows Firewall bloqueando la conexión.

#### Modos de red de WSL2

WSL2 usa red NAT por defecto, lo que puede prevenir la detección de IDE. Tienes dos opciones:

**Opción 1: Configura Windows Firewall** (recomendado)

1. Encuentra tu dirección IP de WSL2:
   ```bash theme={null}
   wsl hostname -I
   # Salida de ejemplo: 172.21.123.45
   ```

2. Abre PowerShell como Administrador y crea una regla de firewall:
   ```powershell theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   Ajusta el rango de IP basado en tu subred de WSL2 del paso 1.

3. Reinicia tanto tu IDE como Claude Code

**Opción 2: Cambia a red reflejada**

Añade a `.wslconfig` en tu directorio de usuario de Windows:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Luego reinicia WSL con `wsl --shutdown` desde PowerShell.

<Note>
  Estos problemas de red solo afectan a WSL2. WSL1 usa la red del host directamente y no requiere estas configuraciones.
</Note>

Para consejos de configuración adicionales de JetBrains, consulta la [guía de IDE de JetBrains](/es/jetbrains#plugin-settings).

### Reporta problemas de integración de IDE en Windows

Si estás experimentando problemas de integración de IDE en Windows, [crea un problema](https://github.com/anthropics/claude-code/issues) con la siguiente información:

* Tipo de entorno: Windows nativo (Git Bash) o WSL1/WSL2
* Modo de red de WSL, si aplica: NAT o reflejado
* Nombre y versión del IDE
* Versión de extensión/plugin de Claude Code
* Tipo de shell: Bash, Zsh, PowerShell, etc.

### La tecla Escape no funciona en terminales de IDE de JetBrains

Si estás usando Claude Code en terminales de JetBrains y la tecla `Esc` no interrumpe el agente como se espera, esto es probablemente debido a un choque de atajos de teclado con los atajos de teclado predeterminados de JetBrains.

Para corregir este problema:

1. Ve a Settings → Tools → Terminal
2. Cualquiera de:
   * Desmarca "Move focus to the editor with Escape", o
   * Haz clic en "Configure terminal keybindings" y elimina el atajo "Switch focus to Editor"
3. Aplica los cambios

Esto permite que la tecla `Esc` interrumpa correctamente las operaciones de Claude Code.

## Problemas de formato de Markdown

Claude Code a veces genera archivos markdown con etiquetas de lenguaje faltantes en cercas de código, lo que puede afectar el resaltado de sintaxis y la legibilidad en GitHub, editores, y herramientas de documentación.

### Etiquetas de lenguaje faltantes en bloques de código

Si notas bloques de código como este en markdown generado:

````markdown theme={null}
```
function example() {
  return "hello";
}
```text
````

En lugar de bloques correctamente etiquetados como:

````markdown theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**Soluciones:**

1. **Pide a Claude que añada etiquetas de lenguaje**: solicita "Add appropriate language tags to all code blocks in this markdown file."

2. **Usa hooks de post-procesamiento**: configura hooks de formato automático para detectar y añadir etiquetas de lenguaje faltantes. Consulta [Auto-format code after edits](/es/hooks-guide#auto-format-code-after-edits) para un ejemplo de un hook de formato PostToolUse.

3. **Verificación manual**: después de generar archivos markdown, revísalos para el formato correcto de bloques de código y solicita correcciones si es necesario.

### Espaciado e formato inconsistentes

Si el markdown generado tiene líneas en blanco excesivas o espaciado inconsistente:

**Soluciones:**

1. **Solicita correcciones de formato**: pide a Claude que "Fix spacing and formatting issues in this markdown file."

2. **Usa herramientas de formato**: configura hooks para ejecutar formateadores de markdown como `prettier` o scripts de formato personalizados en archivos markdown generados.

3. **Especifica preferencias de formato**: incluye requisitos de formato en tus solicitudes o archivos de [memoria](/es/memory) del proyecto.

### Reduce problemas de formato de markdown

Para minimizar problemas de formato:

* **Sé explícito en solicitudes**: pide "properly formatted markdown with language-tagged code blocks"
* **Usa convenciones de proyecto**: documenta tu estilo de markdown preferido en [`CLAUDE.md`](/es/memory)
* **Configura hooks de validación**: usa hooks de post-procesamiento para verificar y corregir automáticamente problemas comunes de formato

## Obtén más ayuda

Si estás experimentando problemas no cubiertos aquí:

1. Usa el comando `/bug` dentro de Claude Code para reportar problemas directamente a Anthropic
2. Verifica el [repositorio de GitHub](https://github.com/anthropics/claude-code) para problemas conocidos
3. Ejecuta `/doctor` para diagnosticar problemas. Verifica:
   * Tipo de instalación, versión, y funcionalidad de búsqueda
   * Estado de actualización automática y versiones disponibles
   * Archivos de configuración inválidos (JSON malformado, tipos incorrectos)
   * Errores de configuración de servidores MCP
   * Problemas de configuración de atajos de teclado
   * Advertencias de uso de contexto (archivos CLAUDE.md grandes, alto uso de tokens de MCP, reglas de permisos inalcanzables)
   * Errores de carga de plugins y agentes
4. Pregunta a Claude directamente sobre sus capacidades y características - Claude tiene acceso integrado a su documentación
