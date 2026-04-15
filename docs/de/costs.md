> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Kosten effektiv verwalten

> Verfolgen Sie die Token-Nutzung, legen Sie Ausgabenlimits für Teams fest und reduzieren Sie Claude Code-Kosten durch Kontextverwaltung, Modellauswahl, Einstellungen für erweitertes Denken und Preprocessing-Hooks.

Claude Code verbraucht Token für jede Interaktion. Die Kosten variieren je nach Codebasis-Größe, Abfragekomplexität und Gesprächslänge. Die durchschnittlichen Kosten betragen 6 USD pro Entwickler pro Tag, wobei die täglichen Kosten für 90 % der Benutzer unter 12 USD bleiben.

Für die Team-Nutzung werden Claude Code-Gebühren nach API-Token-Verbrauch berechnet. Im Durchschnitt kostet Claude Code etwa 100–200 USD pro Entwickler pro Monat mit Sonnet 4.6, es gibt jedoch große Unterschiede je nachdem, wie viele Instanzen Benutzer ausführen und ob sie diese in der Automatisierung verwenden.

Diese Seite behandelt, wie Sie [Ihre Kosten verfolgen](#track-your-costs), [Kosten für Teams verwalten](#managing-costs-for-teams) und [Token-Nutzung reduzieren](#reduce-token-usage).

## Verfolgen Sie Ihre Kosten

### Verwenden des `/cost`-Befehls

<Note>
  Der `/cost`-Befehl zeigt die API-Token-Nutzung an und ist für API-Benutzer vorgesehen. Claude Max und Pro-Abonnenten haben die Nutzung in ihrem Abonnement enthalten, daher sind `/cost`-Daten nicht relevant für Abrechnungszwecke. Abonnenten können `/stats` verwenden, um Nutzungsmuster anzuzeigen.
</Note>

Der `/cost`-Befehl bietet detaillierte Token-Nutzungsstatistiken für Ihre aktuelle Sitzung:

```text theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

## Verwalten Sie Kosten für Teams

Bei Verwendung der Claude API können Sie [Workspace-Ausgabenlimits festlegen](https://platform.claude.com/docs/de/build-with-claude/workspaces#workspace-limits) für die gesamten Claude Code-Workspace-Ausgaben. Administratoren können [Kosten- und Nutzungsberichte anzeigen](https://platform.claude.com/docs/de/build-with-claude/workspaces#usage-and-cost-tracking) in der Konsole.

<Note>
  Wenn Sie Claude Code zum ersten Mal mit Ihrem Claude Console-Konto authentifizieren, wird automatisch ein Workspace namens „Claude Code" für Sie erstellt. Dieser Workspace bietet zentrale Kostenverfolgung und Verwaltung für alle Claude Code-Nutzung in Ihrer Organisation. Sie können keine API-Schlüssel für diesen Workspace erstellen; er ist ausschließlich für Claude Code-Authentifizierung und -Nutzung.
</Note>

Bei Bedrock, Vertex und Foundry sendet Claude Code keine Metriken aus Ihrer Cloud. Um Kostenmetriken zu erhalten, berichteten mehrere große Unternehmen von der Verwendung von [LiteLLM](/de/llm-gateway#litellm-configuration), einem Open-Source-Tool, das Unternehmen hilft, [Ausgaben nach Schlüssel zu verfolgen](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). Dieses Projekt ist nicht mit Anthropic verbunden und wurde nicht auf Sicherheit überprüft.

### Empfehlungen für Ratenlimits

Beim Einrichten von Claude Code für Teams sollten Sie diese Token Pro Minute (TPM) und Anfragen Pro Minute (RPM) pro Benutzer-Empfehlungen basierend auf Ihrer Organisationsgröße berücksichtigen:

| Team-Größe       | TPM pro Benutzer | RPM pro Benutzer |
| ---------------- | ---------------- | ---------------- |
| 1–5 Benutzer     | 200.000–300.000  | 5–7              |
| 5–20 Benutzer    | 100.000–150.000  | 2,5–3,5          |
| 20–50 Benutzer   | 50.000–75.000    | 1,25–1,75        |
| 50–100 Benutzer  | 25.000–35.000    | 0,62–0,87        |
| 100–500 Benutzer | 15.000–20.000    | 0,37–0,47        |
| 500+ Benutzer    | 10.000–15.000    | 0,25–0,35        |

Wenn Sie beispielsweise 200 Benutzer haben, könnten Sie 20.000 TPM für jeden Benutzer anfordern, oder insgesamt 4 Millionen TPM (200\*20.000 = 4 Millionen).

Die TPM pro Benutzer sinkt mit zunehmender Team-Größe, da in größeren Organisationen weniger Benutzer Claude Code gleichzeitig verwenden. Diese Ratenlimits gelten auf Organisationsebene, nicht pro einzelnem Benutzer, was bedeutet, dass einzelne Benutzer vorübergehend mehr als ihren berechneten Anteil verbrauchen können, wenn andere den Service nicht aktiv nutzen.

<Note>
  Wenn Sie Szenarien mit ungewöhnlich hoher gleichzeitiger Nutzung erwarten (z. B. Live-Schulungssitzungen mit großen Gruppen), benötigen Sie möglicherweise höhere TPM-Zuordnungen pro Benutzer.
</Note>

### Token-Kosten für Agent-Teams

[Agent-Teams](/de/agent-teams) starten mehrere Claude Code-Instanzen, jede mit ihrem eigenen Kontextfenster. Die Token-Nutzung skaliert mit der Anzahl der aktiven Teammates und wie lange jeder läuft.

Um Agent-Team-Kosten überschaubar zu halten:

* Verwenden Sie Sonnet für Teammates. Es bietet ein Gleichgewicht zwischen Fähigkeit und Kosten für Koordinationsaufgaben.
* Halten Sie Teams klein. Jeder Teammate führt sein eigenes Kontextfenster aus, daher ist die Token-Nutzung ungefähr proportional zur Team-Größe.
* Halten Sie Spawn-Prompts fokussiert. Teammates laden CLAUDE.md, MCP-Server und Skills automatisch, aber alles im Spawn-Prompt trägt von Anfang an zu ihrem Kontext bei.
* Bereinigen Sie Teams, wenn die Arbeit erledigt ist. Aktive Teammates verbrauchen weiterhin Token, auch wenn sie untätig sind.
* Agent-Teams sind standardmäßig deaktiviert. Setzen Sie `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in Ihrer [settings.json](/de/settings) oder Umgebung, um sie zu aktivieren. Siehe [Agent-Teams aktivieren](/de/agent-teams#enable-agent-teams).

## Reduzieren Sie die Token-Nutzung

Token-Kosten skalieren mit der Kontextgröße: Je mehr Kontext Claude verarbeitet, desto mehr Token verwenden Sie. Claude Code optimiert Kosten automatisch durch Prompt Caching (das Kosten für wiederholte Inhalte wie Systemprompts reduziert) und Auto-Compaction (das Gesprächsverlauf zusammenfasst, wenn sich dem Kontextlimit genähert wird).

Die folgenden Strategien helfen Ihnen, den Kontext klein zu halten und die Kosten pro Nachricht zu reduzieren.

### Verwalten Sie den Kontext proaktiv

Verwenden Sie `/cost`, um Ihre aktuelle Token-Nutzung zu überprüfen, oder [konfigurieren Sie Ihre Statuszeile](/de/statusline#context-window-usage), um sie kontinuierlich anzuzeigen.

* **Zwischen Aufgaben löschen**: Verwenden Sie `/clear`, um neu zu beginnen, wenn Sie zu nicht verwandter Arbeit wechseln. Veralteter Kontext verschwendet Token bei jeder nachfolgenden Nachricht. Verwenden Sie `/rename` vor dem Löschen, damit Sie die Sitzung später leicht finden können, dann `/resume`, um zu ihr zurückzukehren.
* **Fügen Sie benutzerdefinierte Compaction-Anweisungen hinzu**: `/compact Focus on code samples and API usage` teilt Claude mit, was während der Zusammenfassung beibehalten werden soll.

Sie können das Compaction-Verhalten auch in Ihrer CLAUDE.md anpassen:

```markdown theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### Wählen Sie das richtige Modell

Sonnet bewältigt die meisten Codierungsaufgaben gut und kostet weniger als Opus. Reservieren Sie Opus für komplexe architektonische Entscheidungen oder mehrstufiges Denken. Verwenden Sie `/model`, um Modelle während einer Sitzung zu wechseln, oder legen Sie einen Standard in `/config` fest. Für einfache Subagent-Aufgaben geben Sie `model: haiku` in Ihrer [Subagent-Konfiguration](/de/sub-agents#choose-a-model) an.

### Reduzieren Sie den MCP-Server-Overhead

Jeder MCP-Server fügt Tool-Definitionen zu Ihrem Kontext hinzu, auch wenn er untätig ist. Führen Sie `/context` aus, um zu sehen, was Platz verbraucht.

* **Bevorzugen Sie CLI-Tools, wenn verfügbar**: Tools wie `gh`, `aws`, `gcloud` und `sentry-cli` sind kontexteffektiver als MCP-Server, da sie keine persistenten Tool-Definitionen hinzufügen. Claude kann CLI-Befehle direkt ausführen, ohne den Overhead.
* **Deaktivieren Sie ungenutzte Server**: Führen Sie `/mcp` aus, um konfigurierte Server anzuzeigen und alle zu deaktivieren, die Sie nicht aktiv verwenden.
* **Tool-Suche ist automatisch**: Wenn MCP-Tool-Beschreibungen 10 % Ihres Kontextfensters überschreiten, verschiebt Claude Code sie automatisch und lädt Tools bei Bedarf über [Tool-Suche](/de/mcp#scale-with-mcp-tool-search). Da verschobene Tools nur in den Kontext eintreten, wenn sie tatsächlich verwendet werden, bedeutet ein niedrigerer Schwellenwert weniger untätige Tool-Definitionen, die Platz verbrauchen. Legen Sie einen niedrigeren Schwellenwert mit `ENABLE_TOOL_SEARCH=auto:<N>` fest (z. B. `auto:5` wird ausgelöst, wenn Tools 5 % Ihres Kontextfensters überschreiten).

### Installieren Sie Code-Intelligence-Plugins für typisierte Sprachen

[Code-Intelligence-Plugins](/de/discover-plugins#code-intelligence) geben Claude präzise Symbol-Navigation statt textbasierter Suche, wodurch unnötige Dateileser beim Erkunden unbekannten Codes reduziert werden. Ein einzelner „Gehe zu Definition"-Aufruf ersetzt, was sonst ein Grep gefolgt vom Lesen mehrerer Kandidatendateien sein könnte. Installierte Sprachserver melden auch Typfehler automatisch nach Bearbeitungen, sodass Claude Fehler erkennt, ohne einen Compiler auszuführen.

### Verlagern Sie die Verarbeitung auf Hooks und Skills

Benutzerdefinierte [Hooks](/de/hooks) können Daten vorverarbeiten, bevor Claude sie sieht. Anstatt dass Claude eine 10.000-Zeilen-Protokolldatei liest, um Fehler zu finden, kann ein Hook nach `ERROR` suchen und nur übereinstimmende Zeilen zurückgeben, wodurch der Kontext von Zehntausenden Token auf Hunderte reduziert wird.

Ein [Skill](/de/skills) kann Claude Domänenwissen geben, sodass es nicht erkunden muss. Beispielsweise könnte ein „codebase-overview"-Skill die Architektur Ihres Projekts, wichtige Verzeichnisse und Namenskonventionen beschreiben. Wenn Claude den Skill aufruft, erhält es diesen Kontext sofort, anstatt Token zu verschwenden, um mehrere Dateien zu lesen, um die Struktur zu verstehen.

Beispielsweise filtert dieser PreToolUse-Hook die Testausgabe, um nur Fehler anzuzeigen:

<Tabs>
  <Tab title="settings.json">
    Fügen Sie dies zu Ihrer [settings.json](/de/settings#settings-files) hinzu, um den Hook vor jedem Bash-Befehl auszuführen:

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    Der Hook ruft dieses Skript auf, das überprüft, ob der Befehl ein Test-Runner ist, und ihn ändert, um nur Fehler anzuzeigen:

    ```bash theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

### Verschieben Sie Anweisungen von CLAUDE.md zu Skills

Ihre [CLAUDE.md](/de/memory)-Datei wird beim Sitzungsstart in den Kontext geladen. Wenn sie detaillierte Anweisungen für spezifische Workflows enthält (wie PR-Reviews oder Datenbankmigrationen), sind diese Token vorhanden, auch wenn Sie nicht verwandte Arbeit erledigen. [Skills](/de/skills) werden bei Bedarf nur geladen, wenn sie aufgerufen werden, daher hält das Verschieben spezialisierter Anweisungen in Skills Ihren Basis-Kontext kleiner. Streben Sie danach, CLAUDE.md unter etwa 500 Zeilen zu halten, indem Sie nur das Wesentliche einbeziehen.

### Passen Sie das erweiterte Denken an

Erweitertes Denken ist standardmäßig mit einem Budget von 31.999 Token aktiviert, da es die Leistung bei komplexen Planungs- und Denkaufgaben erheblich verbessert. Thinking-Token werden jedoch als Output-Token abgerechnet, daher können Sie für einfachere Aufgaben, bei denen tiefes Denken nicht erforderlich ist, Kosten reduzieren, indem Sie die [Anstrengungsstufe](/de/model-config#adjust-effort-level) mit `/effort` senken oder in `/model`, Denken in `/config` deaktivieren oder das Budget senken (z. B. `MAX_THINKING_TOKENS=8000`).

### Delegieren Sie ausführliche Operationen an Subagents

Das Ausführen von Tests, das Abrufen von Dokumentation oder das Verarbeiten von Protokolldateien kann erheblichen Kontext verbrauchen. Delegieren Sie diese an [Subagents](/de/sub-agents#isolate-high-volume-operations), sodass die ausführliche Ausgabe im Kontext des Subagent bleibt, während nur eine Zusammenfassung zu Ihrem Hauptgespräch zurückkehrt.

### Verwalten Sie Agent-Team-Kosten

Agent-Teams verwenden ungefähr 7-mal mehr Token als Standard-Sitzungen, wenn Teammates im Plan Mode laufen, da jeder Teammate sein eigenes Kontextfenster verwaltet und als separate Claude-Instanz läuft. Halten Sie Team-Aufgaben klein und in sich geschlossen, um die Token-Nutzung pro Teammate zu begrenzen. Siehe [Agent-Teams](/de/agent-teams) für Details.

### Schreiben Sie spezifische Prompts

Vage Anfragen wie „Verbessern Sie diese Codebasis" lösen breites Scannen aus. Spezifische Anfragen wie „Fügen Sie Eingabevalidierung zur Login-Funktion in auth.ts hinzu" ermöglichen es Claude, effizient mit minimalen Dateileser zu arbeiten.

### Arbeiten Sie effizient an komplexen Aufgaben

Für längere oder komplexere Arbeiten helfen diese Gewohnheiten, verschwendete Token durch das Gehen des falschen Weges zu vermeiden:

* **Verwenden Sie Plan Mode für komplexe Aufgaben**: Drücken Sie Shift+Tab, um [Plan Mode](/de/common-workflows#use-plan-mode-for-safe-code-analysis) vor der Implementierung zu betreten. Claude erkundet die Codebasis und schlägt einen Ansatz zur Genehmigung vor, was teure Überarbeitungen verhindert, wenn die anfängliche Richtung falsch ist.
* **Korrigieren Sie den Kurs früh**: Wenn Claude in die falsche Richtung geht, drücken Sie Escape, um sofort zu stoppen. Verwenden Sie `/rewind` oder doppeltippen Sie Escape, um das Gespräch und den Code zu einem vorherigen Checkpoint wiederherzustellen.
* **Geben Sie Verifizierungsziele an**: Fügen Sie Testfälle ein, fügen Sie Screenshots ein oder definieren Sie erwartete Ausgabe in Ihrem Prompt. Wenn Claude seine eigene Arbeit verifizieren kann, erkennt es Probleme, bevor Sie Korrektionen anfordern müssen.
* **Testen Sie schrittweise**: Schreiben Sie eine Datei, testen Sie sie, dann fahren Sie fort. Dies erkennt Probleme früh, wenn sie billig zu beheben sind.

## Hintergrund-Token-Nutzung

Claude Code verwendet Token für einige Hintergrund-Funktionalität, auch wenn untätig:

* **Gesprächszusammenfassung**: Hintergrund-Jobs, die vorherige Gespräche für die `claude --resume`-Funktion zusammenfassen
* **Befehlsverarbeitung**: Einige Befehle wie `/cost` können Anfragen generieren, um den Status zu überprüfen

Diese Hintergrund-Prozesse verbrauchen eine kleine Menge Token (typischerweise unter 0,04 USD pro Sitzung), auch ohne aktive Interaktion.

## Verstehen Sie Änderungen im Claude Code-Verhalten

Claude Code erhält regelmäßig Updates, die ändern können, wie Funktionen funktionieren, einschließlich Kostenberichterstattung. Führen Sie `claude --version` aus, um Ihre aktuelle Version zu überprüfen. Für spezifische Abrechnungsfragen kontaktieren Sie den Anthropic-Support über Ihr [Console-Konto](https://platform.claude.com/login). Für Team-Bereitstellungen beginnen Sie mit einer kleinen Pilotgruppe, um Nutzungsmuster zu etablieren, bevor Sie einen breiteren Rollout durchführen.
