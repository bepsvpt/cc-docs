> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sandboxing

> Aprenda cómo la herramienta bash aislada de Claude Code proporciona aislamiento del sistema de archivos y la red para una ejecución de agentes más segura y autónoma.

## Descripción general

Claude Code incluye sandboxing nativo para proporcionar un entorno más seguro para la ejecución de agentes mientras reduce la necesidad de solicitudes de permiso constantes. En lugar de pedir permiso para cada comando bash, el sandboxing crea límites definidos de antemano donde Claude Code puede trabajar más libremente con riesgo reducido.

La herramienta bash aislada utiliza primitivas a nivel del sistema operativo para aplicar tanto aislamiento del sistema de archivos como de la red.

## Por qué el sandboxing es importante

La seguridad tradicional basada en permisos requiere aprobación constante del usuario para comandos bash. Si bien esto proporciona control, puede llevar a:

* **Fatiga de aprobación**: Hacer clic repetidamente en "aprobar" puede hacer que los usuarios presten menos atención a lo que están aprobando
* **Productividad reducida**: Las interrupciones constantes ralentizan los flujos de trabajo de desarrollo
* **Autonomía limitada**: Claude Code no puede trabajar de manera eficiente cuando espera aprobaciones

El sandboxing aborda estos desafíos mediante:

1. **Definir límites claros**: Especifique exactamente qué directorios y hosts de red puede acceder Claude Code
2. **Reducir solicitudes de permiso**: Los comandos seguros dentro del sandbox no requieren aprobación
3. **Mantener la seguridad**: Los intentos de acceder a recursos fuera del sandbox desencadenan notificaciones inmediatas
4. **Habilitar autonomía**: Claude Code puede ejecutarse de manera más independiente dentro de límites definidos

<Warning>
  El sandboxing efectivo requiere **tanto** aislamiento del sistema de archivos como de la red. Sin aislamiento de red, un agente comprometido podría exfiltrar archivos sensibles como claves SSH. Sin aislamiento del sistema de archivos, un agente comprometido podría instalar una puerta trasera en recursos del sistema para obtener acceso a la red. Al configurar el sandboxing, es importante asegurarse de que la configuración no cree omisiones en estos sistemas.
</Warning>

## Cómo funciona

### Aislamiento del sistema de archivos

La herramienta bash aislada restringe el acceso al sistema de archivos a directorios específicos:

* **Comportamiento de escritura predeterminado**: Acceso de lectura y escritura al directorio de trabajo actual y sus subdirectorios
* **Comportamiento de lectura predeterminado**: Acceso de lectura a toda la computadora, excepto ciertos directorios denegados
* **Acceso bloqueado**: No puede modificar archivos fuera del directorio de trabajo actual sin permiso explícito
* **Configurable**: Defina rutas permitidas y denegadas personalizadas a través de la configuración

Puede otorgar acceso de escritura a rutas adicionales usando `sandbox.filesystem.allowWrite` en su configuración. Estas restricciones se aplican a nivel del sistema operativo (Seatbelt en macOS, bubblewrap en Linux), por lo que se aplican a todos los comandos de subproceso, incluidas herramientas como `kubectl`, `terraform` y `npm`, no solo a las herramientas de archivo de Claude.

### Aislamiento de red

El acceso a la red se controla a través de un servidor proxy que se ejecuta fuera del sandbox:

