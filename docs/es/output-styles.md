> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Estilos de salida

> Adapte Claude Code para usos más allá de la ingeniería de software

Los estilos de salida cambian cómo responde Claude, no lo que Claude sabe. Modifican el mensaje del sistema para establecer el rol, el tono y el formato de salida. Use uno cuando siga re-solicitando la misma voz o formato en cada turno, o cuando desee que Claude actúe como algo diferente a un ingeniero de software.

Un estilo de salida personalizado agrega sus instrucciones al mensaje del sistema y le permite elegir si desea mantener las instrucciones integradas de ingeniería de software de Claude Code. Manténgalas cuando esté cambiando cómo Claude se comunica pero sigue codificando, como siempre respondiendo con un diagrama. Déjelas fuera cuando Claude no esté haciendo ingeniería de software en absoluto, como un asistente de escritura o analista de datos.

Para instrucciones sobre su proyecto, convenciones o base de código, use [CLAUDE.md](/es/memory) en su lugar.

## Estilos de salida integrados

El estilo de salida **Default** de Claude Code es el mensaje del sistema existente, diseñado para ayudarle a completar tareas de ingeniería de software de manera eficiente.

Hay tres estilos de salida integrados adicionales:

* **Proactive**: Claude se ejecuta inmediatamente, realiza suposiciones razonables en lugar de pausarse para decisiones rutinarias, y prefiere la acción sobre la planificación. Esto aplica la misma orientación que [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode) sin cambiar su modo de permisos, por lo que aún ve mensajes de permisos antes de que se ejecuten las herramientas.

* **Explanatory**: Proporciona "Insights" educativos entre ayudarle a completar tareas de ingeniería de software. Le ayuda a entender las opciones de implementación y los patrones de la base de código.

* **Learning**: Modo colaborativo de aprendizaje práctico donde Claude no solo compartirá "Insights" mientras codifica, sino que también le pedirá que contribuya con pequeñas piezas de código estratégicas. Claude Code agregará marcadores `TODO(human)` en su código para que usted implemente.

## Cambiar su estilo de salida

Ejecute `/config` y seleccione **Output style** para elegir un estilo de un menú. Su selección se guarda en `.claude/settings.local.json` en el [nivel de proyecto local](/es/settings).

Para establecer un estilo sin el menú, edite el campo `outputStyle` directamente en un archivo de configuración:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Debido a que el estilo de salida se establece en el mensaje del sistema al inicio de la sesión, los cambios surten efecto la próxima vez que inicie una nueva sesión. Esto mantiene el mensaje del sistema estable durante una conversación para que el almacenamiento en caché de prompts pueda reducir la latencia y el costo.

## Crear un estilo de salida personalizado

Un estilo de salida personalizado es un archivo Markdown: frontmatter para metadatos, luego las instrucciones a agregar al mensaje del sistema.

