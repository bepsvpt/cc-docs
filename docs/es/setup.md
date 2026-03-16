> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurar Claude Code

> Instale, autentíquese e inicie el uso de Claude Code en su máquina de desarrollo.

## Requisitos del sistema

* **Sistema operativo**:
  * macOS 13.0+
  * Windows 10 1809+ o Windows Server 2019+ ([consulte las notas de configuración](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([dependencias adicionales requeridas](#platform-specific-setup))
* **Hardware**: 4 GB+ de RAM
* **Red**: Se requiere conexión a Internet (consulte [configuración de red](/es/network-config#network-access-requirements))
* **Shell**: Funciona mejor en Bash o Zsh
* **Ubicación**: [Países compatibles con Anthropic](https://www.anthropic.com/supported-countries)

### Dependencias adicionales

* **ripgrep**: Generalmente incluido con Claude Code. Si la búsqueda falla, consulte [solución de problemas de búsqueda](/es/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)**: Solo se requiere para [instalación npm obsoleta](#npm-installation-deprecated)

## Instalación

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

Después de que se complete el proceso de instalación, navegue a su proyecto e inicie Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Si encuentra algún problema durante la instalación, consulte la [guía de solución de problemas](/es/troubleshooting).

<Tip>
  Ejecute `claude doctor` después de la instalación para verificar su tipo de instalación y versión.
</Tip>

### Configuración específica de la plataforma

**Windows**: Ejecute Claude Code de forma nativa (requiere [Git Bash](https://git-scm.com/downloads/win)) o dentro de WSL. Se admiten tanto WSL 1 como WSL 2, pero WSL 1 tiene soporte limitado y no admite características como el sandboxing de herramientas Bash.

**Alpine Linux y otras distribuciones basadas en musl/uClibc**:

El instalador nativo en Alpine y otras distribuciones basadas en musl/uClibc requiere `libgcc`, `libstdc++` y `ripgrep`. Instale estos usando el gestor de paquetes de su distribución, luego establezca `USE_BUILTIN_RIPGREP=0`.

En Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Autenticación

#### Para individuos

1. **Plan Claude Pro o Max** (recomendado): Suscríbase al [plan Pro o Max](https://claude.ai/pricing) de Claude para obtener una suscripción unificada que incluya tanto Claude Code como Claude en la web. Administre su cuenta en un solo lugar e inicie sesión con su cuenta de Claude.ai.
2. **Claude Console**: Conéctese a través de [Claude Console](https://console.anthropic.com) y complete el proceso de OAuth. Requiere facturación activa en la Consola de Anthropic. Se crea automáticamente un espacio de trabajo "Claude Code" para el seguimiento de uso y la gestión de costos. No puede crear claves de API para el espacio de trabajo de Claude Code; está dedicado exclusivamente al uso de Claude Code.

#### Para equipos y organizaciones

1. **Claude for Teams o Enterprise** (recomendado): Suscríbase a [Claude for Teams](https://claude.com/pricing#team-&-enterprise) o [Claude for Enterprise](https://anthropic.com/contact-sales) para facturación centralizada, gestión de equipos y acceso tanto a Claude Code como a Claude en la web. Los miembros del equipo inician sesión con sus cuentas de Claude.ai.
2. **Claude Console con facturación de equipo**: Configure una organización compartida de [Claude Console](https://console.anthropic.com) con facturación de equipo. Invite a los miembros del equipo y asigne roles para el seguimiento de uso.
3. **Proveedores de nube**: Configure Claude Code para usar [Amazon Bedrock, Google Vertex AI o Microsoft Foundry](/es/third-party-integrations) para implementaciones con su infraestructura de nube existente.

### Instalar una versión específica

El instalador nativo acepta un número de versión específico o un canal de lanzamiento (`latest` o `stable`). El canal que elija en el momento de la instalación se convierte en su predeterminado para actualizaciones automáticas. Consulte [Configurar canal de lanzamiento](#configure-release-channel) para obtener más información.

Para instalar la versión más reciente (predeterminada):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Para instalar la versión estable:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Para instalar un número de versión específico:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Integridad binaria y firma de código

* Los checksums SHA256 para todas las plataformas se publican en los manifiestos de lanzamiento, actualmente ubicados en `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (ejemplo: reemplace `{VERSION}` con `2.0.30`)
* Los binarios firmados se distribuyen para las siguientes plataformas:
  * macOS: Firmado por "Anthropic PBC" y notarizado por Apple
  * Windows: Firmado por "Anthropic, PBC"

## Instalación NPM (obsoleta)

La instalación de NPM está obsoleta. Use el método de [instalación nativa](#installation) cuando sea posible. Para migrar una instalación npm existente a nativa, ejecute `claude install`.

**Instalación global de npm**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NO use `sudo npm install -g` ya que esto puede causar problemas de permisos y riesgos de seguridad.
  Si encuentra errores de permisos, consulte [solución de problemas de permisos](/es/troubleshooting#command-not-found-claude-or-permission-errors) para obtener soluciones recomendadas.
</Warning>

## Configuración de Windows

**Opción 1: Claude Code dentro de WSL**

* Se admiten tanto WSL 1 como WSL 2
* WSL 2 admite [sandboxing](/es/sandboxing) para mayor seguridad. WSL 1 no admite sandboxing.

**Opción 2: Claude Code en Windows nativo con Git Bash**

* Requiere [Git para Windows](https://git-scm.com/downloads/win)
* Para instalaciones portátiles de Git, especifique la ruta a su `bash.exe`:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Actualizar Claude Code

### Actualizaciones automáticas

Claude Code se mantiene automáticamente actualizado para asegurar que tenga las características más recientes y correcciones de seguridad.

* **Comprobaciones de actualización**: Se realizan al inicio y periódicamente mientras se ejecuta
* **Proceso de actualización**: Descarga e instala automáticamente en segundo plano
* **Notificaciones**: Verá una notificación cuando se instalen las actualizaciones
* **Aplicar actualizaciones**: Las actualizaciones surten efecto la próxima vez que inicie Claude Code

<Note>
  Las instalaciones de Homebrew y WinGet no se actualizan automáticamente. Use `brew upgrade claude-code` o `winget upgrade Anthropic.ClaudeCode` para actualizar manualmente.

  **Problema conocido:** Claude Code puede notificarle sobre actualizaciones antes de que la nueva versión esté disponible en estos gestores de paquetes. Si una actualización falla, espere e intente más tarde.
</Note>

### Configurar canal de lanzamiento

Configure qué canal de lanzamiento sigue Claude Code tanto para actualizaciones automáticas como para `claude update` con la configuración `autoUpdatesChannel`:

* `"latest"` (predeterminado): Reciba nuevas características tan pronto como se lancen
* `"stable"`: Use una versión que típicamente tiene aproximadamente una semana de antigüedad, omitiendo lanzamientos con regresiones importantes

Configure esto a través de `/config` → **Auto-update channel**, o agréguelo a su [archivo settings.json](/es/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Para implementaciones empresariales, puede aplicar un canal de lanzamiento consistente en toda su organización usando [configuraciones administradas](/es/settings#settings-files).

### Deshabilitar actualizaciones automáticas

Establezca la variable de entorno `DISABLE_AUTOUPDATER` en su shell o [archivo settings.json](/es/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Actualizar manualmente

```bash  theme={null}
claude update
```

## Desinstalar Claude Code

Si necesita desinstalar Claude Code, siga las instrucciones para su método de instalación.

### Instalación nativa

Elimine el binario de Claude Code y los archivos de versión:

**macOS, Linux, WSL:**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell:**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD:**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Instalación de Homebrew

```bash  theme={null}
brew uninstall --cask claude-code
```

### Instalación de WinGet

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Instalación de NPM

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Limpiar archivos de configuración (opcional)

<Warning>
  Eliminar archivos de configuración eliminará toda su configuración, herramientas permitidas, configuraciones del servidor MCP e historial de sesiones.
</Warning>

Para eliminar la configuración y datos en caché de Claude Code:

**macOS, Linux, WSL:**

```bash  theme={null}
# Eliminar configuración de usuario y estado
rm -rf ~/.claude
rm ~/.claude.json

# Eliminar configuración específica del proyecto (ejecute desde su directorio de proyecto)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# Eliminar configuración de usuario y estado
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Eliminar configuración específica del proyecto (ejecute desde su directorio de proyecto)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM Eliminar configuración de usuario y estado
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Eliminar configuración específica del proyecto (ejecute desde su directorio de proyecto)
rmdir /s /q ".claude"
del ".mcp.json"
```