* **Restricciones de dominio**: Solo se pueden acceder a dominios aprobados
* **Confirmación del usuario**: Las nuevas solicitudes de dominio desencadenan solicitudes de permiso (a menos que [`allowManagedDomainsOnly`](/es/settings#sandbox-settings) esté habilitado, que bloquea automáticamente dominios no permitidos)
* **Soporte de proxy personalizado**: Los usuarios avanzados pueden implementar reglas personalizadas en el tráfico saliente
* **Cobertura integral**: Las restricciones se aplican a todos los scripts, programas y subprocesos generados por comandos

### Aplicación a nivel del sistema operativo

La herramienta bash aislada aprovecha las primitivas de seguridad del sistema operativo:

* **macOS**: Utiliza Seatbelt para la aplicación del sandbox
* **Linux**: Utiliza [bubblewrap](https://github.com/containers/bubblewrap) para el aislamiento
* **WSL2**: Utiliza bubblewrap, igual que Linux

WSL1 no es compatible porque bubblewrap requiere características del kernel solo disponibles en WSL2.

Estas restricciones a nivel del sistema operativo garantizan que todos los procesos secundarios generados por los comandos de Claude Code hereden los mismos límites de seguridad.

## Primeros pasos

### Requisitos previos

En **macOS**, el sandboxing funciona de inmediato usando el marco Seatbelt integrado.

En **Linux y WSL2**, instale primero los paquetes requeridos:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

### Habilitar sandboxing

Puede habilitar el sandboxing ejecutando el comando `/sandbox`:

```text  theme={null}
/sandbox
```

Esto abre un menú donde puede elegir entre modos de sandbox. Si faltan dependencias requeridas (como `bubblewrap` o `socat` en Linux), el menú muestra instrucciones de instalación para su plataforma.

### Modos de sandbox

Claude Code ofrece dos modos de sandbox:

**Modo de auto-permitir**: Los comandos Bash intentarán ejecutarse dentro del sandbox y se permitirán automáticamente sin requerir permiso. Los comandos que no se pueden aislar (como aquellos que necesitan acceso a la red a hosts no permitidos) vuelven al flujo de permiso regular. Las reglas de solicitud/denegación explícitas que ha configurado siempre se respetan.

**Modo de permisos regulares**: Todos los comandos bash pasan por el flujo de permiso estándar, incluso cuando están aislados. Esto proporciona más control pero requiere más aprobaciones.

En ambos modos, el sandbox aplica las mismas restricciones de sistema de archivos y red. La diferencia es solo si los comandos aislados se aprueban automáticamente o requieren permiso explícito.

<Info>
  El modo de auto-permitir funciona independientemente de su configuración de modo de permiso. Incluso si no está en modo "aceptar ediciones", los comandos bash aislados se ejecutarán automáticamente cuando el auto-permitir esté habilitado. Esto significa que los comandos bash que modifican archivos dentro de los límites del sandbox se ejecutarán sin solicitar, incluso cuando las herramientas de edición de archivos normalmente requerirían aprobación.
</Info>

### Configurar sandboxing

Personalice el comportamiento del sandbox a través de su archivo `settings.json`. Consulte [Configuración](/es/settings#sandbox-settings) para obtener la referencia de configuración completa.

#### Otorgar acceso de escritura de subproceso a rutas específicas

De forma predeterminada, los comandos aislados solo pueden escribir en el directorio de trabajo actual. Si comandos de subproceso como `kubectl`, `terraform` o `npm` necesitan escribir fuera del directorio del proyecto, use `sandbox.filesystem.allowWrite` para otorgar acceso a rutas específicas:

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "//tmp/build"]
    }
  }
}
```

Estas rutas se aplican a nivel del sistema operativo, por lo que todos los comandos que se ejecutan dentro del sandbox, incluidos sus procesos secundarios, las respetan. Este es el enfoque recomendado cuando una herramienta necesita acceso de escritura a una ubicación específica, en lugar de excluir la herramienta del sandbox por completo con `excludedCommands`.

Cuando `allowWrite` (o `denyWrite`/`denyRead`) se define en múltiples [ámbitos de configuración](/es/settings#settings-precedence), los arrays se **fusionan**, lo que significa que las rutas de cada ámbito se combinan, no se reemplazan. Por ejemplo, si la configuración administrada permite escrituras en `//opt/company-tools` y un usuario agrega `~/.kube` en su configuración personal, ambas rutas se incluyen en la configuración final del sandbox. Esto significa que los usuarios y proyectos pueden extender la lista sin duplicar ni anular las rutas establecidas por ámbitos de mayor prioridad.

Los prefijos de ruta controlan cómo se resuelven las rutas:

| Prefijo            | Significado                                                     | Ejemplo                                        |
| :----------------- | :-------------------------------------------------------------- | :--------------------------------------------- |
| `//`               | Ruta absoluta desde la raíz del sistema de archivos             | `//tmp/build` se convierte en `/tmp/build`     |
| `~/`               | Relativo al directorio de inicio                                | `~/.kube` se convierte en `$HOME/.kube`        |
| `/`                | Relativo al directorio del archivo de configuración             | `/build` se convierte en `$SETTINGS_DIR/build` |
| `./` o sin prefijo | Ruta relativa (resuelta por el tiempo de ejecución del sandbox) | `./output`                                     |

También puede denegar acceso de escritura o lectura usando `sandbox.filesystem.denyWrite` y `sandbox.filesystem.denyRead`. Estos se fusionan con cualquier ruta de las reglas de permiso `Edit(...)` y `Read(...)`.

<Tip>
  No todos los comandos son compatibles con el sandboxing de inmediato. Algunas notas que pueden ayudarle a aprovechar al máximo el sandbox:

  * Muchas herramientas CLI requieren acceder a ciertos hosts. A medida que utiliza estas herramientas, solicitarán permiso para acceder a ciertos hosts. Otorgar permiso les permitirá acceder a estos hosts ahora y en el futuro, permitiéndoles ejecutarse de manera segura dentro del sandbox.
  * `watchman` es incompatible con la ejecución en el sandbox. Si está ejecutando `jest`, considere usar `jest --no-watchman`
  * `docker` es incompatible con la ejecución en el sandbox. Considere especificar `docker` en `excludedCommands` para forzarlo a ejecutarse fuera del sandbox.
