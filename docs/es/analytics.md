> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Rastrear el uso del equipo con análisis

> Ver métricas de uso de Claude Code, rastrear la adopción y medir la velocidad de ingeniería en el panel de análisis.

Claude Code proporciona paneles de análisis para ayudar a las organizaciones a comprender los patrones de uso de desarrolladores, rastrear métricas de contribución y medir cómo Claude Code impacta la velocidad de ingeniería. Acceda al panel para su plan:

| Plan                          | URL del panel                                                              | Incluye                                                                                                           | Más información                                        |
| ----------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Claude for Teams / Enterprise | [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code) | Métricas de uso, métricas de contribución con integración de GitHub, tabla de clasificación, exportación de datos | [Detalles](#access-analytics-for-teams-and-enterprise) |
| API (Claude Console)          | [platform.claude.com/claude-code](https://platform.claude.com/claude-code) | Métricas de uso, seguimiento de gastos, información del equipo                                                    | [Detalles](#access-analytics-for-api-customers)        |

## Acceder a análisis para Teams y Enterprise

Navegue a [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code). Los administradores y propietarios pueden ver el panel.

El panel de Teams y Enterprise incluye:

* **Métricas de uso**: líneas de código aceptadas, tasa de aceptación de sugerencias, usuarios activos diarios y sesiones
* **Métricas de contribución**: PRs y líneas de código enviadas con asistencia de Claude Code, con [integración de GitHub](#enable-contribution-metrics)
* **Tabla de clasificación**: principales contribuyentes clasificados por uso de Claude Code
* **Exportación de datos**: descargar datos de contribución como CSV para informes personalizados

### Habilitar métricas de contribución

<Note>
  Las métricas de contribución están en versión beta pública y disponibles en los planes Claude for Teams y Claude for Enterprise. Estas métricas solo cubren usuarios dentro de su organización de claude.ai. El uso a través de la API de Claude Console o integraciones de terceros no se incluye.
</Note>

Los datos de uso y adopción están disponibles para todas las cuentas de Claude for Teams y Claude for Enterprise. Las métricas de contribución requieren configuración adicional para conectar su organización de GitHub.

Necesita el rol de propietario para configurar los ajustes de análisis. Un administrador de GitHub debe instalar la aplicación de GitHub.

<Warning>
  Las métricas de contribución no están disponibles para organizaciones con [Retención de datos cero](/es/zero-data-retention) habilitada. El panel de análisis mostrará solo métricas de uso.
</Warning>

<Steps>
  <Step title="Instalar la aplicación de GitHub">
    Un administrador de GitHub instala la aplicación Claude GitHub en la cuenta de GitHub de su organización en [github.com/apps/claude](https://github.com/apps/claude).
  </Step>

  <Step title="Habilitar análisis de Claude Code">
    Un propietario de Claude navega a [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) y habilita la función de análisis de Claude Code.
  </Step>

  <Step title="Habilitar análisis de GitHub">
    En la misma página, habilite el botón de alternancia "GitHub analytics".
  </Step>

  <Step title="Autenticarse con GitHub">
    Complete el flujo de autenticación de GitHub y seleccione qué organizaciones de GitHub incluir en el análisis.
  </Step>
</Steps>

Los datos generalmente aparecen dentro de 24 horas después de habilitar, con actualizaciones diarias. Si no aparecen datos, puede ver uno de estos mensajes:

* **"GitHub app required"**: instale la aplicación de GitHub para ver métricas de contribución
* **"Data processing in progress"**: vuelva a verificar en unos días y confirme que la aplicación de GitHub está instalada si los datos no aparecen

Las métricas de contribución admiten GitHub Cloud y GitHub Enterprise Server.

### Revisar métricas de resumen

<Note>
  Estas métricas son deliberadamente conservadoras y representan una subestimación del impacto real de Claude Code. Solo se cuentan las líneas y PRs donde hay alta confianza en la participación de Claude Code.
</Note>

El panel muestra estas métricas de resumen en la parte superior:

* **PRs with CC**: recuento total de solicitudes de extracción fusionadas que contienen al menos una línea de código escrita con Claude Code
* **Lines of code with CC**: líneas totales de código en todos los PRs fusionados que fueron escritas con asistencia de Claude Code. Solo se cuentan las "líneas efectivas": líneas con más de 3 caracteres después de la normalización, excluyendo líneas vacías y líneas con solo corchetes o puntuación trivial.
* **PRs with Claude Code (%)**: porcentaje de todos los PRs fusionados que contienen código asistido por Claude Code
* **Suggestion accept rate**: porcentaje de veces que los usuarios aceptan las sugerencias de edición de código de Claude Code, incluido el uso de herramientas Edit, Write y NotebookEdit
* **Lines of code accepted**: líneas totales de código escritas por Claude Code que los usuarios han aceptado en sus sesiones. Esto excluye sugerencias rechazadas y no rastrea eliminaciones posteriores.

### Explorar los gráficos

El panel incluye varios gráficos para visualizar tendencias a lo largo del tiempo.

#### Rastrear adopción

El gráfico de Adopción muestra tendencias de uso diario:

* **users**: usuarios activos diarios
* **sessions**: número de sesiones activas de Claude Code por día

#### Medir PRs por usuario

Este gráfico muestra la actividad de desarrolladores individuales a lo largo del tiempo:

* **PRs per user**: número total de PRs fusionados por día dividido por usuarios activos diarios
* **users**: usuarios activos diarios

Utilice esto para comprender cómo cambia la productividad individual a medida que aumenta la adopción de Claude Code.

#### Ver desglose de solicitudes de extracción

El gráfico de Pull requests muestra un desglose diario de PRs fusionados:

* **PRs with CC**: solicitudes de extracción que contienen código asistido por Claude Code
* **PRs without CC**: solicitudes de extracción sin código asistido por Claude Code

Cambie a la vista **Lines of code** para ver el mismo desglose por líneas de código en lugar de recuento de PR.

#### Encontrar principales contribuyentes

La Tabla de clasificación muestra los 10 principales usuarios clasificados por volumen de contribución. Alterne entre:

* **Pull requests**: muestra PRs con Claude Code vs Todos los PRs para cada usuario
* **Lines of code**: muestra líneas con Claude Code vs Todas las líneas para cada usuario

Haga clic en **Export all users** para descargar datos de contribución completos para todos los usuarios como archivo CSV. La exportación incluye todos los usuarios, no solo los 10 principales mostrados.

### Atribución de PR

Cuando las métricas de contribución están habilitadas, Claude Code analiza las solicitudes de extracción fusionadas para determinar qué código fue escrito con asistencia de Claude Code. Esto se hace haciendo coincidir la actividad de sesión de Claude Code con el código en cada PR.

#### Criterios de etiquetado

Los PRs se etiquetan como "with Claude Code" si contienen al menos una línea de código escrita durante una sesión de Claude Code. El sistema utiliza coincidencia conservadora: solo el código donde hay alta confianza en la participación de Claude Code se cuenta como asistido.

#### Proceso de atribución

Cuando se fusiona una solicitud de extracción:

1. Se extraen las líneas agregadas del diff de PR
2. Se identifican las sesiones de Claude Code que editaron archivos coincidentes dentro de una ventana de tiempo
3. Las líneas de PR se comparan con la salida de Claude Code utilizando múltiples estrategias
4. Se calculan métricas para líneas asistidas por IA y líneas totales

Antes de la comparación, las líneas se normalizan: se recorta el espacio en blanco, se contraen múltiples espacios, se estandarizan las comillas y el texto se convierte a minúsculas.

Las solicitudes de extracción fusionadas que contienen líneas asistidas por Claude Code se etiquetan como `claude-code-assisted` en GitHub.

#### Ventana de tiempo

Se consideran sesiones de 21 días antes a 2 días después de la fecha de fusión de PR para la coincidencia de atribución.

#### Archivos excluidos

Ciertos archivos se excluyen automáticamente del análisis porque se generan automáticamente:

* Archivos de bloqueo: package-lock.json, yarn.lock, Cargo.lock y similares
* Código generado: salidas de Protobuf, artefactos de compilación, archivos minificados
* Directorios de compilación: dist/, build/, node\_modules/, target/
* Accesorios de prueba: instantáneas, cassettes, datos simulados
* Líneas con más de 1.000 caracteres, que probablemente sean minificadas o generadas

#### Notas de atribución

Tenga en cuenta estos detalles adicionales al interpretar datos de atribución:

* El código sustancialmente reescrito por desarrolladores, con más del 20% de diferencia, no se atribuye a Claude Code
* Las sesiones fuera de la ventana de 21 días no se consideran
* El algoritmo no considera la rama de origen o destino de PR al realizar la atribución

### Obtener lo máximo de los análisis

Utilice métricas de contribución para demostrar ROI, identificar patrones de adopción y encontrar miembros del equipo que puedan ayudar a otros a comenzar.

#### Monitorear adopción

Rastreé el gráfico de Adopción y los recuentos de usuarios para identificar:

* Usuarios activos que pueden compartir mejores prácticas
* Tendencias generales de adopción en su organización
* Caídas en el uso que pueden indicar fricción o problemas

#### Medir ROI

Las métricas de contribución ayudan a responder "¿Vale la pena esta herramienta la inversión?" con datos de su propio código base:

* Rastreé cambios en PRs por usuario a lo largo del tiempo a medida que aumenta la adopción
* Compare PRs y líneas de código enviadas con y sin Claude Code
* Utilice junto con [métricas DORA](https://dora.dev/), velocidad de sprint u otros KPI de ingeniería para comprender cambios por adoptar Claude Code

#### Identificar usuarios avanzados

La Tabla de clasificación le ayuda a encontrar miembros del equipo con alta adopción de Claude Code que pueden:

* Compartir técnicas de prompting y flujos de trabajo con el equipo
* Proporcionar comentarios sobre qué está funcionando bien
* Ayudar a incorporar nuevos usuarios

#### Acceder a datos mediante programación

Para consultar estos datos a través de GitHub, busque PRs etiquetados con `claude-code-assisted`.

## Acceder a análisis para clientes de API

Los clientes de API que utilizan Claude Console pueden acceder a análisis en [platform.claude.com/claude-code](https://platform.claude.com/claude-code). Necesita el permiso UsageView para acceder al panel, que se otorga a los roles Developer, Billing, Admin, Owner y Primary Owner.

<Note>
  Las métricas de contribución con integración de GitHub no están disponibles actualmente para clientes de API. El panel de Console muestra solo métricas de uso y gastos.
</Note>

El panel de Console muestra:

* **Lines of code accepted**: líneas totales de código escritas por Claude Code que los usuarios han aceptado en sus sesiones. Esto excluye sugerencias rechazadas y no rastrea eliminaciones posteriores.
* **Suggestion accept rate**: porcentaje de veces que los usuarios aceptan el uso de herramientas de edición de código, incluidas las herramientas Edit, Write y NotebookEdit.
* **Activity**: usuarios activos diarios y sesiones mostradas en un gráfico.
* **Spend**: costos diarios de API en dólares junto con el recuento de usuarios.

### Ver información del equipo

La tabla de información del equipo muestra métricas por usuario:

* **Members**: todos los usuarios que se han autenticado en Claude Code. Los usuarios de clave API se muestran por identificador de clave, los usuarios de OAuth se muestran por dirección de correo electrónico.
* **Spend this month**: costos totales de API por usuario para el mes actual.
* **Lines this month**: total por usuario de líneas de código aceptadas para el mes actual.

<Note>
  Las cifras de gastos en el panel de Console son estimaciones para fines de análisis. Para costos reales, consulte su página de facturación.
</Note>

## Recursos relacionados

* [Monitoring with OpenTelemetry](/es/monitoring-usage): exportar métricas y eventos en tiempo real a su pila de observabilidad
* [Manage costs effectively](/es/costs): establecer límites de gastos y optimizar el uso de tokens
* [Permissions](/es/permissions): configurar roles y permisos
