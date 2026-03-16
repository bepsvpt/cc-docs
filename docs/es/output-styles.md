> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Estilos de salida

> Adapte Claude Code para usos más allá de la ingeniería de software

Los estilos de salida le permiten usar Claude Code como cualquier tipo de agente mientras se mantienen sus capacidades principales, como ejecutar scripts locales, leer/escribir archivos y realizar un seguimiento de TODOs.

## Estilos de salida integrados

El estilo de salida **Default** de Claude Code es el mensaje del sistema existente, diseñado para ayudarle a completar tareas de ingeniería de software de manera eficiente.

Hay dos estilos de salida integrados adicionales enfocados en enseñarle la base de código y cómo funciona Claude:

* **Explanatory**: Proporciona "Insights" educativos entre ayudarle a completar tareas de ingeniería de software. Le ayuda a entender las opciones de implementación y los patrones de la base de código.

* **Learning**: Modo colaborativo de aprendizaje práctico donde Claude no solo compartirá "Insights" mientras codifica, sino que también le pedirá que contribuya con pequeñas piezas de código estratégicas. Claude Code agregará marcadores `TODO(human)` en su código para que usted implemente.

## Cómo funcionan los estilos de salida

Los estilos de salida modifican directamente el mensaje del sistema de Claude Code.

* Todos los estilos de salida excluyen instrucciones para una salida eficiente (como responder de manera concisa).
* Los estilos de salida personalizados excluyen instrucciones para codificación (como verificar código con pruebas), a menos que `keep-coding-instructions` sea verdadero.
* Todos los estilos de salida tienen sus propias instrucciones personalizadas agregadas al final del mensaje del sistema.
* Todos los estilos de salida activan recordatorios para que Claude se adhiera a las instrucciones del estilo de salida durante la conversación.

## Cambiar su estilo de salida

Ejecute `/config` y seleccione **Output style** para elegir un estilo de un menú. Su selección se guarda en `.claude/settings.local.json` en el [nivel de proyecto local](/es/settings).

Para establecer un estilo sin el menú, edite el campo `outputStyle` directamente en un archivo de configuración:

```json  theme={null}
{
  "outputStyle": "Explanatory"
}
```

Debido a que el estilo de salida se establece en el mensaje del sistema al inicio de la sesión, los cambios surten efecto la próxima vez que inicie una nueva sesión. Esto mantiene el mensaje del sistema estable durante una conversación para que el almacenamiento en caché de prompts pueda reducir la latencia y el costo.

## Crear un estilo de salida personalizado

Los estilos de salida personalizados son archivos Markdown con frontmatter y el texto que se agregará al mensaje del sistema:

```markdown  theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

Puede guardar estos archivos en el nivel de usuario (`~/.claude/output-styles`) o en el nivel de proyecto (`.claude/output-styles`).

### Frontmatter

Los archivos de estilo de salida admiten frontmatter para especificar metadatos:

| Frontmatter                | Propósito                                                                                                | Predeterminado                   |
| :------------------------- | :------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `name`                     | Nombre del estilo de salida, si no es el nombre del archivo                                              | Se hereda del nombre del archivo |
| `description`              | Descripción del estilo de salida, mostrada en el selector `/config`                                      | Ninguno                          |
| `keep-coding-instructions` | Si se deben mantener las partes del mensaje del sistema de Claude Code relacionadas con la codificación. | false                            |

## Comparaciones con características relacionadas

### Estilos de salida vs. CLAUDE.md vs. --append-system-prompt

Los estilos de salida "apagan" completamente las partes del mensaje del sistema predeterminado de Claude Code específicas de la ingeniería de software. Ni CLAUDE.md ni `--append-system-prompt` editan el mensaje del sistema predeterminado de Claude Code. CLAUDE.md agrega el contenido como un mensaje de usuario *después* del mensaje del sistema predeterminado de Claude Code. `--append-system-prompt` agrega el contenido al mensaje del sistema.

### Estilos de salida vs. [Agents](/es/sub-agents)

Los estilos de salida afectan directamente el bucle del agente principal y solo afectan el mensaje del sistema. Los agentes se invocan para manejar tareas específicas y pueden incluir configuraciones adicionales como el modelo a usar, las herramientas disponibles y algo de contexto sobre cuándo usar el agente.

### Estilos de salida vs. [Skills](/es/skills)

Los estilos de salida modifican cómo responde Claude (formato, tono, estructura) y siempre están activos una vez seleccionados. Skills son prompts específicos de tareas que invoca con `/skill-name` o que Claude carga automáticamente cuando es relevante. Use estilos de salida para preferencias de formato consistentes; use skills para flujos de trabajo y tareas reutilizables.