</Tip>

<Note>
  Claude Code incluye un mecanismo de escape intencional que permite que los comandos se ejecuten fuera del sandbox cuando sea necesario. Cuando un comando falla debido a restricciones del sandbox (como problemas de conectividad de red o herramientas incompatibles), se solicita a Claude que analice la falla y puede reintentar el comando con el parámetro `dangerouslyDisableSandbox`. Los comandos que utilizan este parámetro pasan por el flujo de permisos normal de Claude Code que requiere permiso del usuario para ejecutarse. Esto permite que Claude Code maneje casos extremos donde ciertas herramientas u operaciones de red no pueden funcionar dentro de las restricciones del sandbox.

  Puede deshabilitar este mecanismo de escape configurando `"allowUnsandboxedCommands": false` en su [configuración de sandbox](/es/settings#sandbox-settings). Cuando está deshabilitado, el parámetro `dangerouslyDisableSandbox` se ignora completamente y todos los comandos deben ejecutarse aislados o estar explícitamente listados en `excludedCommands`.
</Note>

## Beneficios de seguridad

### Protección contra inyección de solicitud

Incluso si un atacante manipula con éxito el comportamiento de Claude Code a través de inyección de solicitud, el sandbox garantiza que su sistema permanezca seguro:

**Protección del sistema de archivos:**

* No puede modificar archivos de configuración críticos como `~/.bashrc`
* No puede modificar archivos a nivel del sistema en `/bin/`
* No puede leer archivos que se deniegan en su [configuración de permisos de Claude](/es/permissions#manage-permissions)

**Protección de red:**

* No puede exfiltrar datos a servidores controlados por atacantes
* No puede descargar scripts maliciosos de dominios no autorizados
* No puede realizar llamadas API inesperadas a servicios no aprobados
* No puede contactar a ningún dominio que no esté explícitamente permitido

**Monitoreo y control:**

* Todos los intentos de acceso fuera del sandbox se bloquean a nivel del sistema operativo
* Recibe notificaciones inmediatas cuando se prueban los límites
* Puede elegir denegar, permitir una vez o actualizar permanentemente su configuración

### Superficie de ataque reducida

El sandboxing limita el daño potencial de:

* **Dependencias maliciosas**: Paquetes NPM u otras dependencias con código dañino
* **Scripts comprometidos**: Scripts de compilación o herramientas con vulnerabilidades de seguridad
* **Ingeniería social**: Ataques que engañan a los usuarios para que ejecuten comandos peligrosos
* **Inyección de solicitud**: Ataques que engañan a Claude para que ejecute comandos peligrosos

### Operación transparente

Cuando Claude Code intenta acceder a recursos de red fuera del sandbox:

1. La operación se bloquea a nivel del sistema operativo
2. Recibe una notificación inmediata
3. Puede elegir:
   * Denegar la solicitud
   * Permitirla una vez
   * Actualizar su configuración de sandbox para permitirla permanentemente

## Limitaciones de seguridad

* Limitaciones de sandboxing de red: El sistema de filtrado de red funciona restringiendo los dominios a los que se permite que se conecten los procesos. De lo contrario, no inspecciona el tráfico que pasa a través del proxy y los usuarios son responsables de asegurarse de que solo permitan dominios confiables en su política.

<Warning>
  Los usuarios deben ser conscientes de los riesgos potenciales que conlleva permitir dominios amplios como `github.com` que pueden permitir la exfiltración de datos. Además, en algunos casos puede ser posible eludir el filtrado de red a través de [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting).
</Warning>

* Escalada de privilegios a través de sockets Unix: La configuración `allowUnixSockets` puede otorgar inadvertidamente acceso a servicios del sistema poderosos que podrían llevar a omisiones del sandbox. Por ejemplo, si se usa para permitir acceso a `/var/run/docker.sock`, esto efectivamente otorgaría acceso al sistema host explotando el socket de docker. Se anima a los usuarios a considerar cuidadosamente cualquier socket unix que permitan a través del sandbox.
* Escalada de permisos del sistema de archivos: Los permisos de escritura del sistema de archivos demasiado amplios pueden permitir ataques de escalada de privilegios. Permitir escrituras en directorios que contienen ejecutables en `$PATH`, directorios de configuración del sistema o archivos de configuración de shell del usuario (`.bashrc`, `.zshrc`) puede llevar a la ejecución de código en diferentes contextos de seguridad cuando otros usuarios o procesos del sistema acceden a estos archivos.
* Fortaleza del sandbox de Linux: La implementación de Linux proporciona un fuerte aislamiento del sistema de archivos y la red pero incluye un modo `enableWeakerNestedSandbox` que le permite funcionar dentro de entornos Docker sin espacios de nombres privilegiados. Esta opción debilita considerablemente la seguridad y solo debe usarse en casos donde se aplica aislamiento adicional de otra manera.

## Cómo se relaciona el sandboxing con los permisos

El sandboxing y los [permisos](/es/permissions) son capas de seguridad complementarias que funcionan juntas:

* **Permisos** controlan qué herramientas puede usar Claude Code y se evalúan antes de que se ejecute cualquier herramienta. Se aplican a todas las herramientas: Bash, Read, Edit, WebFetch, MCP y otras.
* **Sandboxing** proporciona aplicación a nivel del sistema operativo que restringe lo que los comandos Bash pueden acceder a nivel del sistema de archivos y la red. Se aplica solo a comandos Bash y sus procesos secundarios.

Las restricciones del sistema de archivos y la red se configuran tanto a través de la configuración del sandbox como de las reglas de permiso:

* Use `sandbox.filesystem.allowWrite` para otorgar acceso de escritura de subproceso a rutas fuera del directorio de trabajo
* Use `sandbox.filesystem.denyWrite` y `sandbox.filesystem.denyRead` para bloquear el acceso de subproceso a rutas específicas
* Use reglas de denegación `Read` y `Edit` para bloquear el acceso a archivos o directorios específicos
* Use reglas de permitir/denegar `WebFetch` para controlar el acceso al dominio
* Use `allowedDomains` del sandbox para controlar qué dominios pueden alcanzar los comandos Bash

Las rutas de ambas configuraciones `sandbox.filesystem` y reglas de permiso se fusionan en la configuración final del sandbox.

Este [repositorio](https://github.com/anthropics/claude-code/tree/main/examples/settings) incluye configuraciones de configuración de inicio para escenarios de implementación comunes, incluidos ejemplos específicos del sandbox. Úselos como puntos de partida y ajústelos según sus necesidades.

## Uso avanzado

### Configuración de proxy personalizado

Para organizaciones que requieren seguridad de red avanzada, puede implementar un proxy personalizado para:

* Descifrar e inspeccionar tráfico HTTPS
* Aplicar reglas de filtrado personalizadas
* Registrar todas las solicitudes de red
* Integrar con infraestructura de seguridad existente

```json  theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### Integración con herramientas de seguridad existentes

La herramienta bash aislada funciona junto con:

* **Reglas de permiso**: Combinar con [configuración de permisos](/es/permissions) para defensa en profundidad
* **Contenedores de desarrollo**: Usar con [devcontainers](/es/devcontainer) para aislamiento adicional
* **Políticas empresariales**: Aplicar configuraciones de sandbox a través de [configuración administrada](/es/settings#settings-precedence)

## Mejores prácticas

1. **Comience restrictivo**: Comience con permisos mínimos y expanda según sea necesario
2. **Monitoree registros**: Revise los intentos de violación del sandbox para entender las necesidades de Claude Code
3. **Use configuraciones específicas del entorno**: Diferentes reglas de sandbox para contextos de desarrollo versus producción
4. **Combine con permisos**: Use sandboxing junto con políticas IAM para seguridad integral
5. **Pruebe configuraciones**: Verifique que su configuración de sandbox no bloquee flujos de trabajo legítimos

## Código abierto

El tiempo de ejecución del sandbox está disponible como un paquete npm de código abierto para usar en sus propios proyectos de agentes. Esto permite que la comunidad más amplia de agentes de IA construya sistemas autónomos más seguros y protegidos. Esto también se puede usar para aislar otros programas que desee ejecutar. Por ejemplo, para aislar un servidor MCP podría ejecutar:

```bash  theme={null}
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Para detalles de implementación y código fuente, visite el [repositorio de GitHub](https://github.com/anthropic-experimental/sandbox-runtime).

## Limitaciones

* **Sobrecarga de rendimiento**: Mínima, pero algunas operaciones del sistema de archivos pueden ser ligeramente más lentas
* **Compatibilidad**: Algunas herramientas que requieren patrones de acceso específicos del sistema pueden necesitar ajustes de configuración, o incluso pueden necesitar ejecutarse fuera del sandbox
* **Soporte de plataforma**: Admite macOS, Linux y WSL2. WSL1 no es compatible. Se planea soporte nativo de Windows.

## Ver también

* [Seguridad](/es/security) - Características de seguridad integral y mejores prácticas
* [Permisos](/es/permissions) - Configuración de permisos y control de acceso
* [Configuración](/es/settings) - Referencia de configuración completa
* [Referencia de CLI](/es/cli-reference) - Opciones de línea de comandos
