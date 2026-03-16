> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Contenedores de desarrollo

> Aprende sobre el contenedor de desarrollo de Claude Code para equipos que necesitan entornos consistentes y seguros.

La [configuración de devcontainer](https://github.com/anthropics/claude-code/tree/main/.devcontainer) de referencia y el [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) asociado ofrecen un contenedor de desarrollo preconfigurado que puedes usar tal como está, o personalizar según tus necesidades. Este devcontainer funciona con la extensión [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) de Visual Studio Code y herramientas similares.

Las medidas de seguridad mejoradas del contenedor (aislamiento y reglas de firewall) te permiten ejecutar `claude --dangerously-skip-permissions` para omitir solicitudes de permisos para operación desatendida.

<Warning>
  Aunque el devcontainer proporciona protecciones sustanciales, ningún sistema es completamente inmune a todos los ataques.
  Cuando se ejecuta con `--dangerously-skip-permissions`, los devcontainers no previenen que un proyecto malicioso exfiltre cualquier cosa accesible en el devcontainer, incluyendo credenciales de Claude Code.
  Recomendamos usar devcontainers solo cuando se desarrolla con repositorios de confianza.
  Siempre mantén buenas prácticas de seguridad y monitorea las actividades de Claude.
</Warning>

## Características clave

* **Node.js listo para producción**: Construido sobre Node.js 20 con dependencias de desarrollo esenciales
* **Seguridad por diseño**: Firewall personalizado que restringe el acceso de red solo a servicios necesarios
* **Herramientas amigables para desarrolladores**: Incluye git, ZSH con mejoras de productividad, fzf y más
* **Integración perfecta con VS Code**: Extensiones preconfiguradas y configuraciones optimizadas
* **Persistencia de sesión**: Preserva el historial de comandos y configuraciones entre reinicios del contenedor
* **Funciona en todas partes**: Compatible con entornos de desarrollo en macOS, Windows y Linux

## Comenzar en 4 pasos

1. Instala VS Code y la extensión Remote - Containers
2. Clona el repositorio de [implementación de referencia de Claude Code](https://github.com/anthropics/claude-code/tree/main/.devcontainer)
3. Abre el repositorio en VS Code
4. Cuando se te solicite, haz clic en "Reopen in Container" (o usa Command Palette: Cmd+Shift+P → "Remote-Containers: Reopen in Container")

## Desglose de configuración

La configuración de devcontainer consta de tres componentes principales:

* [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Controla la configuración del contenedor, extensiones y montajes de volumen
* [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Define la imagen del contenedor y las herramientas instaladas
* [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Establece las reglas de seguridad de red

## Características de seguridad

El contenedor implementa un enfoque de seguridad multicapa con su configuración de firewall:

* **Control de acceso preciso**: Restringe las conexiones salientes solo a dominios en la lista blanca (registro npm, GitHub, API de Claude, etc.)
* **Conexiones salientes permitidas**: El firewall permite conexiones DNS y SSH salientes
* **Política de negación por defecto**: Bloquea todo otro acceso de red externo
* **Verificación de inicio**: Valida las reglas del firewall cuando se inicializa el contenedor
* **Aislamiento**: Crea un entorno de desarrollo seguro separado de tu sistema principal

## Opciones de personalización

La configuración de devcontainer está diseñada para ser adaptable a tus necesidades:

* Añade o elimina extensiones de VS Code según tu flujo de trabajo
* Modifica asignaciones de recursos para diferentes entornos de hardware
* Ajusta permisos de acceso de red
* Personaliza configuraciones de shell y herramientas de desarrollador

## Casos de uso de ejemplo

### Trabajo seguro con clientes

Usa devcontainers para aislar diferentes proyectos de clientes, asegurando que el código y las credenciales nunca se mezclen entre entornos.

### Incorporación de equipo

Los nuevos miembros del equipo pueden obtener un entorno de desarrollo completamente configurado en minutos, con todas las herramientas y configuraciones necesarias preinstaladas.

### Entornos CI/CD consistentes

Refleja tu configuración de devcontainer en canalizaciones CI/CD para asegurar que los entornos de desarrollo y producción coincidan.

## Recursos relacionados

* [Documentación de devcontainers de VS Code](https://code.visualstudio.com/docs/devcontainers/containers)
* [Mejores prácticas de seguridad de Claude Code](/es/security)
* [Configuración de red empresarial](/es/network-config)
