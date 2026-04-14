> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code en Microsoft Foundry

> Aprende a configurar Claude Code a través de Microsoft Foundry, incluyendo configuración, instalación y solución de problemas.

## Requisitos previos

Antes de configurar Claude Code con Microsoft Foundry, asegúrate de que tienes:

* Una suscripción de Azure con acceso a Microsoft Foundry
* Permisos RBAC para crear recursos e implementaciones de Microsoft Foundry
* Azure CLI instalado y configurado (opcional - solo necesario si no tienes otro mecanismo para obtener credenciales)

## Configuración

### 1. Aprovisionar recurso de Microsoft Foundry

Primero, crea un recurso de Claude en Azure:

1. Navega al [portal de Microsoft Foundry](https://ai.azure.com/)
2. Crea un nuevo recurso, anotando el nombre de tu recurso
3. Crea implementaciones para los modelos de Claude:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Configurar credenciales de Azure

Claude Code admite dos métodos de autenticación para Microsoft Foundry. Elige el método que mejor se ajuste a tus requisitos de seguridad.

**Opción A: Autenticación por clave API**

1. Navega a tu recurso en el portal de Microsoft Foundry
2. Ve a la sección **Endpoints and keys** (Puntos finales y claves)
3. Copia **API Key** (Clave API)
4. Establece la variable de entorno:

```bash  theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Opción B: Autenticación de Microsoft Entra ID**

Cuando `ANTHROPIC_FOUNDRY_API_KEY` no está configurado, Claude Code utiliza automáticamente la [cadena de credenciales predeterminada](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview) del SDK de Azure.
Esto admite una variedad de métodos para autenticar cargas de trabajo locales y remotas.

En entornos locales, comúnmente puedes usar Azure CLI:

```bash  theme={null}
az login
```

<Note>
  Cuando se usa Microsoft Foundry, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de credenciales de Azure.
</Note>

### 3. Configurar Claude Code

Establece las siguientes variables de entorno para habilitar Microsoft Foundry. Ten en cuenta que los nombres de tus implementaciones se establecen como identificadores de modelo en Claude Code (puede ser opcional si usas nombres de implementación sugeridos).

```bash  theme={null}
# Enable Microsoft Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# Set models to your resource's deployment names
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'
```

Para más detalles sobre las opciones de configuración de modelos, consulta [Configuración de modelos](/es/model-config).

## Configuración de RBAC de Azure

Los roles predeterminados `Azure AI User` y `Cognitive Services User` incluyen todos los permisos necesarios para invocar modelos de Claude.

Para permisos más restrictivos, crea un rol personalizado con lo siguiente:

```json  theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

Para más detalles, consulta la [documentación de RBAC de Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Solución de problemas

Si recibes un error "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Configura Entra ID en el entorno, o establece `ANTHROPIC_FOUNDRY_API_KEY`.

## Recursos adicionales

* [Documentación de Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Modelos de Microsoft Foundry](https://ai.azure.com/explore/models)
* [Precios de Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
