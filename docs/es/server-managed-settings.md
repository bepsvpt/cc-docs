> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurar la configuración administrada por servidor (beta pública)

> Configure Claude Code centralmente para su organización a través de configuración entregada por servidor, sin requerir infraestructura de administración de dispositivos.

La configuración administrada por servidor permite a los administradores configurar Claude Code centralmente a través de una interfaz basada en web en Claude.ai. Los clientes de Claude Code reciben automáticamente estas configuraciones cuando los usuarios se autentican con sus credenciales organizacionales.

Este enfoque está diseñado para organizaciones que no tienen infraestructura de administración de dispositivos implementada, o que necesitan administrar configuraciones para usuarios en dispositivos no administrados.

<Note>
  La configuración administrada por servidor está en beta pública y disponible para clientes de [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) y [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise). Las características pueden evolucionar antes de la disponibilidad general.
</Note>

## Requisitos

Para usar la configuración administrada por servidor, necesita:

* Plan Claude for Teams o Claude for Enterprise
* Claude Code versión 2.1.38 o posterior para Claude for Teams, o versión 2.1.30 o posterior para Claude for Enterprise
* Acceso de red a `api.anthropic.com`

## Elegir entre configuración administrada por servidor y administrada por endpoint

Claude Code admite dos enfoques para la configuración centralizada. La configuración administrada por servidor entrega la configuración desde los servidores de Anthropic. La [configuración administrada por endpoint](/es/settings#settings-files) se implementa directamente en dispositivos a través de políticas nativas del sistema operativo (preferencias administradas de macOS, registro de Windows) o archivos de configuración administrados.

| Enfoque                                                                    | Mejor para                                                          | Modelo de seguridad                                                                                                                                   |
| :------------------------------------------------------------------------- | :------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Configuración administrada por servidor**                                | Organizaciones sin MDM, o usuarios en dispositivos no administrados | Configuración entregada desde los servidores de Anthropic en el momento de la autenticación                                                           |
| **[Configuración administrada por endpoint](/es/settings#settings-files)** | Organizaciones con MDM o administración de endpoint                 | Configuración implementada en dispositivos a través de perfiles de configuración MDM, políticas de registro o archivos de configuración administrados |

Si sus dispositivos están inscritos en una solución MDM o de administración de endpoint, la configuración administrada por endpoint proporciona garantías de seguridad más sólidas porque el archivo de configuración puede protegerse de la modificación del usuario a nivel del sistema operativo.

## Configurar la configuración administrada por servidor

<Steps>
  <Step title="Abrir la consola de administración">
    En [Claude.ai](https://claude.ai), navegue a **Admin Settings > Claude Code > Managed settings**.
  </Step>

  <Step title="Definir su configuración">
    Agregue su configuración como JSON. Todas las [configuraciones disponibles en `settings.json`](/es/settings#available-settings) son compatibles, incluidos [hooks](/es/hooks), [variables de entorno](/es/env-vars) y [configuraciones solo administradas](/es/permissions#managed-only-settings) como `allowManagedPermissionRulesOnly`.

    Este ejemplo aplica una lista de denegación de permisos e impide que los usuarios omitan permisos:

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      }
    }
    ```

    Los hooks utilizan el mismo formato que en `settings.json`.

    Este ejemplo ejecuta un script de auditoría después de cada edición de archivo en toda la organización:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    Para configurar el clasificador del [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode) para que sepa qué repositorios, buckets y dominios confía su organización:

    ```json  theme={null}
    {
      "autoMode": {
        "environment": [
          "Source control: github.example.com/acme-corp and all repos under it",
          "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
          "Trusted internal domains: *.corp.example.com"
        ]
      }
    }
    ```

    Debido a que los hooks ejecutan comandos de shell, los usuarios ven un [diálogo de aprobación de seguridad](#security-approval-dialogs) antes de que se apliquen. Consulte [Configurar el clasificador del modo automático](/es/permissions#configure-the-auto-mode-classifier) para ver cómo las entradas de `autoMode` afectan lo que el clasificador bloquea y advertencias importantes sobre los campos `allow` y `soft_deny`.
  </Step>

  <Step title="Guardar e implementar">
    Guarde sus cambios. Los clientes de Claude Code reciben la configuración actualizada en su próximo inicio o ciclo de sondeo por hora.
  </Step>
</Steps>

### Verificar la entrega de configuración

Para confirmar que la configuración se está aplicando, pida a un usuario que reinicie Claude Code. Si la configuración incluye configuraciones que activan el [diálogo de aprobación de seguridad](#security-approval-dialogs), el usuario ve un mensaje que describe la configuración administrada al inicio. También puede verificar que las reglas de permisos administrados estén activas haciendo que un usuario ejecute `/permissions` para ver sus reglas de permisos efectivas.

### Control de acceso

Los siguientes roles pueden administrar la configuración administrada por servidor:

* **Propietario principal**
* **Propietario**

Restrinja el acceso al personal de confianza, ya que los cambios de configuración se aplican a todos los usuarios de la organización.

### Limitaciones actuales

La configuración administrada por servidor tiene las siguientes limitaciones durante el período beta:

* La configuración se aplica uniformemente a todos los usuarios de la organización. Las configuraciones por grupo aún no son compatibles.
* Las [configuraciones de servidor MCP](/es/mcp#managed-mcp-configuration) no se pueden distribuir a través de la configuración administrada por servidor.

## Entrega de configuración

### Precedencia de configuración

La configuración administrada por servidor y la [configuración administrada por endpoint](/es/settings#settings-files) ocupan el nivel más alto en la [jerarquía de configuración](/es/settings#settings-precedence) de Claude Code. Ningún otro nivel de configuración puede anularlas, incluidos los argumentos de línea de comandos. Cuando ambas están presentes, la configuración administrada por servidor tiene prioridad y la configuración administrada por endpoint no se utiliza.

### Comportamiento de obtención y almacenamiento en caché

Claude Code obtiene la configuración de los servidores de Anthropic al inicio y sondea actualizaciones cada hora durante sesiones activas.

**Primer lanzamiento sin configuración en caché:**

* Claude Code obtiene la configuración de forma asincrónica
* Si la obtención falla, Claude Code continúa sin configuración administrada
* Hay una breve ventana antes de que se cargue la configuración donde las restricciones aún no se aplican

**Lanzamientos posteriores con configuración en caché:**

* La configuración en caché se aplica inmediatamente al inicio
* Claude Code obtiene configuración nueva en segundo plano
* La configuración en caché persiste a través de fallos de red

Claude Code aplica actualizaciones de configuración automáticamente sin reinicio, excepto para configuraciones avanzadas como la configuración de OpenTelemetry, que requieren un reinicio completo para tomar efecto.

### Diálogos de aprobación de seguridad

Ciertas configuraciones que podrían presentar riesgos de seguridad requieren aprobación explícita del usuario antes de ser aplicadas:

* **Configuraciones de comandos de shell**: configuraciones que ejecutan comandos de shell
* **Variables de entorno personalizadas**: variables que no están en la lista de permitidos conocida y segura
* **Configuraciones de hooks**: cualquier definición de hook

Cuando estas configuraciones están presentes, los usuarios ven un diálogo de seguridad que explica qué se está configurando. Los usuarios deben aprobar para continuar. Si un usuario rechaza la configuración, Claude Code se cierra.

<Note>
  En modo no interactivo con la bandera `-p`, Claude Code omite los diálogos de seguridad y aplica la configuración sin aprobación del usuario.
</Note>

## Disponibilidad de plataforma

La configuración administrada por servidor requiere una conexión directa a `api.anthropic.com` y no está disponible cuando se utilizan proveedores de modelos de terceros:

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* Endpoints de API personalizados a través de `ANTHROPIC_BASE_URL` o [puertas de enlace LLM](/es/llm-gateway)

## Registro de auditoría

Los eventos del registro de auditoría para cambios de configuración están disponibles a través de la API de cumplimiento o exportación del registro de auditoría. Póngase en contacto con su equipo de cuenta de Anthropic para obtener acceso.

Los eventos de auditoría incluyen el tipo de acción realizada, la cuenta y el dispositivo que realizó la acción, y referencias a los valores anteriores y nuevos.

## Consideraciones de seguridad

La configuración administrada por servidor proporciona aplicación de políticas centralizada, pero funciona como un control del lado del cliente. En dispositivos no administrados, los usuarios con acceso de administrador o sudo pueden modificar el binario de Claude Code, el sistema de archivos o la configuración de red.

| Escenario                                                      | Comportamiento                                                                                                                                           |
| :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El usuario edita el archivo de configuración en caché          | El archivo manipulado se aplica al inicio, pero la configuración correcta se restaura en la siguiente obtención del servidor                             |
| El usuario elimina el archivo de configuración en caché        | Ocurre el comportamiento del primer lanzamiento: la configuración se obtiene de forma asincrónica con una breve ventana no aplicada                      |
| La API no está disponible                                      | La configuración en caché se aplica si está disponible, de lo contrario, la configuración administrada no se aplica hasta la siguiente obtención exitosa |
| El usuario se autentica con una organización diferente         | La configuración no se entrega para cuentas fuera de la organización administrada                                                                        |
| El usuario establece un `ANTHROPIC_BASE_URL` no predeterminado | La configuración administrada por servidor se omite cuando se utilizan proveedores de API de terceros                                                    |

Para detectar cambios de configuración en tiempo de ejecución, use [hooks `ConfigChange`](/es/hooks#configchange) para registrar modificaciones o bloquear cambios no autorizados antes de que surtan efecto.

Para garantías de aplicación más sólidas, use la [configuración administrada por endpoint](/es/settings#settings-files) en dispositivos inscritos en una solución MDM.

## Ver también

Páginas relacionadas para administrar la configuración de Claude Code:

* [Settings](/es/settings): referencia de configuración completa que incluye todas las configuraciones disponibles
* [Endpoint-managed settings](/es/settings#settings-files): configuración administrada implementada en dispositivos por TI
* [Authentication](/es/authentication): configurar el acceso de usuarios a Claude Code
* [Security](/es/security): salvaguardas de seguridad y mejores prácticas
