> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code GitLab CI/CD

> Aprenda a integrar Claude Code en su flujo de trabajo de desarrollo con GitLab CI/CD

<Info>
  Claude Code para GitLab CI/CD se encuentra actualmente en beta. Las características y funcionalidades pueden evolucionar a medida que refinamos la experiencia.

  Esta integración es mantenida por GitLab. Para obtener soporte, consulte el siguiente [problema de GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/573776).
</Info>

<Note>
  Esta integración se basa en el [Claude Code CLI y Agent SDK](https://platform.claude.com/docs/es/agent-sdk/overview), lo que permite el uso programático de Claude en sus trabajos de CI/CD y flujos de trabajo de automatización personalizados.
</Note>

## ¿Por qué usar Claude Code con GitLab?

* **Creación instantánea de MR**: Describa lo que necesita, y Claude propone un MR completo con cambios y explicación
* **Implementación automatizada**: Convierta problemas en código funcional con un único comando o mención
* **Consciente del proyecto**: Claude sigue sus directrices `CLAUDE.md` y patrones de código existentes
* **Configuración simple**: Agregue un trabajo a `.gitlab-ci.yml` y una variable de CI/CD enmascarada
* **Listo para empresas**: Elija Claude API, AWS Bedrock o Google Vertex AI para cumplir con los requisitos de residencia de datos y adquisición
* **Seguro por defecto**: Se ejecuta en sus ejecutores de GitLab con su protección de rama y aprobaciones

## Cómo funciona

Claude Code utiliza GitLab CI/CD para ejecutar tareas de IA en trabajos aislados y confirmar resultados a través de MRs:

1. **Orquestación impulsada por eventos**: GitLab escucha los desencadenantes elegidos (por ejemplo, un comentario que menciona `@claude` en un problema, MR o hilo de revisión). El trabajo recopila contexto del hilo y repositorio, construye indicaciones a partir de esa entrada y ejecuta Claude Code.

2. **Abstracción de proveedores**: Utilice el proveedor que se ajuste a su entorno:
   * Claude API (SaaS)
   * AWS Bedrock (acceso basado en IAM, opciones entre regiones)
   * Google Vertex AI (nativo de GCP, Federación de Identidad de Carga de Trabajo)

3. **Ejecución en sandbox**: Cada interacción se ejecuta en un contenedor con reglas estrictas de red y sistema de archivos. Claude Code aplica permisos con alcance de espacio de trabajo para restringir escrituras. Cada cambio fluye a través de un MR para que los revisores vean el diff y las aprobaciones sigan siendo aplicables.

Elija puntos finales regionales para reducir la latencia y cumplir con los requisitos de soberanía de datos mientras utiliza acuerdos en la nube existentes.

## ¿Qué puede hacer Claude?

Claude Code habilita flujos de trabajo de CI/CD poderosos que transforman la forma en que trabaja con código:

* Crear y actualizar MRs a partir de descripciones o comentarios de problemas
* Analizar regresiones de rendimiento y proponer optimizaciones
* Implementar características directamente en una rama, luego abrir un MR
* Corregir errores y regresiones identificados por pruebas o comentarios
* Responder a comentarios de seguimiento para iterar sobre cambios solicitados

## Configuración

### Configuración rápida

La forma más rápida de comenzar es agregar un trabajo mínimo a su `.gitlab-ci.yml` y establecer su clave de API como una variable enmascarada.

1. **Agregue una variable de CI/CD enmascarada**
   * Vaya a **Configuración** → **CI/CD** → **Variables**
   * Agregue `ANTHROPIC_API_KEY` (enmascarada, protegida según sea necesario)

2. **Agregue un trabajo de Claude a `.gitlab-ci.yml`**

```yaml theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  # Ajuste las reglas para que se adapten a cómo desea desencadenar el trabajo:
  # - ejecuciones manuales
  # - eventos de solicitud de fusión
  # - desencadenadores web/API cuando un comentario contiene '@claude'
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    # Opcional: inicie un servidor MCP de GitLab si su configuración proporciona uno
    - /bin/gitlab-mcp-server || true
    # Utilice variables AI_FLOW_* cuando invoque a través de desencadenadores web/API con cargas de contexto
    - echo "$AI_FLOW_INPUT for $AI_FLOW_CONTEXT on $AI_FLOW_EVENT"
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
```

Después de agregar el trabajo y su variable `ANTHROPIC_API_KEY`, pruebe ejecutando el trabajo manualmente desde **CI/CD** → **Pipelines**, o desencadénelo desde un MR para permitir que Claude proponga actualizaciones en una rama y abra un MR si es necesario.

<Note>
  Para ejecutar en AWS Bedrock o Google Vertex AI en lugar de Claude API, consulte la sección [Usar con AWS Bedrock y Google Vertex AI](#using-with-aws-bedrock--google-vertex-ai) a continuación para obtener instrucciones de autenticación y configuración del entorno.
</Note>

### Configuración manual (recomendada para producción)

Si prefiere una configuración más controlada o necesita proveedores empresariales:

1. **Configure el acceso del proveedor**:
   * **Claude API**: Cree y almacene `ANTHROPIC_API_KEY` como una variable de CI/CD enmascarada
   * **AWS Bedrock**: **Configure GitLab** → **AWS OIDC** y cree un rol de IAM para Bedrock
   * **Google Vertex AI**: **Configure la Federación de Identidad de Carga de Trabajo para GitLab** → **GCP**

2. **Agregue credenciales de proyecto para operaciones de API de GitLab**:
   * Utilice `CI_JOB_TOKEN` de forma predeterminada, o cree un Token de Acceso de Proyecto con alcance `api`
   * Almacene como `GITLAB_ACCESS_TOKEN` (enmascarado) si utiliza un PAT

3. **Agregue el trabajo de Claude a `.gitlab-ci.yml`** (consulte los ejemplos a continuación)

4. **(Opcional) Habilite desencadenadores impulsados por menciones**:
   * Agregue un webhook de proyecto para "Comentarios (notas)" a su escucha de eventos (si utiliza uno)
   * Haga que el escucha llame a la API de desencadenador de canalización con variables como `AI_FLOW_INPUT` y `AI_FLOW_CONTEXT` cuando un comentario contiene `@claude`

## Casos de uso de ejemplo

### Convertir problemas en MRs

En un comentario de problema:

```text theme={null}
@claude implement this feature based on the issue description
```

Claude analiza el problema y la base de código, escribe cambios en una rama y abre un MR para revisión.

### Obtener ayuda de implementación

En una discusión de MR:

```text theme={null}
@claude suggest a concrete approach to cache the results of this API call
```

Claude propone cambios, agrega código con almacenamiento en caché apropiado y actualiza el MR.

### Corregir errores rápidamente

En un comentario de problema o MR:

```text theme={null}
@claude fix the TypeError in the user dashboard component
```

Claude localiza el error, implementa una corrección y actualiza la rama o abre un nuevo MR.

## Usar con AWS Bedrock y Google Vertex AI

Para entornos empresariales, puede ejecutar Claude Code completamente en su infraestructura en la nube con la misma experiencia de desarrollador.

<Tabs>
  <Tab title="AWS Bedrock">
    ### Requisitos previos

    Antes de configurar Claude Code con AWS Bedrock, necesita:

    1. Una cuenta de AWS con acceso a Amazon Bedrock para los modelos Claude deseados
    2. GitLab configurado como proveedor de identidad OIDC en AWS IAM
    3. Un rol de IAM con permisos de Bedrock y una política de confianza restringida a su proyecto/referencias de GitLab
    4. Variables de CI/CD de GitLab para asumir el rol:
       * `AWS_ROLE_TO_ASSUME` (ARN del rol)
       * `AWS_REGION` (región de Bedrock)

    ### Instrucciones de configuración

    Configure AWS para permitir que los trabajos de CI de GitLab asuman un rol de IAM a través de OIDC (sin claves estáticas).

    **Configuración requerida:**

    1. Habilite Amazon Bedrock y solicite acceso a sus modelos Claude objetivo
    2. Cree un proveedor OIDC de IAM para GitLab si aún no está presente
    3. Cree un rol de IAM confiado por el proveedor OIDC de GitLab, restringido a su proyecto y referencias protegidas
    4. Adjunte permisos de menor privilegio para las API de invocación de Bedrock

    **Valores requeridos para almacenar en variables de CI/CD:**

    * `AWS_ROLE_TO_ASSUME`
    * `AWS_REGION`

    Agregue variables en Configuración → CI/CD → Variables:

    ```yaml theme={null}
    # Para AWS Bedrock:
    - AWS_ROLE_TO_ASSUME
    - AWS_REGION
    ```

    Utilice el ejemplo de trabajo de AWS Bedrock anterior para intercambiar el token de trabajo de GitLab por credenciales temporales de AWS en tiempo de ejecución.
  </Tab>

  <Tab title="Google Vertex AI">
    ### Requisitos previos

    Antes de configurar Claude Code con Google Vertex AI, necesita:

    1. Un proyecto de Google Cloud con:
       * API de Vertex AI habilitada
       * Federación de Identidad de Carga de Trabajo configurada para confiar en OIDC de GitLab
    2. Una cuenta de servicio dedicada con solo los roles de Vertex AI requeridos
    3. Variables de CI/CD de GitLab para WIF:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER` (nombre de recurso completo)
       * `GCP_SERVICE_ACCOUNT` (correo electrónico de la cuenta de servicio)

    ### Instrucciones de configuración

    Configure Google Cloud para permitir que los trabajos de CI de GitLab suplanten una cuenta de servicio a través de la Federación de Identidad de Carga de Trabajo.

    **Configuración requerida:**

    1. Habilite la API de Credenciales de IAM, la API de STS y la API de Vertex AI
    2. Cree un Grupo de Identidad de Carga de Trabajo y un proveedor para OIDC de GitLab
    3. Cree una cuenta de servicio dedicada con roles de Vertex AI
    4. Otorgue al principal de WIF permiso para suplantar la cuenta de servicio

    **Valores requeridos para almacenar en variables de CI/CD:**

    * `GCP_WORKLOAD_IDENTITY_PROVIDER`
    * `GCP_SERVICE_ACCOUNT`

    Agregue variables en Configuración → CI/CD → Variables:

    ```yaml theme={null}
    # Para Google Vertex AI:
    - GCP_WORKLOAD_IDENTITY_PROVIDER
    - GCP_SERVICE_ACCOUNT
    - CLOUD_ML_REGION (por ejemplo, us-east5)
    ```

    Utilice el ejemplo de trabajo de Google Vertex AI anterior para autenticarse sin almacenar claves.
  </Tab>
</Tabs>

## Ejemplos de configuración

A continuación se muestran fragmentos listos para usar que puede adaptar a su canalización.

### .gitlab-ci.yml básico (Claude API)

```yaml theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Summarize recent changes and suggest improvements'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  # Claude Code utilizará ANTHROPIC_API_KEY de las variables de CI/CD
```

### Ejemplo de trabajo de AWS Bedrock (OIDC)

**Requisitos previos:**

* Amazon Bedrock habilitado con acceso a su modelo Claude elegido
* OIDC de GitLab configurado en AWS con un rol que confía en su proyecto y referencias de GitLab
* Rol de IAM con permisos de Bedrock (se recomienda menor privilegio)

**Variables de CI/CD requeridas:**

* `AWS_ROLE_TO_ASSUME`: ARN del rol de IAM para acceso a Bedrock
* `AWS_REGION`: Región de Bedrock (por ejemplo, `us-west-2`)

```yaml theme={null}
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Intercambie el token OIDC de GitLab por credenciales de AWS
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implement the requested changes and open an MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

<Note>
  Los ID de modelo para Bedrock incluyen prefijos específicos de región (por ejemplo, `us.anthropic.claude-sonnet-4-6`). Pase el modelo deseado a través de su configuración de trabajo o indicación si su flujo de trabajo lo admite.
</Note>

### Ejemplo de trabajo de Google Vertex AI (Federación de Identidad de Carga de Trabajo)

**Requisitos previos:**

* API de Vertex AI habilitada en su proyecto de GCP
* Federación de Identidad de Carga de Trabajo configurada para confiar en OIDC de GitLab
* Una cuenta de servicio con permisos de Vertex AI

**Variables de CI/CD requeridas:**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Nombre de recurso completo del proveedor
* `GCP_SERVICE_ACCOUNT`: Correo electrónico de la cuenta de servicio
* `CLOUD_ML_REGION`: Región de Vertex (por ejemplo, `us-east5`)

```yaml theme={null}
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apt-get update && apt-get install -y git && apt-get clean
    - curl -fsSL https://claude.ai/install.sh | bash
    # Autentíquese en Google Cloud a través de WIF (sin claves descargadas)
    - >
      gcloud auth login --cred-file=<(cat <<EOF
      {
        "type": "external_account",
        "audience": "${GCP_WORKLOAD_IDENTITY_PROVIDER}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken",
        "token_url": "https://sts.googleapis.com/v1/token"
      }
      EOF
      )
    - gcloud config set project "$(gcloud projects list --format='value(projectId)' --filter="name:${CI_PROJECT_NAMESPACE}" | head -n1)" || true
  script:
    - /bin/gitlab-mcp-server || true
    - >
      CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}"
      claude
      -p "${AI_FLOW_INPUT:-'Review and update code as requested'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    CLOUD_ML_REGION: "us-east5"
```

<Note>
  Con la Federación de Identidad de Carga de Trabajo, no necesita almacenar claves de cuenta de servicio. Utilice condiciones de confianza específicas del repositorio y cuentas de servicio con menor privilegio.
</Note>

## Mejores prácticas

### Configuración de CLAUDE.md

Cree un archivo `CLAUDE.md` en la raíz del repositorio para definir estándares de codificación, criterios de revisión y reglas específicas del proyecto. Claude lee este archivo durante las ejecuciones y sigue sus convenciones al proponer cambios.

### Consideraciones de seguridad

**Nunca confirme claves de API o credenciales en la nube en su repositorio**. Siempre utilice variables de CI/CD de GitLab:

* Agregue `ANTHROPIC_API_KEY` como una variable enmascarada (y protéjala si es necesario)
* Utilice OIDC específico del proveedor donde sea posible (sin claves de larga duración)
* Limite los permisos de trabajo y la salida de red
* Revise los MRs de Claude como cualquier otro colaborador

### Optimización del rendimiento

* Mantenga `CLAUDE.md` enfocado y conciso
* Proporcione descripciones claras de problemas/MR para reducir iteraciones
* Configure tiempos de espera de trabajo sensatos para evitar ejecuciones descontroladas
* Almacene en caché npm e instalaciones de paquetes en ejecutores donde sea posible

### Costos de CI

Cuando utiliza Claude Code con GitLab CI/CD, tenga en cuenta los costos asociados:

* **Tiempo de ejecución de GitLab**:
  * Claude se ejecuta en sus ejecutores de GitLab y consume minutos de cálculo
  * Consulte la facturación de ejecutores de su plan de GitLab para obtener detalles

* **Costos de API**:
  * Cada interacción de Claude consume tokens según el tamaño de la indicación y la respuesta
  * El uso de tokens varía según la complejidad de la tarea y el tamaño de la base de código
  * Consulte [Precios de Anthropic](https://platform.claude.com/docs/es/about-claude/pricing) para obtener detalles

* **Consejos de optimización de costos**:
  * Utilice comandos específicos de `@claude` para reducir turnos innecesarios
  * Establezca valores apropiados de `max_turns` y tiempo de espera de trabajo
  * Limite la concurrencia para controlar ejecuciones paralelas

## Seguridad y gobernanza

* Cada trabajo se ejecuta en un contenedor aislado con acceso de red restringido
* Los cambios de Claude fluyen a través de MRs para que los revisores vean cada diff
* Las reglas de protección de rama y aprobación se aplican al código generado por IA
* Claude Code utiliza permisos con alcance de espacio de trabajo para restringir escrituras
* Los costos permanecen bajo su control porque usted proporciona sus propias credenciales de proveedor

## Solución de problemas

### Claude no responde a comandos @claude

* Verifique que su canalización se esté desencadenando (manualmente, evento de MR o a través de un escucha de eventos de nota/webhook)
* Asegúrese de que las variables de CI/CD (`ANTHROPIC_API_KEY` o configuración del proveedor en la nube) estén presentes y no enmascaradas
* Compruebe que el comentario contiene `@claude` (no `/claude`) y que su desencadenador de mención está configurado

### El trabajo no puede escribir comentarios ni abrir MRs

* Asegúrese de que `CI_JOB_TOKEN` tenga permisos suficientes para el proyecto, o utilice un Token de Acceso de Proyecto con alcance `api`
* Compruebe que la herramienta `mcp__gitlab` esté habilitada en `--allowedTools`
* Confirme que el trabajo se ejecuta en el contexto del MR o tiene suficiente contexto a través de variables `AI_FLOW_*`

### Errores de autenticación

* **Para Claude API**: Confirme que `ANTHROPIC_API_KEY` es válida y no ha expirado
* **Para Bedrock/Vertex**: Verifique la configuración de OIDC/WIF, la suplantación de rol y los nombres secretos; confirme la disponibilidad de región y modelo

## Configuración avanzada

### Parámetros y variables comunes

Claude Code admite estas entradas comúnmente utilizadas:

* `prompt` / `prompt_file`: Proporcione instrucciones en línea (`-p`) o a través de un archivo
* `max_turns`: Limite el número de iteraciones de ida y vuelta
* `timeout_minutes`: Limite el tiempo total de ejecución
* `ANTHROPIC_API_KEY`: Requerido para Claude API (no se utiliza para Bedrock/Vertex)
* Entorno específico del proveedor: `AWS_REGION`, variables de proyecto/región para Vertex

<Note>
  Las banderas y parámetros exactos pueden variar según la versión de `@anthropic-ai/claude-code`. Ejecute `claude --help` en su trabajo para ver las opciones admitidas.
</Note>

### Personalización del comportamiento de Claude

Puede guiar a Claude de dos formas principales:

1. **CLAUDE.md**: Defina estándares de codificación, requisitos de seguridad y convenciones de proyecto. Claude lee esto durante las ejecuciones y sigue sus reglas.
2. **Indicaciones personalizadas**: Pase instrucciones específicas de tareas a través de `prompt`/`prompt_file` en el trabajo. Utilice diferentes indicaciones para diferentes trabajos (por ejemplo, revisión, implementación, refactorización).
