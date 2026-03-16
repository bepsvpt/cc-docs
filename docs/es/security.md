> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Seguridad

> Aprenda sobre las medidas de seguridad de Claude Code y las mejores prácticas para un uso seguro.

## Cómo abordamos la seguridad

### Fundamento de seguridad

La seguridad de su código es primordial. Claude Code está construido con la seguridad en su núcleo, desarrollado de acuerdo con el programa de seguridad integral de Anthropic. Obtenga más información y acceda a recursos (informe SOC 2 Type 2, certificado ISO 27001, etc.) en [Anthropic Trust Center](https://trust.anthropic.com).

### Arquitectura basada en permisos

Claude Code utiliza permisos de solo lectura estrictos de forma predeterminada. Cuando se necesitan acciones adicionales (editar archivos, ejecutar pruebas, ejecutar comandos), Claude Code solicita permiso explícito. Los usuarios controlan si aprobar acciones una sola vez o permitirlas automáticamente.

Diseñamos Claude Code para ser transparente y seguro. Por ejemplo, requerimos aprobación para comandos bash antes de ejecutarlos, lo que le da control directo. Este enfoque permite a los usuarios y organizaciones configurar permisos directamente.

Para la configuración detallada de permisos, consulte [Permissions](/es/permissions).

### Protecciones integradas

Para mitigar riesgos en sistemas agénticos:

* **Herramienta bash en sandbox**: [Sandbox](/es/sandboxing) comandos bash con aislamiento del sistema de archivos y red, reduciendo solicitudes de permiso mientras se mantiene la seguridad. Habilite con `/sandbox` para definir límites donde Claude Code puede trabajar de forma autónoma
* **Restricción de acceso de escritura**: Claude Code solo puede escribir en la carpeta donde se inició y sus subcarpetas—no puede modificar archivos en directorios principales sin permiso explícito. Aunque Claude Code puede leer archivos fuera del directorio de trabajo (útil para acceder a bibliotecas del sistema y dependencias), las operaciones de escritura están estrictamente limitadas al alcance del proyecto, creando un límite de seguridad claro
* **Mitigación de fatiga de solicitudes**: Soporte para listas de permitidos de comandos seguros frecuentemente utilizados por usuario, por base de código u por organización
* **Modo Aceptar Ediciones**: Aceptar por lotes múltiples ediciones mientras se mantienen solicitudes de permiso para comandos con efectos secundarios

### Responsabilidad del usuario

Claude Code solo tiene los permisos que usted le otorga. Usted es responsable de revisar el código y los comandos propuestos para verificar su seguridad antes de aprobarlos.

## Protéjase contra la inyección de solicitudes

La inyección de solicitudes es una técnica donde un atacante intenta anular o manipular las instrucciones de un asistente de IA insertando texto malicioso. Claude Code incluye varias medidas de protección contra estos ataques:

### Protecciones principales

* **Sistema de permisos**: Las operaciones sensibles requieren aprobación explícita
* **Análisis consciente del contexto**: Detecta instrucciones potencialmente dañinas analizando la solicitud completa
* **Sanitización de entrada**: Previene la inyección de comandos procesando entradas del usuario
* **Lista de bloqueo de comandos**: Bloquea comandos arriesgados que obtienen contenido arbitrario de la web como `curl` y `wget` de forma predeterminada. Cuando se permite explícitamente, tenga en cuenta las [limitaciones del patrón de permisos](/es/permissions#tool-specific-permission-rules)

### Medidas de protección de privacidad

Hemos implementado varias medidas de protección para proteger sus datos, incluyendo:

* Períodos de retención limitados para información sensible (consulte el [Privacy Center](https://privacy.anthropic.com/en/articles/10023548-how-long-do-you-store-my-data) para obtener más información)
* Acceso restringido a datos de sesión del usuario
* Control del usuario sobre preferencias de entrenamiento de datos. Los usuarios de consumidor pueden cambiar su [configuración de privacidad](https://claude.ai/settings/privacy) en cualquier momento.

Para obtener detalles completos, consulte nuestros [Términos de Servicio Comerciales](https://www.anthropic.com/legal/commercial-terms) (para usuarios de Team, Enterprise y API) o [Términos de Consumidor](https://www.anthropic.com/legal/consumer-terms) (para usuarios de Free, Pro y Max) y [Política de Privacidad](https://www.anthropic.com/legal/privacy).

### Medidas de protección adicionales

* **Aprobación de solicitudes de red**: Las herramientas que realizan solicitudes de red requieren aprobación del usuario de forma predeterminada
* **Ventanas de contexto aisladas**: La obtención web utiliza una ventana de contexto separada para evitar inyectar solicitudes potencialmente maliciosas
* **Verificación de confianza**: Las primeras ejecuciones de base de código y los nuevos servidores MCP requieren verificación de confianza
  * Nota: La verificación de confianza está deshabilitada cuando se ejecuta de forma no interactiva con la bandera `-p`
* **Detección de inyección de comandos**: Los comandos bash sospechosos requieren aprobación manual incluso si fueron permitidos previamente
* **Coincidencia de cierre seguro**: Los comandos no coincidentes se establecen de forma predeterminada para requerir aprobación manual
* **Descripciones en lenguaje natural**: Los comandos bash complejos incluyen explicaciones para la comprensión del usuario
* **Almacenamiento seguro de credenciales**: Las claves API y tokens están encriptados. Consulte [Credential Management](/es/authentication#credential-management)

<Warning>
  **Riesgo de seguridad de WebDAV en Windows**: Cuando ejecute Claude Code en Windows, le recomendamos que no habilite WebDAV ni permita que Claude Code acceda a rutas como `\\*` que pueden contener subdirectorios de WebDAV. [WebDAV ha sido deprecado por Microsoft](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features#:~:text=The%20Webclient%20\(WebDAV\)%20service%20is%20deprecated) debido a riesgos de seguridad. Habilitar WebDAV puede permitir que Claude Code desencadene solicitudes de red a hosts remotos, eludiendo el sistema de permisos.
</Warning>

**Mejores prácticas para trabajar con contenido no confiable**:

1. Revise los comandos sugeridos antes de aprobarlos
2. Evite canalizar contenido no confiable directamente a Claude
3. Verifique los cambios propuestos en archivos críticos
4. Utilice máquinas virtuales (VMs) para ejecutar scripts y realizar llamadas de herramientas, especialmente cuando interactúe con servicios web externos
5. Reporte comportamiento sospechoso con `/bug`

<Warning>
  Aunque estas protecciones reducen significativamente el riesgo, ningún sistema es completamente
  inmune a todos los ataques. Siempre mantenga buenas prácticas de seguridad cuando trabaje
  con cualquier herramienta de IA.
</Warning>

## Seguridad de MCP

Claude Code permite a los usuarios configurar servidores del Protocolo de Contexto del Modelo (MCP). La lista de servidores MCP permitidos se configura en su código fuente, como parte de la configuración de Claude Code que los ingenieros verifican en el control de versiones.

Le recomendamos que escriba sus propios servidores MCP o utilice servidores MCP de proveedores en los que confíe. Puede configurar permisos de Claude Code para servidores MCP. Anthropic no gestiona ni audita ningún servidor MCP.

## Seguridad del IDE

Consulte [Seguridad y privacidad de VS Code](/es/vs-code#security-and-privacy) para obtener más información sobre cómo ejecutar Claude Code en un IDE.

## Seguridad de ejecución en la nube

Cuando utiliza [Claude Code en la web](/es/claude-code-on-the-web), hay controles de seguridad adicionales en su lugar:

* **Máquinas virtuales aisladas**: Cada sesión en la nube se ejecuta en una VM aislada gestionada por Anthropic
* **Controles de acceso a la red**: El acceso a la red está limitado de forma predeterminada y se puede configurar para deshabilitarse o permitir solo dominios específicos
* **Protección de credenciales**: La autenticación se maneja a través de un proxy seguro que utiliza una credencial con alcance dentro del sandbox, que luego se traduce a su token de autenticación de GitHub real
* **Restricciones de rama**: Las operaciones de inserción de Git están restringidas a la rama de trabajo actual
* **Registro de auditoría**: Todas las operaciones en entornos en la nube se registran para fines de cumplimiento y auditoría
* **Limpieza automática**: Los entornos en la nube se terminan automáticamente después de la finalización de la sesión

Para obtener más detalles sobre la ejecución en la nube, consulte [Claude Code en la web](/es/claude-code-on-the-web).

Las sesiones de [Remote Control](/es/remote-control) funcionan de manera diferente: la interfaz web se conecta a un proceso de Claude Code que se ejecuta en su máquina local. Toda la ejecución de código y el acceso a archivos permanecen locales, y los mismos datos que fluyen durante cualquier sesión local de Claude Code viajan a través de la API de Anthropic sobre TLS. No hay VMs en la nube ni sandboxing involucrados. La conexión utiliza múltiples credenciales de corta duración y alcance estrecho, cada una limitada a un propósito específico y expirando independientemente, para limitar el radio de explosión de cualquier credencial comprometida.

## Mejores prácticas de seguridad

### Trabajar con código sensible

* Revise todos los cambios sugeridos antes de aprobarlos
* Utilice configuración de permisos específica del proyecto para repositorios sensibles
* Considere utilizar [devcontainers](/es/devcontainer) para aislamiento adicional
* Audite regularmente su configuración de permisos con `/permissions`

### Seguridad del equipo

* Utilice [configuración gestionada](/es/settings#settings-files) para aplicar estándares organizacionales
* Comparta configuraciones de permisos aprobadas a través del control de versiones
* Capacite a los miembros del equipo sobre mejores prácticas de seguridad
* Monitoree el uso de Claude Code a través de [métricas de OpenTelemetry](/es/monitoring-usage)
* Audite o bloquee cambios de configuración durante sesiones con [hooks `ConfigChange`](/es/hooks#configchange)

### Reportar problemas de seguridad

Si descubre una vulnerabilidad de seguridad en Claude Code:

1. No la divulgue públicamente
2. Repórtela a través de nuestro [programa HackerOne](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability)
3. Incluya pasos de reproducción detallados
4. Permita tiempo para que abordemos el problema antes de la divulgación pública

## Recursos relacionados

* [Sandboxing](/es/sandboxing) - Aislamiento del sistema de archivos y red para comandos bash
* [Permissions](/es/permissions) - Configure permisos y controles de acceso
* [Monitoring usage](/es/monitoring-usage) - Rastree y audite la actividad de Claude Code
* [Development containers](/es/devcontainer) - Entornos seguros y aislados
* [Anthropic Trust Center](https://trust.anthropic.com) - Certificaciones de seguridad y cumplimiento
