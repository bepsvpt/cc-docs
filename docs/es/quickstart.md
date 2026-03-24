> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Inicio rápido

> ¡Bienvenido a Claude Code!

Esta guía de inicio rápido te permitirá usar asistencia de codificación impulsada por IA en pocos minutos. Al final, comprenderás cómo usar Claude Code para tareas comunes de desarrollo.

## Antes de comenzar

Asegúrate de tener:

* Una terminal o símbolo del sistema abiertos
  * Si nunca has usado la terminal antes, consulta la [guía de terminal](/es/terminal-guide)
* Un proyecto de código con el que trabajar
* Una [suscripción a Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_prereq) (Pro, Max, Teams o Enterprise), una cuenta de [Claude Console](https://console.anthropic.com/), o acceso a través de un [proveedor de nube compatible](/es/third-party-integrations)

<Note>
  Esta guía cubre la CLI de terminal. Claude Code también está disponible en la [web](https://claude.ai/code), como una [aplicación de escritorio](/es/desktop), en [VS Code](/es/vs-code) e [IDEs de JetBrains](/es/jetbrains), en [Slack](/es/slack), y en CI/CD con [GitHub Actions](/es/github-actions) y [GitLab](/es/gitlab-ci-cd). Consulta [todas las interfaces](/es/overview#use-claude-code-everywhere).
</Note>

## Paso 1: Instalar Claude Code

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

## Paso 2: Inicia sesión en tu cuenta

Claude Code requiere una cuenta para usarse. Cuando inicies una sesión interactiva con el comando `claude`, deberás iniciar sesión:

```bash  theme={null}
claude
# Se te pedirá que inicies sesión en el primer uso
```

```bash  theme={null}
/login
# Sigue las indicaciones para iniciar sesión con tu cuenta
```

Puedes iniciar sesión usando cualquiera de estos tipos de cuenta:

* [Claude Pro, Max, Teams o Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_login) (recomendado)
* [Claude Console](https://console.anthropic.com/) (acceso a API con créditos prepagados). En el primer inicio de sesión, se crea automáticamente un espacio de trabajo "Claude Code" en la Console para el seguimiento centralizado de costos.
* [Amazon Bedrock, Google Vertex AI o Microsoft Foundry](/es/third-party-integrations) (proveedores de nube empresariales)

Una vez que hayas iniciado sesión, tus credenciales se almacenan y no necesitarás iniciar sesión nuevamente. Para cambiar de cuenta más tarde, usa el comando `/login`.

## Paso 3: Inicia tu primera sesión

Abre tu terminal en cualquier directorio de proyecto e inicia Claude Code:

```bash  theme={null}
cd /path/to/your/project
claude
```

Verás la pantalla de bienvenida de Claude Code con la información de tu sesión, conversaciones recientes y las últimas actualizaciones. Escribe `/help` para ver los comandos disponibles o `/resume` para continuar una conversación anterior.

<Tip>
  Después de iniciar sesión (Paso 2), tus credenciales se almacenan en tu sistema. Obtén más información en [Gestión de credenciales](/es/authentication#credential-management).
</Tip>

## Paso 4: Haz tu primera pregunta

Comencemos por entender tu base de código. Intenta uno de estos comandos:

```text  theme={null}
¿qué hace este proyecto?
```

Claude analizará tus archivos y proporcionará un resumen. También puedes hacer preguntas más específicas:

```text  theme={null}
¿qué tecnologías usa este proyecto?
```

```text  theme={null}
¿dónde está el punto de entrada principal?
```

```text  theme={null}
explica la estructura de carpetas
```

También puedes preguntarle a Claude sobre sus propias capacidades:

```text  theme={null}
¿qué puede hacer Claude Code?
```

```text  theme={null}
¿cómo creo skills personalizados en Claude Code?
```

```text  theme={null}
¿puede Claude Code trabajar con Docker?
```

<Note>
  Claude Code lee los archivos de tu proyecto según sea necesario. No tienes que agregar contexto manualmente.
</Note>

## Paso 5: Realiza tu primer cambio de código

Ahora hagamos que Claude Code haga algo de codificación real. Intenta una tarea simple:

```text  theme={null}
agrega una función hello world al archivo principal
```

Claude Code hará lo siguiente:

1. Encontrará el archivo apropiado
2. Te mostrará los cambios propuestos
3. Te pedirá tu aprobación
4. Realizará la edición

<Note>
  Claude Code siempre pide permiso antes de modificar archivos. Puedes aprobar cambios individuales o habilitar el modo "Aceptar todo" para una sesión.
</Note>

## Paso 6: Usa Git con Claude Code

Claude Code hace que las operaciones de Git sean conversacionales:

```text  theme={null}
¿qué archivos he cambiado?
```

```text  theme={null}
confirma mis cambios con un mensaje descriptivo
```

También puedes solicitar operaciones de Git más complejas:

```text  theme={null}
crea una nueva rama llamada feature/quickstart
```

```text  theme={null}
muéstrame los últimos 5 commits
```

```text  theme={null}
ayúdame a resolver conflictos de fusión
```

## Paso 7: Corrige un error o agrega una función

Claude es competente en depuración e implementación de funciones.

Describe lo que deseas en lenguaje natural:

```text  theme={null}
agrega validación de entrada al formulario de registro de usuarios
```

O corrige problemas existentes:

```text  theme={null}
hay un error donde los usuarios pueden enviar formularios vacíos - corrígelo
```

Claude Code hará lo siguiente:

* Localizará el código relevante
* Comprenderá el contexto
* Implementará una solución
* Ejecutará pruebas si están disponibles

## Paso 8: Prueba otros flujos de trabajo comunes

Hay varias formas de trabajar con Claude:

**Refactorizar código**

```text  theme={null}
refactoriza el módulo de autenticación para usar async/await en lugar de callbacks
```

**Escribir pruebas**

```text  theme={null}
escribe pruebas unitarias para las funciones de calculadora
```

**Actualizar documentación**

```text  theme={null}
actualiza el README con instrucciones de instalación
```

**Revisión de código**

```text  theme={null}
revisa mis cambios y sugiere mejoras
```

<Tip>
  Habla con Claude como lo harías con un colega útil. Describe lo que deseas lograr y te ayudará a llegar allí.
</Tip>

## Comandos esenciales

Aquí están los comandos más importantes para el uso diario:

| Comando             | Qué hace                                                      | Ejemplo                             |
| ------------------- | ------------------------------------------------------------- | ----------------------------------- |
| `claude`            | Inicia el modo interactivo                                    | `claude`                            |
| `claude "task"`     | Ejecuta una tarea única                                       | `claude "fix the build error"`      |
| `claude -p "query"` | Ejecuta una consulta única y luego sale                       | `claude -p "explain this function"` |
| `claude -c`         | Continúa la conversación más reciente en el directorio actual | `claude -c`                         |
| `claude -r`         | Reanuda una conversación anterior                             | `claude -r`                         |
| `claude commit`     | Crea un commit de Git                                         | `claude commit`                     |
| `/clear`            | Borra el historial de conversación                            | `/clear`                            |
| `/help`             | Muestra los comandos disponibles                              | `/help`                             |
| `exit` o Ctrl+C     | Salir de Claude Code                                          | `exit`                              |

Consulta la [referencia de CLI](/es/cli-reference) para obtener una lista completa de comandos.

## Consejos profesionales para principiantes

Para más información, consulta [mejores prácticas](/es/best-practices) y [flujos de trabajo comunes](/es/common-workflows).

<AccordionGroup>
  <Accordion title="Sé específico con tus solicitudes">
    En lugar de: "corrige el error"

    Intenta: "corrige el error de inicio de sesión donde los usuarios ven una pantalla en blanco después de ingresar credenciales incorrectas"
  </Accordion>

  <Accordion title="Usa instrucciones paso a paso">
    Divide tareas complejas en pasos:

    ```text  theme={null}
    1. crea una nueva tabla de base de datos para perfiles de usuario
    2. crea un endpoint de API para obtener y actualizar perfiles de usuario
    3. construye una página web que permita a los usuarios ver y editar su información
    ```
  </Accordion>

  <Accordion title="Deja que Claude explore primero">
    Antes de hacer cambios, deja que Claude entienda tu código:

    ```text  theme={null}
    analiza el esquema de la base de datos
    ```

    ```text  theme={null}
    construye un panel que muestre los productos que nuestros clientes del Reino Unido devuelven con más frecuencia
    ```
  </Accordion>

  <Accordion title="Ahorra tiempo con atajos de teclado">
    * Presiona `?` para ver todos los atajos de teclado disponibles
    * Usa Tab para completar comandos
    * Presiona ↑ para el historial de comandos
    * Escribe `/` para ver todos los comandos y skills
  </Accordion>
</AccordionGroup>

## ¿Qué sigue?

Ahora que has aprendido lo básico, explora funciones más avanzadas:

<CardGroup cols={2}>
  <Card title="Cómo funciona Claude Code" icon="microchip" href="/es/how-claude-code-works">
    Comprende el bucle de agente, las herramientas integradas y cómo Claude Code interactúa con tu proyecto
  </Card>

  <Card title="Mejores prácticas" icon="star" href="/es/best-practices">
    Obtén mejores resultados con indicaciones efectivas y configuración de proyecto
  </Card>

  <Card title="Flujos de trabajo comunes" icon="graduation-cap" href="/es/common-workflows">
    Guías paso a paso para tareas comunes
  </Card>

  <Card title="Extiende Claude Code" icon="puzzle-piece" href="/es/features-overview">
    Personaliza con CLAUDE.md, skills, hooks, MCP y más
  </Card>
</CardGroup>

## Obtener ayuda

* **En Claude Code**: Escribe `/help` o pregunta "¿cómo..."
* **Documentación**: ¡Estás aquí! Explora otras guías
* **Comunidad**: Únete a nuestro [Discord](https://www.anthropic.com/discord) para consejos y soporte
