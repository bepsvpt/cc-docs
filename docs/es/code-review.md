> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Configure revisiones automatizadas de PR que detecten errores lógicos, vulnerabilidades de seguridad y regresiones mediante análisis multiagente de su base de código completa

<Note>
  Code Review está en vista previa de investigación, disponible para suscripciones de [Teams y Enterprise](https://claude.ai/admin-settings/claude-code). No está disponible para organizaciones con [Zero Data Retention](/es/zero-data-retention) habilitado.
</Note>

Code Review analiza sus solicitudes de extracción de GitHub y publica hallazgos como comentarios en línea en las líneas de código donde encontró problemas. Una flota de agentes especializados examina los cambios de código en el contexto de su base de código completa, buscando errores lógicos, vulnerabilidades de seguridad, casos límite rotos y regresiones sutiles.

Los hallazgos se etiquetan por severidad y no aprueban ni bloquean su PR, por lo que los flujos de trabajo de revisión existentes permanecen intactos. Puede ajustar lo que Claude marca agregando un archivo `CLAUDE.md` o `REVIEW.md` a su repositorio.

Para ejecutar Claude en su propia infraestructura de CI en lugar de este servicio administrado, consulte [GitHub Actions](/es/github-actions) o [GitLab CI/CD](/es/gitlab-ci-cd). Para repositorios en una instancia de GitHub autohospedada, consulte [GitHub Enterprise Server](/es/github-enterprise-server).

Esta página cubre:

* [Cómo funcionan las revisiones](#how-reviews-work)
* [Configuración](#set-up-code-review)
* [Disparar revisiones manualmente](#manually-trigger-reviews) con `@claude review` y `@claude review once`
* [Personalizar revisiones](#customize-reviews) con `CLAUDE.md` y `REVIEW.md`
* [Precios](#pricing)
* [Solución de problemas](#troubleshooting) ejecuciones fallidas y comentarios faltantes

## Cómo funcionan las revisiones

Una vez que un administrador [habilita Code Review](#set-up-code-review) para su organización, las revisiones se activan cuando se abre un PR, en cada push, o cuando se solicita manualmente, según el comportamiento configurado del repositorio. Comentar `@claude review` [inicia revisiones en un PR](#manually-trigger-reviews) en cualquier modo.

Cuando se ejecuta una revisión, múltiples agentes analizan el diff y el código circundante en paralelo en la infraestructura de Anthropic. Cada agente busca una clase diferente de problema, luego un paso de verificación verifica los candidatos contra el comportamiento real del código para filtrar falsos positivos. Los resultados se desduplican, se clasifican por severidad y se publican como comentarios en línea en las líneas específicas donde se encontraron problemas. Si no se encuentran problemas, Claude publica un breve comentario de confirmación en el PR.

Las revisiones se escalan en costo con el tamaño y la complejidad del PR, completándose en un promedio de 20 minutos. Los administradores pueden monitorear la actividad de revisión y el gasto a través del [panel de análisis](#view-usage).

### Niveles de severidad

Cada hallazgo se etiqueta con un nivel de severidad:

| Marcador | Severidad    | Significado                                                                  |
| :------- | :----------- | :--------------------------------------------------------------------------- |
| 🔴       | Importante   | Un error que debe corregirse antes de fusionar                               |
| 🟡       | Nit          | Un problema menor, vale la pena corregir pero no bloqueante                  |
| 🟣       | Preexistente | Un error que existe en la base de código pero no fue introducido por este PR |

Los hallazgos incluyen una sección de razonamiento extendido contraíble que puede expandir para entender por qué Claude marcó el problema y cómo verificó el problema.

### Salida de ejecución de verificación

Más allá de los comentarios de revisión en línea, cada revisión completa la ejecución de verificación **Claude Code Review** que aparece junto a sus verificaciones de CI. Expanda su enlace **Details** para ver un resumen de cada hallazgo en un solo lugar, ordenado por severidad:

| Severidad     | Archivo:Línea             | Problema                                                                                                |
| ------------- | ------------------------- | ------------------------------------------------------------------------------------------------------- |
| 🔴 Importante | `src/auth/session.ts:142` | La actualización de token corre una carrera con el cierre de sesión, dejando sesiones obsoletas activas |
| 🟡 Nit        | `src/auth/session.ts:88`  | `parseExpiry` devuelve silenciosamente 0 en entrada malformada                                          |

Cada hallazgo también aparece como una anotación en la pestaña **Files changed**, marcado directamente en las líneas de diff relevantes. Los hallazgos importantes se representan con un marcador rojo, los nits con una advertencia amarilla y los errores preexistentes con un aviso gris. Las anotaciones y la tabla de severidad se escriben en la ejecución de verificación independientemente de los comentarios de revisión en línea, por lo que permanecen disponibles incluso si GitHub rechaza un comentario en línea en una línea que se movió.

La ejecución de verificación siempre se completa con una conclusión neutral para que nunca bloquee la fusión a través de reglas de protección de rama. Si desea bloquear fusiones en hallazgos de Code Review, lea el desglose de severidad de la salida de ejecución de verificación en su propio CI. La última línea del texto de Details es un comentario legible por máquina que su flujo de trabajo puede analizar con `gh` y jq:

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

Esto devuelve un objeto JSON con conteos por severidad, por ejemplo `{"normal": 2, "nit": 1, "pre_existing": 0}`. La clave `normal` contiene el conteo de hallazgos Importantes; un valor distinto de cero significa que Claude encontró al menos un error que vale la pena corregir antes de fusionar.

### Qué verifica Code Review

Por defecto, Code Review se enfoca en la corrección: errores que romperían la producción, no preferencias de formato o cobertura de pruebas faltante. Puede expandir lo que verifica [agregando archivos de orientación](#customize-reviews) a su repositorio.

## Configurar Code Review

Un administrador habilita Code Review una vez para la organización y selecciona qué repositorios incluir.

<Steps>
  <Step title="Abrir configuración de administrador de Claude Code">
    Vaya a [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) y encuentre la sección Code Review. Necesita acceso de administrador a su organización de Claude y permiso para instalar GitHub Apps en su organización de GitHub.
  </Step>

  <Step title="Iniciar configuración">
    Haga clic en **Setup**. Esto inicia el flujo de instalación de GitHub App.
  </Step>

  <Step title="Instalar la Claude GitHub App">
    Siga las indicaciones para instalar la Claude GitHub App en su organización de GitHub. La aplicación solicita estos permisos de repositorio:

    * **Contents**: lectura y escritura
    * **Issues**: lectura y escritura
    * **Pull requests**: lectura y escritura

    Code Review utiliza acceso de lectura a contenidos y acceso de escritura a solicitudes de extracción. El conjunto de permisos más amplio también admite [GitHub Actions](/es/github-actions) si lo habilita más adelante.
  </Step>

  <Step title="Seleccionar repositorios">
    Elija qué repositorios habilitar para Code Review. Si no ve un repositorio, asegúrese de haber dado a la Claude GitHub App acceso a él durante la instalación. Puede agregar más repositorios más adelante.
  </Step>

  <Step title="Establecer disparadores de revisión por repositorio">
    Después de que se complete la configuración, la sección Code Review muestra sus repositorios en una tabla. Para cada repositorio, use el menú desplegable **Review Behavior** para elegir cuándo se ejecutan las revisiones:

    * **Once after PR creation**: la revisión se ejecuta una vez cuando se abre un PR o se marca como listo para revisión
    * **After every push**: la revisión se ejecuta en cada push a la rama del PR, detectando nuevos problemas a medida que el PR evoluciona y resolviendo automáticamente los hilos cuando corrige problemas marcados
    * **Manual**: las revisiones comienzan solo cuando alguien [comenta `@claude review` o `@claude review once` en un PR](#manually-trigger-reviews); `@claude review` también suscribe el PR a revisiones en push posteriores

    Revisar en cada push ejecuta la mayoría de revisiones y cuesta más. El modo manual es útil para repositorios de alto tráfico donde desea optar por revisión en PR específicos, o para comenzar a revisar sus PR solo cuando estén listos.
  </Step>
</Steps>

La tabla de repositorios también muestra el costo promedio por revisión para cada repositorio basado en la actividad reciente. Use el menú de acciones de fila para activar o desactivar Code Review por repositorio, o para eliminar un repositorio por completo.

Para verificar la configuración, abra un PR de prueba. Si eligió un disparador automático, aparece una ejecución de verificación llamada **Claude Code Review** dentro de unos minutos. Si eligió Manual, comente `@claude review` en el PR para iniciar la primera revisión. Si no aparece ninguna ejecución de verificación, confirme que el repositorio esté listado en su configuración de administrador y que la Claude GitHub App tenga acceso a él.

## Disparar revisiones manualmente

Dos comandos de comentario inician una revisión bajo demanda. Ambos funcionan independientemente del disparador configurado del repositorio, por lo que puede usarlos para optar por PR específicos en revisión en modo Manual o para obtener una re-revisión inmediata en otros modos.

| Comando               | Lo que hace                                                                      |
| :-------------------- | :------------------------------------------------------------------------------- |
| `@claude review`      | Inicia una revisión y suscribe el PR a revisiones activadas por push en adelante |
| `@claude review once` | Inicia una única revisión sin suscribir el PR a push futuros                     |

Use `@claude review once` cuando desee comentarios sobre el estado actual de un PR pero no desee que cada push posterior incurra en una revisión. Esto es útil para PR de larga duración con push frecuentes, o cuando desea una segunda opinión única sin cambiar el comportamiento de revisión del PR.

Para que cualquiera de los comandos active una revisión:

* Publíquelo como un comentario de PR de nivel superior, no un comentario en línea en una línea de diff
* Ponga el comando al inicio del comentario, con `once` en la misma línea si está usando la forma de un solo disparo
* Debe tener acceso de propietario, miembro o colaborador al repositorio
* El PR debe estar abierto

A diferencia de los disparadores automáticos, los disparadores manuales se ejecutan en PR de borrador, ya que una solicitud explícita señala que desea la revisión ahora independientemente del estado de borrador.

Si una revisión ya se está ejecutando en ese PR, la solicitud se pone en cola hasta que se complete la revisión en progreso. Puede monitorear el progreso a través de la ejecución de verificación en el PR.

## Personalizar revisiones

Code Review lee dos archivos de su repositorio para guiar lo que marca. Ambos son aditivos además de las verificaciones de corrección predeterminadas:

* **`CLAUDE.md`**: instrucciones de proyecto compartidas que Claude Code utiliza para todas las tareas, no solo revisiones. Úselo cuando la orientación también se aplique a sesiones interactivas de Claude Code.
* **`REVIEW.md`**: orientación solo de revisión, leída exclusivamente durante revisiones de código. Úselo para reglas que son estrictamente sobre qué marcar u omitir durante la revisión y que abarrotarían su `CLAUDE.md` general.

### CLAUDE.md

Code Review lee sus archivos `CLAUDE.md` del repositorio y trata las violaciones recién introducidas como hallazgos de nivel nit. Esto funciona bidireccionalamente: si su PR cambia el código de una manera que hace que una declaración `CLAUDE.md` esté desactualizada, Claude marca que los documentos necesitan actualización también.

Claude lee archivos `CLAUDE.md` en cada nivel de su jerarquía de directorios, por lo que las reglas en el `CLAUDE.md` de un subdirectorio se aplican solo a archivos bajo esa ruta. Consulte la [documentación de memoria](/es/memory) para obtener más información sobre cómo funciona `CLAUDE.md`.

Para orientación específica de revisión que no desea aplicar a sesiones generales de Claude Code, use [`REVIEW.md`](#review-md) en su lugar.

### REVIEW\.md

Agregue un archivo `REVIEW.md` a la raíz de su repositorio para reglas específicas de revisión. Úselo para codificar:

* Directrices de estilo de empresa o equipo: "preferir retornos tempranos sobre condicionales anidados"
* Convenciones específicas de lenguaje o marco no cubiertas por linters
* Cosas que Claude siempre debe marcar: "cualquier nueva ruta de API debe tener una prueba de integración"
* Cosas que Claude debe omitir: "no comentar sobre formato en código generado bajo `/gen/`"

Ejemplo `REVIEW.md`:

```markdown theme={null}
# Directrices de revisión de código

## Siempre verificar
- Los nuevos puntos finales de API tienen pruebas de integración correspondientes
- Las migraciones de base de datos son compatibles hacia atrás
- Los mensajes de error no filtran detalles internos a los usuarios

## Estilo
- Preferir declaraciones `match` sobre verificaciones `isinstance` encadenadas
- Usar registro estructurado, no interpolación de f-string en llamadas de registro

## Omitir
- Archivos generados bajo `src/gen/`
- Cambios solo de formato en archivos `*.lock`
```

Claude descubre automáticamente `REVIEW.md` en la raíz del repositorio. No se necesita configuración.

## Ver uso

Vaya a [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) para ver la actividad de Code Review en toda su organización. El panel muestra:

| Sección              | Lo que muestra                                                                                                  |
| :------------------- | :-------------------------------------------------------------------------------------------------------------- |
| PRs reviewed         | Conteo diario de solicitudes de extracción revisadas durante el rango de tiempo seleccionado                    |
| Cost weekly          | Gasto semanal en Code Review                                                                                    |
| Feedback             | Conteo de comentarios de revisión que se resolvieron automáticamente porque un desarrollador abordó el problema |
| Repository breakdown | Conteos por repositorio de PR revisados y comentarios resueltos                                                 |

La tabla de repositorios en la configuración de administrador también muestra el costo promedio por revisión para cada repositorio.

## Precios

Code Review se factura según el uso de tokens. Cada revisión promedia \$15-25 en costo, escalando con el tamaño del PR, la complejidad de la base de código y cuántos problemas requieren verificación. El uso de Code Review se factura por separado a través de [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) y no cuenta contra el uso incluido de su plan.

El disparador de revisión que elija afecta el costo total:

* **Once after PR creation**: se ejecuta una vez por PR
* **After every push**: se ejecuta en cada push, multiplicando el costo por el número de push
* **Manual**: sin revisiones hasta que alguien comente `@claude review` en un PR

En cualquier modo, comentar `@claude review` [opta el PR en revisiones activadas por push](#manually-trigger-reviews), por lo que se acumula costo adicional por push después de ese comentario. Para ejecutar una única revisión sin suscribirse a push futuros, comente `@claude review once` en su lugar.

Los costos aparecen en su factura de Anthropic independientemente de si su organización usa AWS Bedrock o Google Vertex AI para otras características de Claude Code. Para establecer un límite de gasto mensual para Code Review, vaya a [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) y configure el límite para el servicio Claude Code Review.

Monitoree el gasto a través del gráfico de costo semanal en [analytics](#view-usage) o la columna de costo promedio por repositorio en la configuración de administrador.

## Solución de problemas

Las ejecuciones de revisión son de mejor esfuerzo. Una ejecución fallida nunca bloquea su PR, pero tampoco se reintenta por sí sola. Esta sección cubre cómo recuperarse de una ejecución fallida y dónde buscar cuando la ejecución de verificación reporta problemas que no puede encontrar.

### Reactivar una revisión fallida o agotada por tiempo

Cuando la infraestructura de revisión golpea un error interno o excede su límite de tiempo, la ejecución de verificación se completa con un título de **Code review encountered an error** o **Code review timed out**. La conclusión sigue siendo neutral, por lo que nada bloquea su fusión, pero no se publican hallazgos.

Para ejecutar la revisión nuevamente, comente `@claude review once` en el PR. Esto inicia una revisión nueva sin suscribir el PR a push futuros. Si el PR ya está suscrito a revisiones activadas por push, hacer push de un nuevo commit también inicia una nueva revisión.

El botón **Re-run** en la pestaña Checks de GitHub no reactiva Code Review. Use el comando de comentario o un nuevo push en su lugar.

### Encontrar problemas que no se muestran como comentarios en línea

Si el título de la ejecución de verificación dice que se encontraron problemas pero no ve comentarios de revisión en línea en el diff, busque en estas otras ubicaciones donde se muestran los hallazgos:

* **Check run Details**: haga clic en **Details** junto a la verificación Claude Code Review en la pestaña Checks. La tabla de severidad enumera cada hallazgo con su archivo, línea y resumen independientemente de si el comentario en línea fue aceptado.
* **Files changed annotations**: abra la pestaña **Files changed** en el PR. Los hallazgos se representan como anotaciones adjuntas directamente a las líneas de diff, separadas de los comentarios de revisión.
* **Review body**: si hizo push al PR mientras se ejecutaba una revisión, algunos hallazgos pueden hacer referencia a líneas que ya no existen en el diff actual. Esos aparecen bajo un encabezado **Additional findings** en el texto del cuerpo de revisión en lugar de como comentarios en línea.

## Recursos relacionados

Code Review está diseñado para funcionar junto con el resto de Claude Code. Si desea ejecutar revisiones localmente antes de abrir un PR, necesita una configuración autohospedada, o desea profundizar en cómo `CLAUDE.md` forma el comportamiento de Claude en todas las herramientas, estas páginas son buenos siguientes pasos:

* [Plugins](/es/discover-plugins): explore el mercado de plugins, incluido un plugin `code-review` para ejecutar revisiones bajo demanda localmente antes de hacer push
* [GitHub Actions](/es/github-actions): ejecute Claude en sus propios flujos de trabajo de GitHub Actions para automatización personalizada más allá de la revisión de código
* [GitLab CI/CD](/es/gitlab-ci-cd): integración de Claude autohospedada para canalizaciones de GitLab
* [Memory](/es/memory): cómo funcionan los archivos `CLAUDE.md` en Claude Code
* [Analytics](/es/analytics): rastrear el uso de Claude Code más allá de la revisión de código
