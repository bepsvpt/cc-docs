> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code en Amazon Bedrock

> Aprenda a configurar Claude Code a través de Amazon Bedrock, incluyendo configuración, configuración de IAM y solución de problemas.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

<ContactSalesCard surface="bedrock" />

## Requisitos previos

Antes de configurar Claude Code con Bedrock, asegúrese de tener:

* Una cuenta de AWS con acceso a Bedrock habilitado
* Acceso a los modelos Claude deseados (por ejemplo, Claude Sonnet 4.6) en Bedrock
* AWS CLI instalado y configurado (opcional - solo se necesita si no tiene otro mecanismo para obtener credenciales)
* Permisos de IAM apropiados

Para iniciar sesión con sus propias credenciales de Bedrock, siga [Iniciar sesión con Bedrock](#sign-in-with-bedrock) a continuación. Para implementar Claude Code en un equipo, utilice los pasos de [configuración manual](#set-up-manually) y [fije las versiones de su modelo](#4-pin-model-versions) antes de implementar.

## Iniciar sesión con Bedrock

Si tiene credenciales de AWS y desea comenzar a usar Claude Code a través de Bedrock, el asistente de inicio de sesión lo guía a través del proceso. Completa los requisitos previos del lado de AWS una vez por cuenta; el asistente maneja el lado de Claude Code.

<Steps>
  <Step title="Habilitar modelos de Anthropic en su cuenta de AWS">
    En la [consola de Amazon Bedrock](https://console.aws.amazon.com/bedrock/), abra el catálogo de modelos, seleccione un modelo de Anthropic y envíe el formulario de caso de uso. El acceso se otorga inmediatamente después del envío. Vea [Enviar detalles del caso de uso](#1-submit-use-case-details) para AWS Organizations y [configuración de IAM](#iam-configuration) para los permisos que su rol necesita.
  </Step>

  <Step title="Inicie Claude Code y elija Bedrock">
    Ejecute `claude`. En el mensaje de inicio de sesión, seleccione **3rd-party platform**, luego **Amazon Bedrock**.
  </Step>

  <Step title="Siga los mensajes del asistente">
    Elija cómo se autentica en AWS: un perfil de AWS detectado desde su directorio `~/.aws`, una clave de API de Bedrock, una clave de acceso y secreto, o credenciales ya en su entorno. El asistente recoge su región, verifica qué modelos de Claude puede invocar su cuenta, y le permite fijarlos. Guarda el resultado en el bloque `env` de su [archivo de configuración de usuario](/es/settings), por lo que no necesita exportar variables de entorno usted mismo.
  </Step>
</Steps>

Después de haber iniciado sesión, ejecute `/setup-bedrock` en cualquier momento para reabrirlo el asistente y cambiar sus credenciales, región o fijaciones de modelo.

## Configurar manualmente

Para configurar Bedrock a través de variables de entorno en lugar del asistente, por ejemplo en CI o una implementación empresarial con script, siga los pasos a continuación.

### 1. Enviar detalles del caso de uso

Los usuarios por primera vez de modelos de Anthropic deben enviar detalles del caso de uso antes de invocar un modelo. Esto se realiza una vez por cuenta de AWS.

1. Asegúrese de tener los permisos de IAM correctos descritos a continuación
2. Navegue a la [consola de Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Seleccione un modelo de Anthropic del **catálogo de modelos**
4. Complete el formulario de caso de uso. El acceso se otorga inmediatamente después del envío.

Si utiliza AWS Organizations, puede enviar el formulario una vez desde la cuenta de administración utilizando la [API `PutUseCaseForModelAccess`](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). Esta llamada requiere el permiso de IAM `bedrock:PutUseCaseForModelAccess`. La aprobación se extiende a las cuentas secundarias automáticamente.

### 2. Configurar credenciales de AWS

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

Estas dos configuraciones tienen diferentes condiciones de activación:

* **`awsAuthRefresh`**: se ejecuta solo cuando Claude Code detecta que sus credenciales de AWS han expirado, ya sea localmente según su marca de tiempo o cuando Bedrock devuelve un error de credencial, luego reintenta la solicitud con credenciales actualizadas.
* **`awsCredentialExport`**: se ejecuta al inicio de la sesión y en cada recarga de credenciales, incluso cuando las credenciales en su cadena de proveedores de credenciales predeterminada de AWS aún son válidas. Utilice esto cuando su cuenta de Bedrock requiera credenciales entre cuentas que difieran de las que la cadena de proveedores predeterminada resolvería.

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

**`awsCredentialExport`**: Solo use esto si no puede modificar `.aws` y debe devolver credenciales directamente. Este comando se ejecuta siempre que sea necesario actualizar las credenciales, no solo cuando las credenciales han expirado. La salida se captura silenciosamente y no se muestra al usuario. El comando debe generar JSON en este formato:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configurar Claude Code

Establezca las siguientes variables de entorno para habilitar Bedrock:

```bash theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku).
# Also applies to Bedrock Mantle.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Override the Bedrock endpoint URL for custom endpoints or gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Al habilitar Bedrock para Claude Code, tenga en cuenta lo siguiente:

* `AWS_REGION` es una variable de entorno requerida. Claude Code no lee desde el archivo de configuración `.aws` para esta configuración.
* Cuando se usa Bedrock, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de credenciales de AWS.
* Puede usar archivos de configuración para variables de entorno como `AWS_PROFILE` que no desea filtrar a otros procesos. Vea [Configuración](/es/settings) para más información.

### 4. Fijar versiones de modelo

<Warning>
  Fije versiones de modelo específicas al implementar para múltiples usuarios. Sin fijar, alias de modelo como `sonnet` y `opus` se resuelven a la versión más reciente, que puede no estar disponible aún en su cuenta de Bedrock cuando Anthropic lanza una actualización. Claude Code [retrocede](#startup-model-checks) a la versión anterior al inicio cuando la más reciente no está disponible, pero fijar le permite controlar cuándo sus usuarios se mueven a un nuevo modelo.
</Warning>

Establezca estas variables de entorno en IDs de modelo de Bedrock específicos.

Sin `ANTHROPIC_DEFAULT_OPUS_MODEL`, el alias `opus` en Bedrock se resuelve a Opus 4.6. Establézcalo en el ID de Opus 4.7 para usar el modelo más reciente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
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
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Request 1-hour prompt cache TTL instead of the 5-minute default
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) puede no estar disponible en todas las regiones. Las escrituras de caché con un TTL de 1 hora se facturan a una tasa más alta que las escrituras de 5 minutos.</Note>

#### Asignar cada versión de modelo a un perfil de inferencia

Las variables de entorno `ANTHROPIC_DEFAULT_*_MODEL` configuran un perfil de inferencia por familia de modelo. Si su organización necesita exponer varias versiones de la misma familia en el selector `/model`, cada una enrutada a su propio ARN de perfil de inferencia de aplicación, utilice la configuración `modelOverrides` en su [archivo de configuración](/es/settings#settings-files) en su lugar.

Este ejemplo asigna cuatro versiones de Opus a ARN distintos para que los usuarios puedan cambiar entre ellas sin eludir los perfiles de inferencia de su organización:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Cuando un usuario selecciona una de estas versiones en `/model`, Claude Code llama a Bedrock con el ARN asignado. Las versiones sin una anulación se revierten al ID de modelo de Bedrock integrado o a cualquier perfil de inferencia coincidente descubierto al inicio. Vea [Anular IDs de modelo por versión](/es/model-config#override-model-ids-per-version) para detalles sobre cómo las anulaciones interactúan con `availableModels` y otras configuraciones de modelo.

## Verificaciones de modelo al inicio

Cuando Claude Code se inicia con Bedrock configurado, verifica que los modelos que pretende usar sean accesibles en su cuenta. Esta verificación requiere Claude Code v2.1.94 o posterior.

Si ha fijado una versión de modelo que es más antigua que el valor predeterminado actual de Claude Code, y su cuenta puede invocar la versión más reciente, Claude Code le solicita que actualice la fijación. Aceptar escribe el nuevo ID de modelo en su [archivo de configuración de usuario](/es/settings) y reinicia Claude Code. Rechazar se recuerda hasta el próximo cambio de versión predeterminada. Las fijaciones que apuntan a un [ARN de perfil de inferencia de aplicación](#map-each-model-version-to-an-inference-profile) se omiten, ya que son administradas por su administrador.

Si no ha fijado un modelo y el valor predeterminado actual no está disponible en su cuenta, Claude Code retrocede a la versión anterior para la sesión actual y muestra un aviso. El retroceso no se persiste. Habilite el modelo más reciente en su cuenta de Bedrock o [fije una versión](#4-pin-model-versions) para hacer la opción permanente.

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
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
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

`bedrock:GetInferenceProfile` permite que Claude Code resuelva un [ARN de perfil de inferencia de aplicación](#map-each-model-version-to-an-inference-profile) a su modelo de fundación de respaldo, que se utiliza para seleccionar la forma de solicitud correcta para ese modelo.

Si el token carece de este permiso, Claude Code se recupera automáticamente reintentando una vez con la forma alternativa, por lo que las solicitudes aún tienen éxito pero cada nuevo modelo agrega un viaje de ida y vuelta adicional. Otorgar el permiso evita el reintento. Esto se aplica con mayor frecuencia a implementaciones de `AWS_BEARER_TOKEN_BEDROCK`, donde la política del token es típicamente más estrecha que un rol de IAM completo.

Para más detalles, vea [documentación de IAM de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Cree una cuenta de AWS dedicada para Claude Code para simplificar el seguimiento de costos y el control de acceso.
</Note>

## Ventana de contexto de 1M de tokens

Claude Opus 4.7, Opus 4.6 y Sonnet 4.6 admiten la [ventana de contexto de 1M de tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) en Amazon Bedrock. Claude Code habilita automáticamente la ventana de contexto extendida cuando selecciona una variante de modelo de 1M.

El [asistente de configuración](#sign-in-with-bedrock) ofrece una opción de contexto de 1M cuando fija modelos. Para habilitarlo para un modelo fijado manualmente en su lugar, agregue `[1m]` al ID del modelo. Vea [Fijar modelos para implementaciones de terceros](/es/model-config#pin-models-for-third-party-deployments) para detalles.

## Niveles de servicio

[Los niveles de servicio de Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html) le permiten compensar el costo contra la latencia. Establezca `ANTHROPIC_BEDROCK_SERVICE_TIER` en `default`, `flex` o `priority`:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code envía esto como el encabezado `X-Amzn-Bedrock-Service-Tier` en cada solicitud. La disponibilidad de niveles varía según el modelo y la región. La capacidad reservada utiliza un [ARN de rendimiento aprovisionado](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) como el ID del modelo en lugar de esta configuración.

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

## Usar el punto final de Mantle

Mantle es un punto final de Amazon Bedrock que sirve modelos de Claude a través de la forma de API nativa de Anthropic en lugar de la API de Invoke de Bedrock. Utiliza las mismas credenciales de AWS, permisos de IAM y configuración de `awsAuthRefresh` descritos anteriormente en esta página.

<Note>
  Mantle requiere Claude Code v2.1.94 o posterior. Ejecute `claude --version` para verificar.
</Note>

### Habilitar Mantle

Con credenciales de AWS ya configuradas, establezca `CLAUDE_CODE_USE_MANTLE` para enrutar solicitudes al punto final de Mantle:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code construye la URL del punto final desde `AWS_REGION`. Para anularla para un punto final personalizado o puerta de enlace, establezca `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Ejecute `/status` dentro de Claude Code para confirmar. La línea del proveedor muestra `Amazon Bedrock (Mantle)` cuando Mantle está activo.

### Seleccionar un modelo de Mantle

Mantle utiliza IDs de modelo con prefijo `anthropic.` y sin sufijo de versión, por ejemplo `anthropic.claude-haiku-4-5`. Los modelos disponibles para su cuenta dependen de lo que su organización haya sido autorizada; los IDs de modelo adicionales se enumeran en sus materiales de incorporación de AWS. Póngase en contacto con su equipo de cuenta de AWS para solicitar acceso a modelos permitidos.

Establezca el modelo con la bandera `--model` o con `/model` dentro de Claude Code:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Ejecutar Mantle junto con la API de Invoke

Los modelos disponibles para usted en Mantle pueden no incluir todos los modelos que usa hoy. Establecer tanto `CLAUDE_CODE_USE_BEDROCK` como `CLAUDE_CODE_USE_MANTLE` permite que Claude Code llame a ambos puntos finales desde la misma sesión. Los IDs de modelo que coinciden con el formato de Mantle se enrutan a Mantle, y todos los demás IDs de modelo van a la API de Invoke de Bedrock.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Para mostrar un modelo de Mantle en el selector `/model`, enumere su ID en `availableModels` en su [archivo de configuración](/es/settings). Esta configuración también restringe el selector a las entradas enumeradas, por lo que incluya cada alias que desee mantener disponible:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Las entradas con el prefijo `anthropic.` se agregan como opciones de selector personalizado y se enrutan a Mantle. Reemplace `anthropic.claude-haiku-4-5` con el ID de modelo que su cuenta ha sido autorizada. Vea [Restringir selección de modelo](/es/model-config#restrict-model-selection) para cómo `availableModels` interactúa con otras configuraciones de modelo.

Cuando ambos proveedores están activos, `/status` muestra `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Enrutar Mantle a través de una puerta de enlace

Si su organización enruta el tráfico de modelo a través de una [puerta de enlace LLM](/es/llm-gateway) centralizada que inyecta credenciales de AWS del lado del servidor, deshabilite la autenticación del lado del cliente para que Claude Code envíe solicitudes sin firmas SigV4 o encabezados `x-api-key`:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Variables de entorno de Mantle

Estas variables son específicas del punto final de Mantle. Vea [Variables de entorno](/es/env-vars) para la lista completa.

| Variable                                | Propósito                                                                      |
| :-------------------------------------- | :----------------------------------------------------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | Habilitar el punto final de Mantle. Establezca en `1` o `true`.                |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Anular la URL del punto final de Mantle predeterminada                         |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Omitir la autenticación del lado del cliente para configuraciones de proxy     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Anular la región de AWS para el modelo de clase Haiku (compartido con Bedrock) |

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

### Errores del punto final de Mantle

Si `/status` no muestra `Amazon Bedrock (Mantle)` después de establecer `CLAUDE_CODE_USE_MANTLE`, la variable no está llegando al proceso. Confirme que se exporta en el shell donde lanzó `claude`, o establézcala en el bloque `env` de su [archivo de configuración](/es/settings).

Un `403` del punto final de Mantle con credenciales válidas significa que su cuenta de AWS no ha sido autorizada para acceder al modelo que solicitó. Póngase en contacto con su equipo de cuenta de AWS para solicitar acceso.

Un `400` que nombra el ID del modelo significa que ese modelo no se sirve en Mantle. Mantle tiene su propio catálogo de modelos separado del catálogo estándar de Bedrock, por lo que los IDs de perfil de inferencia como `us.anthropic.claude-sonnet-4-6` no funcionarán. Utilice un ID de formato de Mantle, o habilite [ambos puntos finales](#run-mantle-alongside-the-invoke-api) para que Claude Code enrute cada solicitud al punto final donde el modelo está disponible.

## Recursos adicionales

* [Documentación de Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Perfiles de inferencia de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Burndown de tokens de Bedrock y cuotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code en Amazon Bedrock: Guía de configuración rápida](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementación de monitoreo de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
