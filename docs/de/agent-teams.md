> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Orchestrieren Sie Teams von Claude Code-Sitzungen

> Koordinieren Sie mehrere Claude Code-Instanzen, die zusammen als Team arbeiten, mit gemeinsamen Aufgaben, Messaging zwischen Agenten und zentraler Verwaltung.

<Warning>
  Agent-Teams sind experimentell und standardmäßig deaktiviert. Aktivieren Sie sie, indem Sie `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` zu Ihrer [settings.json](/de/settings) oder Umgebung hinzufügen. Agent-Teams haben [bekannte Einschränkungen](#limitations) bezüglich Sitzungswiederaufnahme, Aufgabenkoordination und Abschaltungsverhalten.
</Warning>

Agent-Teams ermöglichen es Ihnen, mehrere Claude Code-Instanzen zu koordinieren, die zusammenarbeiten. Eine Sitzung fungiert als Team-Lead und koordiniert die Arbeit, weist Aufgaben zu und synthetisiert Ergebnisse. Teammates arbeiten unabhängig, jeder in seinem eigenen Kontextfenster, und kommunizieren direkt miteinander.

Im Gegensatz zu [subagents](/de/sub-agents), die innerhalb einer einzelnen Sitzung ausgeführt werden und nur an den Hauptagenten berichten können, können Sie auch direkt mit einzelnen Teammates interagieren, ohne den Lead einzubeziehen.

<Note>
  Agent-Teams erfordern Claude Code v2.1.32 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

Diese Seite behandelt:

* [Wann Agent-Teams verwendet werden](#when-to-use-agent-teams), einschließlich der besten Anwendungsfälle und wie sie sich mit subagents vergleichen
* [Starten eines Teams](#start-your-first-agent-team)
* [Kontrolle von Teammates](#control-your-agent-team), einschließlich Anzeigemodi, Aufgabenzuweisung und Delegation
* [Best Practices für parallele Arbeit](#best-practices)

## Wann Agent-Teams verwendet werden

Agent-Teams sind am effektivsten für Aufgaben, bei denen parallele Exploration echten Wert bietet. Siehe [Anwendungsbeispiele](#use-case-examples) für vollständige Szenarien. Die stärksten Anwendungsfälle sind:

* **Recherche und Überprüfung**: mehrere Teammates können verschiedene Aspekte eines Problems gleichzeitig untersuchen und dann ihre Erkenntnisse austauschen und in Frage stellen
* **Neue Module oder Features**: Teammates können jeweils ein separates Stück besitzen, ohne sich gegenseitig zu behindern
* **Debugging mit konkurrierenden Hypothesen**: Teammates testen verschiedene Theorien parallel und konvergieren schneller zur Antwort
* **Schichtenübergreifende Koordination**: Änderungen, die Frontend, Backend und Tests umfassen, jeweils von einem anderen Teammate verwaltet

Agent-Teams fügen Koordinationsaufwand hinzu und verwenden deutlich mehr Tokens als eine einzelne Sitzung. Sie funktionieren am besten, wenn Teammates unabhängig arbeiten können. Für sequenzielle Aufgaben, Bearbeitungen in derselben Datei oder Arbeit mit vielen Abhängigkeiten sind eine einzelne Sitzung oder [subagents](/de/sub-agents) effektiver.

### Vergleich mit subagents

Sowohl Agent-Teams als auch [subagents](/de/sub-agents) ermöglichen es Ihnen, Arbeit zu parallelisieren, aber sie funktionieren unterschiedlich. Wählen Sie basierend darauf, ob Ihre Worker miteinander kommunizieren müssen:

<Frame caption="Subagents berichten Ergebnisse nur an den Hauptagenten zurück und sprechen nie miteinander. Bei Agent-Teams teilen sich Teammates eine Aufgabenliste, beanspruchen Arbeit und kommunizieren direkt miteinander.">
  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-light.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=2f8db9b4f3705dd3ab931fbe2d96e42a" className="dark:hidden" alt="Diagramm zum Vergleich von Subagent- und Agent-Team-Architekturen. Subagents werden vom Hauptagenten erzeugt, führen Arbeit aus und berichten Ergebnisse zurück. Agent-Teams koordinieren sich über eine gemeinsame Aufgabenliste, wobei Teammates direkt miteinander kommunizieren." width="4245" height="1615" data-path="images/subagents-vs-agent-teams-light.png" />

  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-dark.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=d573a037540f2ada6a9ae7d8285b46fd" className="hidden dark:block" alt="Diagramm zum Vergleich von Subagent- und Agent-Team-Architekturen. Subagents werden vom Hauptagenten erzeugt, führen Arbeit aus und berichten Ergebnisse zurück. Agent-Teams koordinieren sich über eine gemeinsame Aufgabenliste, wobei Teammates direkt miteinander kommunizieren." width="4245" height="1615" data-path="images/subagents-vs-agent-teams-dark.png" />
</Frame>

|                   | Subagents                                                     | Agent-Teams                                                  |
| :---------------- | :------------------------------------------------------------ | :----------------------------------------------------------- |
| **Kontext**       | Eigenes Kontextfenster; Ergebnisse kehren zum Aufrufer zurück | Eigenes Kontextfenster; vollständig unabhängig               |
| **Kommunikation** | Berichte Ergebnisse nur an den Hauptagenten zurück            | Teammates senden sich gegenseitig direkt Nachrichten         |
| **Koordination**  | Hauptagent verwaltet alle Arbeiten                            | Gemeinsame Aufgabenliste mit Selbstkoordination              |
| **Am besten für** | Fokussierte Aufgaben, bei denen nur das Ergebnis zählt        | Komplexe Arbeit, die Diskussion und Zusammenarbeit erfordert |
| **Token-Kosten**  | Niedriger: Ergebnisse werden zum Hauptkontext zusammengefasst | Höher: jeder Teammate ist eine separate Claude-Instanz       |

Verwenden Sie subagents, wenn Sie schnelle, fokussierte Worker benötigen, die berichten. Verwenden Sie Agent-Teams, wenn Teammates Erkenntnisse austauschen, sich gegenseitig in Frage stellen und selbst koordinieren müssen.

## Agent-Teams aktivieren

Agent-Teams sind standardmäßig deaktiviert. Aktivieren Sie sie, indem Sie die Umgebungsvariable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` auf `1` setzen, entweder in Ihrer Shell-Umgebung oder über [settings.json](/de/settings):

```json settings.json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Starten Sie Ihr erstes Agent-Team

Nach der Aktivierung von Agent-Teams teilen Sie Claude mit, dass Sie ein Agent-Team erstellen möchten, und beschreiben Sie die Aufgabe und die gewünschte Teamstruktur in natürlicher Sprache. Claude erstellt das Team, erzeugt Teammates und koordiniert die Arbeit basierend auf Ihrem Prompt.

Dieses Beispiel funktioniert gut, weil die drei Rollen unabhängig sind und das Problem erkunden können, ohne aufeinander zu warten:

```text  theme={null}
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

Von dort aus erstellt Claude ein Team mit einer [gemeinsamen Aufgabenliste](/de/interactive-mode#task-list), erzeugt Teammates für jede Perspektive, lässt sie das Problem erkunden, synthetisiert Erkenntnisse und versucht, [das Team zu bereinigen](#clean-up-the-team), wenn es fertig ist.

Das Terminal des Leads listet alle Teammates und ihre aktuelle Arbeit auf. Verwenden Sie Shift+Down, um durch Teammates zu wechseln und ihnen direkt Nachrichten zu senden. Nach dem letzten Teammate wickelt Shift+Down zum Lead zurück.

Wenn Sie jeden Teammate in seinem eigenen Split-Pane haben möchten, siehe [Wählen Sie einen Anzeigemodus](#choose-a-display-mode).

## Kontrolle Ihres Agent-Teams

Teilen Sie dem Lead in natürlicher Sprache mit, was Sie möchten. Es kümmert sich um Teamkoordination, Aufgabenzuweisung und Delegation basierend auf Ihren Anweisungen.

### Wählen Sie einen Anzeigemodus

Agent-Teams unterstützen zwei Anzeigemodi:

* **In-Process**: alle Teammates laufen in Ihrem Hauptterminal. Verwenden Sie Shift+Down, um durch Teammates zu wechseln und geben Sie ein, um ihnen direkt eine Nachricht zu senden. Funktioniert in jedem Terminal, keine zusätzliche Einrichtung erforderlich.
* **Split Panes**: jeder Teammate erhält seinen eigenen Pane. Sie können die Ausgabe aller gleichzeitig sehen und in einen Pane klicken, um direkt zu interagieren. Erfordert tmux oder iTerm2.

<Note>
  `tmux` hat bekannte Einschränkungen auf bestimmten Betriebssystemen und funktioniert traditionell am besten auf macOS. Die Verwendung von `tmux -CC` in iTerm2 ist der empfohlene Einstiegspunkt in `tmux`.
</Note>

Der Standard ist `"auto"`, der Split Panes verwendet, wenn Sie bereits in einer tmux-Sitzung ausgeführt werden, und ansonsten In-Process. Die Einstellung `"tmux"` aktiviert den Split-Pane-Modus und erkennt automatisch, ob tmux oder iTerm2 basierend auf Ihrem Terminal verwendet werden soll. Um zu überschreiben, setzen Sie `teammateMode` in Ihrer [globalen Konfiguration](/de/settings#global-config-settings) unter `~/.claude.json`:

```json  theme={null}
{
  "teammateMode": "in-process"
}
```

Um den In-Process-Modus für eine einzelne Sitzung zu erzwingen, übergeben Sie ihn als Flag:

```bash  theme={null}
claude --teammate-mode in-process
```

Der Split-Pane-Modus erfordert entweder [tmux](https://github.com/tmux/tmux/wiki) oder iTerm2 mit der [`it2` CLI](https://github.com/mkusaka/it2). Zur manuellen Installation:

* **tmux**: installieren Sie über den Paketmanager Ihres Systems. Siehe das [tmux Wiki](https://github.com/tmux/tmux/wiki/Installing) für plattformspezifische Anweisungen.
* **iTerm2**: installieren Sie die [`it2` CLI](https://github.com/mkusaka/it2), aktivieren Sie dann die Python-API in **iTerm2 → Settings → General → Magic → Enable Python API**.

### Geben Sie Teammates und Modelle an

Claude entscheidet die Anzahl der zu erzeugenden Teammates basierend auf Ihrer Aufgabe, oder Sie können genau angeben, was Sie möchten:

```text  theme={null}
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### Genehmigung von Plänen für Teammates erforderlich

Für komplexe oder riskante Aufgaben können Sie verlangen, dass Teammates planen, bevor sie implementieren. Der Teammate arbeitet im schreibgeschützten Plan-Modus, bis der Lead seinen Ansatz genehmigt:

```text  theme={null}
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

Wenn ein Teammate die Planung abgeschlossen hat, sendet er eine Genehmigungsanfrage an den Lead. Der Lead überprüft den Plan und genehmigt ihn entweder oder lehnt ihn mit Feedback ab. Bei Ablehnung bleibt der Teammate im Plan-Modus, überarbeitet basierend auf dem Feedback und reicht erneut ein. Nach der Genehmigung beendet der Teammate den Plan-Modus und beginnt mit der Implementierung.

Der Lead trifft Genehmigungsentscheidungen autonom. Um das Urteil des Leads zu beeinflussen, geben Sie ihm Kriterien in Ihrem Prompt, wie z. B. „genehmigen Sie nur Pläne, die Testabdeckung enthalten" oder „lehnen Sie Pläne ab, die das Datenbankschema ändern".

### Sprechen Sie direkt mit Teammates

Jeder Teammate ist eine vollständige, unabhängige Claude Code-Sitzung. Sie können jedem Teammate direkt eine Nachricht senden, um zusätzliche Anweisungen zu geben, Folgefragen zu stellen oder seinen Ansatz umzuleiten.

* **In-Process-Modus**: Verwenden Sie Shift+Down, um durch Teammates zu wechseln, geben Sie dann ein, um ihnen eine Nachricht zu senden. Drücken Sie Enter, um die Sitzung eines Teammates anzuzeigen, dann Escape, um ihren aktuellen Turn zu unterbrechen. Drücken Sie Ctrl+T, um die Aufgabenliste umzuschalten.
* **Split-Pane-Modus**: klicken Sie in den Pane eines Teammates, um direkt mit seiner Sitzung zu interagieren. Jeder Teammate hat eine vollständige Ansicht seines eigenen Terminals.

### Aufgaben zuweisen und beanspruchen

Die gemeinsame Aufgabenliste koordiniert die Arbeit im Team. Der Lead erstellt Aufgaben und Teammates arbeiten sie durch. Aufgaben haben drei Zustände: ausstehend, in Bearbeitung und abgeschlossen. Aufgaben können auch von anderen Aufgaben abhängen: eine ausstehende Aufgabe mit ungelösten Abhängigkeiten kann nicht beansprucht werden, bis diese Abhängigkeiten erfüllt sind.

Der Lead kann Aufgaben explizit zuweisen oder Teammates können selbst beanspruchen:

* **Lead weist zu**: teilen Sie dem Lead mit, welche Aufgabe welchem Teammate gegeben werden soll
* **Selbst beanspruchen**: nach Abschluss einer Aufgabe wählt ein Teammate die nächste nicht zugewiesene, nicht blockierte Aufgabe selbst aus

Das Beanspruchen von Aufgaben verwendet Dateisperrung, um Race Conditions zu verhindern, wenn mehrere Teammates versuchen, gleichzeitig dieselbe Aufgabe zu beanspruchen.

### Teammates herunterfahren

Um die Sitzung eines Teammates ordnungsgemäß zu beenden:

```text  theme={null}
Ask the researcher teammate to shut down
```

Der Lead sendet eine Abschaltungsanfrage. Der Teammate kann zustimmen und ordnungsgemäß beenden oder mit einer Erklärung ablehnen.

### Bereinigen Sie das Team

Wenn Sie fertig sind, bitten Sie den Lead zu bereinigen:

```text  theme={null}
Clean up the team
```

Dies entfernt die gemeinsamen Teamressourcen. Wenn der Lead die Bereinigung ausführt, prüft er auf aktive Teammates und schlägt fehl, wenn noch welche laufen, also fahren Sie diese zuerst herunter.

<Warning>
  Verwenden Sie immer den Lead zum Bereinigen. Teammates sollten keine Bereinigung ausführen, da ihr Teamkontext möglicherweise nicht korrekt aufgelöst wird, was möglicherweise Ressourcen in einem inkonsistenten Zustand hinterlässt.
</Warning>

### Erzwingen Sie Qualitätsgates mit hooks

Verwenden Sie [hooks](/de/hooks), um Regeln durchzusetzen, wenn Teammates ihre Arbeit abschließen oder Aufgaben erstellt oder abgeschlossen werden:

* [`TeammateIdle`](/de/hooks#teammateidle): wird ausgeführt, wenn ein Teammate im Begriff ist, untätig zu werden. Beenden Sie mit Code 2, um Feedback zu senden und den Teammate weiterarbeiten zu lassen.
* [`TaskCreated`](/de/hooks#taskcreated): wird ausgeführt, wenn eine Aufgabe erstellt wird. Beenden Sie mit Code 2, um die Erstellung zu verhindern und Feedback zu senden.
* [`TaskCompleted`](/de/hooks#taskcompleted): wird ausgeführt, wenn eine Aufgabe als abgeschlossen markiert wird. Beenden Sie mit Code 2, um die Fertigstellung zu verhindern und Feedback zu senden.

## Wie Agent-Teams funktionieren

Dieser Abschnitt behandelt die Architektur und Mechanik hinter Agent-Teams. Wenn Sie sie verwenden möchten, siehe [Kontrolle Ihres Agent-Teams](#control-your-agent-team) oben.

### Wie Claude Agent-Teams startet

Es gibt zwei Möglichkeiten, wie Agent-Teams gestartet werden:

* **Sie fordern ein Team an**: geben Sie Claude eine Aufgabe, die von paralleler Arbeit profitiert, und fordern Sie explizit ein Agent-Team an. Claude erstellt eines basierend auf Ihren Anweisungen.
* **Claude schlägt ein Team vor**: wenn Claude feststellt, dass Ihre Aufgabe von paralleler Arbeit profitieren würde, kann es ein Team vorschlagen. Sie bestätigen, bevor es fortfährt.

In beiden Fällen behalten Sie die Kontrolle. Claude wird kein Team ohne Ihre Genehmigung erstellen.

### Architektur

Ein Agent-Team besteht aus:

| Komponente        | Rolle                                                                                              |
| :---------------- | :------------------------------------------------------------------------------------------------- |
| **Team Lead**     | Die Haupt-Claude Code-Sitzung, die das Team erstellt, Teammates erzeugt und die Arbeit koordiniert |
| **Teammates**     | Separate Claude Code-Instanzen, die jeweils an zugewiesenen Aufgaben arbeiten                      |
| **Aufgabenliste** | Gemeinsame Liste von Arbeitselementen, die Teammates beanspruchen und abschließen                  |
| **Mailbox**       | Nachrichtensystem für Kommunikation zwischen Agenten                                               |

Siehe [Wählen Sie einen Anzeigemodus](#choose-a-display-mode) für Anzeigeoptionen. Teammate-Nachrichten kommen automatisch beim Lead an.

Das System verwaltet Aufgabenabhängigkeiten automatisch. Wenn ein Teammate eine Aufgabe abschließt, von der andere Aufgaben abhängen, werden blockierte Aufgaben automatisch entsperrt.

Teams und Aufgaben werden lokal gespeichert:

* **Team-Konfiguration**: `~/.claude/teams/{team-name}/config.json`
* **Aufgabenliste**: `~/.claude/tasks/{team-name}/`

Claude Code generiert beide automatisch, wenn Sie ein Team erstellen, und aktualisiert sie, wenn Teammates beitreten, untätig werden oder gehen. Die Team-Konfiguration enthält Laufzeitzustand wie Session-IDs und tmux-Pane-IDs, also bearbeiten Sie sie nicht von Hand oder verfassen Sie sie nicht im Voraus: Ihre Änderungen werden beim nächsten Zustandsupdate überschrieben.

Um wiederverwendbare Teammate-Rollen zu definieren, verwenden Sie stattdessen [Subagent-Definitionen](#use-subagent-definitions-for-teammates).

Die Team-Konfiguration enthält ein `members`-Array mit dem Namen, der Agent-ID und dem Agent-Typ jedes Teammates. Teammates können diese Datei lesen, um andere Teammitglieder zu entdecken.

Es gibt kein Projekt-Level-Äquivalent der Team-Konfiguration. Eine Datei wie `.claude/teams/teams.json` in Ihrem Projektverzeichnis wird nicht als Konfiguration erkannt; Claude behandelt sie als gewöhnliche Datei.

### Verwenden Sie Subagent-Definitionen für Teammates

Beim Erzeugen eines Teammates können Sie einen [Subagent](/de/sub-agents)-Typ aus jedem [Subagent-Bereich](/de/sub-agents#choose-the-subagent-scope) referenzieren: Projekt, Benutzer, Plugin oder CLI-definiert. Der Teammate erbt den System-Prompt, die Tools und das Modell dieses Subagents. Dies ermöglicht es Ihnen, eine Rolle einmal zu definieren, wie z. B. einen Security-Reviewer oder Test-Runner, und sie sowohl als delegierter Subagent als auch als Agent-Team-Teammate wiederzuverwenden.

Um eine Subagent-Definition zu verwenden, erwähnen Sie sie nach Name, wenn Sie Claude auffordern, den Teammate zu erzeugen:

```text  theme={null}
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

### Berechtigungen

Teammates starten mit den Berechtigungseinstellungen des Leads. Wenn der Lead mit `--dangerously-skip-permissions` ausgeführt wird, tun dies auch alle Teammates. Nach dem Erzeugen können Sie einzelne Teammate-Modi ändern, aber Sie können keine Pro-Teammate-Modi zum Zeitpunkt des Erzeugung setzen.

### Kontext und Kommunikation

Jeder Teammate hat sein eigenes Kontextfenster. Beim Erzeugen lädt ein Teammate denselben Projektkontext wie eine reguläre Sitzung: CLAUDE.md, MCP servers und skills. Er erhält auch den Spawn-Prompt vom Lead. Die Gesprächshistorie des Leads wird nicht übertragen.

**Wie Teammates Informationen teilen:**

* **Automatische Nachrichtenlieferung**: wenn Teammates Nachrichten senden, werden sie automatisch an Empfänger geliefert. Der Lead muss nicht auf Updates abfragen.
* **Untätigkeitsbenachrichtigungen**: wenn ein Teammate fertig ist und stoppt, benachrichtigt er automatisch den Lead.
* **Gemeinsame Aufgabenliste**: alle Agenten können den Aufgabenstatus sehen und verfügbare Arbeit beanspruchen.

**Teammate-Messaging:**

* **message**: senden Sie eine Nachricht an einen bestimmten Teammate
* **broadcast**: senden Sie an alle Teammates gleichzeitig. Verwenden Sie sparsam, da die Kosten mit der Teamgröße skalieren.

### Token-Nutzung

Agent-Teams verwenden deutlich mehr Tokens als eine einzelne Sitzung. Jeder Teammate hat sein eigenes Kontextfenster, und die Token-Nutzung skaliert mit der Anzahl der aktiven Teammates. Für Recherche, Überprüfung und neue Feature-Arbeit sind die zusätzlichen Tokens normalerweise lohnenswert. Für Routineaufgaben ist eine einzelne Sitzung kostengünstiger. Siehe [Agent-Team-Token-Kosten](/de/costs#agent-team-token-costs) für Nutzungsleitfäden.

## Anwendungsbeispiele

Diese Beispiele zeigen, wie Agent-Teams Aufgaben handhaben, bei denen parallele Exploration Wert bietet.

### Führen Sie eine parallele Code-Überprüfung durch

Ein einzelner Reviewer neigt dazu, sich jeweils auf eine Art von Problem zu konzentrieren. Das Aufteilen von Überprüfungskriterien in unabhängige Domänen bedeutet, dass Sicherheit, Leistung und Testabdeckung alle gleichzeitig gründlich beachtet werden. Der Prompt weist jedem Teammate eine unterschiedliche Perspektive zu, damit sie sich nicht überlappen:

```text  theme={null}
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Jeder Reviewer arbeitet vom selben PR aus, wendet aber einen anderen Filter an. Der Lead synthetisiert Erkenntnisse über alle drei nach Abschluss.

### Untersuchen Sie mit konkurrierenden Hypothesen

Wenn die Grundursache unklar ist, neigt ein einzelner Agent dazu, eine plausible Erklärung zu finden und zu stoppen. Der Prompt bekämpft dies, indem er Teammates explizit gegnerisch macht: die Aufgabe jedes ist nicht nur, seine eigene Theorie zu untersuchen, sondern auch die anderen in Frage zu stellen.

```text  theme={null}
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

Die Debattenstruktur ist der Schlüsselmechanismus hier. Sequenzielle Untersuchung leidet unter Verankerung: sobald eine Theorie untersucht wird, ist die nachfolgende Untersuchung zu ihr vorgespannt.

Mit mehreren unabhängigen Ermittlern, die aktiv versuchen, sich gegenseitig zu widerlegen, ist die Theorie, die überlebt, viel wahrscheinlicher die tatsächliche Grundursache.

## Best Practices

### Geben Sie Teammates genug Kontext

Teammates laden Projektkontext automatisch, einschließlich CLAUDE.md, MCP servers und skills, aber sie erben nicht die Gesprächshistorie des Leads. Siehe [Kontext und Kommunikation](#context-and-communication) für Details. Fügen Sie aufgabenspezifische Details in den Spawn-Prompt ein:

```text  theme={null}
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

### Wählen Sie eine angemessene Teamgröße

Es gibt keine harte Grenze für die Anzahl der Teammates, aber praktische Einschränkungen gelten:

* **Token-Kosten skalieren linear**: jeder Teammate hat sein eigenes Kontextfenster und verbraucht Tokens unabhängig. Siehe [Agent-Team-Token-Kosten](/de/costs#agent-team-token-costs) für Details.
* **Koordinationsaufwand nimmt zu**: mehr Teammates bedeutet mehr Kommunikation, Aufgabenkoordination und Konfliktpotenzial
* **Sinkende Erträge**: über einen bestimmten Punkt hinaus beschleunigen zusätzliche Teammates die Arbeit nicht proportional

Beginnen Sie mit 3-5 Teammates für die meisten Workflows. Dies balanciert parallele Arbeit mit verwaltbarer Koordination. Die Beispiele in diesem Leitfaden verwenden 3-5 Teammates, weil dieser Bereich über verschiedene Aufgabentypen hinweg gut funktioniert.

Mit 5-6 [Aufgaben](/de/agent-teams#architecture) pro Teammate bleibt jeder produktiv, ohne übermäßiges Kontextwechsel. Wenn Sie 15 unabhängige Aufgaben haben, sind 3 Teammates ein guter Ausgangspunkt.

Skalieren Sie nur auf, wenn die Arbeit wirklich davon profitiert, dass Teammates gleichzeitig arbeiten. Drei fokussierte Teammates übertreffen oft fünf verstreute.

### Dimensionieren Sie Aufgaben angemessen

* **Zu klein**: Koordinationsaufwand übersteigt den Nutzen
* **Zu groß**: Teammates arbeiten zu lange ohne Check-ins, was das Risiko verschwendeter Anstrengungen erhöht
* **Genau richtig**: in sich geschlossene Einheiten, die ein klares Ergebnis liefern, wie eine Funktion, eine Testdatei oder eine Überprüfung

<Tip>
  Der Lead teilt Arbeit in Aufgaben auf und weist sie Teammates automatisch zu. Wenn er nicht genug Aufgaben erstellt, bitten Sie ihn, die Arbeit in kleinere Stücke aufzuteilen. Mit 5-6 Aufgaben pro Teammate bleibt jeder produktiv und der Lead kann Arbeit neu zuweisen, wenn jemand steckenbleibt.
</Tip>

### Warten Sie, bis Teammates fertig sind

Manchmal beginnt der Lead, Aufgaben selbst zu implementieren, anstatt auf Teammates zu warten. Wenn Sie dies bemerken:

```text  theme={null}
Wait for your teammates to complete their tasks before proceeding
```

### Beginnen Sie mit Recherche und Überprüfung

Wenn Sie neu bei Agent-Teams sind, beginnen Sie mit Aufgaben, die klare Grenzen haben und nicht das Schreiben von Code erfordern: Überprüfung eines PR, Recherche einer Bibliothek oder Untersuchung eines Bugs. Diese Aufgaben zeigen den Wert paralleler Exploration ohne die Koordinationschallenges, die mit paralleler Implementierung einhergehen.

### Vermeiden Sie Dateikonflikte

Zwei Teammates, die dieselbe Datei bearbeiten, führen zu Überschreibungen. Teilen Sie die Arbeit so auf, dass jeder Teammate einen anderen Satz von Dateien besitzt.

### Überwachen und lenken Sie

Überprüfen Sie den Fortschritt der Teammates, leiten Sie Ansätze um, die nicht funktionieren, und synthetisieren Sie Erkenntnisse, wenn sie eintreffen. Ein Team zu lange unbeaufsichtigt laufen zu lassen, erhöht das Risiko verschwendeter Anstrengungen.

## Fehlerbehebung

### Teammates erscheinen nicht

Wenn Teammates nicht erscheinen, nachdem Sie Claude aufgefordert haben, ein Team zu erstellen:

* Im In-Process-Modus können Teammates bereits laufen, sind aber nicht sichtbar. Drücken Sie Shift+Down, um durch aktive Teammates zu wechseln.
* Überprüfen Sie, dass die Aufgabe, die Sie Claude gegeben haben, komplex genug war, um ein Team zu rechtfertigen. Claude entscheidet basierend auf der Aufgabe, ob Teammates erzeugt werden sollen.
* Wenn Sie explizit Split Panes angefordert haben, stellen Sie sicher, dass tmux installiert ist und in Ihrem PATH verfügbar ist:
  ```bash  theme={null}
  which tmux
  ```
* Für iTerm2 überprüfen Sie, dass die `it2` CLI installiert ist und die Python-API in iTerm2-Einstellungen aktiviert ist.

### Zu viele Berechtigungsaufforderungen

Teammate-Berechtigungsanfragen sprudeln zum Lead auf, was zu Reibung führen kann. Genehmigen Sie häufige Operationen in Ihren [Berechtigungseinstellungen](/de/permissions) vor dem Erzeugen von Teammates, um Unterbrechungen zu reduzieren.

### Teammates stoppen bei Fehlern

Teammates können nach Fehlern stoppen, anstatt sich zu erholen. Überprüfen Sie ihre Ausgabe mit Shift+Down im In-Process-Modus oder durch Klicken auf den Pane im Split-Modus, dann entweder:

* Geben Sie ihnen zusätzliche Anweisungen direkt
* Erzeugen Sie einen Ersatz-Teammate, um die Arbeit fortzusetzen

### Lead fährt herunter, bevor die Arbeit erledigt ist

Der Lead kann entscheiden, dass das Team fertig ist, bevor alle Aufgaben tatsächlich abgeschlossen sind. Wenn dies geschieht, teilen Sie ihm mit, dass er weitermachen soll. Sie können dem Lead auch mitteilen, auf Teammates zu warten, um zu beenden, bevor er fortfährt, wenn er anfängt, Arbeit zu erledigen, anstatt zu delegieren.

### Verwaiste tmux-Sitzungen

Wenn eine tmux-Sitzung nach dem Ende des Teams bestehen bleibt, wurde sie möglicherweise nicht vollständig bereinigt. Listen Sie Sitzungen auf und beenden Sie die vom Team erstellte:

```bash  theme={null}
tmux ls
tmux kill-session -t <session-name>
```

## Einschränkungen

Agent-Teams sind experimentell. Aktuelle Einschränkungen, die Sie beachten sollten:

* **Keine Sitzungswiederaufnahme mit In-Process-Teammates**: `/resume` und `/rewind` stellen In-Process-Teammates nicht wieder her. Nach der Wiederaufnahme einer Sitzung kann der Lead versuchen, mit Teammates zu kommunizieren, die nicht mehr existieren. Wenn dies geschieht, teilen Sie dem Lead mit, neue Teammates zu erzeugen.
* **Aufgabenstatus kann verzögert sein**: Teammates markieren Aufgaben manchmal nicht als abgeschlossen, was abhängige Aufgaben blockiert. Wenn eine Aufgabe steckenbleibt, überprüfen Sie, ob die Arbeit tatsächlich erledigt ist, und aktualisieren Sie den Aufgabenstatus manuell oder teilen Sie dem Lead mit, den Teammate zu anstoßen.
* **Abschaltung kann langsam sein**: Teammates beenden ihre aktuelle Anfrage oder ihren Werkzeugaufruf, bevor sie herunterfahren, was Zeit in Anspruch nehmen kann.
* **Ein Team pro Sitzung**: ein Lead kann jeweils nur ein Team verwalten. Bereinigen Sie das aktuelle Team, bevor Sie ein neues starten.
* **Keine verschachtelten Teams**: Teammates können ihre eigenen Teams oder Teammates nicht erzeugen. Nur der Lead kann das Team verwalten.
* **Lead ist fest**: die Sitzung, die das Team erstellt, ist der Lead für seine Lebensdauer. Sie können einen Teammate nicht zum Lead befördern oder die Führung übertragen.
* **Berechtigungen beim Erzeugen gesetzt**: alle Teammates starten mit dem Berechtigungsmodus des Leads. Sie können einzelne Teammate-Modi nach dem Erzeugen ändern, aber Sie können keine Pro-Teammate-Modi zum Zeitpunkt des Erzeugung setzen.
* **Split Panes erfordern tmux oder iTerm2**: der Standard-In-Process-Modus funktioniert in jedem Terminal. Der Split-Pane-Modus wird in VS Code's integriertem Terminal, Windows Terminal oder Ghostty nicht unterstützt.

<Tip>
  **`CLAUDE.md` funktioniert normal**: Teammates lesen `CLAUDE.md`-Dateien aus ihrem Arbeitsverzeichnis. Verwenden Sie dies, um projektspezifische Anleitung für alle Teammates bereitzustellen.
</Tip>

## Nächste Schritte

Erkunden Sie verwandte Ansätze für parallele Arbeit und Delegation:

* **Leichte Delegation**: [subagents](/de/sub-agents) erzeugen Helper-Agenten für Recherche oder Überprüfung innerhalb Ihrer Sitzung, besser für Aufgaben, die keine Inter-Agent-Koordination benötigen
* **Manuelle parallele Sitzungen**: [Git worktrees](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) ermöglichen es Ihnen, mehrere Claude Code-Sitzungen selbst ohne automatisierte Teamkoordination auszuführen
* **Vergleichen Sie Ansätze**: siehe den [Subagent vs Agent-Team](/de/features-overview#compare-similar-features) Vergleich für eine Seite-an-Seite-Aufschlüsselung
