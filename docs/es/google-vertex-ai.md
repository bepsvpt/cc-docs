> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code en Google Vertex AI

> Aprenda a configurar Claude Code a través de Google Vertex AI, incluida la configuración, la configuración de IAM y la solución de problemas.

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

<ContactSalesCard surface="vertex" />

## Requisitos previos

Antes de configurar Claude Code con Vertex AI, asegúrese de tener:

* Una cuenta de Google Cloud Platform (GCP) con facturación habilitada
* Un proyecto de GCP con la API de Vertex AI habilitada
* Acceso a los modelos Claude deseados (por ejemplo, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) instalado y configurado
* Cuota asignada en la región de GCP deseada

Para iniciar sesión con sus propias credenciales de Vertex AI, siga [Iniciar sesión con Vertex AI](#sign-in-with-vertex-ai) a continuación. Para implementar Claude Code en un equipo, utilice los pasos de [configuración manual](#set-up-manually) y [fije las versiones de su modelo](#5-pin-model-versions) antes de implementar.

## Iniciar sesión con Vertex AI

Si tiene credenciales de Google Cloud y desea comenzar a usar Claude Code a través de Vertex AI, el asistente de inicio de sesión lo guía a través del proceso. Completa los requisitos previos del lado de GCP una vez por proyecto; el asistente maneja el lado de Claude Code.

<Note>
  El asistente de configuración de Vertex AI requiere Claude Code v2.1.98 o posterior. Ejecute `claude --version` para verificar.
</Note>

<Steps>
  <Step title="Habilitar modelos Claude en su proyecto de GCP">
    [Habilite la API de Vertex AI](#1-enable-vertex-ai-api) para su proyecto, luego solicite acceso a los modelos Claude que desee en el [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). Consulte [Configuración de IAM](#iam-configuration) para los permisos que su cuenta necesita.
  </Step>

  <Step title="Inicie Claude Code y elija Vertex AI">
    Ejecute `claude`. En el mensaje de inicio de sesión, seleccione **3rd-party platform**, luego **Google Vertex AI**.
  </Step>

  <Step title="Siga los mensajes del asistente">
    Elija cómo se autentica en Google Cloud: Credenciales predeterminadas de aplicación de `gcloud`, un archivo de clave de cuenta de servicio, o credenciales ya en su entorno. El asistente detecta su proyecto y región, verifica qué modelos Claude puede invocar su proyecto, y le permite fijarlos. Guarda el resultado en el bloque `env` de su [archivo de configuración de usuario](/es/settings), por lo que no necesita exportar variables de entorno usted mismo.
  </Step>
</Steps>

Después de haber iniciado sesión, ejecute `/setup-vertex` en cualquier momento para reabrirlo el asistente y cambiar sus credenciales, proyecto, región o fijaciones de modelo.

## Configuración de región

Claude Code admite puntos finales de Vertex AI [globales](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multirregión y regionales. Establezca `CLOUD_ML_REGION` en `global`, una ubicación multirregión como `eu` o `us`, o una región específica como `us-east5`. Claude Code selecciona el nombre de host correcto de Vertex AI para cada formulario, incluidos los hosts `aiplatform.eu.rep.googleapis.com` y `aiplatform.us.rep.googleapis.com` para ubicaciones multirregión.

<Note>
  Vertex AI puede no admitir los modelos predeterminados de Claude Code en todos los tipos de puntos finales. La disponibilidad del modelo varía según [regiones específicas](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), ubicaciones multirregión y [puntos finales globales](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Es posible que deba cambiar a una ubicación compatible o especificar un modelo compatible.
</Note>

## Configurar manualmente

Para configurar Vertex AI a través de variables de entorno en lugar del asistente, por ejemplo en CI o una implementación empresarial con script, siga los pasos a continuación.

### 1. Habilitar la API de Vertex AI

Habilite la API de Vertex AI en su proyecto de GCP:

```bash theme={null}
# Establezca su ID de proyecto
gcloud config set project YOUR-PROJECT-ID

# Habilitar la API de Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Solicitar acceso al modelo

Solicite acceso a los modelos Claude en Vertex AI:

1. Navegue al [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Busque modelos "Claude"
3. Solicite acceso a los modelos Claude deseados (por ejemplo, Claude Sonnet 4.6)
4. Espere la aprobación (puede tomar 24-48 horas)

### 3. Configurar credenciales de GCP

Claude Code utiliza la autenticación estándar de Google Cloud.

Para obtener más información, consulte la [documentación de autenticación de Google Cloud](https://cloud.google.com/docs/authentication).

Claude Code v2.1.121 o posterior admite [Federación de identidad de carga de trabajo basada en certificados X.509](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) a través de la misma cadena de credenciales de aplicación predeterminada. Establezca `GOOGLE_APPLICATION_CREDENTIALS` en la ruta de su archivo de configuración de credenciales.

<Note>
  Claude Code utiliza `ANTHROPIC_VERTEX_PROJECT_ID` como el ID de proyecto para solicitudes de Vertex AI. Las variables de entorno `GCLOUD_PROJECT` y `GOOGLE_CLOUD_PROJECT` y el archivo de credenciales referenciado por `GOOGLE_APPLICATION_CREDENTIALS` tienen prioridad sobre él. Si ninguno de estos está establecido, el ID de proyecto se resuelve desde su configuración de `gcloud` o la cuenta de servicio adjunta.
</Note>

#### Configuración avanzada de credenciales

Claude Code admite la actualización automática de credenciales para GCP a través de la configuración `gcpAuthRefresh`. Cuando Claude Code detecta que sus credenciales de GCP han expirado o no se pueden cargar, ejecuta el comando configurado para obtener nuevas credenciales antes de reintentar la solicitud.

```json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

La salida del comando se muestra al usuario, pero la entrada interactiva no es compatible. Esto funciona bien para flujos de autenticación basados en navegador donde la CLI muestra una URL y usted completa la autenticación en el navegador. El comando de actualización agota el tiempo de espera después de tres minutos si la autenticación no se completa. Si establece `gcpAuthRefresh` en la configuración del proyecto como `.claude/settings.json`, el comando se ejecuta solo después de que acepte el mensaje de confianza del espacio de trabajo.

### 4. Configurar Claude Code

Establezca las siguientes variables de entorno:

```bash theme={null}
# Habilitar la integración de Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Opcional: Anular la URL del punto final de Vertex para puntos finales personalizados o puertas de enlace
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Opcional: Deshabilitar el almacenamiento en caché de indicaciones si es necesario
export DISABLE_PROMPT_CACHING=1

# Opcional: Solicitar TTL de caché de indicaciones de 1 hora en lugar del predeterminado de 5 minutos
export ENABLE_PROMPT_CACHING_1H=1

# Cuando CLOUD_ML_REGION=global, anule la región para modelos que no admiten puntos finales globales
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

La mayoría de las versiones de modelo tienen una variable `VERTEX_REGION_CLAUDE_*` correspondiente. Consulte la [referencia de variables de entorno](/es/env-vars) para obtener la lista completa. Verifique [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) para determinar qué modelos admiten puntos finales globales frente a solo regionales.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) se habilita automáticamente. Para deshabilitarlo, establezca `DISABLE_PROMPT_CACHING=1`. Para solicitar un TTL de caché de 1 hora en lugar del predeterminado de 5 minutos, establezca `ENABLE_PROMPT_CACHING_1H=1`; las escrituras de caché con un TTL de 1 hora se facturan a una tarifa más alta. Para límites de velocidad elevados, póngase en contacto con el soporte de Google Cloud. Al usar Vertex AI, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de credenciales de Google Cloud.

Claude Code deshabilita [MCP tool search](/es/mcp#scale-with-mcp-tool-search) de forma predeterminada en Vertex AI, por lo que las definiciones de herramientas MCP se cargan por adelantado. Vertex AI admite búsqueda de herramientas para Claude Sonnet 4.5 y posterior y Claude Opus 4.5 y posterior. Establezca `ENABLE_TOOL_SEARCH=true` para habilitarlo en esos modelos. Los modelos anteriores en Vertex AI no aceptan el encabezado beta requerido, y las solicitudes fallan si habilita la búsqueda de herramientas con ellos.

### 5. Fijar versiones de modelo

<Warning>
  Fije versiones de modelo específicas al implementar para varios usuarios. Sin fijar, alias de modelo como `sonnet` y `opus` se resuelven a la versión más reciente, que puede no estar habilitada aún en su proyecto de Vertex AI cuando Anthropic lanza una actualización. Claude Code [retrocede](#startup-model-checks) a la versión anterior al inicio cuando la más reciente no está disponible, pero fijar le permite controlar cuándo sus usuarios se mueven a un nuevo modelo.
</Warning>

Establezca estas variables de entorno en ID de modelo específicos de Vertex AI.

Sin `ANTHROPIC_DEFAULT_OPUS_MODEL`, el alias `opus` en Vertex se resuelve a Opus 4.6. Establézcalo en el ID de Opus 4.7 para usar el modelo más reciente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Para los ID de modelo actuales y heredados, consulte [Descripción general de modelos](https://platform.claude.com/docs/en/about-claude/models/overview). Consulte [Configuración de modelo](/es/model-config#pin-models-for-third-party-deployments) para obtener la lista completa de variables de entorno.

Claude Code utiliza estos modelos predeterminados cuando no se establecen variables de fijación:

| Tipo de modelo        | Valor predeterminado          |
| :-------------------- | :---------------------------- |
| Modelo principal      | `claude-sonnet-4-5@20250929`  |
| Modelo pequeño/rápido | Igual que el modelo principal |

Las tareas en segundo plano como la generación de títulos de sesión utilizan el modelo pequeño/rápido, normalmente un modelo de clase Haiku. En Vertex AI, Claude Code establece por defecto esto al modelo principal porque Haiku puede no estar habilitado en todos los proyectos o regiones. Para usar Haiku para tareas en segundo plano, establezca `ANTHROPIC_DEFAULT_HAIKU_MODEL` en un ID de modelo que esté disponible en su proyecto.

Para personalizar aún más los modelos:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Verificaciones de modelo al inicio

Cuando Claude Code se inicia con Vertex AI configurado, verifica que los modelos que pretende usar sean accesibles en su proyecto. Esta verificación requiere Claude Code v2.1.98 o posterior.

Si ha fijado una versión de modelo que es más antigua que el valor predeterminado actual de Claude Code, y su proyecto puede invocar la versión más reciente, Claude Code le solicita que actualice la fijación. Aceptar escribe el nuevo ID de modelo en su [archivo de configuración de usuario](/es/settings) y reinicia Claude Code. Rechazar se recuerda hasta el próximo cambio de versión predeterminada.

Si no ha fijado un modelo y el valor predeterminado actual no está disponible en su proyecto, Claude Code retrocede a la versión anterior para la sesión actual y muestra un aviso. El retroceso no se persiste. Habilite el modelo más reciente en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) o [fije una versión](#5-pin-model-versions) para hacer la opción permanente.

## Configuración de IAM

Asigne los permisos de IAM requeridos:

El rol `roles/aiplatform.user` incluye los permisos requeridos:

* `aiplatform.endpoints.predict` - Requerido para la invocación de modelo y conteo de tokens

Para permisos más restrictivos, cree un rol personalizado con solo los permisos anteriores.

Para obtener más detalles, consulte la [documentación de IAM de Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Cree un proyecto de GCP dedicado para Claude Code para simplificar el seguimiento de costos y el control de acceso.
</Note>

## Ventana de contexto de 1M de tokens

Claude Opus 4.7, Opus 4.6 y Sonnet 4.6 admiten la [ventana de contexto de 1M de tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) en Vertex AI. Claude Code habilita automáticamente la ventana de contexto extendida cuando selecciona una variante de modelo de 1M.

El [asistente de configuración](#sign-in-with-vertex-ai) ofrece una opción de contexto de 1M cuando fija modelos. Para habilitarlo para un modelo fijado manualmente en su lugar, agregue `[1m]` al ID del modelo. Consulte [Fijar modelos para implementaciones de terceros](/es/model-config#pin-models-for-third-party-deployments) para obtener detalles.

## Solución de problemas

Si encuentra errores "No se pudieron cargar las credenciales predeterminadas":

* Ejecute `gcloud auth application-default login` para configurar las credenciales predeterminadas de la aplicación
* Establezca `GOOGLE_APPLICATION_CREDENTIALS` en una ruta de archivo de clave de cuenta de servicio
* Consulte [Configurar credenciales de GCP](#3-configure-gcp-credentials) para todas las opciones

Si encuentra problemas de cuota:

* Verifique las cuotas actuales o solicite un aumento de cuota a través de [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Si encuentra errores "modelo no encontrado" 404:

* Confirme que el modelo está habilitado en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifique que el modelo esté disponible en la ubicación que especificó. Algunos modelos se ofrecen solo en ubicaciones `global` o multirregión como `eu` y `us`, no en regiones específicas
* Si utiliza `CLOUD_ML_REGION=global`, verifique que sus modelos admitan puntos finales globales en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) en "Características compatibles". Para modelos que no admiten puntos finales globales, ya sea:
  * Especifique un modelo compatible a través de `ANTHROPIC_MODEL` o `ANTHROPIC_DEFAULT_HAIKU_MODEL`, o
  * Establezca una región o ubicación multirregión usando variables de entorno `VERTEX_REGION_<MODEL_NAME>`

Si encuentra errores 429:

* Para puntos finales regionales, asegúrese de que el modelo principal y el modelo pequeño/rápido sean compatibles en su región seleccionada
* Considere cambiar a `CLOUD_ML_REGION=global` para una mejor disponibilidad

## Recursos adicionales

* [Documentación de Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Precios de Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Cuotas y límites de Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
