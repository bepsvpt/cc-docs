> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Solución de problemas

> Corrige el alto uso de CPU o memoria, cuelgues, thrashing de auto-compact, y problemas de búsqueda en Claude Code, y encuentra la página correcta para otros problemas.

Esta página cubre problemas de rendimiento, estabilidad y búsqueda una vez que Claude Code está en ejecución. Para otros problemas, comienza con la página que coincida con dónde estés atrapado:

| Síntoma                                                                                                                             | Ir a                                                                                                        |
| :---------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| `command not found`, falla de instalación, problemas de PATH, `EACCES`, errores de TLS                                              | [Solucionar problemas de instalación e inicio de sesión](/es/troubleshoot-install)                          |
| Bucles de inicio de sesión, errores de OAuth, `403 Forbidden`, "organización deshabilitada", credenciales de Bedrock/Vertex/Foundry | [Solucionar problemas de instalación e inicio de sesión](/es/troubleshoot-install#login-and-authentication) |
| La configuración no se aplica, hooks no se disparan, servidores MCP no se cargan                                                    | [Depurar tu configuración](/es/debug-your-config)                                                           |
| `API Error: 5xx`, `529 Overloaded`, `429`, errores de validación de solicitudes                                                     | [Referencia de errores](/es/errors)                                                                         |
| `model not found` o `you may not have access to it`                                                                                 | [Referencia de errores](/es/errors#theres-an-issue-with-the-selected-model)                                 |
| La extensión de VS Code no se conecta o no detecta Claude                                                                           | [Integración de VS Code](/es/vs-code#fix-common-issues)                                                     |
| Plugin de JetBrains o IDE no detectado                                                                                              | [Integración de JetBrains](/es/jetbrains#troubleshooting)                                                   |
| Alto uso de CPU o memoria, respuestas lentas, cuelgues, búsqueda no encuentra archivos                                              | [Rendimiento y estabilidad](#performance-and-stability) abajo                                               |

Si no estás seguro de cuál aplica, ejecuta `/doctor` dentro de Claude Code para una verificación automatizada de tu instalación, configuración, servidores MCP, y uso de contexto. Si `claude` no inicia en absoluto, ejecuta `claude doctor` desde tu shell en su lugar.

## Rendimiento y estabilidad

Estas secciones cubren problemas relacionados con el uso de recursos, capacidad de respuesta, y comportamiento de búsqueda.

### Alto uso de CPU o memoria

Claude Code está diseñado para funcionar con la mayoría de entornos de desarrollo, pero puede consumir recursos significativos al procesar bases de código grandes. Si estás experimentando problemas de rendimiento:

1. Usa `/compact` regularmente para reducir el tamaño del contexto
2. Cierra y reinicia Claude Code entre tareas principales
3. Considera añadir directorios de compilación grandes a tu archivo `.gitignore`

Si el uso de memoria se mantiene alto después de estos pasos, ejecuta `/heapdump` para escribir una instantánea de montón de JavaScript y un desglose de memoria a `~/Desktop`. En Linux sin una carpeta Desktop, los archivos se escriben en tu directorio de inicio.

El desglose muestra el tamaño del conjunto residente, montón de JS, búferes de matriz, y memoria nativa no contabilizada, lo que ayuda a identificar si el crecimiento está en objetos de JavaScript o en código nativo. Para inspeccionar retentores, abre el archivo `.heapsnapshot` en Chrome DevTools bajo Memory → Load. Adjunta ambos archivos al reportar un problema de memoria en [GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compaction se detiene con un error de thrashing

Si ves `Autocompact is thrashing: the context refilled to the limit...`, la compactación automática fue exitosa pero un archivo o salida de herramienta rellenó inmediatamente la ventana de contexto varias veces seguidas. Claude Code deja de reintentar para evitar desperdiciar llamadas de API en un bucle que no está haciendo progreso.

Para recuperarse:

1. Pide a Claude que lea el archivo de gran tamaño en fragmentos más pequeños, como un rango de línea específico o función, en lugar de todo el archivo
2. Ejecuta `/compact` con un enfoque que elimine la salida grande, por ejemplo `/compact keep only the plan and the diff`
3. Mueve el trabajo de archivo grande a un [subagente](/es/sub-agents) para que se ejecute en una ventana de contexto separada
4. Ejecuta `/clear` si la conversación anterior ya no es necesaria

### El comando se cuelga o congela

Si Claude Code parece no responder:

1. Presiona Ctrl+C para intentar cancelar la operación actual
2. Si no responde, es posible que necesites cerrar la terminal y reiniciar

Reiniciar no pierde tu conversación. Ejecuta `claude --resume` en el mismo directorio para retomar la sesión.

### Problemas de búsqueda y descubrimiento

Si la herramienta Search, menciones `@file`, agentes personalizados, o skills personalizados no encuentran archivos, el binario `ripgrep` incluido puede no ejecutarse en tu sistema. Instala el paquete `ripgrep` de tu plataforma e indica a Claude Code que lo use en su lugar:

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

Luego establece `USE_BUILTIN_RIPGREP=0` en tu [entorno](/es/env-vars).

### Resultados de búsqueda lentos o incompletos en WSL

Las penalizaciones de rendimiento de lectura de disco al [trabajar entre sistemas de archivos en WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) pueden resultar en menos coincidencias de las esperadas al usar Claude Code en WSL. La búsqueda aún funciona, pero devuelve menos resultados que en un sistema de archivos nativo.

<Note>
  `/doctor` mostrará Search como OK en este caso.
</Note>

**Soluciones:**

1. **Envía búsquedas más específicas**: reduce el número de archivos buscados especificando directorios o tipos de archivo: "Search for JWT validation logic in the auth-service package" o "Find use of md5 hash in JS files".

2. **Mueve el proyecto al sistema de archivos de Linux**: si es posible, asegúrate de que tu proyecto esté ubicado en el sistema de archivos de Linux (`/home/`) en lugar del sistema de archivos de Windows (`/mnt/c/`).

3. **Usa Windows nativo en su lugar**: considera ejecutar Claude Code nativamente en Windows en lugar de a través de WSL, para mejor rendimiento del sistema de archivos.

## Obtén más ayuda

Si estás experimentando problemas no cubiertos aquí:

1. Ejecuta `/doctor` para verificar la salud de la instalación, validez de la configuración, configuración de MCP, y uso de contexto en un solo paso
2. Usa el comando `/feedback` dentro de Claude Code para reportar problemas directamente a Anthropic
3. Verifica el [repositorio de GitHub](https://github.com/anthropics/claude-code) para problemas conocidos
4. Pregunta a Claude directamente sobre sus capacidades y características. Claude tiene acceso integrado a su documentación.
