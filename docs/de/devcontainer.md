> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Entwicklungscontainer

> Erfahren Sie mehr über den Claude Code-Entwicklungscontainer für Teams, die konsistente, sichere Umgebungen benötigen.

Die Referenz [devcontainer-Einrichtung](https://github.com/anthropics/claude-code/tree/main/.devcontainer) und die zugehörige [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) bieten einen vorkonfigurierten Entwicklungscontainer, den Sie unverändert verwenden oder nach Ihren Anforderungen anpassen können. Dieser devcontainer funktioniert mit der Visual Studio Code [Dev Containers-Erweiterung](https://code.visualstudio.com/docs/devcontainers/containers) und ähnlichen Tools.

Die erweiterten Sicherheitsmaßnahmen des Containers (Isolierung und Firewall-Regeln) ermöglichen es Ihnen, `claude --dangerously-skip-permissions` auszuführen, um Berechtigungsaufforderungen für unbeaufsichtigte Operationen zu umgehen.

<Warning>
  Obwohl der devcontainer erhebliche Schutzmaßnahmen bietet, ist kein System vollständig immun gegen alle Angriffe.
  Bei Ausführung mit `--dangerously-skip-permissions` verhindern devcontainer nicht, dass ein bösartiges Projekt alles exfiltriert, das im devcontainer zugänglich ist, einschließlich Claude Code-Anmeldedaten.
  Wir empfehlen, devcontainer nur bei der Entwicklung mit vertrauenswürdigen Repositories zu verwenden.
  Halten Sie immer gute Sicherheitspraktiken ein und überwachen Sie die Aktivitäten von Claude.
</Warning>

## Wichtigste Funktionen

* **Produktionsreifes Node.js**: Basierend auf Node.js 20 mit wesentlichen Entwicklungsabhängigkeiten
* **Sicherheit nach Design**: Benutzerdefinierte Firewall, die den Netzwerkzugriff auf nur notwendige Dienste beschränkt
* **Benutzerfreundliche Tools**: Umfasst git, ZSH mit Produktivitätsverbesserungen, fzf und mehr
* **Nahtlose VS Code-Integration**: Vorkonfigurierte Erweiterungen und optimierte Einstellungen
* **Sitzungspersistenz**: Bewahrt Befehlsverlauf und Konfigurationen zwischen Container-Neustarts
* **Funktioniert überall**: Kompatibel mit macOS-, Windows- und Linux-Entwicklungsumgebungen

## Erste Schritte in 4 Schritten

1. Installieren Sie VS Code und die Remote - Containers-Erweiterung
2. Klonen Sie das [Claude Code-Referenzimplementierungs](https://github.com/anthropics/claude-code/tree/main/.devcontainer)-Repository
3. Öffnen Sie das Repository in VS Code
4. Wenn Sie dazu aufgefordert werden, klicken Sie auf „In Container erneut öffnen" (oder verwenden Sie die Befehlspalette: Cmd+Shift+P → „Remote-Containers: In Container erneut öffnen")

## Konfigurationsübersicht

Die devcontainer-Einrichtung besteht aus drei Hauptkomponenten:

* [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Steuert Container-Einstellungen, Erweiterungen und Volume-Mounts
* [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Definiert das Container-Image und installierte Tools
* [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Etabliert Netzwerksicherheitsregeln

## Sicherheitsfunktionen

Der Container implementiert einen mehrschichtigen Sicherheitsansatz mit seiner Firewall-Konfiguration:

* **Präzise Zugriffskontrolle**: Beschränkt ausgehende Verbindungen auf nur auf die Whitelist gesetzten Domains (npm-Registry, GitHub, Claude API usw.)
* **Zulässige ausgehende Verbindungen**: Die Firewall erlaubt ausgehende DNS- und SSH-Verbindungen
* **Standard-Deny-Richtlinie**: Blockiert alle anderen externen Netzwerkzugriffe
* **Startupüberprüfung**: Validiert Firewall-Regeln, wenn der Container initialisiert wird
* **Isolierung**: Erstellt eine sichere Entwicklungsumgebung, die von Ihrem Hauptsystem getrennt ist

## Anpassungsoptionen

Die devcontainer-Konfiguration ist so konzipiert, dass sie an Ihre Anforderungen angepasst werden kann:

* Fügen Sie VS Code-Erweiterungen basierend auf Ihrem Workflow hinzu oder entfernen Sie sie
* Ändern Sie Ressourcenzuordnungen für verschiedene Hardware-Umgebungen
* Passen Sie Netzwerkzugriffsberechtigungen an
* Passen Sie Shell-Konfigurationen und Entwickler-Tools an

## Beispiel-Anwendungsfälle

### Sichere Kundenarbeit

Verwenden Sie devcontainer, um verschiedene Kundenprojekte zu isolieren und sicherzustellen, dass Code und Anmeldedaten niemals zwischen Umgebungen vermischt werden.

### Team-Onboarding

Neue Teammitglieder können in wenigen Minuten eine vollständig konfigurierte Entwicklungsumgebung erhalten, mit allen notwendigen Tools und Einstellungen, die vorinstalliert sind.

### Konsistente CI/CD-Umgebungen

Spiegeln Sie Ihre devcontainer-Konfiguration in CI/CD-Pipelines, um sicherzustellen, dass Entwicklungs- und Produktionsumgebungen übereinstimmen.

## Verwandte Ressourcen

* [VS Code devcontainers-Dokumentation](https://code.visualstudio.com/docs/devcontainers/containers)
* [Claude Code-Sicherheitsbest Practices](/de/security)
* [Enterprise-Netzwerkkonfiguration](/de/network-config)
