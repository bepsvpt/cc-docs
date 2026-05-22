> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurieren Sie das Sandboxed-Bash-Tool

> Erfahren Sie, wie das Sandboxed-Bash-Tool von Claude Code Dateisystem- und Netzwerkisolation für sicherere und autonomere Agent-Ausführung bietet.

Die Bash-Sandbox ermöglicht es Claude, die meisten Shell-Befehle auszuführen, ohne um Genehmigung zu fragen. Anstatt jeden Befehl zu genehmigen, definieren Sie, welche Dateien und Netzwerk-Domains Befehle berühren können, und das Betriebssystem erzwingt diese Grenze für jeden Bash-Befehl und seine Kindprozesse.

Diese Seite behandelt Folgendes:

* [Aktivieren Sie die Sandbox](#get-started) und wählen Sie, wie Sandbox-Befehle genehmigt werden
* [Konfigurieren Sie](#configure-sandboxing), welche Pfade und Netzwerk-Domains Befehle erreichen können
* [Kombinieren Sie Sandboxing mit Genehmigungsregeln und Genehmigungsmodi](#how-sandboxing-relates-to-permissions-and-permission-modes)
* [Erzwingen Sie Sandboxing in einer Organisation](#configure-the-sandbox-for-your-organization) mit verwalteten Einstellungen

<Note>
  Um andere Isolationsansätze wie Dev-Container, benutzerdefinierte Container und virtuelle Maschinen zu vergleichen, siehe [Sandbox-Umgebungen](/de/sandbox-environments). Um Genehmigungseingaben für Tools außer Bash zu reduzieren, siehe [Genehmigungsmodi](/de/permission-modes).
</Note>

## Erste Schritte

Die Sandbox ist in Claude Code integriert und läuft auf macOS, Linux und WSL2. Native Windows wird nicht unterstützt. Führen Sie Claude Code unter Windows in einer WSL2-Distribution aus.

Auf macOS gibt es nichts zu installieren: Sandboxing verwendet das integrierte Seatbelt-Framework. Auf Linux und WSL2 basiert die Sandbox auf zwei Paketen, die in [Linux und WSL2 einrichten](#set-up-linux-and-wsl2) behandelt werden. Selbst wenn Sie diese noch nicht installiert haben, können Sie mit `/sandbox` beginnen, da sein Panel anzeigt, ob etwas fehlt.

<Steps>
  <Step title="Führen Sie /sandbox aus">
    Starten Sie eine Claude Code-Sitzung und führen Sie den Befehl `/sandbox` aus:

    ```text theme={null}
    /sandbox
    ```

    Dies öffnet das Sandbox-Panel mit drei Registerkarten:

    * **Mode**: Wählen Sie, wie Sandbox-Befehle genehmigt werden, behandelt im nächsten Schritt
    * **Overrides**: Wählen Sie, ob Befehle, die unter der Sandbox fehlschlagen, auf unsandboxed ausweichen können. Dies ist die Einstellung [`allowUnsandboxedCommands`](/de/settings#sandbox-settings)
    * **Config**: Zeigen Sie die aufgelösten Sandbox-Einstellungen an

    Wenn das Panel nur eine Registerkarte 'Dependencies" anzeigt, fehlt ein erforderliches Paket. Installieren Sie es wie in [Linux und WSL2 einrichten](#set-up-linux-and-wsl2) beschrieben, starten Sie Claude Code neu und führen Sie `/sandbox` erneut aus.
  </Step>

  <Step title="Wählen Sie einen Modus">
    Wählen Sie auf der Registerkarte 'Mode" Auto-Allow oder reguläre Genehmigungen. Auto-Allow führt Sandbox-Befehle ohne Eingabeaufforderung aus, und reguläre Genehmigungen behalten die regulären Genehmigungseingaben bei, auch wenn Befehle in der Sandbox ausgeführt werden. Siehe [Sandbox-Modi](#sandbox-modes) für die Befehle, die im Auto-Allow-Modus immer noch eingeben.
  </Step>

  <Step title="Führen Sie einen Bash-Befehl aus">
    Bitten Sie Claude, einen Befehl auszuführen, z. B. einen Build oder eine Test-Suite. Standardmäßig können Befehle in der Sandbox nur in das Arbeitsverzeichnis schreiben. Wenn ein Befehl zum ersten Mal eine neue Netzwerk-Domain benötigt, fordert Claude Code zur Genehmigung auf.

    Befehle, die nicht in der Sandbox ausgeführt werden können, fallen auf den regulären Genehmigungsfluss zurück. Um diese Grenzen zu erweitern oder zu verengen, siehe [Sandboxing konfigurieren](#configure-sandboxing).
  </Step>
</Steps>

Wenn Sie einen Modus im Panel auswählen, wird in die lokalen Einstellungen Ihres Projekts unter `.claude/settings.local.json` geschrieben, die für das aktuelle Projekt gelten und nicht in Git eingecheckt werden. Um die Sandbox in allen Ihren Projekten zu aktivieren, setzen Sie [`sandbox.enabled`](/de/settings#sandbox-settings) auf `true` in Ihren Benutzereinstellungen unter `~/.claude/settings.json`. Um Sandboxing für jeden Entwickler in einer Organisation zu erzwingen, verwenden Sie [verwaltete Einstellungen](#enforce-sandboxing-with-managed-settings).

<Warning>
  Standardmäßig zeigt Claude Code eine Warnung an und führt Befehle ohne Sandboxing aus, wenn die Sandbox nicht gestartet werden kann, da Abhängigkeiten fehlen oder die Plattform nicht unterstützt wird. Um dies stattdessen zu einem Hard Failure zu machen, setzen Sie [`sandbox.failIfUnavailable`](/de/settings#sandbox-settings) auf `true`. Dies ist für verwaltete Bereitstellungen vorgesehen, die Sandboxing als Sicherheits-Gate erfordern.
</Warning>

### Linux und WSL2 einrichten

Auf Linux und WSL2 basiert die Sandbox auf zwei Paketen:

* [`bubblewrap`](https://github.com/containers/bubblewrap): das unprivilegierte Sandboxing-Tool, das Dateisystem-Isolation erzwingt
* [`socat`](http://www.dest-unreach.org/socat/): das Relay, das verwendet wird, um Netzwerk-Datenverkehr durch den Sandbox-Proxy zu leiten

Installieren Sie diese mit dem Paketmanager Ihrer Distribution:

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

Nach der Installation zeigt die Registerkarte 'Dependencies" in `/sandbox` an, ob `ripgrep`, `bubblewrap`, `socat` und der Seccomp-Filter auf Ihrer Plattform verfügbar sind. Ripgrep ist mit der nativen Claude Code-Binärdatei gebündelt. Der Seccomp-Filter ist optional und fügt Unix-Domain-Socket-Blockierung hinzu. Installieren Sie ihn mit `npm install -g @anthropic-ai/sandbox-runtime`, wenn er fehlt.

Wenn eine erforderliche Abhängigkeit fehlt, ist die Registerkarte „Dependencies" die einzige angezeigte Registerkarte, bis Sie sie installieren. Die Abhängigkeitsprüfung läuft beim Start, daher starten Sie Claude Code nach der Installation von Paketen neu, damit `/sandbox` diese erkennt.

<AccordionGroup>
  <Accordion title="Ubuntu 24.04 und später: Erlauben Sie bubblewrap, Benutzer-Namespaces zu erstellen">
    Auf Ubuntu 24.04 und später verhindert die Standard-AppArmor-Richtlinie, dass bubblewrap die Benutzer-Namespaces erstellt, die es für die Isolation benötigt.

    Um zu überprüfen, ob Ihre Umgebung diese Einschränkung erzwingt, auch in WSL2, führen Sie `sysctl kernel.apparmor_restrict_unprivileged_userns` aus. Wenn der Schlüssel nicht existiert oder `0` zurückgibt, überspringen Sie diesen Schritt. Wenn er `1` zurückgibt, fügen Sie ein AppArmor-Profil hinzu, das `bwrap` diese Fähigkeit gewährt:

    ```bash theme={null}
    sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
    abi <abi/4.0>,
    include <tunables/global>

    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }
    EOF
    ```

    Das Profil gilt nur für `bwrap` selbst, nicht für die Befehle, die es in der Sandbox ausführt. Laden Sie AppArmor neu, um es anzuwenden:

    ```bash theme={null}
    sudo systemctl reload apparmor
    ```
  </Accordion>

  <Accordion title="WSL2-Hinweise">
    Überprüfen Sie Ihre WSL-Version mit `wsl -l -v` aus PowerShell. Wenn Sie `Sandboxing requires WSL2` sehen, läuft Ihre Distribution auf WSL1. Aktualisieren Sie sie auf WSL2 oder führen Sie Claude Code ohne Sandboxing aus.

    Auf WSL2 können Sandbox-Befehle keine Windows-Binärdateien wie `cmd.exe`, `powershell.exe` oder etwas unter `/mnt/c/` starten. WSL übergibt diese über einen Unix-Socket an den Windows-Host, den die Sandbox blockiert. Wenn ein Befehl eine Windows-Binärdatei aufrufen muss, fügen Sie ihn zu [`excludedCommands`](/de/settings#sandbox-settings) hinzu, damit er außerhalb der Sandbox ausgeführt wird.
  </Accordion>
</AccordionGroup>

### Sandbox-Modi

Claude Code bietet zwei Sandbox-Modi:

**Auto-Allow-Modus**: Bash-Befehle werden versuchen, in der Sandbox ausgeführt zu werden und sind automatisch zulässig, ohne dass eine Genehmigung erforderlich ist. Befehle, die nicht in der Sandbox ausgeführt werden können, z. B. solche, die Netzwerkzugriff auf nicht zulässige Hosts benötigen, fallen auf den regulären Genehmigungsfluss zurück, bei dem Claude Code Ihre [Genehmigungsregeln](/de/permissions) überprüft und Sie für jeden Befehl auffordert, den diese Regeln nicht bereits zulassen.

Selbst im Auto-Allow-Modus gelten folgende Punkte:

* Explizite [Deny-Regeln](/de/permissions) werden immer respektiert
* `rm`- oder `rmdir`-Befehle, die auf `/`, Ihr Home-Verzeichnis oder andere kritische Systempfade abzielen, lösen immer noch eine Genehmigungseingabe aus
* [Ask-Regeln](/de/permissions) gelten für Befehle, die auf den regulären Genehmigungsfluss zurückfallen

**Regulärer Genehmigungsmodus**: Alle Bash-Befehle durchlaufen den regulären Genehmigungsfluss, auch wenn sie in der Sandbox ausgeführt werden. Dies bietet mehr Kontrolle, erfordert aber mehr Genehmigungen.

In beiden Modi erzwingt die Sandbox die gleichen Dateisystem- und Netzwerk-Einschränkungen. Der Unterschied liegt nur darin, ob Sandbox-Befehle automatisch genehmigt oder explizit genehmigt werden müssen.

Einige Befehle können überhaupt nicht in der Sandbox ausgeführt werden, z. B. Tools, die nicht kompatibel sind oder einen Host benötigen, den Sie nicht zulässig gemacht haben. Anstatt die Aufgabe fehlschlagen zu lassen oder Sie zu zwingen, Sandboxing auszuschalten, enthält Claude Code eine Fluchtluke: Wenn ein Befehl aufgrund von Sandbox-Einschränkungen fehlschlägt, analysiert Claude den Fehler und kann den Befehl mit dem Parameter `dangerouslyDisableSandbox` erneut versuchen. Der erneut versuchte Befehl läuft außerhalb der Sandbox, daher durchläuft er den regulären Genehmigungsfluss und erfordert Ihre Genehmigung.

Sie können diese Fluchtluke deaktivieren, indem Sie `"allowUnsandboxedCommands": false` in Ihren [Sandbox-Einstellungen](/de/settings#sandbox-settings) setzen. Wenn deaktiviert, was die Registerkarte `/sandbox` Overrides als **Strict Sandbox Mode** anzeigt, wird der Parameter `dangerouslyDisableSandbox` vollständig ignoriert und alle Befehle müssen in der Sandbox ausgeführt oder explizit in `excludedCommands` aufgelistet werden.

<Info>
  Der Auto-Allow-Modus funktioniert unabhängig von Ihrer Genehmigungsmodus-Einstellung. Selbst wenn Sie sich nicht im „Bearbeitungen akzeptieren"-Modus befinden, werden Sandbox-Bash-Befehle automatisch ausgeführt, wenn Auto-Allow aktiviert ist. Dies bedeutet, dass Bash-Befehle, die Dateien innerhalb der Sandbox-Grenzen ändern, ohne Eingabeaufforderung ausgeführt werden, auch wenn Datei-Bearbeitungs-Tools normalerweise eine Genehmigung erfordern würden.
</Info>

## Sandboxing konfigurieren

Passen Sie das Sandbox-Verhalten durch Ihre `settings.json`-Datei an. Siehe [Einstellungen](/de/settings#sandbox-settings) für die vollständige Konfigurationsreferenz.

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

Diese Pfade werden auf OS-Ebene durchgesetzt, daher respektieren alle Befehle, die in der Sandbox ausgeführt werden, einschließlich ihrer Kindprozesse, diese. Dies ist der empfohlene Ansatz, wenn ein Tool Schreibzugriff auf einen bestimmten Ort benötigt, anstatt das Tool mit `excludedCommands` vollständig aus der Sandbox auszuschließen.

Wenn das gleiche Dateisystem-Array in mehreren [Einstellungs-Scopes](/de/settings#settings-precedence) definiert ist, werden die Arrays zusammengeführt: Pfade aus jedem Scope werden kombiniert, nicht ersetzt.

Pfad-Präfixe steuern, wie Pfade aufgelöst werden:

| Präfix                | Bedeutung                                                                                         | Beispiel                                                              |
| :-------------------- | :------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------- |
| `/`                   | Absoluter Pfad vom Dateisystem-Root                                                               | `/tmp/build` bleibt `/tmp/build`                                      |
| `~/`                  | Relativ zum Home-Verzeichnis                                                                      | `~/.kube` wird zu `$HOME/.kube`                                       |
| `./` oder kein Präfix | Relativ zum Projekt-Root für Projekt-Einstellungen oder zu `~/.claude` für Benutzer-Einstellungen | `./output` in `.claude/settings.json` wird zu `<project-root>/output` |

Diese Syntax unterscheidet sich von [Read- und Edit-Genehmigungsregeln](/de/permissions#read-and-edit), die `//path` für absolut und `/path` für projekt-relativ verwenden. Sandbox-Dateisystem-Pfade verwenden Standard-Konventionen: `/tmp/build` ist absolut.

Sie können auch Schreib- oder Lesezugriff mit `sandbox.filesystem.denyWrite` und `sandbox.filesystem.denyRead` blockieren und spezifische Pfade innerhalb einer blockierten Region mit `sandbox.filesystem.allowRead` erneut zulassen.

Das folgende Beispiel blockiert das Lesen aus dem gesamten Home-Verzeichnis und erlaubt gleichzeitig Lesevorgänge aus dem aktuellen Projekt. Platzieren Sie es in der Datei `.claude/settings.json` Ihres Projekts, da der relative Pfad `.` nur aufgelöst wird, wenn die Konfiguration in Projekt-Einstellungen lebt:

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

## Wie Sandboxing funktioniert

### Dateisystem-Isolation

Das Sandboxed-Bash-Tool beschränkt den Dateisystem-Zugriff auf spezifische Verzeichnisse:

* **Standard-Schreibverhalten**: Lese- und Schreibzugriff auf das aktuelle Arbeitsverzeichnis und seine Unterverzeichnisse
* **Standard-Leseverhalten**: Lesezugriff auf den gesamten Computer, außer bestimmten blockierten Verzeichnissen. Beachten Sie, dass diese Standard-Einstellung immer noch das Lesen von Anmeldedatendateien wie `~/.aws/credentials` und `~/.ssh/` ermöglicht. Fügen Sie diese zu `denyRead` hinzu, um sie zu blockieren.
* **Blockierter Zugriff**: Kann Dateien außerhalb des aktuellen Arbeitsverzeichnisses nicht ohne explizite Genehmigung ändern, einschließlich Shell-Konfigurationsdateien wie `~/.bashrc` und System-Binärdateien in `/bin/`
* **Konfigurierbar**: Definieren Sie benutzerdefinierte zulässige und blockierte Pfade durch Einstellungen

Sie können Schreibzugriff auf zusätzliche Pfade mit `sandbox.filesystem.allowWrite` in Ihren Einstellungen gewähren. Diese Einschränkungen werden auf OS-Ebene durchgesetzt, daher gelten sie für alle Subprozess-Befehle, einschließlich Tools wie `kubectl`, `terraform` und `npm`, nicht nur für Claudes Datei-Tools.

### Netzwerk-Isolation

Der Netzwerkzugriff wird durch einen Proxy-Server gesteuert, der außerhalb der Sandbox läuft:

* **Domain-Einschränkungen**: Keine Domains sind vorab zulässig. Wenn ein Befehl zum ersten Mal eine neue Domain benötigt, fordert Claude Code zur Genehmigung auf. Lassen Sie Domains vorab mit [`allowedDomains`](/de/settings#sandbox-settings) zu, um die Eingabeaufforderung zu vermeiden.
* **Verwaltete Sperrung**: Wenn [`allowManagedDomainsOnly`](/de/settings#sandbox-settings) in verwalteten Einstellungen gesetzt ist, werden nicht zulässige Domains automatisch blockiert, anstatt zu fragen, und nur `allowedDomains` aus verwalteten Einstellungen werden berücksichtigt.
* **Benutzerdefinierte Proxy-Unterstützung**: Fortgeschrittene Benutzer können benutzerdefinierte Regeln für ausgehenden Datenverkehr implementieren
* **Umfassende Abdeckung**: Einschränkungen gelten für alle Skripte, Programme und Subprozesse, die durch Befehle erzeugt werden

<Note>
  Der integrierte Proxy erzwingt die Zulassungsliste basierend auf dem angeforderten Hostnamen und beendet oder inspiziert keinen TLS-Datenverkehr. Siehe [Sicherheitsbeschränkungen](#security-limitations) für die Auswirkungen dieses Designs und [Benutzerdefinierte Proxy-Konfiguration](#custom-proxy-configuration), wenn Ihr Bedrohungsmodell TLS-Inspektion erfordert.
</Note>

### OS-Level-Durchsetzung

Das Sandboxed-Bash-Tool nutzt Betriebssystem-Sicherheits-Primitive:

* **macOS**: Verwendet Seatbelt für Sandbox-Durchsetzung
* **Linux**: Verwendet [bubblewrap](https://github.com/containers/bubblewrap) für Isolation
* **WSL2**: Verwendet bubblewrap, wie Linux

WSL1 wird nicht unterstützt, da bubblewrap Kernel-Features erfordert, die nur in WSL2 verfügbar sind. Diese OS-Level-Einschränkungen stellen sicher, dass alle Kindprozesse, die durch Claudes Befehle erzeugt werden, die gleichen Sicherheitsgrenzen erben.

Diese gleichen Primitive sind als das eigenständige Paket [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropic-experimental/sandbox-runtime) verfügbar, das die Seite [Sandbox-Umgebungen](/de/sandbox-environments#sandbox-runtime) als separaten Ansatz zum Wrapping des gesamten Claude Code-Prozesses behandelt.

## Wie Sandboxing sich auf Genehmigungen und Genehmigungsmodi bezieht

Sandboxing, [Genehmigungsregeln](/de/permissions) und [Genehmigungsmodi](/de/permission-modes) sind komplementäre Schichten. Die folgenden Abschnitte behandeln, wie die Sandbox mit jedem interagiert.

### Genehmigungsregeln

Genehmigungsregeln und Sandboxing steuern verschiedene Dinge:

* **Genehmigungsregeln** steuern, welche Tools Claude Code verwenden kann, und werden evaluiert, bevor ein Tool ausgeführt wird. Sie gelten für alle Tools: Bash, Read, Edit, WebFetch, MCP und andere.
* **Sandboxing** bietet OS-Level-Durchsetzung, die einschränkt, worauf Bash-Befehle auf Dateisystem- und Netzwerk-Ebene zugreifen können. Es gilt nur für Bash-Befehle und ihre Kindprozesse.

Die beiden Schichten unterscheiden sich auch in ihrer Durchsetzung. Claude Code evaluiert Genehmigungsentscheidungen, bevor ein Befehl ausgeführt wird, basierend auf der Befehlszeichenfolge und, im Auto-Modus, dem Urteil eines separaten Klassifizierers darüber, ob der Befehl sicher ist. Das Betriebssystem erzwingt die Sandbox-Grenze auf dem laufenden Prozess, daher gilt sie unabhängig davon, was das Modell ausführen wollte, und selbst wenn ein zulässiger Befehl mehr tut als sein Name vermuten lässt.

Dateisystem- und Netzwerk-Einschränkungen werden sowohl durch Sandbox-Einstellungen als auch durch Genehmigungsregeln konfiguriert:

| Einstellung oder Regel                                           | Was es tut                                                                                                |
| :--------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| `sandbox.filesystem.allowWrite`                                  | Gewährt Subprozess-Schreibzugriff auf Pfade außerhalb des Arbeitsverzeichnisses                           |
| `sandbox.filesystem.denyWrite` und `sandbox.filesystem.denyRead` | Blockiert Subprozess-Zugriff auf spezifische Pfade                                                        |
| `sandbox.filesystem.allowRead`                                   | Erlaubt das Lesen spezifischer Pfade innerhalb einer `denyRead`-Region erneut                             |
| `Edit` Zulassungsregeln                                          | Gewähren Schreibzugriff auf spezifische Pfade, auf die gleiche Weise wie `sandbox.filesystem.allowWrite`  |
| `Read` und `Edit` Deny-Regeln                                    | Blockiert Zugriff auf spezifische Dateien oder Verzeichnisse                                              |
| `WebFetch` Zulassungs- und Deny-Regeln                           | Steuern Domain-Zugriff                                                                                    |
| Sandbox `allowedDomains`                                         | Steuert, auf welche Domains Bash-Befehle zugreifen können                                                 |
| Sandbox `deniedDomains`                                          | Blockiert spezifische Domains, auch wenn ein breiteres `allowedDomains`-Wildcard sie sonst zulassen würde |

Pfade aus beiden `sandbox.filesystem`-Einstellungen und Genehmigungsregeln werden zusammengeführt in die endgültige Sandbox-Konfiguration.

Das [Repository der claude-code mit Beispielen](https://github.com/anthropics/claude-code/tree/main/examples/settings) enthält Starter-Einstellungskonfigurationen für häufige Bereitstellungsszenarien, einschließlich Sandbox-spezifischer Beispiele. Verwenden Sie diese als Ausgangspunkte und passen Sie sie an Ihre Anforderungen an.

### Genehmigungsmodi

`/sandbox` ist kein [Genehmigungsmodus](/de/permission-modes). Genehmigungsmodi entscheiden, ob ein Tool-Aufruf ausgeführt wird und ob Sie zuerst aufgefordert werden, während die Sandbox einschränkt, worauf ein Bash-Befehl zugreifen kann, sobald er ausgeführt wird. Sie unterscheiden sich darin, was sie steuern und was die Pro-Aktion-Eingabeaufforderung ersetzt:

|                                                                     | Was es steuert                                                   | Was die Eingabeaufforderung ersetzt                                                                                                                                              |
| :------------------------------------------------------------------ | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/sandbox`                                                          | Worauf ein Bash-Befehl zugreifen kann, sobald er ausgeführt wird | Die Sandbox-Grenze selbst, im [Auto-Allow-Modus](#sandbox-modes)                                                                                                                 |
| [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode) | Ob jeder Tool-Aufruf ausgeführt wird                             | Ein Klassifizierer, der Aktionen überprüft                                                                                                                                       |
| `--dangerously-skip-permissions`                                    | Ob jeder Tool-Aufruf ausgeführt wird                             | Nichts. [Geschützte Pfad](/de/permission-modes#protected-paths)-Prüfungen werden auch übersprungen; nur das Entfernen von `/` oder Ihrem Home-Verzeichnis fordert immer noch auf |

Der [Auto-Allow-Modus](#sandbox-modes) der Sandbox ist separat vom [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode): Auto-Allow genehmigt Bash-Befehle, weil die Sandbox-Grenze sie enthält, während der Auto-Modus einen Klassifizierer verwendet, um Aktionen zu überprüfen. Die beiden funktionieren unabhängig und können kombiniert werden. Um eine Isolationsgrenze für unbeaufsichtigte Läufe zu wählen, siehe [Sandbox-Umgebungen](/de/sandbox-environments#how-isolation-relates-to-permission-modes).

## Konfigurieren Sie die Sandbox für Ihre Organisation

Administratoren können Sandboxing für jeden Benutzer erfordern, Entwickler daran hindern, die Richtlinie zu erweitern, und Sandbox-Datenverkehr durch einen Unternehmens-Proxy leiten.

### Erzwingen Sie Sandboxing mit verwalteten Einstellungen

Um die Sandbox für jeden Entwickler zu erfordern, liefern Sie die `sandbox`-Schlüssel über [verwaltete Einstellungen](/de/settings#settings-files), entweder als Datei, die von Ihrem MDM verwaltet wird, oder über [server-verwaltete Einstellungen](/de/server-managed-settings) auf Claude.ai.

Die folgende Konfiguration verwalteter Einstellungen aktiviert die Sandbox, weigert sich, Claude Code zu starten, wenn die Sandbox nicht initialisiert werden kann, und verhindert, dass das Modell Befehle außerhalb der Sandbox erneut versucht:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

Die beiden Schlüssel über `enabled` hinaus steuern, was passiert, wenn die Sandbox einen Befehl nicht ausführen kann:

* **`failIfUnavailable`**: Eine fehlende Abhängigkeit wie bubblewrap auf Linux blockiert Claude Code vom Start, anstatt eine Warnung anzuzeigen und auf unsandboxed-Ausführung zurückzufallen
* **`allowUnsandboxedCommands: false`**: Die Fluchtluke `dangerouslyDisableSandbox` wird ignoriert, daher können Befehle, die unter der Sandbox fehlschlagen, nicht außerhalb davon erneut versucht werden

Zwei Ergänzungen sind erwägenswert. Fügen Sie `excludedCommands` für alle von der Organisation genehmigten Tools hinzu, die ohne Isolation ausgeführt werden müssen. Fügen Sie [`denyRead`](#filesystem-isolation)-Einträge für Anmeldedaten-Verzeichnisse wie `~/.aws` und `~/.ssh` hinzu, die die Standard-Lesrichtlinie immer noch zulässt.

Die Sandbox läuft nicht auf native Windows, daher müssen Sie diese Konfiguration auf macOS und Linux beschränken oder diese Benutzer Claude Code in WSL2 oder einem Container ausführen lassen, wenn Ihre Flotte Windows-Hosts enthält.

### Verhindern Sie, dass Entwickler die Richtlinie erweitern

Für boolesche Schlüssel wie `enabled` und `failIfUnavailable` verwendet Claude Code den verwalteten Wert und ignoriert alles, das ein Entwickler lokal setzt. Für Array-Schlüssel wie `excludedCommands` und `allowRead` führt Claude Code Einträge aus jedem Scope zusammen, daher kann ein Entwickler Einträge anhängen, die die Richtlinie erweitern.

Setzen Sie `allowManagedReadPathsOnly` auf `true` in verwalteten Einstellungen, damit nur `allowRead`-Einträge aus verwalteten Einstellungen berücksichtigt werden. Benutzer-, Projekt- und lokale `allowRead`-Einträge werden ignoriert. Dies verhindert, dass Entwickler den Lesezugriff über die von der Organisation genehmigten Pfade hinaus erweitern. Um Netzwerk-Domains auf die gleiche Weise auf die verwalteten Werte zu sperren, setzen Sie [`allowManagedDomainsOnly`](/de/settings#sandbox-settings).

`excludedCommands` hat keine äquivalente verwaltete Sperrung, daher kann ein Entwickler immer Einträge anhängen, die zusätzliche Befehle außerhalb der Sandbox ausführen. Halten Sie die verwaltete Liste eng.

### Benutzerdefinierte Proxy-Konfiguration

Für Organisationen, die erweiterte Netzwerk-Sicherheit erfordern, können Sie einen benutzerdefinierten Proxy implementieren, um:

* HTTPS-Datenverkehr zu entschlüsseln und zu inspizieren
* Benutzerdefinierte Filterregeln anzuwenden
* Alle Netzwerk-Anfragen zu protokollieren
* Mit bestehender Sicherheitsinfrastruktur zu integrieren

Um Claude Code auf Ihren Proxy zu verweisen, setzen Sie die Proxy-Ports in [Sandbox-Einstellungen](/de/settings#sandbox-settings):

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

## Fehlerbehebung

Einige Befehle schlagen in der Sandbox fehl, obwohl sie außerhalb davon funktionieren. Die folgenden Fixes behandeln die häufigsten Fälle.

* **Befehle schlagen mit einem Host-not-allowed-Fehler fehl**: Viele CLI-Tools müssen bestimmte Hosts erreichen. Das Gewähren der Genehmigung bei Aufforderung fügt den Host zu Ihrer Zulassungsliste hinzu, damit das Tool in Zukunft in der Sandbox ausgeführt wird.
* **`jest` hängt oder schlägt fehl**: `watchman` ist nicht kompatibel mit der Sandbox. Führen Sie stattdessen `jest --no-watchman` aus.
* **Go-basierte CLIs schlagen TLS-Verifizierung auf macOS fehl**: Tools wie `gh`, `gcloud` und `terraform` können unter Seatbelt TLS-Verifizierung fehlschlagen. Listen Sie diese Tools in `excludedCommands` auf, um sie außerhalb der Sandbox auszuführen. Wenn Sie `httpProxyPort` mit einem MITM-Proxy und benutzerdefinierter CA verwenden, setzen Sie stattdessen [`enableWeakerNetworkIsolation`](/de/settings#sandbox-settings) auf `true`.
* **`docker`-Befehle schlagen fehl**: `docker` ist nicht kompatibel mit der Sandbox. Fügen Sie `docker *` zu `excludedCommands` hinzu, um es außerhalb der Sandbox auszuführen.
* **Bubblewrap schlägt beim Start in einem Container fehl**: In einem unprivilegierten Container kann bubblewrap kein frisches `/proc`-Dateisystem mounten. Setzen Sie [`enableWeakerNestedSandbox`](/de/settings#sandbox-settings) auf `true`, damit die innere Sandbox das vorhandene `/proc` des Containers bind-mountet. Verwenden Sie diese Einstellung nur, wenn der äußere Container bereits die Isolationsgrenze bietet, die Sie benötigen, da sie Prozessinformationen für Sandbox-Befehle verfügbar macht, die ein frisches `/proc`-Mount verbergen würde.
* **Seccomp-Filter auf Linux**: Der Seccomp-Filter ist erforderlich, um Unix-Domain-Sockets zu blockieren. Die Registerkarte „Dependencies" in `/sandbox` zeigt an, ob er verfügbar ist. Wenn er fehlt, führen Sie `npm install -g @anthropic-ai/sandbox-runtime` aus, um den Helper zu installieren.
* **`--dangerously-skip-permissions` schlägt als Root fehl**: Dieses Flag wird blockiert, wenn es als Root oder über sudo auf Linux und macOS ausgeführt wird, da Root-Zugriff kombiniert mit keinen Genehmigungseingaben jede Datei oder jeden Service auf dem System ändern kann. Die Prüfung wird automatisch in einer erkannten Sandbox übersprungen. Um autonom in einem Container auszuführen, verwenden Sie die [Dev-Container](/de/devcontainer)-Konfiguration, die Claude Code als Nicht-Root-Benutzer ausführt.

## Einschränkungen

Sandboxing reduziert das Risiko, ist aber keine vollständige Isolationsgrenze. Überprüfen Sie die folgenden Einschränkungen, bevor Sie sich darauf als Hard-Sicherheitskontrolle verlassen.

### Sicherheitsbeschränkungen

* **Netzwerk-Filterung**: Das Netzwerk-Filtersystem funktioniert durch Einschränkung der Domains, mit denen Prozesse verbunden werden dürfen. Der integrierte Proxy beendet oder führt keine TLS-Inspektion auf ausgehenden Datenverkehr durch, daher werden die Inhalte verschlüsselter Verbindungen nicht untersucht. Sie sind verantwortlich dafür, dass nur vertrauenswürdige Domains in Ihrer Richtlinie zulässig sind.

<Warning>
  Das Zulassen breiter Domains wie `github.com` kann Pfade für Datenexfiltration schaffen. Da der Proxy seine Zulassungsentscheidung vom Client-bereitgestellten Hostnamen trifft, ohne TLS zu inspizieren, kann Code, der in der Sandbox ausgeführt wird, möglicherweise [Domain Fronting](https://en.wikipedia.org/wiki/Domain_fronting) oder ähnliche Techniken verwenden, um Hosts außerhalb der Zulassungsliste zu erreichen. Wenn Ihr Bedrohungsmodell stärkere Garantien erfordert, konfigurieren Sie einen [benutzerdefinierten Proxy](#custom-proxy-configuration), der TLS beendet und Datenverkehr inspiziert, und installieren Sie sein CA-Zertifikat in der Sandbox. Stärkere TLS-bewusste Netzwerk-Isolation ist ein aktives Entwicklungsgebiet.
</Warning>

* **Privilege Escalation über Unix-Sockets**: Die Konfiguration `allowUnixSockets` kann versehentlich Zugriff auf leistungsstarke System-Services gewähren, die zu Sandbox-Umgehungen führen könnten. Wenn Sie beispielsweise Zugriff auf `/var/run/docker.sock` zulassen, würde dies effektiv Zugriff auf das Host-System durch den Docker-Socket gewähren. Überdenken Sie sorgfältig alle Unix-Sockets, die Sie durch die Sandbox zulassen.
* **Dateisystem-Genehmigungseskalation**: Übermäßig breite Dateisystem-Schreibgenehmigungen können Privilege-Escalation-Angriffe ermöglichen. Das Zulassen von Schreibvorgängen zu Verzeichnissen, die ausführbare Dateien in `$PATH`, System-Konfigurationsverzeichnisse oder Benutzer-Shell-Konfigurationsdateien wie `.bashrc` oder `.zshrc` enthalten, kann zu Code-Ausführung in verschiedenen Sicherheitskontexten führen, wenn andere Benutzer oder System-Prozesse auf diese Dateien zugreifen.
* **Linux-Sandbox-Stärke**: Die Linux-Implementierung bietet starke Dateisystem- und Netzwerk-Isolation, enthält aber einen `enableWeakerNestedSandbox`-Modus, der es ermöglicht, in Docker-Umgebungen ohne privilegierte Namespaces zu funktionieren, oder auf Linux-Hosts, wo unprivilegierte Benutzer-Namespaces durch sysctl deaktiviert sind. Diese Option schwächt die Sicherheit erheblich ab und sollte nur verwendet werden, wenn zusätzliche Isolation anderweitig durchgesetzt wird.
* **Einstellungsdateien geschützt**: Die Sandbox verweigert automatisch Schreibzugriff auf Claudes `settings.json`-Dateien in jedem Scope und auf das verwaltete Einstellungsverzeichnis, daher kann ein Sandbox-Befehl seine eigene Richtlinie nicht ändern.

### Plattform- und Tool-Kompatibilität

* **Plattform-Unterstützung**: Unterstützt macOS, Linux und WSL2. WSL1 und native Windows werden nicht unterstützt.
* **Performance-Overhead**: Minimal, aber einige Dateisystem-Operationen können leicht langsamer sein.
* **Tool-Kompatibilität**: Einige Tools, die spezifische System-Zugriffsmuster erfordern, benötigen möglicherweise Konfigurationsanpassungen oder müssen möglicherweise außerhalb der Sandbox ausgeführt werden.

### Umfang

Die Sandbox isoliert Bash-Subprozesse. Andere Tools funktionieren unter verschiedenen Grenzen:

* **Integrierte Datei-Tools**: Read, Edit und Write verwenden das Genehmigungssystem direkt, anstatt durch die Sandbox zu laufen. Siehe [Genehmigungen](/de/permissions).
* **Computer-Nutzung**: Wenn Claude Apps öffnet und Ihren Bildschirm steuert, läuft es auf Ihrem tatsächlichen Desktop, anstatt in einer isolierten Umgebung. Pro-App-Genehmigungseingaben kontrollieren jede Anwendung. Siehe [Computer-Nutzung in der CLI](/de/computer-use) oder [Computer-Nutzung auf Desktop](/de/desktop#let-claude-use-your-computer).
* **Umgebungsvariablen**: Sandbox-Bash-Befehle erben die Umgebung des übergeordneten Prozesses standardmäßig, einschließlich aller dort gesetzten Anmeldedaten. Um Anthropic- und Cloud-Provider-Anmeldedaten aus Subprozessen zu entfernen, setzen Sie [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/de/env-vars).
* **Subagenten**: [Subagenten](/de/sub-agents) laufen im gleichen Prozess wie die übergeordnete Sitzung und verwenden die gleiche Sandbox-Konfiguration. Bash-Befehle in einem Subagenten werden in der Sandbox ausgeführt, wenn Sandboxing in der übergeordneten Sitzung aktiviert ist.

<Warning>
  Effektives Sandboxing erfordert **sowohl** Dateisystem- als auch Netzwerk-Isolation. Ohne Netzwerk-Isolation könnte ein kompromittierter Agent sensible Dateien wie SSH-Schlüssel exfiltrieren. Ohne Dateisystem-Isolation könnte ein kompromittierter Agent System-Ressourcen manipulieren, um Netzwerkzugriff zu erlangen. Wenn Sie die Standardwerte erweitern, überprüfen Sie, dass ein `allowWrite`-Pfad, ein breiter `allowedDomains`-Eintrag oder eine `excludedCommands`-Ausnahme keine Einschränkung auf der anderen Seite rückgängig macht.
</Warning>

## Siehe auch

* [Sandbox-Umgebungen](/de/sandbox-environments): Vergleichen Sie die integrierte Sandbox mit Dev-Containern, Containern und VMs
* [Sicherheit](/de/security): Umfassende Sicherheitsfeatures und Best Practices
* [Genehmigungen](/de/permissions): Genehmigungskonfiguration und Zugriffskontrolle
* [Einstellungen](/de/settings): Vollständige Konfigurationsreferenz
* [CLI-Referenz](/de/cli-reference): Befehlszeilenoptionen
