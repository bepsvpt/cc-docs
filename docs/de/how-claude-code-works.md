> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# So funktioniert Claude Code

> Verstehen Sie die agentengesteuerte Schleife, integrierte Tools und wie Claude Code mit Ihrem Projekt interagiert.

Claude Code ist ein agentengesteuerter Assistent, der in Ihrem Terminal läuft. Obwohl er sich bei der Codierung auszeichnet, kann er bei allem helfen, was Sie von der Befehlszeile aus tun können: Dokumentation schreiben, Builds ausführen, Dateien durchsuchen, Themen recherchieren und vieles mehr.

Dieser Leitfaden behandelt die Kernarchitektur, integrierte Funktionen und [Tipps für effektive Zusammenarbeit mit Claude Code](#work-effectively-with-claude-code). Für schrittweise Anleitungen siehe [Häufige Workflows](/de/common-workflows). Für Erweiterungsfunktionen wie skills, MCP und hooks siehe [Claude Code erweitern](/de/features-overview).

## Die agentengesteuerte Schleife

Wenn Sie Claude eine Aufgabe geben, arbeitet er durch drei Phasen: **Kontext sammeln**, **Maßnahmen ergreifen** und **Ergebnisse überprüfen**. Diese Phasen verschmelzen miteinander. Claude nutzt Tools durchgehend, ob beim Durchsuchen von Dateien zum Verständnis Ihres Codes, beim Bearbeiten zur Vornahme von Änderungen oder beim Ausführen von Tests zur Überprüfung seiner Arbeit.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38" alt="Die agentengesteuerte Schleife: Ihre Eingabeaufforderung führt dazu, dass Claude Kontext sammelt, Maßnahmen ergreift, Ergebnisse überprüft und wiederholt, bis die Aufgabe abgeschlossen ist. Sie können jederzeit unterbrechen." width="720" height="280" data-path="images/agentic-loop.svg" />

Die Schleife passt sich an das an, was Sie fragen. Eine Frage zu Ihrer Codebasis könnte nur Kontextsammlung erfordern. Eine Fehlerbehebung durchläuft alle drei Phasen wiederholt. Eine Umstrukturierung könnte umfangreiche Überprüfung beinhalten. Claude entscheidet, was jeder Schritt erfordert, basierend auf dem, was er aus dem vorherigen Schritt gelernt hat, verkettet Dutzende von Aktionen zusammen und korrigiert seinen Kurs unterwegs.

Sie sind auch Teil dieser Schleife. Sie können jederzeit unterbrechen, um Claude in eine andere Richtung zu lenken, zusätzlichen Kontext bereitzustellen oder ihn zu bitten, einen anderen Ansatz zu versuchen. Claude arbeitet autonom, bleibt aber responsiv gegenüber Ihrer Eingabe.

Die agentengesteuerte Schleife wird von zwei Komponenten angetrieben: [Modellen](#models), die denken, und [Tools](#tools), die handeln. Claude Code dient als **agentengesteuerte Umgebung** um Claude: Sie bietet die Tools, Kontextverwaltung und Ausführungsumgebung, die ein Sprachmodell in einen fähigen Codierungs-Agenten verwandeln.

### Modelle

Claude Code nutzt Claude-Modelle, um Ihren Code zu verstehen und über Aufgaben nachzudenken. Claude kann Code in jeder Sprache lesen, verstehen, wie Komponenten verbunden sind, und herausfinden, was sich ändern muss, um Ihr Ziel zu erreichen. Bei komplexen Aufgaben unterteilt er die Arbeit in Schritte, führt sie aus und passt sich basierend auf dem an, was er lernt.

[Mehrere Modelle](/de/model-config) sind mit unterschiedlichen Kompromissen verfügbar. Sonnet bewältigt die meisten Codierungsaufgaben gut. Opus bietet stärkeres Denken für komplexe architektonische Entscheidungen. Wechseln Sie mit `/model` während einer Sitzung oder starten Sie mit `claude --model <name>`.

Wenn dieser Leitfaden sagt „Claude wählt" oder „Claude entscheidet", ist es das Modell, das die Überlegung durchführt.

### Tools

Tools sind das, was Claude Code agentengesteuert macht. Ohne Tools kann Claude nur mit Text antworten. Mit Tools kann Claude handeln: Ihren Code lesen, Dateien bearbeiten, Befehle ausführen, das Web durchsuchen und mit externen Diensten interagieren. Jede Tool-Nutzung gibt Informationen zurück, die in die Schleife fließen und Claudes nächste Entscheidung informieren.

Die integrierten Tools fallen im Allgemeinen in fünf Kategorien, die jeweils eine andere Art von Agentur darstellen.

| Kategorie            | Was Claude tun kann                                                                                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dateivorgänge**    | Dateien lesen, Code bearbeiten, neue Dateien erstellen, umbenennen und reorganisieren                                                                                        |
| **Suche**            | Dateien nach Muster finden, Inhalte mit Regex durchsuchen, Codebases erkunden                                                                                                |
| **Ausführung**       | Shell-Befehle ausführen, Server starten, Tests ausführen, git verwenden                                                                                                      |
| **Web**              | Das Web durchsuchen, Dokumentation abrufen, Fehlermeldungen nachschlagen                                                                                                     |
| **Code-Intelligenz** | Typfehler und Warnungen nach Bearbeitungen sehen, zu Definitionen springen, Referenzen finden (erfordert [Code-Intelligenz-Plugins](/de/discover-plugins#code-intelligence)) |

Dies sind die primären Funktionen. Claude hat auch Tools zum Spawnen von subagents, zum Stellen von Fragen und für andere Orchestrierungsaufgaben. Siehe [Tools verfügbar für Claude](/de/tools-reference) für die vollständige Liste.

Claude wählt basierend auf Ihrer Eingabeaufforderung und dem, was er unterwegs lernt, aus, welche Tools er verwenden soll. Wenn Sie sagen „beheben Sie die fehlgeschlagenen Tests", könnte Claude:

1. Die Test-Suite ausführen, um zu sehen, was fehlschlägt
2. Die Fehlerausgabe lesen
3. Nach den relevanten Quelldateien suchen
4. Diese Dateien lesen, um den Code zu verstehen
5. Die Dateien bearbeiten, um das Problem zu beheben
6. Die Tests erneut ausführen, um zu überprüfen

Jede Tool-Nutzung gibt Claude neue Informationen, die den nächsten Schritt informieren. Dies ist die agentengesteuerte Schleife in Aktion.

**Erweitern der Basisfunktionen:** Die integrierten Tools sind die Grundlage. Sie können das, was Claude weiß, mit [skills](/de/skills) erweitern, sich mit externen Diensten mit [MCP](/de/mcp) verbinden, Workflows mit [hooks](/de/hooks) automatisieren und Aufgaben an [subagents](/de/sub-agents) delegieren. Diese Erweiterungen bilden eine Schicht auf der Grundlage der agentengesteuerten Schleife. Siehe [Claude Code erweitern](/de/features-overview) für Anleitung zur Auswahl der richtigen Erweiterung für Ihre Anforderungen.

## Worauf Claude zugreifen kann

Dieser Leitfaden konzentriert sich auf das Terminal. Claude Code läuft auch in [VS Code](/de/vs-code), [JetBrains IDEs](/de/jetbrains) und anderen Umgebungen.

Wenn Sie `claude` in einem Verzeichnis ausführen, erhält Claude Code Zugriff auf:

* **Ihr Projekt.** Dateien in Ihrem Verzeichnis und Unterverzeichnissen sowie Dateien an anderer Stelle mit Ihrer Genehmigung.
* **Ihr Terminal.** Jeden Befehl, den Sie ausführen könnten: Build-Tools, git, Paketmanager, Systemdienstprogramme, Skripte. Wenn Sie es von der Befehlszeile aus tun können, kann Claude es auch.
* **Ihren git-Status.** Aktueller Branch, nicht committete Änderungen und aktuelle Commit-Historie.
* **Ihre [CLAUDE.md](/de/memory).** Eine Markdown-Datei, in der Sie projektspezifische Anweisungen, Konventionen und Kontext speichern, den Claude jede Sitzung kennen sollte.
* **[Auto-Speicher](/de/memory#auto-memory).** Erkenntnisse, die Claude automatisch speichert, während Sie arbeiten, wie Projektmuster und Ihre Vorlieben. Die ersten 200 Zeilen von MEMORY.md werden zu Beginn jeder Sitzung geladen.
* **Erweiterungen, die Sie konfigurieren.** [MCP-Server](/de/mcp) für externe Dienste, [skills](/de/skills) für Workflows, [subagents](/de/sub-agents) für delegierte Arbeit und [Claude in Chrome](/de/chrome) für Browser-Interaktion.

Da Claude Ihr gesamtes Projekt sieht, kann er darin arbeiten. Wenn Sie Claude bitten, „den Authentifizierungsfehler zu beheben", sucht er nach relevanten Dateien, liest mehrere Dateien, um den Kontext zu verstehen, nimmt koordinierte Bearbeitungen vor, führt Tests aus, um die Behebung zu überprüfen, und committed die Änderungen, wenn Sie es fragen. Dies unterscheidet sich von Inline-Code-Assistenten, die nur die aktuelle Datei sehen.

## Umgebungen und Schnittstellen

Die agentengesteuerte Schleife, Tools und Funktionen, die oben beschrieben sind, sind überall gleich, wo Sie Claude Code verwenden. Was sich ändert, ist, wo der Code ausgeführt wird und wie Sie damit interagieren.

### Ausführungsumgebungen

Claude Code läuft in drei Umgebungen, jede mit unterschiedlichen Kompromissen für die Ausführung Ihres Codes.

| Umgebung           | Wo Code läuft                             | Anwendungsfall                                                       |
| ------------------ | ----------------------------------------- | -------------------------------------------------------------------- |
| **Lokal**          | Ihr Computer                              | Standard. Vollständiger Zugriff auf Ihre Dateien, Tools und Umgebung |
| **Cloud**          | Von Anthropic verwaltete VMs              | Aufgaben auslagern, an Repos arbeiten, die Sie nicht lokal haben     |
| **Remote Control** | Ihr Computer, gesteuert von einem Browser | Verwenden Sie die Web-UI, während Sie alles lokal halten             |

### Schnittstellen

Sie können auf Claude Code über das Terminal, die [Desktop-App](/de/desktop), [IDE-Erweiterungen](/de/ide-integrations), [claude.ai/code](https://claude.ai/code), [Remote Control](/de/remote-control), [Slack](/de/slack) und [CI/CD-Pipelines](/de/github-actions) zugreifen. Die Schnittstelle bestimmt, wie Sie Claude sehen und damit interagieren, aber die zugrunde liegende agentengesteuerte Schleife ist identisch. Siehe [Claude Code überall verwenden](/de/overview#use-claude-code-everywhere) für die vollständige Liste.

## Mit Sitzungen arbeiten

Claude Code speichert Ihre Konversation lokal, während Sie arbeiten. Jede Nachricht, Tool-Nutzung und jedes Ergebnis wird gespeichert, was [Zurückspulen](#undo-changes-with-checkpoints), [Fortsetzen und Verzweigen](#resume-or-fork-sessions) von Sitzungen ermöglicht. Bevor Claude Code-Änderungen vornimmt, erstellt er auch einen Snapshot der betroffenen Dateien, damit Sie bei Bedarf zurückrollen können.

**Sitzungen sind unabhängig.** Jede neue Sitzung beginnt mit einem frischen Kontextfenster, ohne die Konversationshistorie aus vorherigen Sitzungen. Claude kann Erkenntnisse über Sitzungen hinweg mit [Auto-Speicher](/de/memory#auto-memory) beibehalten, und Sie können Ihre eigenen persistenten Anweisungen in [CLAUDE.md](/de/memory) hinzufügen.

### Über Branches arbeiten

Jede Claude Code-Konversation ist eine Sitzung, die an Ihr aktuelles Verzeichnis gebunden ist. Wenn Sie fortsetzen, sehen Sie nur Sitzungen aus diesem Verzeichnis.

Claude sieht die Dateien Ihres aktuellen Branches. Wenn Sie Branches wechseln, sieht Claude die Dateien des neuen Branches, aber Ihre Konversationshistorie bleibt gleich. Claude erinnert sich an das, was Sie besprochen haben, auch nach dem Wechsel.

Da Sitzungen an Verzeichnisse gebunden sind, können Sie parallele Claude-Sitzungen ausführen, indem Sie [git worktrees](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) verwenden, die separate Verzeichnisse für einzelne Branches erstellen.

### Sitzungen fortsetzen oder verzweigen

Wenn Sie eine Sitzung mit `claude --continue` oder `claude --resume` fortsetzen, setzen Sie dort fort, wo Sie aufgehört haben, mit derselben Sitzungs-ID. Neue Nachrichten werden an die bestehende Konversation angehängt. Ihre vollständige Konversationshistorie wird wiederhergestellt, aber sitzungsspezifische Berechtigungen nicht. Sie müssen diese erneut genehmigen.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30" alt="Sitzungskontinuität: Fortsetzen setzt dieselbe Sitzung fort, Verzweigung erstellt einen neuen Branch mit einer neuen ID." width="560" height="280" data-path="images/session-continuity.svg" />

Um abzuzweigen und einen anderen Ansatz zu versuchen, ohne die ursprüngliche Sitzung zu beeinflussen, verwenden Sie das Flag `--fork-session`:

```bash  theme={null}
claude --continue --fork-session
```

Dies erstellt eine neue Sitzungs-ID, während die Konversationshistorie bis zu diesem Punkt beibehalten wird. Die ursprüngliche Sitzung bleibt unverändert. Wie beim Fortsetzen erben verzweigte Sitzungen keine sitzungsspezifischen Berechtigungen.

**Dieselbe Sitzung in mehreren Terminals**: Wenn Sie dieselbe Sitzung in mehreren Terminals fortsetzen, schreiben beide Terminals in dieselbe Sitzungsdatei. Nachrichten von beiden werden verschachtelt, wie zwei Personen, die in dasselbe Notizbuch schreiben. Nichts wird beschädigt, aber die Konversation wird durcheinander. Jedes Terminal sieht nur seine eigenen Nachrichten während der Sitzung, aber wenn Sie diese Sitzung später fortsetzen, sehen Sie alles verschachtelt. Für parallele Arbeit vom selben Ausgangspunkt verwenden Sie `--fork-session`, um jedem Terminal seine eigene saubere Sitzung zu geben.

### Das Kontextfenster

Claudes Kontextfenster enthält Ihre Konversationshistorie, Dateiinhalte, Befehlsausgaben, [CLAUDE.md](/de/memory), [Auto-Speicher](/de/memory#auto-memory), geladene skills und Systemanweisungen. Während Sie arbeiten, füllt sich der Kontext. Claude komprimiert automatisch, aber Anweisungen von früh in der Konversation können verloren gehen. Legen Sie persistente Regeln in CLAUDE.md ab, und führen Sie `/context` aus, um zu sehen, was Platz verbraucht.

#### Wenn der Kontext voll wird

Claude Code verwaltet den Kontext automatisch, wenn Sie sich dem Limit nähern. Es löscht zuerst ältere Tool-Ausgaben, dann fasst die Konversation zusammen, falls erforderlich. Ihre Anfragen und wichtige Code-Snippets werden beibehalten; detaillierte Anweisungen von früh in der Konversation können verloren gehen. Legen Sie persistente Regeln in CLAUDE.md ab, anstatt sich auf die Konversationshistorie zu verlassen.

Um zu kontrollieren, was während der Komprimierung beibehalten wird, fügen Sie einen Abschnitt „Compact Instructions" zu CLAUDE.md hinzu oder führen Sie `/compact` mit einem Fokus aus (wie `/compact focus on the API changes`).

Führen Sie `/context` aus, um zu sehen, was Platz verbraucht. MCP-Server fügen Tool-Definitionen zu jeder Anfrage hinzu, daher können einige wenige Server erheblichen Kontext verbrauchen, bevor Sie mit der Arbeit beginnen. Führen Sie `/mcp` aus, um die Kosten pro Server zu überprüfen.

#### Kontext mit skills und subagents verwalten

Über die Komprimierung hinaus können Sie andere Funktionen verwenden, um zu kontrollieren, was in den Kontext geladen wird.

[Skills](/de/skills) werden bei Bedarf geladen. Claude sieht Skill-Beschreibungen zu Sitzungsbeginn, aber der vollständige Inhalt wird nur geladen, wenn ein Skill verwendet wird. Für Skills, die Sie manuell aufrufen, setzen Sie `disable-model-invocation: true`, um Beschreibungen aus dem Kontext zu halten, bis Sie sie benötigen.

[Subagents](/de/sub-agents) erhalten ihren eigenen frischen Kontext, völlig getrennt von Ihrer Hauptkonversation. Ihre Arbeit bläht Ihren Kontext nicht auf. Wenn sie fertig sind, geben sie eine Zusammenfassung zurück. Diese Isolation ist der Grund, warum subagents bei langen Sitzungen helfen.

Siehe [Kontextkosten](/de/features-overview#understand-context-costs) für die Kosten jeder Funktion und [Token-Nutzung reduzieren](/de/costs#reduce-token-usage) für Tipps zur Verwaltung des Kontexts.

## Sicher bleiben mit Checkpoints und Berechtigungen

Claude hat zwei Sicherheitsmechanismen: Checkpoints ermöglichen es Ihnen, Dateiänderungen rückgängig zu machen, und Berechtigungen kontrollieren, was Claude ohne Nachfrage tun kann.

### Änderungen mit Checkpoints rückgängig machen

**Jede Dateibearbeitung ist reversibel.** Bevor Claude eine Datei bearbeitet, erstellt er einen Snapshot des aktuellen Inhalts. Wenn etwas schief geht, drücken Sie zweimal `Esc`, um zu einem vorherigen Zustand zurückzuspulen, oder bitten Sie Claude, rückgängig zu machen.

Checkpoints sind lokal für Ihre Sitzung, getrennt von git. Sie decken nur Dateiänderungen ab. Aktionen, die sich auf Remote-Systeme auswirken (Datenbanken, APIs, Bereitstellungen), können nicht checkpointed werden, weshalb Claude vor dem Ausführen von Befehlen mit externen Nebenwirkungen fragt.

### Kontrollieren Sie, was Claude tun kann

Drücken Sie `Shift+Tab`, um durch die Berechtigungsmodi zu wechseln:

* **Standard**: Claude fragt vor Dateibearbeitungen und Shell-Befehlen
* **Auto-accept edits**: Claude bearbeitet Dateien ohne zu fragen, fragt aber immer noch nach Befehlen
* **Plan Mode**: Claude verwendet nur schreibgeschützte Tools und erstellt einen Plan, den Sie vor der Ausführung genehmigen können
* **Auto Mode**: Claude bewertet alle Aktionen mit Hintergrund-Sicherheitsprüfungen. Derzeit eine Forschungsvorschau

Sie können auch spezifische Befehle in `.claude/settings.json` zulassen, damit Claude nicht jedes Mal fragt. Dies ist nützlich für vertrauenswürdige Befehle wie `npm test` oder `git status`. Einstellungen können von organisationsweiten Richtlinien bis zu persönlichen Vorlieben reichen. Siehe [Berechtigungen](/de/permissions) für Details.

***

## Effektiv mit Claude Code arbeiten

Diese Tipps helfen Ihnen, bessere Ergebnisse von Claude Code zu erhalten.

### Fragen Sie Claude Code um Hilfe

Claude Code kann Ihnen beibringen, wie man ihn verwendet. Stellen Sie Fragen wie „Wie richte ich hooks ein?" oder „Was ist der beste Weg, meine CLAUDE.md zu strukturieren?" und Claude wird erklären.

Integrierte Befehle führen Sie auch durch die Einrichtung:

* `/init` führt Sie durch die Erstellung einer CLAUDE.md für Ihr Projekt
* `/agents` hilft Ihnen, benutzerdefinierte subagents zu konfigurieren
* `/doctor` diagnostiziert häufige Probleme mit Ihrer Installation

### Es ist eine Konversation

Claude Code ist konversativ. Sie benötigen keine perfekten Eingabeaufforderungen. Beginnen Sie mit dem, was Sie möchten, und verfeinern Sie dann:

```text  theme={null}
Beheben Sie den Login-Fehler
```

\[Claude untersucht, versucht etwas]

```text  theme={null}
Das ist nicht ganz richtig. Das Problem liegt in der Sitzungsverwaltung.
```

\[Claude passt seinen Ansatz an]

Wenn der erste Versuch nicht richtig ist, müssen Sie nicht von vorne anfangen. Sie iterieren.

#### Unterbrechen und lenken

Sie können Claude jederzeit unterbrechen. Wenn er den falschen Weg geht, geben Sie einfach Ihre Korrektur ein und drücken Sie Enter. Claude wird stoppen, was er tut, und seinen Ansatz basierend auf Ihrer Eingabe anpassen. Sie müssen nicht warten, bis er fertig ist, oder von vorne anfangen.

### Seien Sie von Anfang an spezifisch

Je präziser Ihre anfängliche Eingabeaufforderung ist, desto weniger Korrektionen benötigen Sie. Verweisen Sie auf spezifische Dateien, erwähnen Sie Einschränkungen und zeigen Sie auf Beispielmuster.

```text  theme={null}
Der Checkout-Fluss ist für Benutzer mit abgelaufenen Karten unterbrochen.
Überprüfen Sie src/payments/ auf das Problem, besonders Token-Aktualisierung.
Schreiben Sie zuerst einen fehlgeschlagenen Test, dann beheben Sie ihn.
```

Vage Eingabeaufforderungen funktionieren, aber Sie werden mehr Zeit mit Lenkung verbringen. Spezifische Eingabeaufforderungen wie die obige gelingen oft beim ersten Versuch.

### Geben Sie Claude etwas zum Überprüfen

Claude funktioniert besser, wenn er seine eigene Arbeit überprüfen kann. Fügen Sie Testfälle ein, fügen Sie Screenshots des erwarteten UI ein oder definieren Sie die gewünschte Ausgabe.

```text  theme={null}
Implementieren Sie validateEmail. Testfälle: 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Führen Sie die Tests danach aus.
```

Für visuelle Arbeit fügen Sie einen Screenshot des Designs ein und bitten Sie Claude, seine Implementierung dagegen zu vergleichen.

### Vor der Implementierung erkunden

Bei komplexen Problemen trennen Sie Forschung von Codierung. Verwenden Sie Plan Mode (`Shift+Tab` zweimal), um die Codebasis zuerst zu analysieren:

```text  theme={null}
Lesen Sie src/auth/ und verstehen Sie, wie wir Sitzungen handhaben.
Erstellen Sie dann einen Plan zum Hinzufügen von OAuth-Unterstützung.
```

Überprüfen Sie den Plan, verfeinern Sie ihn durch Konversation, dann lassen Sie Claude implementieren. Dieser zweiphasige Ansatz erzeugt bessere Ergebnisse als direkt zum Code zu springen.

### Delegieren, nicht diktieren

Denken Sie daran, an einen fähigen Kollegen zu delegieren. Geben Sie Kontext und Richtung, dann vertrauen Sie Claude, die Details herauszufinden:

```text  theme={null}
Der Checkout-Fluss ist für Benutzer mit abgelaufenen Karten unterbrochen.
Der relevante Code ist in src/payments/. Können Sie ihn untersuchen und beheben?
```

Sie müssen nicht angeben, welche Dateien zu lesen sind oder welche Befehle auszuführen sind. Claude findet das heraus.

## Nächste Schritte

<CardGroup cols={2}>
  <Card title="Mit Funktionen erweitern" icon="puzzle-piece" href="/de/features-overview">
    Fügen Sie Skills, MCP-Verbindungen und benutzerdefinierte Befehle hinzu
  </Card>

  <Card title="Häufige Workflows" icon="graduation-cap" href="/de/common-workflows">
    Schritt-für-Schritt-Anleitungen für typische Aufgaben
  </Card>
</CardGroup>
