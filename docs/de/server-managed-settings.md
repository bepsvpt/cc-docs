> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Serververwaltete Einstellungen konfigurieren

> Konfigurieren Sie Claude Code zentral für Ihre Organisation durch serververwaltete Einstellungen, ohne dass eine Geräteverwaltungsinfrastruktur erforderlich ist.

Serververwaltete Einstellungen ermöglichen es Administratoren, Claude Code zentral über eine webbasierte Schnittstelle auf Claude.ai zu konfigurieren. Claude Code-Clients erhalten diese Einstellungen automatisch, wenn sich Benutzer mit ihren Organisationsanmeldedaten authentifizieren.

Dieser Ansatz ist für Organisationen konzipiert, die keine Geräteverwaltungsinfrastruktur haben oder Einstellungen für Benutzer auf nicht verwalteten Geräten verwalten müssen.

<Note>
  Serververwaltete Einstellungen sind für [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) und [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise) Kunden verfügbar.
</Note>

## Anforderungen

Um serververwaltete Einstellungen zu verwenden, benötigen Sie:

* Claude for Teams oder Claude for Enterprise Plan
* Claude Code Version 2.1.38 oder später für Claude for Teams oder Version 2.1.30 oder später für Claude for Enterprise
* Netzwerkzugriff auf `api.anthropic.com`

## Wählen Sie zwischen serververwalteten und endpunktverwalteten Einstellungen

