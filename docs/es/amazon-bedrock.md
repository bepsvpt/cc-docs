> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code en Amazon Bedrock

> Aprenda a configurar Claude Code a través de Amazon Bedrock, incluyendo configuración, configuración de IAM y solución de problemas.

## Requisitos previos

Antes de configurar Claude Code con Bedrock, asegúrese de tener:

* Una cuenta de AWS con acceso a Bedrock habilitado
* Acceso a los modelos Claude deseados (por ejemplo, Claude Sonnet 4.6) en Bedrock
* AWS CLI instalado y configurado (opcional - solo se necesita si no tiene otro mecanismo para obtener credenciales)
* Permisos de IAM apropiados

<Note>
  Si está implementando Claude Code para múltiples usuarios, [fije las versiones de su modelo](#4-pin-model-versions) para evitar problemas cuando Anthropic lance nuevos modelos.
</Note>

## Configuración

### 1. Envíe los detalles del caso de uso

Los usuarios por primera vez de modelos de Anthropic deben enviar detalles del caso de uso antes de invocar un modelo. Esto se realiza una vez por cuenta.

1. Asegúrese de tener los permisos de IAM correctos (vea más sobre eso a continuación)
2. Navegue a la [consola de Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Seleccione **Chat/Text playground**
4. Elija cualquier modelo de Anthropic y se le pedirá que complete el formulario de caso de uso

### 2. Configure las credenciales de AWS

Claude Code utiliza la cadena de credenciales predeterminada del SDK de AWS. Configure sus credenciales utilizando uno de estos métodos:

**Opción A: Configuración de AWS CLI**

```bash theme={null}
aws configure
```

**Opción B: Variables de entorno (clave de acceso)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Opción C: Variables de entorno (perfil SSO)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Opción D: Credenciales de la consola de administración de AWS**

```bash theme={null}
aws login
```

[Obtenga más información](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) sobre `aws login`.

**Opción E: Claves de API de Bedrock**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Las claves de API de Bedrock proporcionan un método de autenticación más simple sin necesidad de credenciales completas de AWS. [Obtenga más información sobre las claves de API de Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Configuración avanzada de credenciales

Claude Code admite la actualización automática de credenciales para AWS SSO y proveedores de identidad corporativos. Agregue estas configuraciones a su archivo de configuración de Claude Code (vea [Configuración](/es/settings) para ubicaciones de archivos).

Cuando Claude Code detecta que sus credenciales de AWS han expirado (ya sea localmente según su marca de tiempo o cuando Bedrock devuelve un error de credencial), ejecutará automáticamente sus comandos `awsAuthRefresh` y/o `awsCredentialExport` configurados para obtener nuevas credenciales antes de reintentar la solicitud.

##### Configuración de ejemplo

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Configuración explicada

**`awsAuthRefresh`**: Utilice esto para comandos que modifiquen el directorio `.aws`, como actualizar credenciales, caché de SSO o archivos de configuración. La salida del comando se muestra al usuario, pero la entrada interactiva no es compatible. Esto funciona bien para flujos de SSO basados en navegador donde la CLI muestra una URL o código y usted completa la autenticación en el navegador.

**`awsCredentialExport`**: Solo use esto si no puede modificar `.aws` y debe devolver credenciales directamente. La salida se captura silenciosamente y no se muestra al usuario. El comando debe generar JSON en este formato:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configure Claude Code

Establezca las siguientes variables de entorno para habilitar Bedrock:

```bash theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku)
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Override the Bedrock endpoint URL for custom endpoints or gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Al habilitar Bedrock para Claude Code, tenga en cuenta lo siguiente:

* `AWS_REGION` es una variable de entorno requerida. Claude Code no lee desde el archivo de configuración `.aws` para esta configuración.
* Cuando se usa Bedrock, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de credenciales de AWS.
* Puede usar archivos de configuración para variables de entorno como `AWS_PROFILE` que no desea filtrar a otros procesos. Vea [Configuración](/es/settings) para más información.

### 4. Fije las versiones del modelo

<Warning>
  Fije versiones de modelo específicas para cada implementación. Si utiliza alias de modelo (`sonnet`, `opus`, `haiku`) sin fijar, Claude Code puede intentar utilizar una versión de modelo más nueva que no está disponible en su cuenta de Bedrock, rompiendo usuarios existentes cuando Anthropic lanza actualizaciones.
</Warning>

Establezca estas variables de entorno en IDs de modelo de Bedrock específicos:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Estas variables utilizan IDs de perfil de inferencia entre regiones (con el prefijo `us.`). Si utiliza un prefijo de región diferente o perfiles de inferencia de aplicación, ajuste en consecuencia. Para IDs de modelo actuales y heredados, vea [Descripción general de modelos](https://platform.claude.com/docs/en/about-claude/models/overview). Vea [Configuración de modelo](/es/model-config#pin-models-for-third-party-deployments) para la lista completa de variables de entorno.

Claude Code utiliza estos modelos predeterminados cuando no se establecen variables de fijación:

| Tipo de modelo        | Valor predeterminado                           |
| :-------------------- | :--------------------------------------------- |
| Modelo principal      | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Modelo pequeño/rápido | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

Para personalizar modelos aún más, utilice uno de estos métodos:

```bash theme={null}
# Using inference profile ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) puede no estar disponible en todas las regiones.</Note>

#### Asigne cada versión de modelo a un perfil de inferencia

Las variables de entorno `ANTHROPIC_DEFAULT_*_MODEL` configuran un perfil de inferencia por familia de modelo. Si su organización necesita exponer varias versiones de la misma familia en el selector `/model`, cada una enrutada a su propio ARN de perfil de inferencia de aplicación, utilice la configuración `modelOverrides` en su [archivo de configuración](/es/settings#settings-files) en su lugar.

Este ejemplo asigna tres versiones de Opus a ARN distintos para que los usuarios puedan cambiar entre ellas sin eludir los perfiles de inferencia de su organización:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Cuando un usuario selecciona una de estas versiones en `/model`, Claude Code llama a Bedrock con el ARN asignado. Las versiones sin una anulación se revierten al ID de modelo de Bedrock integrado o a cualquier perfil de inferencia coincidente descubierto al inicio. Vea [Anular IDs de modelo por versión](/es/model-config#override-model-ids-per-version) para detalles sobre cómo las anulaciones interactúan con `availableModels` y otras configuraciones de modelo.

## Configuración de IAM

Cree una política de IAM con los permisos requeridos para Claude Code:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

Para permisos más restrictivos, puede limitar el Resource a ARN de perfil de inferencia específicos.

Para más detalles, vea [documentación de IAM de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Cree una cuenta de AWS dedicada para Claude Code para simplificar el seguimiento de costos y el control de acceso.
</Note>

## Ventana de contexto de 1M de tokens

Claude Opus 4.6 y Sonnet 4.6 admiten la [ventana de contexto de 1M de tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) en Amazon Bedrock. Claude Code habilita automáticamente la ventana de contexto extendida cuando selecciona una variante de modelo de 1M.

Para habilitar la ventana de contexto de 1M para su modelo fijado, agregue `[1m]` al ID del modelo. Vea [Fije modelos para implementaciones de terceros](/es/model-config#pin-models-for-third-party-deployments) para detalles.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) le permite implementar filtrado de contenido para Claude Code. Cree un Guardrail en la [consola de Amazon Bedrock](https://console.aws.amazon.com/bedrock/), publique una versión, luego agregue los encabezados de Guardrail a su [archivo de configuración](/es/settings). Habilite la inferencia entre regiones en su Guardrail si está utilizando perfiles de inferencia entre regiones.

Configuración de ejemplo:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Solución de problemas

### Bucle de autenticación con SSO y proxies corporativos

Si las pestañas del navegador se abren repetidamente cuando se usa AWS SSO, elimine la configuración `awsAuthRefresh` de su [archivo de configuración](/es/settings). Esto puede ocurrir cuando las VPN corporativas o los proxies de inspección TLS interrumpen el flujo del navegador SSO. Claude Code trata la conexión interrumpida como un error de autenticación, vuelve a ejecutar `awsAuthRefresh` y entra en un bucle indefinido.

Si su entorno de red interfiere con los flujos de SSO automáticos basados en navegador, use `aws sso login` manualmente antes de iniciar Claude Code en lugar de depender de `awsAuthRefresh`.

### Problemas de región

Si encuentra problemas de región:

* Verifique la disponibilidad del modelo: `aws bedrock list-inference-profiles --region your-region`
* Cambie a una región compatible: `export AWS_REGION=us-east-1`
* Considere usar perfiles de inferencia para acceso entre regiones

Si recibe un error "on-demand throughput isn't supported":

* Especifique el modelo como un ID de [perfil de inferencia](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code utiliza la [API de Invoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) de Bedrock y no admite la API de Converse.

## Recursos adicionales

* [Documentación de Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Perfiles de inferencia de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code en Amazon Bedrock: Guía de configuración rápida](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementación de monitoreo de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
