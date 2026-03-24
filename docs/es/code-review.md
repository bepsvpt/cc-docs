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

Para ejecutar Claude en su propia infraestructura de CI en lugar de este servicio administrado, consulte [GitHub Actions](/es/github-actions) o [GitLab CI/CD](/es/gitlab-ci-cd).

Esta página cubre:

* [Cómo funcionan las revisiones](#how-reviews-work)
* [Configuración](#set-up-code-review)
* [Personalización de revisiones](#customize-reviews) con `CLAUDE.md` y `REVIEW.md`
* [Precios](#pricing)

## Cómo funcionan las revisiones

Una vez que un administrador [habilita Code Review](#set-up-code-review) para su organización, las revisiones se activan cuando se abre un PR, en cada push, o cuando se solicita manualmente, según el comportamiento configurado del repositorio. Comentar `@claude review` [inicia revisiones en un PR](#manually-trigger-reviews) en cualquier modo.

Cuando se ejecuta una revisión, múltiples agentes analizan el diff y el código circundante en paralelo en la infraestructura de Anthropic. Cada agente busca una clase diferente de problema, luego un paso de verificación verifica los candidatos contra el comportamiento real del código para filtrar falsos positivos. Los resultados se desduplican, se clasifican por severidad y se publican como comentarios en línea en las líneas específicas donde se encontraron problemas. Si no se encuentran problemas, Claude publica un breve comentario de confirmación en el PR.

Las revisiones se escalan en costo con el tamaño y la complejidad del PR, completándose en un promedio de 20 minutos. Los administradores pueden monitorear la actividad de revisión y el gasto a través del [panel de análisis](#view-usage).

### Niveles de severidad

Cada hallazgo se etiqueta con un nivel de severidad:

| Marcador | Severidad    | Significado                                                                  |
| :------- | :----------- | :--------------------------------------------------------------------------- |
| 🔴       | Normal       | Un error que debe corregirse antes de fusionar                               |
| 🟡       | Nit          | Un problema menor, vale la pena corregir pero no bloqueante                  |
| 🟣       | Preexistente | Un error que existe en la base de código pero no fue introducido por este PR |

Los hallazgos incluyen una sección de razonamiento extendido contraíble que puede expandir para entender por qué Claude marcó el problema y cómo verificó el problema.

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
    * **Manual**: las revisiones comienzan solo cuando alguien [comenta `@claude review` en un PR](#manually-trigger-reviews); los push posteriores a ese PR se revisan automáticamente

    Revisar en cada push ejecuta la mayoría de revisiones y cuesta más. El modo manual es útil para repositorios de alto tráfico donde desea optar por revisión en PR específicos, o para comenzar a revisar sus PR solo cuando estén listos.
  </Step>
</Steps>

La tabla de repositorios también muestra el costo promedio por revisión para cada repositorio basado en la actividad reciente. Use el menú de acciones de fila para activar o desactivar Code Review por repositorio, o para eliminar un repositorio por completo.

Para verificar la configuración, abra un PR de prueba. Si eligió un disparador automático, aparece una ejecución de verificación llamada **Claude Code Review** dentro de unos minutos. Si eligió Manual, comente `@claude review` en el PR para iniciar la primera revisión. Si no aparece ninguna ejecución de verificación, confirme que el repositorio esté listado en su configuración de administrador y que la Claude GitHub App tenga acceso a él.

## Disparar revisiones manualmente

Comente `@claude review` en una solicitud de extracción para iniciar una revisión y optar ese PR en revisiones activadas por push en adelante. Esto funciona independientemente del disparador configurado del repositorio: úselo para optar por PR específicos en revisión en modo Manual, u obtener una re-revisión inmediata en otros modos. De cualquier forma, los push a ese PR activan revisiones a partir de entonces.

Para que el comentario active una revisión:

* Publíquelo como un comentario de PR de nivel superior, no un comentario en línea en una línea de diff
* Ponga `@claude review` al inicio del comentario
* Debe tener acceso de propietario, miembro o colaborador al repositorio
* El PR debe estar abierto y no ser un borrador

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

```markdown  theme={null}
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

Code Review se factura según el uso de tokens. Las revisiones promedian \$15-25, escalando con el tamaño del PR, la complejidad de la base de código y cuántos problemas requieren verificación. El uso de Code Review se factura por separado a través de [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) y no cuenta contra el uso incluido de su plan.

El disparador de revisión que elija afecta el costo total:

* **Once after PR creation**: se ejecuta una vez por PR
* **After every push**: se ejecuta en cada push, multiplicando el costo por el número de push
* **Manual**: sin revisiones hasta que alguien comente `@claude review` en un PR

En cualquier modo, comentar `@claude review` [opta el PR en revisiones activadas por push](#manually-trigger-reviews), por lo que se acumula costo adicional por push después de ese comentario.

Los costos aparecen en su factura de Anthropic independientemente de si su organización usa AWS Bedrock o Google Vertex AI para otras características de Claude Code. Para establecer un límite de gasto mensual para Code Review, vaya a [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) y configure el límite para el servicio Claude Code Review.

Monitoree el gasto a través del gráfico de costo semanal en [analytics](#view-usage) o la columna de costo promedio por repositorio en la configuración de administrador.

## Recursos relacionados

Code Review está diseñado para funcionar junto con el resto de Claude Code. Si desea ejecutar revisiones localmente antes de abrir un PR, necesita una configuración autohospedada, o desea profundizar en cómo `CLAUDE.md` forma el comportamiento de Claude en todas las herramientas, estas páginas son buenos siguientes pasos:

* [Plugins](/es/discover-plugins): explore el mercado de plugins, incluido un plugin `code-review` para ejecutar revisiones bajo demanda localmente antes de hacer push
* [GitHub Actions](/es/github-actions): ejecute Claude en sus propios flujos de trabajo de GitHub Actions para automatización personalizada más allá de la revisión de código
* [GitLab CI/CD](/es/gitlab-ci-cd): integración de Claude autohospedada para canalizaciones de GitLab
* [Memory](/es/memory): cómo funcionan los archivos `CLAUDE.md` en Claude Code
* [Analytics](/es/analytics): rastrear el uso de Claude Code más allá de la revisión de código
