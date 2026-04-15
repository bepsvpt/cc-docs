> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sandboxing

> Erfahren Sie, wie das Sandboxing-Tool von Claude Code Dateisystem- und Netzwerkisolation für sicherere und autonomere Agent-Ausführung bietet.

## Übersicht

Claude Code verfügt über natives Sandboxing, um eine sicherere Umgebung für die Agent-Ausführung bereitzustellen und die Notwendigkeit ständiger Genehmigungseingaben zu reduzieren. Anstatt für jeden Bash-Befehl eine Genehmigung zu erbitten, erstellt Sandboxing vordefinierte Grenzen, in denen Claude Code mit reduziertem Risiko freier arbeiten kann.

Das Sandboxing-Bash-Tool verwendet Betriebssystem-Primitive, um sowohl Dateisystem- als auch Netzwerkisolation durchzusetzen.

## Warum Sandboxing wichtig ist

Die traditionelle genehmigungsbasierte Sicherheit erfordert ständige Benutzerbestätigung für Bash-Befehle. Während dies Kontrolle bietet, kann es zu Folgendem führen:

* **Genehmigungsmüdigkeit**: Wiederholtes Klicken auf „Genehmigen" kann dazu führen, dass Benutzer weniger Aufmerksamkeit auf das legen, was sie genehmigen
* **Reduzierte Produktivität**: Ständige Unterbrechungen verlangsamen Entwicklungs-Workflows
* **Begrenzte Autonomie**: Claude Code kann nicht effizient arbeiten, wenn es auf Genehmigungen wartet

Sandboxing adressiert diese Herausforderungen durch:

1. **Klare Grenzen definieren**: Geben Sie genau an, auf welche Verzeichnisse und Netzwerk-Hosts Claude Code zugreifen kann
2. **Genehmigungseingaben reduzieren**: Sichere Befehle innerhalb der Sandbox erfordern keine Genehmigung
3. **Sicherheit beibehalten**: Versuche, auf Ressourcen außerhalb der Sandbox zuzugreifen, lösen sofortige Benachrichtigungen aus
4. **Autonomie ermöglichen**: Claude Code kann unabhängiger innerhalb definierter Grenzen arbeiten

<Warning>
  Effektives Sandboxing erfordert **sowohl** Dateisystem- als auch Netzwerkisolation. Ohne Netzwerkisolation könnte ein kompromittierter Agent sensible Dateien wie SSH-Schlüssel exfiltrieren. Ohne Dateisystem-Isolation könnte ein kompromittierter Agent System-Ressourcen manipulieren, um Netzwerkzugriff zu erlangen. Bei der Konfiguration von Sandboxing ist es wichtig sicherzustellen, dass Ihre konfigurierten Einstellungen keine Umgehungen in diesen Systemen schaffen.
</Warning>

## Wie es funktioniert

### Dateisystem-Isolation

Das Sandboxing-Bash-Tool beschränkt den Dateisystem-Zugriff auf spezifische Verzeichnisse:

* **Standard-Schreibverhalten**: Lese- und Schreibzugriff auf das aktuelle Arbeitsverzeichnis und seine Unterverzeichnisse
* **Standard-Leseverhalten**: Lesezugriff auf den gesamten Computer, außer bestimmten blockierten Verzeichnissen
* **Blockierter Zugriff**: Kann Dateien außerhalb des aktuellen Arbeitsverzeichnisses nicht ohne explizite Genehmigung ändern
* **Konfigurierbar**: Definieren Sie benutzerdefinierte zulässige und blockierte Pfade durch Einstellungen

Sie können Schreibzugriff auf zusätzliche Pfade mit `sandbox.filesystem.allowWrite` in Ihren Einstellungen gewähren. Diese Einschränkungen werden auf OS-Ebene durchgesetzt (Seatbelt auf macOS, bubblewrap auf Linux), daher gelten sie für alle Subprozess-Befehle, einschließlich Tools wie `kubectl`, `terraform` und `npm`, nicht nur für Claudes Datei-Tools.

