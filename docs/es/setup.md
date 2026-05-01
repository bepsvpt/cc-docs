> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuración avanzada

> Requisitos del sistema, instalación específica de plataforma, gestión de versiones y desinstalación para Claude Code.

Esta página cubre requisitos del sistema, detalles de instalación específicos de plataforma, actualizaciones y desinstalación. Para un recorrido guiado de su primera sesión, consulte el [inicio rápido](/es/quickstart). Si nunca ha utilizado una terminal antes, consulte la [guía de terminal](/es/terminal-guide).

## Requisitos del sistema

Claude Code se ejecuta en las siguientes plataformas y configuraciones:

* **Sistema operativo**:
  * macOS 13.0+
  * Windows 10 1809+ o Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Hardware**: 4 GB+ de RAM, procesador x64 o ARM64
* **Red**: se requiere conexión a Internet. Consulte [configuración de red](/es/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell o CMD. En Windows nativo, se recomienda [Git for Windows](https://git-scm.com/downloads/win); Claude Code recurre a PowerShell cuando Git Bash no está presente. Las configuraciones de WSL no requieren Git for Windows.
* **Ubicación**: [países compatibles con Anthropic](https://www.anthropic.com/supported-countries)

### Dependencias adicionales

* **ripgrep**: generalmente incluido con Claude Code. Si la búsqueda falla, consulte [solución de problemas de búsqueda](/es/troubleshooting#search-and-discovery-issues).

## Instalar Claude Code

<Tip>
  ¿Prefiere una interfaz gráfica? La [aplicación de escritorio](/es/desktop-quickstart) le permite usar Claude Code sin la terminal. Descárguela para [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) o [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs).

  ¿Nuevo en la terminal? Consulte la [guía de terminal](/es/terminal-guide) para obtener instrucciones paso a paso.
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

    [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

You can also install with [apt, dnf, or apk](/en/setup#install-with-linux-package-managers) on Debian, Fedora, RHEL, and Alpine.

Después de que se complete la instalación, abra una terminal en el proyecto en el que desea trabajar e inicie Claude Code:

```bash theme={null}
claude
```

Si encuentra algún problema durante la instalación, consulte [Solucionar problemas de instalación e inicio de sesión](/es/troubleshoot-install).

### Configurar en Windows

Puede ejecutar Claude Code de forma nativa en Windows o dentro de WSL. Elija según dónde se encuentren sus proyectos y qué características necesite:

| Opción         | Requiere                                                                                                      | [Sandboxing](/es/sandboxing) | Cuándo usar                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------- |
| Windows nativo | [Git for Windows](https://git-scm.com/downloads/win) recomendado; PowerShell se utiliza si no está disponible | No compatible                | Proyectos y herramientas nativas de Windows                         |
| WSL 2          | WSL 2 habilitado                                                                                              | Compatible                   | Cadenas de herramientas de Linux o ejecución de comandos en sandbox |
| WSL 1          | WSL 1 habilitado                                                                                              | No compatible                | Si WSL 2 no está disponible                                         |

**Opción 1: Windows nativo con Git Bash**

Instale [Git for Windows](https://git-scm.com/downloads/win) y luego ejecute el comando de instalación desde PowerShell o CMD. No necesita ejecutar como Administrador.

Ya sea que instale desde PowerShell o CMD solo afecta qué comando de instalación ejecuta. Su indicador muestra `PS C:\Users\YourName>` en PowerShell y `C:\Users\YourName>` sin el `PS` en CMD. Si es nuevo en la terminal, la [guía de terminal](/es/terminal-guide#windows) le guía a través de cada paso.

Después de la instalación, inicie `claude` desde PowerShell, CMD o Git Bash. Cuando Git Bash está instalado, Claude Code lo utiliza internamente para ejecutar comandos independientemente de dónde lo inicie. Si Claude Code no puede encontrar su instalación de Git Bash, establezca la ruta en su [archivo settings.json](/es/settings):

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code también puede ejecutar PowerShell de forma nativa en Windows. Cuando Git Bash está instalado, la herramienta PowerShell se está implementando progresivamente como una opción adicional: establezca `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` para participar o `0` para no participar. Consulte [herramienta PowerShell](/es/tools-reference#powershell-tool) para configuración y limitaciones.

**Opción 2: WSL**

Abra su distribución de WSL y ejecute el instalador de Linux desde las [instrucciones de instalación](#install-claude-code) anteriores. Instala e inicia `claude` dentro del terminal de WSL, no desde PowerShell o CMD.

### Alpine Linux y distribuciones basadas en musl

El instalador nativo en Alpine y otras distribuciones basadas en musl/uClibc requiere `libgcc`, `libstdc++` y `ripgrep`. Instale estos usando el gestor de paquetes de su distribución y luego establezca `USE_BUILTIN_RIPGREP=0`.

Este ejemplo instala los paquetes requeridos en Alpine:

```bash theme={null}
apk add libgcc libstdc++ ripgrep
```

Luego establezca `USE_BUILTIN_RIPGREP` en `0` en su archivo [`settings.json`](/es/settings#available-settings):

```json theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Verificar su instalación

Después de instalar, confirme que Claude Code está funcionando:

```bash theme={null}
claude --version
```

Si esto falla con `command not found` u otro error, consulte [Solucionar problemas de instalación e inicio de sesión](/es/troubleshoot-install).

Para una verificación más detallada de su instalación y configuración, ejecute [`claude doctor`](/es/troubleshooting#get-more-help):

```bash theme={null}
claude doctor
```

## Autenticar

Claude Code requiere una cuenta Pro, Max, Team, Enterprise o Console. El plan gratuito de Claude.ai no incluye acceso a Claude Code. También puede usar Claude Code con un proveedor de API de terceros como [Amazon Bedrock](/es/amazon-bedrock), [Google Vertex AI](/es/google-vertex-ai) o [Microsoft Foundry](/es/microsoft-foundry).

Después de instalar, inicie sesión ejecutando `claude` y siguiendo las indicaciones del navegador. Consulte [Autenticación](/es/authentication) para todos los tipos de cuenta y opciones de configuración de equipo.

## Actualizar Claude Code

Las instalaciones nativas se actualizan automáticamente en segundo plano. Puede [configurar el canal de lanzamiento](#configure-release-channel) para controlar si recibe actualizaciones inmediatamente o en un cronograma estable retrasado, o [deshabilitar las actualizaciones automáticas](#disable-auto-updates) completamente. Las instalaciones de Homebrew, WinGet y [gestor de paquetes de Linux](#install-with-linux-package-managers) requieren actualizaciones manuales.

### Actualizaciones automáticas

Claude Code busca actualizaciones al iniciar y periódicamente mientras se ejecuta. Las actualizaciones se descargan e instalan en segundo plano y luego surten efecto la próxima vez que inicie Claude Code.

<Note>
  Las instalaciones de Homebrew, WinGet, apt, dnf y apk no se actualizan automáticamente. Para Homebrew, ejecute `brew upgrade claude-code` o `brew upgrade claude-code@latest`, dependiendo de qué cask instaló. Para WinGet, ejecute `winget upgrade Anthropic.ClaudeCode`. Para gestores de paquetes de Linux, consulte los comandos de actualización en [Instalar con gestores de paquetes de Linux](#install-with-linux-package-managers).

  **Problema conocido:** Claude Code puede notificarle sobre actualizaciones antes de que la nueva versión esté disponible en estos gestores de paquetes. Si una actualización falla, espere e intente más tarde.

  Homebrew mantiene versiones antiguas en el disco después de las actualizaciones. Ejecute `brew cleanup` periódicamente para recuperar espacio en disco.
</Note>

### Configurar canal de lanzamiento

Controle qué canal de lanzamiento sigue Claude Code para actualizaciones automáticas y `claude update` con la configuración `autoUpdatesChannel`:

* `"latest"`, el predeterminado: reciba nuevas características tan pronto como se lancen
* `"stable"`: use una versión que típicamente tiene aproximadamente una semana de antigüedad, omitiendo lanzamientos con regresiones importantes

Configure esto a través de `/config` → **Canal de actualización automática**, o agréguelo a su [archivo settings.json](/es/settings):

```json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Para implementaciones empresariales, puede aplicar un canal de lanzamiento consistente en toda su organización usando [configuración administrada](/es/permissions#managed-settings).

Las instalaciones de Homebrew eligen un canal por nombre de cask en lugar de esta configuración: `claude-code` rastrea estable y `claude-code@latest` rastrea latest.

### Fijar una versión mínima

La configuración `minimumVersion` establece un piso. Las actualizaciones automáticas en segundo plano y `claude update` se niegan a instalar cualquier versión por debajo de este valor, por lo que cambiar al canal `"stable"` no lo degrada si ya está en una compilación `"latest"` más nueva.

Cambiar de `"latest"` a `"stable"` a través de `/config` le solicita que permanezca en la versión actual o permita la degradación. Elegir permanecer establece `minimumVersion` en esa versión. Cambiar de nuevo a `"latest"` lo borra.

Agréguelo a su [archivo settings.json](/es/settings) para fijar un piso explícitamente:

```json theme={null}
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

En [configuración administrada](/es/permissions#managed-settings), esto aplica un mínimo en toda la organización que la configuración de usuario y proyecto no puede anular.

### Deshabilitar actualizaciones automáticas

Establezca `DISABLE_AUTOUPDATER` en `"1"` en la clave `env` de su archivo [`settings.json`](/es/settings#available-settings):

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

`DISABLE_AUTOUPDATER` solo detiene la verificación en segundo plano; `claude update` e `claude install` aún funcionan. Para bloquear todas las rutas de actualización, incluidas las actualizaciones manuales, establezca [`DISABLE_UPDATES`](/es/env-vars) en su lugar. Úselo cuando distribuya Claude Code a través de sus propios canales y necesite que los usuarios permanezcan en la versión que proporciona.

### Actualizar manualmente

Para aplicar una actualización inmediatamente sin esperar la próxima verificación en segundo plano, ejecute:

```bash theme={null}
claude update
```

## Opciones de instalación avanzadas

Estas opciones son para fijación de versiones, gestores de paquetes de Linux, npm y verificación de integridad binaria.

### Instalar una versión específica

El instalador nativo acepta un número de versión específico o un canal de lanzamiento (`latest` o `stable`). El canal que elija en el momento de la instalación se convierte en su predeterminado para actualizaciones automáticas. Consulte [configurar canal de lanzamiento](#configure-release-channel) para más información.

Para instalar la versión más reciente (predeterminada):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Para instalar la versión estable:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Para instalar un número de versión específico:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Instalar con gestores de paquetes de Linux

Claude Code publica repositorios apt, dnf y apk firmados. Reemplace `stable` con `latest` para el canal de actualización continua. Las instalaciones del gestor de paquetes no se actualizan automáticamente a través de Claude Code; las actualizaciones llegan a través de su flujo de trabajo de actualización del sistema normal.

Todos los repositorios están firmados con la [clave de firma de lanzamiento de Claude Code](#binary-integrity-and-code-signing). Antes de confiar en la clave, verifíquela como se describe en cada pestaña.

<Tabs>
  <Tab title="apt">
    Para Debian y Ubuntu. Para usar el canal de actualización continua, cambie ambas ocurrencias de `stable` en la línea `deb`: la ruta de URL y el nombre de la suite.

    ```bash theme={null}
    sudo install -d -m 0755 /etc/apt/keyrings
    sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
      -o /etc/apt/keyrings/claude-code.asc
    echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
      | sudo tee /etc/apt/sources.list.d/claude-code.list
    sudo apt update
    sudo apt install claude-code
    ```

    Verifique la huella digital de la clave GPG antes de confiar en ella: `gpg --show-keys /etc/apt/keyrings/claude-code.asc` debe reportar `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`.

    Para actualizar más tarde, ejecute `sudo apt update && sudo apt upgrade claude-code`.
  </Tab>

  <Tab title="dnf">
    Para Fedora y RHEL:

    ```bash theme={null}
    sudo tee /etc/yum.repos.d/claude-code.repo <<'EOF'
    [claude-code]
    name=Claude Code
    baseurl=https://downloads.claude.ai/claude-code/rpm/stable
    enabled=1
    gpgcheck=1
    gpgkey=https://downloads.claude.ai/keys/claude-code.asc
    EOF
    sudo dnf install claude-code
    ```

    dnf descarga la clave en la primera instalación y le solicita que confirme la huella digital. Verifique que coincida con `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE` antes de aceptar.

    Para actualizar más tarde, ejecute `sudo dnf upgrade claude-code`.
  </Tab>

  <Tab title="apk">
    Para Alpine Linux:

    ```sh theme={null}
    wget -O /etc/apk/keys/claude-code.rsa.pub \
      https://downloads.claude.ai/keys/claude-code.rsa.pub
    echo "https://downloads.claude.ai/claude-code/apk/stable" >> /etc/apk/repositories
    apk add claude-code
    ```

    Verifique la clave descargada con `sha256sum /etc/apk/keys/claude-code.rsa.pub`, que debe reportar `395759c1f7449ef4cdef305a42e820f3c766d6090d142634ebdb049f113168b6`.

    Para actualizar más tarde, ejecute `apk update && apk upgrade claude-code`.
  </Tab>
</Tabs>

### Instalar con npm

También puede instalar Claude Code como un paquete npm global. El paquete requiere [Node.js 18 o posterior](https://nodejs.org/en/download).

```bash theme={null}
npm install -g @anthropic-ai/claude-code
```

El paquete npm instala el mismo binario nativo que el instalador independiente. npm extrae el binario a través de una dependencia opcional por plataforma como `@anthropic-ai/claude-code-darwin-arm64`, y un paso postinstall lo vincula en su lugar. El binario `claude` instalado no invoca Node en sí mismo.

Las plataformas de instalación npm compatibles son `darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64` y `win32-arm64`. Su gestor de paquetes debe permitir dependencias opcionales. Consulte [solución de problemas](/es/troubleshoot-install#native-binary-not-found-after-npm-install) si falta el binario después de la instalación.

<Warning>
  NO use `sudo npm install -g` ya que esto puede causar problemas de permisos y riesgos de seguridad. Si encuentra errores de permisos, consulte [solución de problemas de errores de permisos](/es/troubleshoot-install#permission-errors-during-installation).
</Warning>

### Integridad binaria y firma de código

Cada lanzamiento publica un `manifest.json` que contiene sumas de verificación SHA256 para cada binario de plataforma. El manifiesto está firmado con una clave GPG de Anthropic, por lo que verificar la firma en el manifiesto verifica transitivamente cada binario que enumera.

#### Verificar la firma del manifiesto

Los pasos 1-3 requieren un shell POSIX con `gpg` y `curl`. En Windows, ejecútelos en Git Bash o WSL. El paso 4 incluye una opción de PowerShell.

<Steps>
  <Step title="Descargar e importar la clave pública">
    La clave de firma de lanzamiento se publica en una URL fija.

    ```bash theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Muestre la huella digital de la clave importada.

    ```bash theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Confirme que la salida incluye esta huella digital:

    ```text theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Descargar el manifiesto y la firma">
    Establezca `VERSION` en el lanzamiento que desea verificar.

    ```bash theme={null}
    REPO=https://downloads.claude.ai/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Verificar la firma">
    Verifique la firma separada contra el manifiesto.

    ```bash theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    Un resultado válido reporta `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` también imprime `WARNING: This key is not certified with a trusted signature!` para cualquier clave recién importada. Esto es esperado. La línea `Good signature` confirma que la verificación criptográfica pasó. La comparación de huella digital en el Paso 1 confirma que la clave en sí es auténtica.
  </Step>

  <Step title="Verificar el binario contra el manifiesto">
    Compare la suma de verificación SHA256 de su binario descargado con el valor listado bajo `platforms.<platform>.checksum` en `manifest.json`.

    <Tabs>
      <Tab title="Linux">
        ```bash theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  Las firmas de manifiesto están disponibles para lanzamientos desde `2.1.89` en adelante. Los lanzamientos anteriores publican sumas de verificación en `manifest.json` sin una firma separada.
</Note>

#### Firmas de código de plataforma

Además del manifiesto firmado, los binarios individuales llevan firmas de código nativas de plataforma donde se admiten.

* **macOS**: firmado por "Anthropic PBC" y notarizado por Apple. Verifique con `codesign --verify --verbose ./claude`.
* **Windows**: firmado por "Anthropic, PBC". Verifique con `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: los binarios no están firmados individualmente con código. Si descarga directamente del bucket `claude-code-releases` o usa el instalador nativo, verifique la integridad con la firma de manifiesto anterior. Si instala con [apt, dnf o apk](#install-with-linux-package-managers), su gestor de paquetes verifica las firmas automáticamente usando la clave de firma del repositorio.

## Desinstalar Claude Code

Para eliminar Claude Code, siga las instrucciones para su método de instalación.

### Instalación nativa

Elimine el binario de Claude Code y los archivos de versión:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Instalación de Homebrew

Elimine el cask de Homebrew que instaló. Si instaló el cask estable:

```bash theme={null}
brew uninstall --cask claude-code
```

Si instaló el cask latest:

```bash theme={null}
brew uninstall --cask claude-code@latest
```

### Instalación de WinGet

Elimine el paquete de WinGet:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### apt / dnf / apk

Elimine el paquete y la configuración del repositorio:

<Tabs>
  <Tab title="apt">
    ```bash theme={null}
    sudo apt remove claude-code
    sudo rm /etc/apt/sources.list.d/claude-code.list /etc/apt/keyrings/claude-code.asc
    ```
  </Tab>

  <Tab title="dnf">
    ```bash theme={null}
    sudo dnf remove claude-code
    sudo rm /etc/yum.repos.d/claude-code.repo
    ```
  </Tab>

  <Tab title="apk">
    ```sh theme={null}
    apk del claude-code
    sed -i '\|downloads.claude.ai/claude-code/apk|d' /etc/apk/repositories
    rm /etc/apk/keys/claude-code.rsa.pub
    ```
  </Tab>
</Tabs>

### npm

Elimine el paquete npm global:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Eliminar archivos de configuración

<Warning>
  Eliminar archivos de configuración eliminará toda su configuración, herramientas permitidas, configuraciones de servidor MCP e historial de sesiones.
</Warning>

La extensión de VS Code, el plugin de JetBrains y la aplicación de escritorio también escriben en `~/.claude/`. Si alguno de ellos aún está instalado, el directorio se recrea la próxima vez que se ejecuta. Para eliminar Claude Code completamente, desinstale la [extensión de VS Code](/es/vs-code#uninstall-the-extension), el plugin de JetBrains y la aplicación de escritorio antes de eliminar estos archivos.

Para eliminar la configuración y datos en caché de Claude Code:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    # Eliminar configuración de usuario y estado
    rm -rf ~/.claude
    rm ~/.claude.json

    # Eliminar configuración específica del proyecto (ejecutar desde su directorio de proyecto)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    # Eliminar configuración de usuario y estado
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Eliminar configuración específica del proyecto (ejecutar desde su directorio de proyecto)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