<Steps>
  <Step title="Crear un archivo Markdown">
    Guárdelo en uno de tres niveles. El nombre del archivo se convierte en el nombre del estilo a menos que establezca `name` en el frontmatter.

    * Usuario: `~/.claude/output-styles`
    * Proyecto: `.claude/output-styles`
    * Política administrada: `.claude/output-styles` dentro del [directorio de configuración administrada](/es/settings#settings-files)
  </Step>

  <Step title="Agregar frontmatter e instrucciones">
    Decida si desea mantener las instrucciones de ingeniería de software de Claude Code. Establezca `keep-coding-instructions: true` si está cambiando cómo Claude se comunica pero aún desea que codifique de la misma manera. Déjelo fuera si Claude no estará haciendo ingeniería de software.

    Este ejemplo encabeza cada explicación con un diagrama mientras mantiene el comportamiento de codificación de Claude:

    ```markdown theme={null}
    ---
    name: Diagrams first
    description: Lead every explanation with a diagram
    keep-coding-instructions: true
    ---

    When explaining code, architecture, or data flow, start with a Mermaid diagram showing the structure, then explain in prose.

    ## Diagram conventions

    Use `flowchart TD` for control flow and `sequenceDiagram` for request paths. Keep diagrams under 15 nodes.
    ```
  </Step>

  <Step title="Cambiar a su estilo">
    Ejecute `/config` y seleccione su estilo bajo **Output style**. Surte efecto la próxima vez que inicie una sesión.
  </Step>
</Steps>

[Plugins](/es/plugins-reference) también pueden enviar estilos de salida en un directorio `output-styles/`.

### Frontmatter

Los archivos de estilo de salida admiten estos campos de frontmatter:

| Frontmatter                | Propósito                                                                                                                                                                                                                                                                                        | Predeterminado                   |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `name`                     | Nombre del estilo de salida, si no es el nombre del archivo                                                                                                                                                                                                                                      | Se hereda del nombre del archivo |
| `description`              | Descripción del estilo de salida, mostrada en el selector `/config`                                                                                                                                                                                                                              | Ninguno                          |
| `keep-coding-instructions` | Mantener las instrucciones integradas de ingeniería de software de Claude Code                                                                                                                                                                                                                   | `false`                          |
| `force-for-plugin`         | Solo estilos de salida de plugins: aplique este estilo automáticamente siempre que el plugin esté habilitado, sin requerir que los usuarios lo seleccionen. Anula la configuración `outputStyle` del usuario. Si varios plugins habilitados establecen esto, Claude Code usa el primero cargado. | `false`                          |

## Cómo funcionan los estilos de salida

Los estilos de salida modifican directamente el mensaje del sistema de Claude Code.

* Todos los estilos de salida tienen sus propias instrucciones personalizadas agregadas al final del mensaje del sistema.
* Todos los estilos de salida activan recordatorios para que Claude se adhiera a las instrucciones del estilo de salida durante la conversación.
* Los estilos de salida personalizados dejan fuera las instrucciones integradas de ingeniería de software de Claude Code, como cómo delimitar cambios, escribir comentarios y verificar el trabajo, a menos que `keep-coding-instructions` esté establecido en `true`.

El uso de tokens depende del estilo. Agregar instrucciones al mensaje del sistema aumenta los tokens de entrada, aunque el almacenamiento en caché de prompts reduce este costo después de la primera solicitud en una sesión. Los estilos integrados Explanatory y Learning producen respuestas más largas que Default por diseño, lo que aumenta los tokens de salida. Para estilos personalizados, el uso de tokens de salida depende de lo que sus instrucciones le digan a Claude que produzca.

## Comparaciones con características relacionadas

Varias características personalizan cómo se comporta Claude Code. Los estilos de salida modifican el mensaje del sistema directamente y se aplican a cada respuesta. Los otros agregan instrucciones sin cambiar el mensaje del sistema predeterminado, o los limitan a una tarea específica.

| Característica           | Cómo funciona                                                                 | Úselo cuando                                                                          |
| :----------------------- | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| Estilos de salida        | Modifica el mensaje del sistema                                               | Desea un rol, tono o formato de respuesta predeterminado diferente en cada turno      |
| [CLAUDE.md](/es/memory)  | Agrega un mensaje de usuario después del mensaje del sistema                  | Claude siempre debe conocer sus convenciones de proyecto y contexto de base de código |
| `--append-system-prompt` | Se agrega al mensaje del sistema sin eliminar nada                            | Desea una adición única para una única invocación                                     |
| [Agents](/es/sub-agents) | Ejecuta un subagente con su propio mensaje del sistema, modelo y herramientas | Desea un ayudante con alcance separado para una tarea enfocada                        |
| [Skills](/es/skills)     | Carga instrucciones específicas de tareas cuando se invoca o es relevante     | Tiene un flujo de trabajo reutilizable                                                |

## Recursos relacionados

* [Settings](/es/settings): donde vive el campo `outputStyle` y cómo funciona la precedencia de configuración
* [Permission modes](/es/permission-modes): el estilo Proactive refleja el modo automático sin cambiar su modo de permisos
* [Plugins](/es/plugins): empaquete y distribuya estilos de salida junto con skills, hooks y agents
* [Debug your configuration](/es/debug-your-config): diagnostique por qué un estilo de salida no está surtiendo efecto