### Netzwerk-Isolation

Der Netzwerkzugriff wird durch einen Proxy-Server gesteuert, der außerhalb der Sandbox läuft:

* **Domain-Einschränkungen**: Nur genehmigte Domains können zugegriffen werden
* **Benutzerbestätigung**: Neue Domain-Anfragen lösen Genehmigungseingaben aus (es sei denn, [`allowManagedDomainsOnly`](/de/settings#sandbox-settings) ist aktiviert, was nicht zulässige Domains automatisch blockiert)
* **Benutzerdefinierte Proxy-Unterstützung**: Fortgeschrittene Benutzer können benutzerdefinierte Regeln für ausgehenden Datenverkehr implementieren
* **Umfassende Abdeckung**: Einschränkungen gelten für alle Skripte, Programme und Subprozesse, die durch Befehle erzeugt werden

### OS-Level-Durchsetzung

Das Sandboxing-Bash-Tool nutzt Betriebssystem-Sicherheits-Primitive:

* **macOS**: Verwendet Seatbelt für Sandbox-Durchsetzung
* **Linux**: Verwendet [bubblewrap](https://github.com/containers/bubblewrap) für Isolation
* **WSL2**: Verwendet bubblewrap, wie Linux

WSL1 wird nicht unterstützt, da bubblewrap Kernel-Features erfordert, die nur in WSL2 verfügbar sind.

Diese OS-Level-Einschränkungen stellen sicher, dass alle Kindprozesse, die durch Claudes Befehle erzeugt werden, die gleichen Sicherheitsgrenzen erben.

## Erste Schritte

### Voraussetzungen

Auf **macOS** funktioniert Sandboxing sofort mit dem integrierten Seatbelt-Framework.

Auf **Linux und WSL2** installieren Sie zuerst die erforderlichen Pakete:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

### Sandboxing aktivieren

Sie können Sandboxing durch Ausführung des `/sandbox`-Befehls aktivieren:

```text theme={null}
/sandbox
```

Dies öffnet ein Menü, in dem Sie zwischen Sandbox-Modi wählen können. Wenn erforderliche Abhängigkeiten fehlen (wie `bubblewrap` oder `socat` auf Linux), zeigt das Menü Installationsanweisungen für Ihre Plattform an.

Standardmäßig zeigt Claude Code eine Warnung an und führt Befehle ohne Sandboxing aus, wenn die Sandbox nicht gestartet werden kann (fehlende Abhängigkeiten, nicht unterstützte Plattform oder Plattformbeschränkungen). Um dies stattdessen zu einem Hard Failure zu machen, setzen Sie [`sandbox.failIfUnavailable`](/de/settings#sandbox-settings) auf `true`. Dies ist für verwaltete Bereitstellungen vorgesehen, die Sandboxing als Sicherheits-Gate erfordern.

### Sandbox-Modi

Claude Code bietet zwei Sandbox-Modi:

**Auto-Allow-Modus**: Bash-Befehle werden versuchen, innerhalb der Sandbox ausgeführt zu werden und sind automatisch zulässig, ohne dass eine Genehmigung erforderlich ist. Befehle, die nicht in der Sandbox ausgeführt werden können (wie solche, die Netzwerkzugriff auf nicht zulässige Hosts benötigen), fallen auf den regulären Genehmigungsfluss zurück. Explizite Ask/Deny-Regeln, die Sie konfiguriert haben, werden immer respektiert.

**Regulärer Genehmigungsmodus**: Alle Bash-Befehle durchlaufen den Standard-Genehmigungsfluss, auch wenn sie in der Sandbox ausgeführt werden. Dies bietet mehr Kontrolle, erfordert aber mehr Genehmigungen.

In beiden Modi erzwingt die Sandbox die gleichen Dateisystem- und Netzwerk-Einschränkungen. Der Unterschied liegt nur darin, ob Sandbox-Befehle automatisch genehmigt oder explizit genehmigt werden müssen.

<Info>
  Der Auto-Allow-Modus funktioniert unabhängig von Ihrer Genehmigungsmodus-Einstellung. Selbst wenn Sie sich nicht im „Bearbeitungen akzeptieren"-Modus befinden, werden Sandbox-Bash-Befehle automatisch ausgeführt, wenn Auto-Allow aktiviert ist. Dies bedeutet, dass Bash-Befehle, die Dateien innerhalb der Sandbox-Grenzen ändern, ohne Eingabeaufforderung ausgeführt werden, auch wenn Datei-Bearbeitungs-Tools normalerweise eine Genehmigung erfordern würden.
</Info>

### Sandboxing konfigurieren

Passen Sie das Sandbox-Verhalten durch Ihre `settings.json`-Datei an. Siehe [Einstellungen](/de/settings#sandbox-settings) für eine vollständige Konfigurationsreferenz.

#### Schreibzugriff für Subprozesse auf spezifische Pfade gewähren

Standardmäßig können Sandbox-Befehle nur in das aktuelle Arbeitsverzeichnis schreiben. Wenn Subprozess-Befehle wie `kubectl`, `terraform` oder `npm` außerhalb des Projektverzeichnisses schreiben müssen, verwenden Sie `sandbox.filesystem.allowWrite`, um Zugriff auf spezifische Pfade zu gewähren:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

Diese Pfade werden auf OS-Ebene durchgesetzt, daher respektieren alle Befehle, die innerhalb der Sandbox ausgeführt werden, einschließlich ihrer Kindprozesse, diese. Dies ist der empfohlene Ansatz, wenn ein Tool Schreibzugriff auf einen bestimmten Ort benötigt, anstatt das Tool mit `excludedCommands` vollständig aus der Sandbox auszuschließen.

Wenn `allowWrite` (oder `denyWrite`/`denyRead`/`allowRead`) in mehreren [Einstellungs-Scopes](/de/settings#settings-precedence) definiert ist, werden die Arrays **zusammengeführt**, was bedeutet, dass Pfade aus jedem Scope kombiniert werden, nicht ersetzt. Wenn beispielsweise verwaltete Einstellungen Schreibvorgänge zu `/opt/company-tools` zulassen und ein Benutzer `~/.kube` in seinen persönlichen Einstellungen hinzufügt, sind beide Pfade in der endgültigen Sandbox-Konfiguration enthalten. Dies bedeutet, dass Benutzer und Projekte die Liste erweitern können, ohne Pfade zu duplizieren oder zu überschreiben, die durch höher priorisierte Scopes gesetzt sind.

Pfad-Präfixe steuern, wie Pfade aufgelöst werden:

| Präfix                | Bedeutung                                                                                         | Beispiel                                                              |
| :-------------------- | :------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------- |
| `/`                   | Absoluter Pfad vom Dateisystem-Root                                                               | `/tmp/build` bleibt `/tmp/build`                                      |
| `~/`                  | Relativ zum Home-Verzeichnis                                                                      | `~/.kube` wird zu `$HOME/.kube`                                       |
| `./` oder kein Präfix | Relativ zum Projekt-Root für Projekt-Einstellungen oder zu `~/.claude` für Benutzer-Einstellungen | `./output` in `.claude/settings.json` wird zu `<project-root>/output` |

Das ältere `//path`-Präfix für absolute Pfade funktioniert immer noch. Wenn Sie zuvor `/path` erwartet haben, um projekt-relativ aufgelöst zu werden, wechseln Sie zu `./path`. Diese Syntax unterscheidet sich von [Read- und Edit-Genehmigungsregeln](/de/permissions#read-and-edit), die `//path` für absolut und `/path` für projekt-relativ verwenden. Sandbox-Dateisystem-Pfade verwenden Standard-Konventionen: `/tmp/build` ist ein absoluter Pfad.

Sie können auch Schreib- oder Lesezugriff mit `sandbox.filesystem.denyWrite` und `sandbox.filesystem.denyRead` blockieren. Diese werden mit allen Pfaden aus `Edit(...)` und `Read(...)` Genehmigungsregeln zusammengeführt. Um Lesezugriff auf spezifische Pfade innerhalb einer blockierten Region erneut zuzulassen, verwenden Sie `sandbox.filesystem.allowRead`, das Vorrang vor `denyRead` hat. Wenn `allowManagedReadPathsOnly` in verwalteten Einstellungen aktiviert ist, werden nur verwaltete `allowRead`-Einträge respektiert; Benutzer-, Projekt- und lokale `allowRead`-Einträge werden ignoriert. `denyRead` wird immer noch aus allen Quellen zusammengeführt.

Um beispielsweise das Lesen aus dem gesamten Home-Verzeichnis zu blockieren und gleichzeitig Lesevorgänge aus dem aktuellen Projekt zuzulassen, fügen Sie dies zu Ihrer Projekt-Datei `.claude/settings.json` hinzu:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

Das `.` in `allowRead` wird zum Projekt-Root aufgelöst, da diese Konfiguration in Projekt-Einstellungen lebt. Wenn Sie die gleiche Konfiguration in `~/.claude/settings.json` platzieren würden, würde `.` stattdessen zu `~/.claude` aufgelöst, und Projektdateien würden durch die `denyRead`-Regel blockiert bleiben.

<Tip>
  Nicht alle Befehle sind sofort mit Sandboxing kompatibel. Einige Hinweise, die Ihnen helfen können, das Beste aus der Sandbox herauszuholen:

  * Viele CLI-Tools erfordern Zugriff auf bestimmte Hosts. Wenn Sie diese Tools verwenden, werden sie um Genehmigung bitten, auf bestimmte Hosts zuzugreifen. Die Gewährung der Genehmigung ermöglicht ihnen, jetzt und in Zukunft auf diese Hosts zuzugreifen, was ihnen ermöglicht, sicher innerhalb der Sandbox ausgeführt zu werden.
  * `watchman` ist nicht kompatibel mit der Ausführung in der Sandbox. Wenn Sie `jest` ausführen, erwägen Sie die Verwendung von `jest --no-watchman`
  * `docker` ist nicht kompatibel mit der Ausführung in der Sandbox. Erwägen Sie, `docker` in `excludedCommands` anzugeben, um zu erzwingen, dass es außerhalb der Sandbox ausgeführt wird.
</Tip>

<Note>
  Claude Code enthält einen absichtlichen Escape-Hatch-Mechanismus, der es Befehlen ermöglicht, außerhalb der Sandbox ausgeführt zu werden, wenn nötig. Wenn ein Befehl aufgrund von Sandbox-Einschränkungen fehlschlägt (wie Netzwerkverbindungsprobleme oder inkompatible Tools), wird Claude aufgefordert, den Fehler zu analysieren und kann den Befehl mit dem `dangerouslyDisableSandbox`-Parameter erneut versuchen. Befehle, die diesen Parameter verwenden, durchlaufen den normalen Claude Code-Genehmigungsfluss, der Benutzererlaubnis zur Ausführung erfordert. Dies ermöglicht Claude Code, Grenzfälle zu handhaben, in denen bestimmte Tools oder Netzwerkoperationen nicht innerhalb von Sandbox-Einschränkungen funktionieren können.

  Sie können diesen Escape-Hatch deaktivieren, indem Sie `"allowUnsandboxedCommands": false` in Ihren [Sandbox-Einstellungen](/de/settings#sandbox-settings) setzen. Wenn deaktiviert, wird der `dangerouslyDisableSandbox`-Parameter vollständig ignoriert und alle Befehle müssen in der Sandbox ausgeführt oder explizit in `excludedCommands` aufgelistet werden.
</Note>

## Sicherheitsvorteile

### Schutz vor Prompt-Injection

Selbst wenn ein Angreifer Claude Code's Verhalten erfolgreich durch Prompt-Injection manipuliert, stellt die Sandbox sicher, dass Ihr System sicher bleibt:

**Dateisystem-Schutz:**

* Kann kritische Konfigurationsdateien wie `~/.bashrc` nicht ändern
* Kann System-Level-Dateien in `/bin/` nicht ändern
* Kann Dateien nicht lesen, die in Ihren [Claude-Genehmigungseinstellungen](/de/permissions#manage-permissions) blockiert sind

**Netzwerk-Schutz:**

* Kann Daten nicht zu von Angreifern kontrollierten Servern exfiltrieren
* Kann bösartige Skripte nicht von nicht autorisierten Domains herunterladen
* Kann keine unerwarteten API-Aufrufe an nicht genehmigten Diensten tätigen
* Kann keine Domains kontaktieren, die nicht explizit zulässig sind

**Überwachung und Kontrolle:**

* Alle Zugriffversuche außerhalb der Sandbox werden auf OS-Ebene blockiert
* Sie erhalten sofortige Benachrichtigungen, wenn Grenzen getestet werden
* Sie können wählen, zu verweigern, einmal zuzulassen oder Ihre Konfiguration dauerhaft zu aktualisieren

### Reduzierte Angriffsfläche

Sandboxing begrenzt den potenziellen Schaden durch:

* **Bösartige Abhängigkeiten**: NPM-Pakete oder andere Abhängigkeiten mit schädlichem Code
* **Kompromittierte Skripte**: Build-Skripte oder Tools mit Sicherheitslücken
* **Social Engineering**: Angriffe, die Benutzer dazu verleiten, gefährliche Befehle auszuführen
* **Prompt-Injection**: Angriffe, die Claude dazu verleiten, gefährliche Befehle auszuführen

### Transparente Bedienung

Wenn Claude Code versucht, auf Netzwerk-Ressourcen außerhalb der Sandbox zuzugreifen:

1. Der Vorgang wird auf OS-Ebene blockiert
2. Sie erhalten eine sofortige Benachrichtigung
3. Sie können wählen zu:
   * Die Anfrage verweigern
   * Sie einmal zuzulassen
   * Ihre Sandbox-Konfiguration aktualisieren, um sie dauerhaft zuzulassen

## Sicherheitsbeschränkungen

* Netzwerk-Sandboxing-Einschränkungen: Das Netzwerk-Filtersystem funktioniert durch Einschränkung der Domains, mit denen Prozesse verbunden werden dürfen. Es inspiziert den Datenverkehr, der durch den Proxy fließt, nicht anderweitig, und Benutzer sind verantwortlich dafür, dass sie nur vertrauenswürdige Domains in ihrer Richtlinie zulassen.

<Warning>
  Benutzer sollten sich der potenziellen Risiken bewusst sein, die sich aus der Zulassung breiter Domains wie `github.com` ergeben, die Datenexfiltration ermöglichen können. Auch kann es in einigen Fällen möglich sein, das Netzwerk-Filtern durch [Domain Fronting](https://en.wikipedia.org/wiki/Domain_fronting) zu umgehen.
</Warning>

* Privilege Escalation über Unix-Sockets: Die `allowUnixSockets`-Konfiguration kann versehentlich Zugriff auf leistungsstarke System-Services gewähren, die zu Sandbox-Umgehungen führen könnten. Wenn sie beispielsweise verwendet wird, um Zugriff auf `/var/run/docker.sock` zu zulassen, würde dies effektiv Zugriff auf das Host-System durch Ausnutzung des Docker-Sockets gewähren. Benutzer werden ermutigt, sorgfältig zu überlegen, welche Unix-Sockets sie durch die Sandbox zulassen.
* Dateisystem-Genehmigungseskalation: Übermäßig breite Dateisystem-Schreibgenehmigungen können Privilege-Escalation-Angriffe ermöglichen. Das Zulassen von Schreibvorgängen zu Verzeichnissen, die ausführbare Dateien in `$PATH`, System-Konfigurationsverzeichnisse oder Benutzer-Shell-Konfigurationsdateien (`.bashrc`, `.zshrc`) enthalten, kann zu Code-Ausführung in verschiedenen Sicherheitskontexten führen, wenn andere Benutzer oder System-Prozesse auf diese Dateien zugreifen.
* Linux-Sandbox-Stärke: Die Linux-Implementierung bietet starke Dateisystem- und Netzwerk-Isolation, enthält aber einen `enableWeakerNestedSandbox`-Modus, der es ermöglicht, in Docker-Umgebungen ohne privilegierte Namespaces zu funktionieren. Diese Option schwächt die Sicherheit erheblich ab und sollte nur in Fällen verwendet werden, in denen zusätzliche Isolation anderweitig durchgesetzt wird.

## Wie Sandboxing sich auf Genehmigungen bezieht

Sandboxing und [Genehmigungen](/de/permissions) sind komplementäre Sicherheitsebenen, die zusammenarbeiten:

* **Genehmigungen** steuern, welche Tools Claude Code verwenden kann, und werden evaluiert, bevor ein Tool ausgeführt wird. Sie gelten für alle Tools: Bash, Read, Edit, WebFetch, MCP und andere.
* **Sandboxing** bietet OS-Level-Durchsetzung, die einschränkt, worauf Bash-Befehle auf Dateisystem- und Netzwerk-Ebene zugreifen können. Es gilt nur für Bash-Befehle und ihre Kindprozesse.

Dateisystem- und Netzwerk-Einschränkungen werden sowohl durch Sandbox-Einstellungen als auch durch Genehmigungsregeln konfiguriert:

* Verwenden Sie `sandbox.filesystem.allowWrite`, um Subprozess-Schreibzugriff auf Pfade außerhalb des Arbeitsverzeichnisses zu gewähren
* Verwenden Sie `sandbox.filesystem.denyWrite` und `sandbox.filesystem.denyRead`, um Subprozess-Zugriff auf spezifische Pfade zu blockieren
* Verwenden Sie `sandbox.filesystem.allowRead`, um Lesezugriff auf spezifische Pfade innerhalb einer `denyRead`-Region erneut zuzulassen
* Verwenden Sie `Read` und `Edit` Deny-Regeln, um Zugriff auf spezifische Dateien oder Verzeichnisse zu blockieren
* Verwenden Sie `WebFetch` Allow/Deny-Regeln, um Domain-Zugriff zu steuern
* Verwenden Sie Sandbox `allowedDomains`, um zu steuern, auf welche Domains Bash-Befehle zugreifen können

Pfade aus beiden `sandbox.filesystem`-Einstellungen und Genehmigungsregeln werden zusammengeführt in die endgültige Sandbox-Konfiguration.

Dieses [Repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) enthält Starter-Einstellungskonfigurationen für häufige Bereitstellungsszenarien, einschließlich Sandbox-spezifischer Beispiele. Verwenden Sie diese als Ausgangspunkte und passen Sie sie an Ihre Anforderungen an.

## Erweiterte Verwendung

### Benutzerdefinierte Proxy-Konfiguration

Für Organisationen, die erweiterte Netzwerk-Sicherheit benötigen, können Sie einen benutzerdefinierten Proxy implementieren, um:

* HTTPS-Datenverkehr zu entschlüsseln und zu inspizieren
* Benutzerdefinierte Filterregeln anzuwenden
* Alle Netzwerk-Anfragen zu protokollieren
* Mit bestehender Sicherheitsinfrastruktur zu integrieren

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### Integration mit bestehenden Sicherheits-Tools

Das Sandboxing-Bash-Tool funktioniert zusammen mit:

* **Genehmigungsregeln**: Kombinieren Sie mit [Genehmigungseinstellungen](/de/permissions) für Defense-in-Depth
* **Entwicklungs-Container**: Verwenden Sie mit [devcontainers](/de/devcontainer) für zusätzliche Isolation
* **Enterprise-Richtlinien**: Erzwingen Sie Sandbox-Konfigurationen durch [verwaltete Einstellungen](/de/settings#settings-precedence)

## Best Practices

1. **Beginnen Sie restriktiv**: Beginnen Sie mit minimalen Genehmigungen und erweitern Sie nach Bedarf
2. **Überwachen Sie Protokolle**: Überprüfen Sie Sandbox-Verletzungsversuche, um Claude Code's Anforderungen zu verstehen
3. **Verwenden Sie umgebungsspezifische Konfigurationen**: Unterschiedliche Sandbox-Regeln für Entwicklungs- vs. Produktionsumgebungen
4. **Kombinieren Sie mit Genehmigungen**: Verwenden Sie Sandboxing zusammen mit IAM-Richtlinien für umfassende Sicherheit
5. **Testen Sie Konfigurationen**: Überprüfen Sie, dass Ihre Sandbox-Einstellungen legitime Workflows nicht blockieren

## Open Source

Die Sandbox-Runtime ist als Open-Source-npm-Paket für die Verwendung in Ihren eigenen Agent-Projekten verfügbar. Dies ermöglicht der breiteren AI-Agent-Community, sicherere und autonomere Systeme zu bauen. Dies kann auch verwendet werden, um andere Programme zu sandboxen, die Sie ausführen möchten. Um beispielsweise einen MCP-Server zu sandboxen, könnten Sie ausführen:

```bash theme={null}
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Für Implementierungsdetails und Quellcode besuchen Sie das [GitHub-Repository](https://github.com/anthropic-experimental/sandbox-runtime).

## Einschränkungen

* **Performance-Overhead**: Minimal, aber einige Dateisystem-Operationen können leicht langsamer sein
* **Kompatibilität**: Einige Tools, die spezifische System-Zugriffsmuster erfordern, benötigen möglicherweise Konfigurationsanpassungen oder müssen sogar außerhalb der Sandbox ausgeführt werden
* **Plattform-Unterstützung**: Unterstützt macOS, Linux und WSL2. WSL1 wird nicht unterstützt. Native Windows-Unterstützung ist geplant.

## Was Sandboxing nicht abdeckt

Die Sandbox isoliert Bash-Subprozesse. Andere Tools funktionieren unter verschiedenen Grenzen:

* **Integrierte Datei-Tools**: Read, Edit und Write verwenden das Genehmigungssystem direkt, anstatt durch die Sandbox zu laufen. Siehe [Genehmigungen](/de/permissions).
* **Computer-Nutzung**: Wenn Claude Apps öffnet und Ihren Bildschirm auf macOS steuert, läuft es auf Ihrem tatsächlichen Desktop, anstatt in einer isolierten Umgebung. Pro-App-Genehmigungseingaben kontrollieren jede Anwendung. Siehe [Computer-Nutzung in der CLI](/de/computer-use) oder [Computer-Nutzung auf Desktop](/de/desktop#let-claude-use-your-computer).

## Siehe auch

* [Sicherheit](/de/security) - Umfassende Sicherheitsfeatures und Best Practices
* [Genehmigungen](/de/permissions) - Genehmigungskonfiguration und Zugriffskontrolle
* [Einstellungen](/de/settings) - Vollständige Konfigurationsreferenz
* [CLI-Referenz](/de/cli-reference) - Befehlszeilenoptionen
