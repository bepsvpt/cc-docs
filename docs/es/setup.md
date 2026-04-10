> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

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
* **Hardware**: 4 GB+ de RAM
* **Red**: se requiere conexión a Internet. Consulte [configuración de red](/es/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell o CMD. En Windows, se requiere [Git for Windows](https://git-scm.com/downloads/win).
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

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
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

Después de que se complete la instalación, abra una terminal en el proyecto en el que desea trabajar e inicie Claude Code:

```bash  theme={null}
claude
```

Si encuentra algún problema durante la instalación, consulte la [guía de solución de problemas](/es/troubleshooting).

### Configurar en Windows

Claude Code en Windows requiere [Git for Windows](https://git-scm.com/downloads/win) o WSL. Puede iniciar `claude` desde PowerShell, CMD o Git Bash. Claude Code utiliza Git Bash internamente para ejecutar comandos. No necesita ejecutar PowerShell como Administrador.

**Opción 1: Windows nativo con Git Bash**

Instale [Git for Windows](https://git-scm.com/downloads/win) y luego ejecute el comando de instalación desde PowerShell o CMD.

Si Claude Code no puede encontrar su instalación de Git Bash, establezca la ruta en su [archivo settings.json](/es/settings):

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code también puede ejecutar PowerShell de forma nativa en Windows como una vista previa de participación. Consulte [herramienta PowerShell](/es/tools-reference#powershell-tool) para configuración y limitaciones.

**Opción 2: WSL**

Se admiten tanto WSL 1 como WSL 2. WSL 2 admite [sandboxing](/es/sandboxing) para mayor seguridad. WSL 1 no admite sandboxing.

### Alpine Linux y distribuciones basadas en musl

El instalador nativo en Alpine y otras distribuciones basadas en musl/uClibc requiere `libgcc`, `libstdc++` y `ripgrep`. Instale estos usando el gestor de paquetes de su distribución y luego establezca `USE_BUILTIN_RIPGREP=0`.

Este ejemplo instala los paquetes requeridos en Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

Luego establezca `USE_BUILTIN_RIPGREP` en `0` en su archivo [`settings.json`](/es/settings#available-settings):

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Verificar su instalación

Después de instalar, confirme que Claude Code está funcionando:

```bash  theme={null}
claude --version
```

Para una verificación más detallada de su instalación y configuración, ejecute [`claude doctor`](/es/troubleshooting#get-more-help):

```bash  theme={null}
claude doctor
```

## Autenticar

Claude Code requiere una cuenta Pro, Max, Team, Enterprise o Console. El plan gratuito de Claude.ai no incluye acceso a Claude Code. También puede usar Claude Code con un proveedor de API de terceros como [Amazon Bedrock](/es/amazon-bedrock), [Google Vertex AI](/es/google-vertex-ai) o [Microsoft Foundry](/es/microsoft-foundry).

Después de instalar, inicie sesión ejecutando `claude` y siguiendo las indicaciones del navegador. Consulte [Autenticación](/es/authentication) para todos los tipos de cuenta y opciones de configuración de equipo.

## Actualizar Claude Code

Las instalaciones nativas se actualizan automáticamente en segundo plano. Puede [configurar el canal de lanzamiento](#configure-release-channel) para controlar si recibe actualizaciones inmediatamente o en un cronograma estable retrasado, o [deshabilitar las actualizaciones automáticas](#disable-auto-updates) completamente. Las instalaciones de Homebrew y WinGet requieren actualizaciones manuales.

### Actualizaciones automáticas

Claude Code busca actualizaciones al iniciar y periódicamente mientras se ejecuta. Las actualizaciones se descargan e instalan en segundo plano y luego surten efecto la próxima vez que inicie Claude Code.

<Note>
  Las instalaciones de Homebrew y WinGet no se actualizan automáticamente. Use `brew upgrade claude-code` o `winget upgrade Anthropic.ClaudeCode` para actualizar manualmente.

  **Problema conocido:** Claude Code puede notificarle sobre actualizaciones antes de que la nueva versión esté disponible en estos gestores de paquetes. Si una actualización falla, espere e intente más tarde.

  Homebrew mantiene versiones antiguas en el disco después de las actualizaciones. Ejecute `brew cleanup claude-code` periódicamente para recuperar espacio en disco.
</Note>

### Configurar canal de lanzamiento

Controle qué canal de lanzamiento sigue Claude Code para actualizaciones automáticas y `claude update` con la configuración `autoUpdatesChannel`:

* `"latest"`, el predeterminado: reciba nuevas características tan pronto como se lancen
* `"stable"`: use una versión que típicamente tiene aproximadamente una semana de antigüedad, omitiendo lanzamientos con regresiones importantes

Configure esto a través de `/config` → **Auto-update channel**, o agréguelo a su [archivo settings.json](/es/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Para implementaciones empresariales, puede aplicar un canal de lanzamiento consistente en toda su organización usando [configuración administrada](/es/permissions#managed-settings).

### Deshabilitar actualizaciones automáticas

Establezca `DISABLE_AUTOUPDATER` en `"1"` en la clave `env` de su archivo [`settings.json`](/es/settings#available-settings):

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Actualizar manualmente

Para aplicar una actualización inmediatamente sin esperar la próxima verificación en segundo plano, ejecute:

```bash  theme={null}
claude update
```

## Opciones de instalación avanzadas

Estas opciones son para fijación de versiones, migración desde npm y verificación de integridad binaria.

### Instalar una versión específica

El instalador nativo acepta un número de versión específico o un canal de lanzamiento (`latest` o `stable`). El canal que elija en el momento de la instalación se convierte en su predeterminado para actualizaciones automáticas. Consulte [configurar canal de lanzamiento](#configure-release-channel) para más información.

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
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Instalación npm obsoleta

La instalación con npm está obsoleta. El instalador nativo es más rápido, no requiere dependencias y se actualiza automáticamente en segundo plano. Use el método de [instalación nativa](#install-claude-code) cuando sea posible.

#### Migrar de npm a nativo

Si instaló previamente Claude Code con npm, cambie al instalador nativo:

```bash  theme={null}
# Instalar el binario nativo
curl -fsSL https://claude.ai/install.sh | bash

# Eliminar la instalación anterior de npm
npm uninstall -g @anthropic-ai/claude-code
```

También puede ejecutar `claude install` desde una instalación npm existente para instalar el binario nativo junto a ella y luego eliminar la versión npm.

#### Instalar con npm

Si necesita instalación con npm por razones de compatibilidad, debe tener [Node.js 18+](https://nodejs.org/en/download) instalado. Instale el paquete globalmente:

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NO use `sudo npm install -g` ya que esto puede causar problemas de permisos y riesgos de seguridad. Si encuentra errores de permisos, consulte [solución de problemas de errores de permisos](/es/troubleshooting#permission-errors-during-installation).
</Warning>

### Integridad binaria y firma de código

Cada lanzamiento publica un `manifest.json` que contiene sumas de verificación SHA256 para cada binario de plataforma. El manifiesto está firmado con una clave GPG de Anthropic, por lo que verificar la firma en el manifiesto verifica transitivamente cada binario que enumera.

#### Verificar la firma del manifiesto

Los pasos 1-3 requieren un shell POSIX con `gpg` y `curl`. En Windows, ejecútelos en Git Bash o WSL. El paso 4 incluye una opción de PowerShell.

<Steps>
  <Step title="Descargar e importar la clave pública">
    La clave de firma de lanzamiento se publica en una URL fija.

    ```bash  theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Muestre la huella digital de la clave importada.

    ```bash  theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Confirme que la salida incluye esta huella digital:

    ```text  theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Descargar el manifiesto y la firma">
    Establezca `VERSION` en el lanzamiento que desea verificar.

    ```bash  theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Verificar la firma">
    Verifique la firma separada contra el manifiesto.

    ```bash  theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    Un resultado válido reporta `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` también imprime `WARNING: This key is not certified with a trusted signature!` para cualquier clave recién importada. Esto es esperado. La línea `Good signature` confirma que la verificación criptográfica pasó. La comparación de huella digital en el Paso 1 confirma que la clave en sí es auténtica.
  </Step>

  <Step title="Verificar el binario contra el manifiesto">
    Compare la suma de verificación SHA256 de su binario descargado con el valor listado bajo `platforms.<platform>.checksum` en `manifest.json`.

    <Tabs>
      <Tab title="Linux">
        ```bash  theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash  theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell  theme={null}
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
* **Linux**: use la firma de manifiesto anterior para verificar la integridad. Los binarios de Linux no están firmados individualmente con código.

## Desinstalar Claude Code

Para eliminar Claude Code, siga las instrucciones para su método de instalación.

### Instalación nativa

Elimine el binario de Claude Code y los archivos de versión:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Instalación de Homebrew

Elimine el cask de Homebrew:

```bash  theme={null}
brew uninstall --cask claude-code
```

### Instalación de WinGet

Elimine el paquete de WinGet:

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Elimine el paquete npm global:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Eliminar archivos de configuración

<Warning>
  Eliminar archivos de configuración eliminará toda su configuración, herramientas permitidas, configuraciones de servidor MCP e historial de sesiones.
</Warning>

Para eliminar la configuración y datos en caché de Claude Code:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # Eliminar configuración de usuario y estado
    rm -rf ~/.claude
    rm ~/.claude.json

    # Eliminar configuración específica del proyecto (ejecutar desde su directorio de proyecto)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # Eliminar configuración de usuario y estado
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Eliminar configuración específica del proyecto (ejecutar desde su directorio de proyecto)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
