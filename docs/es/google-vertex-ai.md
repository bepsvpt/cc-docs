> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code en Google Vertex AI

> Aprenda a configurar Claude Code a través de Google Vertex AI, incluyendo configuración, configuración de IAM y solución de problemas.

## Requisitos previos

Antes de configurar Claude Code con Vertex AI, asegúrese de tener:

* Una cuenta de Google Cloud Platform (GCP) con facturación habilitada
* Un proyecto de GCP con la API de Vertex AI habilitada
* Acceso a los modelos Claude deseados (por ejemplo, Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) instalado y configurado
* Cuota asignada en la región de GCP deseada

## Configuración de región

Claude Code se puede utilizar tanto con [puntos finales globales](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) como regionales de Vertex AI.

<Note>
  Vertex AI puede no admitir los modelos predeterminados de Claude Code en todas las regiones. Es posible que deba cambiar a una [región o modelo compatible](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  Vertex AI puede no admitir los modelos predeterminados de Claude Code en puntos finales globales. Es posible que deba cambiar a un punto final regional o a un [modelo compatible](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
</Note>

## Configuración

### 1. Habilitar la API de Vertex AI

Habilite la API de Vertex AI en su proyecto de GCP:

```bash  theme={null}
# Establezca su ID de proyecto
gcloud config set project YOUR-PROJECT-ID

# Habilitar la API de Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Solicitar acceso al modelo

Solicite acceso a los modelos Claude en Vertex AI:

1. Navegue al [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Busque modelos "Claude"
3. Solicite acceso a los modelos Claude deseados (por ejemplo, Claude Sonnet 4.5)
4. Espere la aprobación (puede tomar 24-48 horas)

### 3. Configurar credenciales de GCP

Claude Code utiliza la autenticación estándar de Google Cloud.

Para obtener más información, consulte la [documentación de autenticación de Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Al autenticarse, Claude Code utilizará automáticamente el ID de proyecto de la variable de entorno `ANTHROPIC_VERTEX_PROJECT_ID`. Para anular esto, establezca una de estas variables de entorno: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` o `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Configurar Claude Code

Establezca las siguientes variables de entorno:

```bash  theme={null}
# Habilitar integración de Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Opcional: Deshabilitar almacenamiento en caché de solicitudes si es necesario
export DISABLE_PROMPT_CACHING=1

# Cuando CLOUD_ML_REGION=global, anule la región para modelos no compatibles
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Opcional: Anular regiones para otros modelos específicos
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) se admite automáticamente cuando especifica la bandera efímera `cache_control`. Para deshabilitarlo, establezca `DISABLE_PROMPT_CACHING=1`. Para límites de velocidad mejorados, póngase en contacto con el soporte de Google Cloud.
</Note>

<Note>
  Al utilizar Vertex AI, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de credenciales de Google Cloud.
</Note>

### 5. Configuración del modelo

Claude Code utiliza estos modelos predeterminados para Vertex AI:

| Tipo de modelo        | Valor predeterminado         |
| :-------------------- | :--------------------------- |
| Modelo principal      | `claude-sonnet-4-5@20250929` |
| Modelo pequeño/rápido | `claude-haiku-4-5@20251001`  |

<Note>
  Para usuarios de Vertex AI, Claude Code no se actualizará automáticamente de Haiku 3.5 a Haiku 4.5. Para cambiar manualmente a un modelo Haiku más nuevo, establezca la variable de entorno `ANTHROPIC_DEFAULT_HAIKU_MODEL` en el nombre completo del modelo (por ejemplo, `claude-haiku-4-5@20251001`).
</Note>

Para personalizar modelos:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Configuración de IAM

Asigne los permisos de IAM requeridos:

El rol `roles/aiplatform.user` incluye los permisos requeridos:

* `aiplatform.endpoints.predict` - Requerido para la invocación de modelos y conteo de tokens

Para permisos más restrictivos, cree un rol personalizado solo con los permisos anteriores.

Para obtener más detalles, consulte la [documentación de IAM de Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Recomendamos crear un proyecto de GCP dedicado para Claude Code para simplificar el seguimiento de costos y el control de acceso.
</Note>

## Ventana de contexto de 1M de tokens

Claude Sonnet 4 y Sonnet 4.5 admiten la [ventana de contexto de 1M de tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) en Vertex AI.

<Note>
  La ventana de contexto de 1M de tokens está actualmente en versión beta. Para utilizar la ventana de contexto extendida, incluya el encabezado beta `context-1m-2025-08-07` en sus solicitudes de Vertex AI.
</Note>

## Solución de problemas

Si encuentra problemas de cuota:

* Verifique las cuotas actuales o solicite un aumento de cuota a través de [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Si encuentra errores 404 "modelo no encontrado":

* Confirme que el modelo está habilitado en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifique que tenga acceso a la región especificada
* Si utiliza `CLOUD_ML_REGION=global`, verifique que sus modelos admitan puntos finales globales en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) en "Características compatibles". Para modelos que no admiten puntos finales globales, ya sea:
  * Especifique un modelo compatible a través de `ANTHROPIC_MODEL` o `ANTHROPIC_SMALL_FAST_MODEL`, o
  * Establezca un punto final regional usando variables de entorno `VERTEX_REGION_<MODEL_NAME>`

Si encuentra errores 429:

* Para puntos finales regionales, asegúrese de que el modelo principal y el modelo pequeño/rápido sean compatibles en su región seleccionada
* Considere cambiar a `CLOUD_ML_REGION=global` para una mejor disponibilidad

## Recursos adicionales

* [Documentación de Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Precios de Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Cuotas y límites de Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