Claude Code unterstützt zwei Ansätze für zentralisierte Konfiguration. Serververwaltete Einstellungen liefern Konfiguration von Anthropics Servern. [Endpunktverwaltete Einstellungen](/de/settings#settings-files) werden direkt auf Geräten über native Betriebssystemrichtlinien (macOS verwaltete Einstellungen, Windows-Registrierung) oder verwaltete Einstellungsdateien bereitgestellt.

| Ansatz                                                              | Am besten geeignet für                                              | Sicherheitsmodell                                                                                                                                  |
| :------------------------------------------------------------------ | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Serververwaltete Einstellungen**                                  | Organisationen ohne MDM oder Benutzer auf nicht verwalteten Geräten | Einstellungen, die von Anthropics Servern zum Authentifizierungszeitpunkt bereitgestellt werden                                                    |
| **[Endpunktverwaltete Einstellungen](/de/settings#settings-files)** | Organisationen mit MDM oder Endpunktverwaltung                      | Einstellungen, die auf Geräten über MDM-Konfigurationsprofile, Registrierungsrichtlinien oder verwaltete Einstellungsdateien bereitgestellt werden |

Wenn Ihre Geräte in einer MDM- oder Endpunktverwaltungslösung registriert sind, bieten endpunktverwaltete Einstellungen stärkere Sicherheitsgarantien, da die Einstellungsdatei auf Betriebssystemebene vor Benutzermodifikationen geschützt werden kann.

## Serververwaltete Einstellungen konfigurieren

<Steps>
  <Step title="Öffnen Sie die Admin-Konsole">
    Navigieren Sie in [Claude.ai](https://claude.ai) zu **Admin-Einstellungen > Claude Code > Verwaltete Einstellungen**.
  </Step>

  <Step title="Definieren Sie Ihre Einstellungen">
    Fügen Sie Ihre Konfiguration als JSON hinzu. Alle [in `settings.json` verfügbaren Einstellungen](/de/settings#available-settings) werden unterstützt, mit Ausnahme derjenigen, die auf die Bereitstellung auf OS-Ebene beschränkt sind. Siehe [Aktuelle Einschränkungen](#current-limitations) für diese kurze Liste. Dies umfasst [hooks](/de/hooks), [Umgebungsvariablen](/de/env-vars) und [nur verwaltete Einstellungen](/de/permissions#managed-only-settings) wie `allowManagedPermissionRulesOnly`.

    Dieses Beispiel erzwingt eine Berechtigungsverweigerungsliste, verhindert, dass Benutzer Berechtigungen umgehen, und beschränkt Berechtigungsregeln auf diejenigen, die in verwalteten Einstellungen definiert sind:

    ```json theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      },
      "allowManagedPermissionRulesOnly": true
    }
    ```

    Hooks verwenden das gleiche Format wie in `settings.json`.

    Dieses Beispiel führt ein Audit-Skript nach jeder Dateibearbeitung in der gesamten Organisation aus:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    Um den [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode) Klassifizierer zu konfigurieren, damit er weiß, welche Repos, Buckets und Domains Ihre Organisation vertraut:

    ```json theme={null}
    {
      "autoMode": {
        "environment": [
          "Source control: github.example.com/acme-corp and all repos under it",
          "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
          "Trusted internal domains: *.corp.example.com"
        ]
      }
    }
    ```

    Da Hooks Shell-Befehle ausführen, sehen Benutzer einen [Sicherheitsgenehmigungsdialog](#security-approval-dialogs), bevor sie angewendet werden. Siehe [Auto-Modus konfigurieren](/de/auto-mode-config), um zu erfahren, wie die `autoMode` Einträge beeinflussen, was der Klassifizierer blockiert, und wichtige Warnungen zu den Feldern `environment`, `allow`, `soft_deny` und `hard_deny`.
  </Step>

  <Step title="Speichern und bereitstellen">
    Speichern Sie Ihre Änderungen. Claude Code-Clients erhalten die aktualisierten Einstellungen beim nächsten Start oder während des stündlichen Abrufzyklus.
  </Step>
</Steps>

### Einstellungsbereitstellung überprüfen

Um zu bestätigen, dass Einstellungen angewendet werden, bitten Sie einen Benutzer, Claude Code neu zu starten. Wenn die Konfiguration Einstellungen enthält, die den [Sicherheitsgenehmigungsdialog](#security-approval-dialogs) auslösen, sieht der Benutzer beim Start eine Eingabeaufforderung, die die verwalteten Einstellungen beschreibt. Sie können auch überprüfen, dass verwaltete Berechtigungsregeln aktiv sind, indem Sie einen Benutzer `/permissions` ausführen lassen, um seine geltenden Berechtigungsregeln anzuzeigen.

### Zugriffskontrolle

Die folgenden Rollen können serververwaltete Einstellungen verwalten:

* **Primärer Eigentümer**
* **Eigentümer**

Beschränken Sie den Zugriff auf vertrauenswürdiges Personal, da Einstellungsänderungen für alle Benutzer in der Organisation gelten.

### Nur verwaltete Einstellungen

Die meisten [Einstellungsschlüssel](/de/settings#available-settings) funktionieren in jedem Bereich. Eine Handvoll Schlüssel werden nur aus verwalteten Einstellungen gelesen und haben keine Auswirkung, wenn sie in Benutzer- oder Projekteinstellungsdateien platziert werden. Siehe [nur verwaltete Einstellungen](/de/permissions#managed-only-settings) für die vollständige Liste. Jede Einstellung, die nicht auf dieser Liste steht, kann immer noch in verwalteten Einstellungen platziert werden und hat die höchste Priorität.

### Aktuelle Einschränkungen

Serververwaltete Einstellungen haben die folgenden Einschränkungen:

* Einstellungen gelten einheitlich für alle Benutzer in der Organisation. Konfigurationen pro Gruppe werden noch nicht unterstützt.
* Eine [`managed-mcp.json`](/de/managed-mcp) Datei kann nicht über serververwaltete Einstellungen verteilt werden. Stellen Sie stattdessen die Richtlinienschlüssel `allowedMcpServers` und `deniedMcpServers` dort bereit.
* Einstellungen, die auf OS-Ebene-Richtlinienquellen beschränkt sind, wie `policyHelper` und `wslInheritsWindowsSettings`, werden nicht berücksichtigt. Stellen Sie sie stattdessen über MDM oder eine System-Datei `managed-settings.json` bereit.

## Einstellungsbereitstellung

### Einstellungspriorität

Serververwaltete Einstellungen und [endpunktverwaltete Einstellungen](/de/settings#settings-files) nehmen beide die höchste Ebene in der Claude Code [Einstellungshierarchie](/de/settings#settings-precedence) ein. Keine andere Einstellungsebene kann sie überschreiben, einschließlich Befehlszeilenargumenten.

Innerhalb der verwalteten Ebene gewinnt die erste Quelle, die eine nicht leere Konfiguration liefert. Serververwaltete Einstellungen werden zuerst überprüft, dann endpunktverwaltete Einstellungen. Quellen werden nicht zusammengeführt: Wenn serververwaltete Einstellungen überhaupt Schlüssel liefern, werden endpunktverwaltete Einstellungen vollständig ignoriert. Wenn serververwaltete Einstellungen nichts liefern, gelten endpunktverwaltete Einstellungen.

Wenn Sie Ihre serververwaltete Konfiguration in der Admin-Konsole mit der Absicht löschen, auf eine endpunktverwaltete plist oder Registrierungsrichtlinie zurückzugreifen, beachten Sie, dass [zwischengespeicherte Einstellungen](#fetch-and-caching-behavior) auf Client-Maschinen bestehen bleiben, bis der nächste erfolgreiche Abruf erfolgt. Führen Sie `/status` aus, um zu sehen, welche verwaltete Quelle aktiv ist.

### Abruf- und Caching-Verhalten

Claude Code ruft Einstellungen beim Start von Anthropics Servern ab und fragt stündlich während aktiver Sitzungen nach Updates ab.

**Erster Start ohne zwischengespeicherte Einstellungen:**

* Claude Code ruft Einstellungen asynchron ab
* Wenn der Abruf fehlschlägt, wird Claude Code ohne verwaltete Einstellungen fortgesetzt
* Es gibt ein kurzes Fenster, bevor Einstellungen geladen werden, in dem Einschränkungen noch nicht erzwungen werden

**Nachfolgende Starts mit zwischengespeicherten Einstellungen:**

* Zwischengespeicherte Einstellungen werden beim Start sofort angewendet
* Claude Code ruft frische Einstellungen im Hintergrund ab
* Zwischengespeicherte Einstellungen bleiben bei Netzwerkfehlern erhalten

Claude Code wendet Einstellungsaktualisierungen automatisch ohne Neustart an, außer für erweiterte Einstellungen wie OpenTelemetry-Konfiguration, die einen vollständigen Neustart erfordern, um wirksam zu werden.

### Erzwingen Sie einen Fail-Closed-Start

Standardmäßig wird die CLI ohne verwaltete Einstellungen fortgesetzt, wenn der Abruf der Remote-Einstellungen beim Start fehlschlägt. Für Umgebungen, in denen dieses kurze nicht erzwungene Fenster nicht akzeptabel ist, setzen Sie `forceRemoteSettingsRefresh: true` in Ihren verwalteten Einstellungen.

Wenn diese Einstellung aktiv ist, blockiert die CLI beim Start, bis Remote-Einstellungen neu abgerufen werden. Wenn der Abruf fehlschlägt, wird die CLI beendet, anstatt ohne die Richtlinie fortzufahren. Diese Einstellung perpetuiert sich selbst: Sobald sie vom Server bereitgestellt wird, wird sie auch lokal zwischengespeichert, sodass nachfolgende Starts das gleiche Verhalten erzwingen, auch bevor der erste erfolgreiche Abruf einer neuen Sitzung erfolgt.

Um dies zu aktivieren, fügen Sie den Schlüssel zu Ihrer verwalteten Einstellungskonfiguration hinzu:

```json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

Bevor Sie diese Einstellung aktivieren, stellen Sie sicher, dass Ihre Netzwerkrichtlinien die Konnektivität zu `api.anthropic.com` ermöglichen. Wenn dieser Endpunkt nicht erreichbar ist, wird die CLI beim Start beendet und Benutzer können Claude Code nicht starten.

Ab v2.1.139 sind die `claude auth` Unterbefehle wie `claude auth login` von dieser Überprüfung ausgenommen, sodass Benutzer sich erneut authentifizieren können, wenn abgelaufene Anmeldedaten der Grund für den fehlgeschlagenen Einstellungsabruf sind.

### Sicherheitsgenehmigungsdialoge

Bestimmte Einstellungen, die Sicherheitsrisiken darstellen könnten, erfordern explizite Benutzergenehmigung, bevor sie angewendet werden:

* **Shell-Befehlseinstellungen**: Einstellungen, die Shell-Befehle ausführen
* **Benutzerdefinierte Umgebungsvariablen**: Variablen, die nicht in der bekannten sicheren Zulassungsliste enthalten sind
* **Hook-Konfigurationen**: jede Hook-Definition

Wenn diese Einstellungen vorhanden sind, sehen Benutzer einen Sicherheitsdialog, der erklärt, was konfiguriert wird. Benutzer müssen genehmigen, um fortzufahren. Wenn ein Benutzer die Einstellungen ablehnt, wird Claude Code beendet.

<Note>
  Im nicht-interaktiven Modus mit dem `-p` Flag überspringt Claude Code Sicherheitsdialoge und wendet Einstellungen ohne Benutzergenehmigung an.
</Note>

## Plattformverfügbarkeit

Serververwaltete Einstellungen erfordern eine direkte Verbindung zu `api.anthropic.com` und sind nicht verfügbar, wenn Drittanbieter-Modellprovider verwendet werden:

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* Benutzerdefinierte API-Endpunkte über `ANTHROPIC_BASE_URL` oder [LLM-Gateways](/de/llm-gateway)

## Audit-Protokollierung

Audit-Log-Ereignisse für Einstellungsänderungen sind über die Compliance-API oder den Audit-Log-Export verfügbar. Kontaktieren Sie Ihr Anthropic-Kontoteam für Zugriff.

Audit-Ereignisse enthalten den Typ der durchgeführten Aktion, das Konto und das Gerät, das die Aktion durchgeführt hat, sowie Verweise auf die vorherigen und neuen Werte.

## Sicherheitsüberlegungen

Serververwaltete Einstellungen bieten zentralisierte Richtliniendurchsetzung, funktionieren aber als clientseitige Kontrolle. Auf nicht verwalteten Geräten können Benutzer mit Admin- oder Sudo-Zugriff die Claude Code-Binärdatei, das Dateisystem oder die Netzwerkkonfiguration ändern.

| Szenario                                                                           | Verhalten                                                                                                                                                                                                                                                                                                                     |
| :--------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Benutzer bearbeitet die zwischengespeicherte Einstellungsdatei                     | Manipulierte Datei wird beim Start angewendet, aber korrekte Einstellungen werden beim nächsten Serverfetch wiederhergestellt                                                                                                                                                                                                 |
| Benutzer löscht die zwischengespeicherte Einstellungsdatei                         | Verhalten beim ersten Start tritt auf: Einstellungen werden asynchron abgerufen mit einem kurzen nicht erzwungenen Fenster                                                                                                                                                                                                    |
| API ist nicht verfügbar                                                            | Zwischengespeicherte Einstellungen werden angewendet, falls verfügbar, andernfalls werden verwaltete Einstellungen nicht erzwungen, bis der nächste erfolgreiche Abruf erfolgt. Mit `forceRemoteSettingsRefresh: true` wird die CLI stattdessen beendet, außer für [`claude auth` Unterbefehle](#enforce-fail-closed-startup) |
| Benutzer authentifiziert sich mit einer anderen Organisation                       | Einstellungen werden nicht für Konten außerhalb der verwalteten Organisation bereitgestellt                                                                                                                                                                                                                                   |
| Benutzer konfiguriert einen [Drittanbieter-Modellprovider](#platform-availability) | Serververwaltete Einstellungen werden umgangen. Dies umfasst das Setzen von `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_MANTLE`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY` oder einer nicht standardmäßigen `ANTHROPIC_BASE_URL`                                                                                    |

Um Laufzeitkonfigurationsänderungen zu erkennen, verwenden Sie [`ConfigChange` hooks](/de/hooks#configchange), um Änderungen zu protokollieren oder nicht autorisierte Änderungen zu blockieren, bevor sie wirksam werden.

Für stärkere Durchsetzungsgarantien verwenden Sie [endpunktverwaltete Einstellungen](/de/settings#settings-files) auf Geräten, die in einer MDM-Lösung registriert sind.

## Siehe auch

Verwandte Seiten zur Verwaltung der Claude Code-Konfiguration:

* [Einstellungen](/de/settings): vollständige Konfigurationsreferenz einschließlich aller verfügbaren Einstellungen
* [Endpunktverwaltete Einstellungen](/de/settings#settings-files): verwaltete Einstellungen, die von der IT auf Geräten bereitgestellt werden
* [Authentifizierung](/de/authentication): Einrichtung des Benutzerzugriffs auf Claude Code
* [Sicherheit](/de/security): Sicherheitsvorkehrungen und Best Practices
