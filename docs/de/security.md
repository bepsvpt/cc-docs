> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sicherheit

> Erfahren Sie mehr über die Sicherheitsvorkehrungen von Claude Code und Best Practices für sichere Nutzung.

## Wie wir Sicherheit angehen

### Sicherheitsfundament

Die Sicherheit Ihres Codes ist von größter Bedeutung. Claude Code ist mit Sicherheit im Kern entwickelt worden, gemäß Anthropics umfassendem Sicherheitsprogramm. Erfahren Sie mehr und greifen Sie auf Ressourcen zu (SOC 2 Type 2 Bericht, ISO 27001 Zertifikat usw.) im [Anthropic Trust Center](https://trust.anthropic.com).

### Berechtigungsbasierte Architektur

Claude Code verwendet standardmäßig strikte Nur-Lesen-Berechtigungen. Wenn zusätzliche Aktionen erforderlich sind (Dateien bearbeiten, Tests ausführen, Befehle ausführen), fordert Claude Code explizite Genehmigung an. Benutzer kontrollieren, ob sie Aktionen einmalig genehmigen oder automatisch zulassen möchten.

Wir haben Claude Code so gestaltet, dass es transparent und sicher ist. Beispielsweise erfordern wir Genehmigung für Bash-Befehle vor ihrer Ausführung, was Ihnen direkte Kontrolle gibt. Dieser Ansatz ermöglicht es Benutzern und Organisationen, Berechtigungen direkt zu konfigurieren.

Für detaillierte Berechtigungskonfiguration siehe [Berechtigungen](/de/permissions).

### Integrierte Schutzmaßnahmen

Um Risiken in agentengestützten Systemen zu mindern:

* **Sandbox-Bash-Tool**: [Sandbox](/de/sandboxing) Bash-Befehle mit Dateisystem- und Netzwerkisolation, wodurch Berechtigungsaufforderungen reduziert werden, während die Sicherheit gewährleistet bleibt. Aktivieren Sie mit `/sandbox`, um Grenzen zu definieren, in denen Claude Code autonom arbeiten kann
* **Schreibzugriffsbeschränkung**: Claude Code kann nur in den Ordner schreiben, in dem es gestartet wurde, und in dessen Unterordner – es kann Dateien in übergeordneten Verzeichnissen nicht ohne explizite Genehmigung ändern. Während Claude Code Dateien außerhalb des Arbeitsverzeichnisses lesen kann (nützlich für den Zugriff auf Systembibliotheken und Abhängigkeiten), sind Schreibvorgänge streng auf den Projektumfang beschränkt und schaffen eine klare Sicherheitsgrenze
* **Minderung von Genehmigungsmüdigkeit**: Unterstützung für das Zulassen häufig verwendeter sicherer Befehle pro Benutzer, pro Codebasis oder pro Organisation
* **Accept Edits-Modus**: Mehrere Bearbeitungen stapelweise akzeptieren, während Berechtigungsaufforderungen für Befehle mit Nebenwirkungen beibehalten werden

### Benutzerverantwortung

Claude Code hat nur die Berechtigungen, die Sie ihm gewähren. Sie sind verantwortlich für die Überprüfung vorgeschlagener Code und Befehle auf Sicherheit vor der Genehmigung.

## Schutz vor Prompt-Injection

Prompt-Injection ist eine Technik, bei der ein Angreifer versucht, die Anweisungen eines KI-Assistenten durch das Einfügen bösartiger Texte zu überschreiben oder zu manipulieren. Claude Code enthält mehrere Schutzmaßnahmen gegen diese Angriffe:

### Kernschutzmaßnahmen

* **Berechtigungssystem**: Sensible Operationen erfordern explizite Genehmigung
* **Kontextbewusste Analyse**: Erkennt potenziell schädliche Anweisungen durch Analyse der vollständigen Anfrage
* **Eingabebereinigung**: Verhindert Befehlsinjektionen durch Verarbeitung von Benutzereingaben
* **Befehlsblockliste**: Blockiert standardmäßig riskante Befehle, die beliebige Inhalte aus dem Web abrufen, wie `curl` und `wget`. Wenn explizit zulässig, beachten Sie [Einschränkungen des Berechtigungsmusters](/de/permissions#tool-specific-permission-rules)

### Datenschutzvorkehrungen

Wir haben mehrere Schutzmaßnahmen implementiert, um Ihre Daten zu schützen, einschließlich:

* Begrenzte Aufbewahrungszeiträume für sensible Informationen (siehe [Privacy Center](https://privacy.anthropic.com/en/articles/10023548-how-long-do-you-store-my-data), um mehr zu erfahren)
* Eingeschränkter Zugriff auf Benutzersitzungsdaten
* Benutzerkontrolle über Datenschulungspräferenzen. Verbraucherbenutzer können ihre [Datenschutzeinstellungen](https://claude.ai/settings/privacy) jederzeit ändern.

Für vollständige Details überprüfen Sie bitte unsere [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (für Team-, Enterprise- und API-Benutzer) oder [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (für Free-, Pro- und Max-Benutzer) und [Privacy Policy](https://www.anthropic.com/legal/privacy).

### Zusätzliche Schutzmaßnahmen

* **Genehmigung von Netzwerkanfragen**: Tools, die Netzwerkanfragen stellen, erfordern standardmäßig Benutzergenehmigung
* **Isolierte Kontextfenster**: Web Fetch verwendet ein separates Kontextfenster, um die Injection potenziell bösartiger Prompts zu vermeiden
* **Vertrauensüberprüfung**: Erste Codebasis-Ausführungen und neue MCP-Server erfordern Vertrauensüberprüfung
  * Hinweis: Vertrauensüberprüfung ist deaktiviert, wenn nicht-interaktiv mit dem `-p`-Flag ausgeführt wird
* **Erkennung von Befehlsinjektionen**: Verdächtige Bash-Befehle erfordern manuelle Genehmigung, auch wenn sie zuvor auf die Zulassungsliste gesetzt wurden
* **Fail-Closed-Matching**: Nicht übereinstimmende Befehle erfordern standardmäßig manuelle Genehmigung
* **Beschreibungen in natürlicher Sprache**: Komplexe Bash-Befehle enthalten Erklärungen zum Verständnis des Benutzers
* **Sichere Anmeldedatenspeicherung**: API-Schlüssel und Token sind verschlüsselt. Siehe [Credential Management](/de/authentication#credential-management)

<Warning>
  **Windows WebDAV-Sicherheitsrisiko**: Wenn Sie Claude Code unter Windows ausführen, empfehlen wir, WebDAV nicht zu aktivieren oder Claude Code keinen Zugriff auf Pfade wie `\\*` zu gewähren, die WebDAV-Unterverzeichnisse enthalten können. [WebDAV wurde von Microsoft als veraltet eingestuft](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features#:~:text=The%20Webclient%20\(WebDAV\)%20service%20is%20deprecated) aufgrund von Sicherheitsrisiken. Das Aktivieren von WebDAV kann Claude Code ermöglichen, Netzwerkanfragen an Remote-Hosts auszulösen und das Berechtigungssystem zu umgehen.
</Warning>

**Best Practices für die Arbeit mit nicht vertrauenswürdigem Inhalt**:

1. Überprüfen Sie vorgeschlagene Befehle vor der Genehmigung
2. Vermeiden Sie es, nicht vertrauenswürdige Inhalte direkt an Claude zu pipen
3. Überprüfen Sie vorgeschlagene Änderungen an kritischen Dateien
4. Verwenden Sie virtuelle Maschinen (VMs), um Skripte auszuführen und Tool-Aufrufe zu tätigen, besonders bei der Interaktion mit externen Webdiensten
5. Melden Sie verdächtiges Verhalten mit `/bug`

<Warning>
  Während diese Schutzmaßnahmen das Risiko erheblich reduzieren, ist kein System
  vollständig immun gegen alle Angriffe. Halten Sie immer gute Sicherheitspraktiken
  bei der Arbeit mit einem KI-Tool ein.
</Warning>

## MCP-Sicherheit

Claude Code ermöglicht es Benutzern, Model Context Protocol (MCP)-Server zu konfigurieren. Die Liste der zulässigen MCP-Server wird in Ihrem Quellcode konfiguriert, als Teil der Claude Code-Einstellungen, die Ingenieure in die Versionskontrolle einchecken.

Wir ermutigen Sie, entweder Ihre eigenen MCP-Server zu schreiben oder MCP-Server von Anbietern zu verwenden, denen Sie vertrauen. Sie können Claude Code-Berechtigungen für MCP-Server konfigurieren. Anthropic verwaltet oder prüft keine MCP-Server.

## IDE-Sicherheit

Siehe [VS Code-Sicherheit und Datenschutz](/de/vs-code#security-and-privacy) für weitere Informationen zum Ausführen von Claude Code in einer IDE.

## Cloud-Ausführungssicherheit

Bei Verwendung von [Claude Code im Web](/de/claude-code-on-the-web) sind zusätzliche Sicherheitskontrollen vorhanden:

* **Isolierte virtuelle Maschinen**: Jede Cloud-Sitzung wird in einer isolierten, von Anthropic verwalteten VM ausgeführt
* **Netzwerkzugriffskontrollen**: Der Netzwerkzugriff ist standardmäßig begrenzt und kann so konfiguriert werden, dass er deaktiviert ist oder nur bestimmte Domänen zulässt
* **Anmeldedatenschutz**: Die Authentifizierung wird über einen sicheren Proxy durchgeführt, der einen scoped Credential in der Sandbox verwendet, der dann in Ihr tatsächliches GitHub-Authentifizierungstoken übersetzt wird
* **Branch-Einschränkungen**: Git-Push-Operationen sind auf den aktuellen Arbeitsbranch beschränkt
* **Audit-Protokollierung**: Alle Operationen in Cloud-Umgebungen werden zu Compliance- und Audit-Zwecken protokolliert
* **Automatische Bereinigung**: Cloud-Umgebungen werden nach Abschluss der Sitzung automatisch beendet

Weitere Details zur Cloud-Ausführung finden Sie unter [Claude Code im Web](/de/claude-code-on-the-web).

[Remote Control](/de/remote-control)-Sitzungen funktionieren anders: Die Weboberfläche verbindet sich mit einem Claude Code-Prozess, der auf Ihrem lokalen Computer ausgeführt wird. Alle Code-Ausführungen und Dateizugriffe bleiben lokal, und die gleichen Daten, die während einer lokalen Claude Code-Sitzung fließen, werden über die Anthropic API über TLS übertragen. Es sind keine Cloud-VMs oder Sandboxing beteiligt. Die Verbindung verwendet mehrere kurzlebige, eng begrenzte Anmeldedaten, die jeweils auf einen bestimmten Zweck beschränkt sind und unabhängig ablaufen, um den Blast-Radius eines einzelnen kompromittierten Credentials zu begrenzen.

## Best Practices für Sicherheit

### Arbeiten mit sensiblem Code

* Überprüfen Sie alle vorgeschlagenen Änderungen vor der Genehmigung
* Verwenden Sie projektspezifische Berechtigungseinstellungen für sensible Repositories
* Erwägen Sie die Verwendung von [devcontainers](/de/devcontainer) für zusätzliche Isolierung
* Überprüfen Sie regelmäßig Ihre Berechtigungseinstellungen mit `/permissions`

### Team-Sicherheit

* Verwenden Sie [verwaltete Einstellungen](/de/settings#settings-files), um organisatorische Standards durchzusetzen
* Teilen Sie genehmigte Berechtigungskonfigurationen über Versionskontrolle
* Schulen Sie Teammitglieder in Best Practices für Sicherheit
* Überwachen Sie die Claude Code-Nutzung durch [OpenTelemetry-Metriken](/de/monitoring-usage)
* Überprüfen oder blockieren Sie Einstellungsänderungen während Sitzungen mit [`ConfigChange`-Hooks](/de/hooks#configchange)

### Meldung von Sicherheitsproblemen

Wenn Sie eine Sicherheitslücke in Claude Code entdecken:

1. Offenbaren Sie sie nicht öffentlich
2. Melden Sie sie über unser [HackerOne-Programm](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability)
3. Fügen Sie detaillierte Reproduktionsschritte ein
4. Geben Sie uns Zeit, das Problem zu beheben, bevor Sie es öffentlich offenbaren

## Verwandte Ressourcen

* [Sandboxing](/de/sandboxing) - Dateisystem- und Netzwerkisolation für Bash-Befehle
* [Berechtigungen](/de/permissions) - Konfigurieren Sie Berechtigungen und Zugriffskontrolle
* [Nutzungsüberwachung](/de/monitoring-usage) - Verfolgen und überprüfen Sie Claude Code-Aktivität
* [Entwicklungscontainer](/de/devcontainer) - Sichere, isolierte Umgebungen
* [Anthropic Trust Center](https://trust.anthropic.com) - Sicherheitszertifizierungen und Compliance
