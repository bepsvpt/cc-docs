> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fehlerbehebung

> Beheben Sie hohe CPU- oder Speichernutzung, Hänger, Auto-Compact-Thrashing und Suchprobleme in Claude Code und finden Sie die richtige Seite für andere Probleme.

Diese Seite behandelt Leistungs-, Stabilitäts- und Suchprobleme, sobald Claude Code läuft. Für andere Probleme beginnen Sie mit der Seite, die zu Ihrer Situation passt:

| Symptom                                                                                                          | Gehen Sie zu                                                                                       |
| :--------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `command not found`, Installation schlägt fehl, PATH-Probleme, `EACCES`, TLS-Fehler                              | [Fehlerbehebung bei Installation und Anmeldung](/de/troubleshoot-install)                          |
| Anmeldeschleifen, OAuth-Fehler, `403 Forbidden`, „Organisation deaktiviert", Bedrock/Vertex/Foundry-Anmeldedaten | [Fehlerbehebung bei Installation und Anmeldung](/de/troubleshoot-install#login-and-authentication) |
| Einstellungen werden nicht angewendet, Hooks werden nicht ausgelöst, MCP-Server werden nicht geladen             | [Debuggen Sie Ihre Konfiguration](/de/debug-your-config)                                           |
| `API Error: 5xx`, `529 Overloaded`, `429`, Request-Validierungsfehler                                            | [Fehlerreferenz](/de/errors)                                                                       |
| `model not found` oder `you may not have access to it`                                                           | [Fehlerreferenz](/de/errors#theres-an-issue-with-the-selected-model)                               |
| VS Code-Erweiterung verbindet sich nicht oder erkennt Claude nicht                                               | [VS Code-Integration](/de/vs-code#fix-common-issues)                                               |
| JetBrains-Plugin oder IDE wird nicht erkannt                                                                     | [JetBrains-Integration](/de/jetbrains#troubleshooting)                                             |
| Hohe CPU oder Speicher, langsame Antworten, Hänger, Suche findet Dateien nicht                                   | [Leistung und Stabilität](#performance-and-stability) unten                                        |

Wenn Sie sich nicht sicher sind, welcher Fall zutrifft, führen Sie `/doctor` in Claude Code aus, um eine automatisierte Überprüfung Ihrer Installation, Einstellungen, MCP-Server und Kontextnutzung durchzuführen. Wenn `claude` überhaupt nicht startet, führen Sie stattdessen `claude doctor` aus Ihrer Shell aus.

## Leistung und Stabilität

Diese Abschnitte behandeln Probleme im Zusammenhang mit Ressourcennutzung, Reaktionsfähigkeit und Suchverhalten.

### Hohe CPU- oder Speichernutzung

Claude Code ist für die Zusammenarbeit mit den meisten Entwicklungsumgebungen konzipiert, kann aber bei der Verarbeitung großer Codebases erhebliche Ressourcen verbrauchen. Wenn Sie Leistungsprobleme haben:

1. Verwenden Sie `/compact` regelmäßig, um die Kontextgröße zu reduzieren
2. Schließen und starten Sie Claude Code zwischen großen Aufgaben neu
3. Erwägen Sie, große Build-Verzeichnisse zu Ihrer `.gitignore`-Datei hinzuzufügen

Wenn die Speichernutzung nach diesen Schritten hoch bleibt, führen Sie `/heapdump` aus, um einen JavaScript-Heap-Snapshot und eine Speicheraufschlüsselung auf `~/Desktop` zu schreiben. Auf Linux ohne Desktop-Ordner werden die Dateien in Ihr Home-Verzeichnis geschrieben.

Die Aufschlüsselung zeigt Resident Set Size, JS Heap, Array Buffers und nicht berechneten nativen Speicher, was hilft zu identifizieren, ob das Wachstum in JavaScript-Objekten oder in nativem Code liegt. Um Retainer zu überprüfen, öffnen Sie die `.heapsnapshot`-Datei in Chrome DevTools unter Memory → Load. Fügen Sie beide Dateien bei, wenn Sie ein Speicherproblem auf [GitHub](https://github.com/anthropics/claude-code/issues) melden.

### Auto-Kompaktierung stoppt mit einem Thrashing-Fehler

Wenn Sie `Autocompact is thrashing: the context refilled to the limit...` sehen, war die automatische Kompaktierung erfolgreich, aber eine Datei oder ein Tool-Output hat das Kontextfenster sofort mehrmals hintereinander gefüllt. Claude Code stoppt die Wiederholung, um zu vermeiden, dass API-Aufrufe auf einer Schleife verschwendet werden, die keinen Fortschritt macht.

Um sich zu erholen:

1. Bitten Sie Claude, die übergroße Datei in kleineren Chunks zu lesen, z. B. einen bestimmten Zeilenbereich oder eine Funktion, statt der ganzen Datei
2. Führen Sie `/compact` mit einem Fokus aus, der die große Ausgabe löscht, z. B. `/compact keep only the plan and the diff`
3. Verschieben Sie die Arbeit mit großen Dateien zu einem [Subagenten](/de/sub-agents), damit er in einem separaten Kontextfenster ausgeführt wird
4. Führen Sie `/clear` aus, wenn das frühere Gespräch nicht mehr benötigt wird

### Befehl hängt oder friert ein

Wenn Claude Code nicht reagiert:

1. Drücken Sie Strg+C, um zu versuchen, den aktuellen Vorgang abzubrechen
2. Wenn nicht reagiert, müssen Sie möglicherweise das Terminal schließen und neu starten

Das Neustarten verliert Ihre Konversation nicht. Führen Sie `claude --resume` im selben Verzeichnis aus, um die Sitzung fortzusetzen.

### Such- und Erkennungsprobleme

Wenn das Such-Tool, `@file`-Erwähnungen, benutzerdefinierte Agenten oder benutzerdefinierte Skills Dateien nicht finden, kann die gebündelte `ripgrep`-Binärdatei auf Ihrem System möglicherweise nicht ausgeführt werden. Installieren Sie das `ripgrep`-Paket Ihrer Plattform und teilen Sie Claude Code mit, es stattdessen zu verwenden:

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

Setzen Sie dann `USE_BUILTIN_RIPGREP=0` in Ihrer [Umgebung](/de/env-vars).

### Langsame oder unvollständige Suchergebnisse auf WSL

Leistungseinbußen beim Lesen von Festplatten beim [Arbeiten über Dateisysteme auf WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) können zu weniger als erwarteten Übereinstimmungen führen, wenn Sie Claude Code auf WSL verwenden. Die Suche funktioniert immer noch, gibt aber weniger Ergebnisse zurück als auf einem nativen Dateisystem.

<Note>
  `/doctor` zeigt in diesem Fall die Suche als OK an.
</Note>

**Lösungen:**

1. **Senden Sie spezifischere Suchen**: Reduzieren Sie die Anzahl der durchsuchten Dateien, indem Sie Verzeichnisse oder Dateitypen angeben: 'Search for JWT validation logic in the auth-service package" oder „Find use of md5 hash in JS files".

2. **Verschieben Sie das Projekt auf das Linux-Dateisystem**: Stellen Sie sicher, dass sich Ihr Projekt auf dem Linux-Dateisystem (`/home/`) statt auf dem Windows-Dateisystem (`/mnt/c/`) befindet.

3. **Verwenden Sie stattdessen natives Windows**: Erwägen Sie, Claude Code nativ unter Windows statt über WSL auszuführen, um eine bessere Dateisystem-Leistung zu erzielen.

## Weitere Hilfe erhalten

Wenn Sie Probleme haben, die hier nicht behandelt werden:

1. Führen Sie `/doctor` aus, um Installationsintegrität, Einstellungsgültigkeit, MCP-Konfiguration und Kontextnutzung in einem Durchgang zu überprüfen
2. Verwenden Sie den `/feedback`-Befehl in Claude Code, um Probleme direkt an Anthropic zu melden
3. Überprüfen Sie das [GitHub-Repository](https://github.com/anthropics/claude-code) auf bekannte Probleme
4. Fragen Sie Claude direkt nach seinen Fähigkeiten und Funktionen. Claude hat integrierten Zugriff auf seine Dokumentation.
