> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Descripción general de implementación empresarial

> Aprende cómo Claude Code puede integrarse con varios servicios de terceros e infraestructura para cumplir con los requisitos de implementación empresarial.

Esta página proporciona una descripción general de las opciones de implementación disponibles y te ayuda a elegir la configuración correcta para tu organización.

## Comparación de proveedores

<table>
  <thead>
    <tr>
      <th>Característica</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Regiones</td>
      <td>[Países](https://www.anthropic.com/supported-countries) compatibles</td>
      <td>Múltiples [regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) de AWS</td>
      <td>Múltiples [regiones](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) de GCP</td>
      <td>Múltiples [regiones](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) de Azure</td>
    </tr>

    <tr>
      <td>Almacenamiento en caché de indicaciones</td>
      <td>Habilitado de forma predeterminada</td>
      <td>Habilitado de forma predeterminada</td>
      <td>Habilitado de forma predeterminada</td>
      <td>Habilitado de forma predeterminada</td>
    </tr>

    <tr>
      <td>Autenticación</td>
      <td>Clave API</td>
      <td>Clave API o credenciales de AWS</td>
      <td>Credenciales de GCP</td>
      <td>Clave API o Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Seguimiento de costos</td>
      <td>Panel de control</td>
      <td>AWS Cost Explorer</td>
      <td>Facturación de GCP</td>
      <td>Administración de costos de Azure</td>
    </tr>

    <tr>
      <td>Características empresariales</td>
      <td>Equipos, monitoreo de uso</td>
      <td>Políticas de IAM, CloudTrail</td>
      <td>Roles de IAM, registros de auditoría en la nube</td>
      <td>Políticas de RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Proveedores de nube

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/es/amazon-bedrock">
    Utiliza modelos Claude a través de la infraestructura de AWS con autenticación basada en clave API o IAM y monitoreo nativo de AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/es/google-vertex-ai">
    Accede a modelos Claude a través de Google Cloud Platform con seguridad y cumplimiento de nivel empresarial
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/es/microsoft-foundry">
    Accede a Claude a través de Azure con autenticación de clave API o Microsoft Entra ID y facturación de Azure
  </Card>
</CardGroup>

## Infraestructura corporativa

<CardGroup cols={2}>
  <Card title="Red empresarial" icon="shield" href="/es/network-config">
    Configura Claude Code para trabajar con los servidores proxy de tu organización y requisitos de SSL/TLS
  </Card>

  <Card title="Puerta de enlace LLM" icon="server" href="/es/llm-gateway">
    Implementa acceso centralizado a modelos con seguimiento de uso, presupuesto y registro de auditoría
  </Card>
</CardGroup>

## Descripción general de la configuración

Claude Code admite opciones de configuración flexible que te permiten combinar diferentes proveedores e infraestructura:

<Note>
  Comprende la diferencia entre:

  * **Proxy corporativo**: Un proxy HTTP/HTTPS para enrutar tráfico (establecido a través de `HTTPS_PROXY` o `HTTP_PROXY`)
  * **Puerta de enlace LLM**: Un servicio que maneja la autenticación y proporciona puntos finales compatibles con proveedores (establecido a través de `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, o `ANTHROPIC_VERTEX_BASE_URL`)

  Ambas configuraciones se pueden usar en conjunto.
</Note>

### Uso de Bedrock con proxy corporativo

Enruta el tráfico de Bedrock a través de un proxy HTTP/HTTPS corporativo:

```bash  theme={null}
# Habilitar Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Uso de Bedrock con puerta de enlace LLM

Utiliza un servicio de puerta de enlace que proporciona puntos finales compatibles con Bedrock:

```bash  theme={null}
# Habilitar Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configurar puerta de enlace LLM
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Si la puerta de enlace maneja la autenticación de AWS
```

### Uso de Foundry con proxy corporativo

Enruta el tráfico de Azure a través de un proxy HTTP/HTTPS corporativo:

```bash  theme={null}
# Habilitar Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # O omitir para autenticación de Entra ID

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Uso de Foundry con puerta de enlace LLM

Utiliza un servicio de puerta de enlace que proporciona puntos finales compatibles con Azure:

```bash  theme={null}
# Habilitar Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Configurar puerta de enlace LLM
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Si la puerta de enlace maneja la autenticación de Azure
```

### Uso de Vertex AI con proxy corporativo

Enruta el tráfico de Vertex AI a través de un proxy HTTP/HTTPS corporativo:

```bash  theme={null}
# Habilitar Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Uso de Vertex AI con puerta de enlace LLM

Combina modelos de Google Vertex AI con una puerta de enlace LLM para gestión centralizada:

```bash  theme={null}
# Habilitar Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configurar puerta de enlace LLM
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Si la puerta de enlace maneja la autenticación de GCP
```

### Configuración de autenticación

Claude Code utiliza `ANTHROPIC_AUTH_TOKEN` para el encabezado `Authorization` cuando sea necesario. Las banderas `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) se utilizan en escenarios de puerta de enlace LLM donde la puerta de enlace maneja la autenticación del proveedor.

## Elegir la configuración de implementación correcta

Considera estos factores al seleccionar tu enfoque de implementación:

### Acceso directo al proveedor

Mejor para organizaciones que:

* Desean la configuración más simple
* Tienen infraestructura existente de AWS o GCP
* Necesitan monitoreo nativo del proveedor y cumplimiento

### Proxy corporativo

Mejor para organizaciones que:

* Tienen requisitos de proxy corporativo existentes
* Necesitan monitoreo de tráfico y cumplimiento
* Deben enrutar todo el tráfico a través de rutas de red específicas

### Puerta de enlace LLM

Mejor para organizaciones que:

* Necesitan seguimiento de uso entre equipos
* Desean cambiar dinámicamente entre modelos
* Requieren limitación de velocidad personalizada o presupuestos
* Necesitan gestión centralizada de autenticación

## Depuración

Al depurar tu implementación:

* Utiliza el [comando de barra](/es/slash-commands) `claude /status`. Este comando proporciona observabilidad en cualquier autenticación, proxy y configuración de URL aplicados.
* Establece la variable de entorno `export ANTHROPIC_LOG=debug` para registrar solicitudes.

## Mejores prácticas para organizaciones

### 1. Invertir en documentación y memoria

Recomendamos encarecidamente invertir en documentación para que Claude Code comprenda tu base de código. Las organizaciones pueden implementar archivos CLAUDE.md en múltiples niveles:

* **En toda la organización**: Implementa en directorios del sistema como `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) para estándares de toda la empresa
* **A nivel de repositorio**: Crea archivos `CLAUDE.md` en raíces de repositorio que contengan arquitectura del proyecto, comandos de compilación y directrices de contribución. Verifica estos en el control de código fuente para que todos los usuarios se beneficien

  [Aprende más](/es/memory).

### 2. Simplificar la implementación

Si tienes un entorno de desarrollo personalizado, encontramos que crear una forma "de un clic" para instalar Claude Code es clave para aumentar la adopción en toda una organización.

### 3. Comenzar con uso guiado

Anima a los nuevos usuarios a probar Claude Code para preguntas sobre la base de código, o en correcciones de errores más pequeñas o solicitudes de características. Pide a Claude Code que haga un plan. Verifica las sugerencias de Claude y proporciona retroalimentación si se desvía. Con el tiempo, a medida que los usuarios comprendan mejor este nuevo paradigma, serán más efectivos al permitir que Claude Code funcione de manera más autónoma.

### 4. Configurar políticas de seguridad

Los equipos de seguridad pueden configurar permisos administrados para lo que Claude Code puede y no puede hacer, lo que no puede ser sobrescrito por la configuración local. [Aprende más](/es/security).

### 5. Aprovechar MCP para integraciones

MCP es una excelente manera de dar a Claude Code más información, como conectarse a sistemas de gestión de tickets o registros de errores. Recomendamos que un equipo central configure servidores MCP y verifique una configuración `.mcp.json` en la base de código para que todos los usuarios se beneficien. [Aprende más](/es/mcp).

En Anthropic, confiamos en Claude Code para potenciar el desarrollo en todas las bases de código de Anthropic. Esperamos que disfrutes usando Claude Code tanto como nosotros.

## Próximos pasos

* [Configurar Amazon Bedrock](/es/amazon-bedrock) para implementación nativa de AWS
* [Configurar Google Vertex AI](/es/google-vertex-ai) para implementación de GCP
* [Configurar Microsoft Foundry](/es/microsoft-foundry) para implementación de Azure
* [Configurar red empresarial](/es/network-config) para requisitos de red
* [Implementar puerta de enlace LLM](/es/llm-gateway) para gestión empresarial
* [Configuración](/es/settings) para opciones de configuración y variables de entorno
