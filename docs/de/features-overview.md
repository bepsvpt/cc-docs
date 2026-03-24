> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code erweitern

> Verstehen Sie, wann Sie CLAUDE.md, Skills, Subagents, Hooks, MCP und Plugins verwenden.

Claude Code kombiniert ein Modell, das über Ihren Code nachdenkt, mit [integrierten Tools](/de/how-claude-code-works#tools) für Dateivorgänge, Suche, Ausführung und Webzugriff. Die integrierten Tools decken die meisten Codierungsaufgaben ab. Dieses Handbuch behandelt die Erweiterungsebene: Funktionen, die Sie hinzufügen, um anzupassen, was Claude weiß, es mit externen Diensten zu verbinden und Workflows zu automatisieren.

<Note>
  Informationen zur Funktionsweise der Kern-Agentenschleife finden Sie unter [How Claude Code works](/de/how-claude-code-works).
</Note>

**Neu bei Claude Code?** Beginnen Sie mit [CLAUDE.md](/de/memory) für Projektkonventionen. Fügen Sie andere Erweiterungen nach Bedarf hinzu.

## Übersicht

Erweiterungen verbinden sich mit verschiedenen Teilen der Agentenschleife:

* **[CLAUDE.md](/de/memory)** fügt persistenten Kontext hinzu, den Claude in jeder Sitzung sieht
* **[Skills](/de/skills)** fügen wiederverwendbares Wissen und aufrufbare Workflows hinzu
* **[MCP](/de/mcp)** verbindet Claude mit externen Diensten und Tools
* **[Subagents](/de/sub-agents)** führen ihre eigenen Schleifen in isoliertem Kontext aus und geben Zusammenfassungen zurück
* **[Agent teams](/de/agent-teams)** koordinieren mehrere unabhängige Sitzungen mit gemeinsamen Aufgaben und Peer-to-Peer-Messaging
* **[Hooks](/de/hooks)** laufen vollständig außerhalb der Schleife als deterministische Skripte
* **[Plugins](/de/plugins)** und **[Marketplaces](/de/plugin-marketplaces)** verpacken und verteilen diese Funktionen

[Skills](/de/skills) sind die flexibelste Erweiterung. Ein Skill ist eine Markdown-Datei, die Wissen, Workflows oder Anweisungen enthält. Sie können Skills mit einem Befehl wie `/deploy` aufrufen, oder Claude kann sie automatisch laden, wenn sie relevant sind. Skills können in Ihrer aktuellen Konversation oder in einem isolierten Kontext über Subagents ausgeführt werden.

## Funktionen an Ihr Ziel anpassen

Funktionen reichen von immer aktivem Kontext, den Claude in jeder Sitzung sieht, bis zu On-Demand-Funktionen, die Sie oder Claude aufrufen können, bis zu Hintergrundautomatisierung, die bei bestimmten Ereignissen ausgeführt wird. Die folgende Tabelle zeigt, was verfügbar ist und wann jede Funktion sinnvoll ist.

| Funktion                           | Was sie tut                                                               | Wann man sie verwendet                                                                   | Beispiel                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **CLAUDE.md**                      | Persistenter Kontext, der in jeder Konversation geladen wird              | Projektkonventionen, „immer X tun"-Regeln                                                | „Verwenden Sie pnpm, nicht npm. Führen Sie Tests vor dem Commit aus."                    |
| **Skill**                          | Anweisungen, Wissen und Workflows, die Claude verwenden kann              | Wiederverwendbarer Inhalt, Referenzdokumente, wiederholbare Aufgaben                     | `/deploy` führt Ihre Bereitstellungs-Checkliste aus; API-Docs-Skill mit Endpunkt-Mustern |
| **Subagent**                       | Isolierter Ausführungskontext, der zusammengefasste Ergebnisse zurückgibt | Kontextisolation, parallele Aufgaben, spezialisierte Worker                              | Recherche-Aufgabe, die viele Dateien liest, aber nur wichtige Erkenntnisse zurückgibt    |
| **[Agent teams](/de/agent-teams)** | Koordinieren Sie mehrere unabhängige Claude Code-Sitzungen                | Parallele Recherche, neue Funktionsentwicklung, Debugging mit konkurrierenden Hypothesen | Spawnen Sie Reviewer, um Sicherheit, Leistung und Tests gleichzeitig zu überprüfen       |
| **MCP**                            | Verbindung zu externen Diensten                                           | Externe Daten oder Aktionen                                                              | Abfrage Ihrer Datenbank, Posten auf Slack, Steuerung eines Browsers                      |
| **Hook**                           | Deterministisches Skript, das bei Ereignissen ausgeführt wird             | Vorhersagbare Automatisierung, kein LLM beteiligt                                        | Führen Sie ESLint nach jeder Dateibearbeitung aus                                        |

**[Plugins](/de/plugins)** sind die Verpackungsebene. Ein Plugin bündelt Skills, Hooks, Subagents und MCP-Server in eine einzelne installierbare Einheit. Plugin-Skills sind namensgebunden (wie `/my-plugin:review`), sodass mehrere Plugins nebeneinander existieren können. Verwenden Sie Plugins, wenn Sie dasselbe Setup über mehrere Repositories hinweg wiederverwenden möchten oder es über einen **[Marketplace](/de/plugin-marketplaces)** an andere verteilen möchten.

### Ähnliche Funktionen vergleichen

Einige Funktionen können ähnlich wirken. Hier erfahren Sie, wie Sie sie unterscheiden.

<Tabs>
  <Tab title="Skill vs Subagent">
    Skills und Subagents lösen unterschiedliche Probleme:

    * **Skills** sind wiederverwendbare Inhalte, die Sie in jeden Kontext laden können
    * **Subagents** sind isolierte Worker, die separat von Ihrer Hauptkonversation ausgeführt werden

    | Aspekt            | Skill                                                | Subagent                                                                                 |
    | ----------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
    | **Was es ist**    | Wiederverwendbare Anweisungen, Wissen oder Workflows | Isolierter Worker mit eigenem Kontext                                                    |
    | **Hauptvorteil**  | Inhalte über Kontexte hinweg teilen                  | Kontextisolation. Die Arbeit erfolgt separat, nur die Zusammenfassung wird zurückgegeben |
    | **Am besten für** | Referenzmaterial, aufrufbare Workflows               | Aufgaben, die viele Dateien lesen, parallele Arbeit, spezialisierte Worker               |

    **Skills können Referenz oder Aktion sein.** Referenz-Skills bieten Wissen, das Claude während Ihrer Sitzung nutzt (wie Ihr API-Stilhandbuch). Action-Skills sagen Claude, etwas Bestimmtes zu tun (wie `/deploy`, das Ihren Bereitstellungs-Workflow ausführt).

    **Verwenden Sie einen Subagent**, wenn Sie Kontextisolation benötigen oder wenn Ihr Kontextfenster voll wird. Der Subagent könnte Dutzende von Dateien lesen oder umfangreiche Suchen durchführen, aber Ihre Hauptkonversation erhält nur eine Zusammenfassung. Da die Arbeit des Subagent Ihren Hauptkontext nicht verbraucht, ist dies auch nützlich, wenn Sie nicht möchten, dass die Zwischenarbeit sichtbar bleibt. Benutzerdefinierte Subagents können ihre eigenen Anweisungen haben und Skills vorladen.

    **Sie können sich kombinieren.** Ein Subagent kann spezifische Skills vorladen (`skills:`-Feld). Ein Skill kann in isoliertem Kontext mit `context: fork` ausgeführt werden. Weitere Informationen finden Sie unter [Skills](/de/skills).
  </Tab>

  <Tab title="CLAUDE.md vs Skill">
    Beide speichern Anweisungen, aber sie werden unterschiedlich geladen und dienen unterschiedlichen Zwecken.

    | Aspekt                      | CLAUDE.md                 | Skill                                  |
    | --------------------------- | ------------------------- | -------------------------------------- |
    | **Lädt**                    | Jede Sitzung, automatisch | On Demand                              |
    | **Kann Dateien enthalten**  | Ja, mit `@path`-Importen  | Ja, mit `@path`-Importen               |
    | **Kann Workflows auslösen** | Nein                      | Ja, mit `/<name>`                      |
    | **Am besten für**           | „Immer X tun"-Regeln      | Referenzmaterial, aufrufbare Workflows |

    **Fügen Sie es in CLAUDE.md ein**, wenn Claude es immer wissen sollte: Codierungskonventionen, Build-Befehle, Projektstruktur, „niemals X tun"-Regeln.

    **Fügen Sie es in einen Skill ein**, wenn es Referenzmaterial ist, das Claude manchmal benötigt (API-Docs, Stilhandbücher) oder ein Workflow, den Sie mit `/<name>` auslösen (bereitstellen, überprüfen, freigeben).

    **Faustregel:** Halten Sie CLAUDE.md unter 200 Zeilen. Wenn es wächst, verschieben Sie Referenzinhalte zu Skills oder teilen Sie sie in [`.claude/rules/`](/de/memory#organize-rules-with-clauderules)-Dateien auf.
  </Tab>

  <Tab title="CLAUDE.md vs Rules vs Skills">
    Alle drei speichern Anweisungen, aber sie werden unterschiedlich geladen:

    | Aspekt            | CLAUDE.md                          | `.claude/rules/`                                                | Skill                                     |
    | ----------------- | ---------------------------------- | --------------------------------------------------------------- | ----------------------------------------- |
    | **Lädt**          | Jede Sitzung                       | Jede Sitzung oder wenn übereinstimmende Dateien geöffnet werden | On Demand, wenn aufgerufen oder relevant  |
    | **Umfang**        | Ganzes Projekt                     | Kann auf Dateipfade begrenzt werden                             | Aufgabenspezifisch                        |
    | **Am besten für** | Kernkonventionen und Build-Befehle | Sprachspezifische oder verzeichnisspezifische Richtlinien       | Referenzmaterial, wiederholbare Workflows |

    **Verwenden Sie CLAUDE.md** für Anweisungen, die jede Sitzung benötigt: Build-Befehle, Test-Konventionen, Projektarchitektur.

    **Verwenden Sie Regeln**, um CLAUDE.md fokussiert zu halten. Regeln mit [`paths`-Frontmatter](/de/memory#path-specific-rules) werden nur geladen, wenn Claude mit übereinstimmenden Dateien arbeitet, was Kontext spart.

    **Verwenden Sie Skills** für Inhalte, die Claude nur manchmal benötigt, wie API-Dokumentation oder eine Bereitstellungs-Checkliste, die Sie mit `/<name>` auslösen.
  </Tab>

  <Tab title="Subagent vs Agent team">
    Beide parallelisieren Arbeit, aber sie sind architektonisch unterschiedlich:

    * **Subagents** laufen in Ihrer Sitzung und berichten Ergebnisse an Ihren Hauptkontext zurück
    * **Agent teams** sind unabhängige Claude Code-Sitzungen, die miteinander kommunizieren

    | Aspekt            | Subagent                                                      | Agent team                                                   |
    | ----------------- | ------------------------------------------------------------- | ------------------------------------------------------------ |
    | **Kontext**       | Eigenes Kontextfenster; Ergebnisse kehren zum Aufrufer zurück | Eigenes Kontextfenster; vollständig unabhängig               |
    | **Kommunikation** | Berichtet Ergebnisse nur an den Hauptagent zurück             | Teammates senden sich gegenseitig direkt Nachrichten         |
    | **Koordination**  | Hauptagent verwaltet alle Arbeiten                            | Gemeinsame Aufgabenliste mit Selbstkoordination              |
    | **Am besten für** | Fokussierte Aufgaben, bei denen nur das Ergebnis zählt        | Komplexe Arbeit, die Diskussion und Zusammenarbeit erfordert |
    | **Token-Kosten**  | Niedriger: Ergebnisse werden zum Hauptkontext zusammengefasst | Höher: jeder Teammate ist eine separate Claude-Instanz       |

    **Verwenden Sie einen Subagent**, wenn Sie einen schnellen, fokussierten Worker benötigen: eine Frage recherchieren, eine Behauptung überprüfen, eine Datei überprüfen. Der Subagent erledigt die Arbeit und gibt eine Zusammenfassung zurück. Ihre Hauptkonversation bleibt sauber.

    **Verwenden Sie ein Agent Team**, wenn Teammates Erkenntnisse teilen, sich gegenseitig in Frage stellen und unabhängig koordinieren müssen. Agent Teams sind am besten für Recherche mit konkurrierenden Hypothesen, parallele Code-Überprüfung und neue Funktionsentwicklung, bei der jeder Teammate ein separates Stück besitzt.

    **Übergangspunkt:** Wenn Sie parallele Subagents ausführen, aber auf Kontextgrenzen stoßen, oder wenn Ihre Subagents miteinander kommunizieren müssen, sind Agent Teams der natürliche nächste Schritt.

    <Note>
      Agent Teams sind experimentell und standardmäßig deaktiviert. Weitere Informationen zu Setup und aktuellen Einschränkungen finden Sie unter [agent teams](/de/agent-teams).
    </Note>
  </Tab>

  <Tab title="MCP vs Skill">
    MCP verbindet Claude mit externen Diensten. Skills erweitern das Wissen von Claude, einschließlich der effektiven Verwendung dieser Dienste.

    | Aspekt         | MCP                                                     | Skill                                                              |
    | -------------- | ------------------------------------------------------- | ------------------------------------------------------------------ |
    | **Was es ist** | Protokoll zur Verbindung mit externen Diensten          | Wissen, Workflows und Referenzmaterial                             |
    | **Bietet**     | Tools und Datenzugriff                                  | Wissen, Workflows, Referenzmaterial                                |
    | **Beispiele**  | Slack-Integration, Datenbankabfragen, Browser-Steuerung | Code-Review-Checkliste, Bereitstellungs-Workflow, API-Stilhandbuch |

    Diese lösen unterschiedliche Probleme und funktionieren gut zusammen:

    **MCP** gibt Claude die Möglichkeit, mit externen Systemen zu interagieren. Ohne MCP kann Claude Ihre Datenbank nicht abfragen oder auf Slack posten.

    **Skills** geben Claude Wissen darüber, wie diese Tools effektiv verwendet werden, plus Workflows, die Sie mit `/<name>` auslösen können. Ein Skill könnte Ihr Team-Datenbankschema und Abfragemuster enthalten, oder einen `/post-to-slack`-Workflow mit Ihren Team-Nachrichtenformatierungsregeln.

    Beispiel: Ein MCP-Server verbindet Claude mit Ihrer Datenbank. Ein Skill lehrt Claude Ihr Datenmodell, häufige Abfragemuster und welche Tabellen für verschiedene Aufgaben verwendet werden.
  </Tab>
</Tabs>

### Verstehen Sie, wie Funktionen sich schichten

Funktionen können auf mehreren Ebenen definiert werden: benutzerübergreifend, pro Projekt, über Plugins oder durch verwaltete Richtlinien. Sie können auch CLAUDE.md-Dateien in Unterverzeichnissen verschachteln oder Skills in bestimmten Paketen eines Monorepos platzieren. Wenn dieselbe Funktion auf mehreren Ebenen vorhanden ist, so schichten sie sich:

* **CLAUDE.md-Dateien** sind additiv: alle Ebenen tragen gleichzeitig Inhalte zu Claudes Kontext bei. Dateien aus Ihrem Arbeitsverzeichnis und darüber werden beim Start geladen; Unterverzeichnisse werden geladen, wenn Sie darin arbeiten. Wenn Anweisungen in Konflikt geraten, nutzt Claude sein Urteilsvermögen, um sie zu reconciliieren, wobei spezifischere Anweisungen typischerweise Vorrang haben. Siehe [wie CLAUDE.md-Dateien geladen werden](/de/memory#how-claudemd-files-load).
* **Skills und Subagents** überschreiben nach Name: wenn derselbe Name auf mehreren Ebenen vorhanden ist, gewinnt eine Definition basierend auf Priorität (verwaltet > Benutzer > Projekt für Skills; verwaltet > CLI-Flag > Projekt > Benutzer > Plugin für Subagents). Plugin-Skills sind [namensgebunden](/de/plugins#add-skills-to-your-plugin), um Konflikte zu vermeiden. Siehe [Skill-Erkennung](/de/skills#where-skills-live) und [Subagent-Umfang](/de/sub-agents#choose-the-subagent-scope).
* **MCP-Server** überschreiben nach Name: lokal > Projekt > Benutzer. Siehe [MCP-Umfang](/de/mcp#scope-hierarchy-and-precedence).
* **Hooks** zusammenführen: alle registrierten Hooks werden für ihre übereinstimmenden Ereignisse unabhängig von der Quelle ausgelöst. Siehe [Hooks](/de/hooks).

### Funktionen kombinieren

Jede Erweiterung löst ein anderes Problem: CLAUDE.md behandelt immer aktivem Kontext, Skills behandeln On-Demand-Wissen und Workflows, MCP behandelt externe Verbindungen, Subagents behandeln Isolation und Hooks behandeln Automatisierung. Echte Setups kombinieren sie basierend auf Ihrem Workflow.

Beispielsweise könnten Sie CLAUDE.md für Projektkonventionen, einen Skill für Ihren Bereitstellungs-Workflow, MCP zur Verbindung mit Ihrer Datenbank und einen Hook zum Ausführen von Linting nach jeder Bearbeitung verwenden. Jede Funktion behandelt das, wofür sie am besten geeignet ist.

| Muster                 | Wie es funktioniert                                                                             | Beispiel                                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Skill + MCP**        | MCP bietet die Verbindung; ein Skill lehrt Claude, sie gut zu nutzen                            | MCP verbindet sich mit Ihrer Datenbank, ein Skill dokumentiert Ihr Schema und Abfragemuster               |
| **Skill + Subagent**   | Ein Skill spawnt Subagents für parallele Arbeit                                                 | `/audit`-Skill startet Sicherheits-, Leistungs- und Style-Subagents, die in isoliertem Kontext arbeiten   |
| **CLAUDE.md + Skills** | CLAUDE.md hält immer aktivem Regeln; Skills halten Referenzmaterial, das On Demand geladen wird | CLAUDE.md sagt 'folgen Sie unseren API-Konventionen", ein Skill enthält das vollständige API-Stilhandbuch |
| **Hook + MCP**         | Ein Hook löst externe Aktionen über MCP aus                                                     | Post-Edit-Hook sendet eine Slack-Benachrichtigung, wenn Claude kritische Dateien ändert                   |

## Verstehen Sie Kontextkosten

Jede Funktion, die Sie hinzufügen, verbraucht etwas von Claudes Kontext. Zu viel kann Ihr Kontextfenster füllen, aber es kann auch Rauschen hinzufügen, das Claude weniger effektiv macht; Skills werden möglicherweise nicht korrekt ausgelöst, oder Claude kann Ihre Konventionen aus den Augen verlieren. Das Verständnis dieser Kompromisse hilft Ihnen, ein effektives Setup zu erstellen.

### Kontextkosten nach Funktion

Jede Funktion hat eine andere Ladestrategie und Kontextkosten:

| Funktion       | Wann sie lädt                  | Was lädt                                                       | Kontextkosten                                            |
| -------------- | ------------------------------ | -------------------------------------------------------------- | -------------------------------------------------------- |
| **CLAUDE.md**  | Sitzungsstart                  | Vollständiger Inhalt                                           | Jede Anfrage                                             |
| **Skills**     | Sitzungsstart + wenn verwendet | Beschreibungen beim Start, vollständiger Inhalt bei Verwendung | Niedrig (Beschreibungen jede Anfrage)\*                  |
| **MCP-Server** | Sitzungsstart                  | Alle Tool-Definitionen und Schemas                             | Jede Anfrage                                             |
| **Subagents**  | Wenn gespawnt                  | Frischer Kontext mit angegebenen Skills                        | Isoliert von Hauptsitzung                                |
| **Hooks**      | Bei Auslösung                  | Nichts (läuft extern)                                          | Null, es sei denn, Hook gibt zusätzlichen Kontext zurück |

\*Standardmäßig werden Skill-Beschreibungen beim Sitzungsstart geladen, damit Claude entscheiden kann, wann sie verwendet werden. Setzen Sie `disable-model-invocation: true` in das Frontmatter eines Skills, um es vollständig vor Claude zu verbergen, bis Sie es manuell aufrufen. Dies reduziert die Kontextkosten auf Null für Skills, die Sie nur selbst auslösen.

### Verstehen Sie, wie Funktionen geladen werden

Jede Funktion wird an verschiedenen Punkten in Ihrer Sitzung geladen. Die folgenden Registerkarten erklären, wann jede geladen wird und was in den Kontext geht.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/context-loading.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=729b5b634ba831d1d64772c6c9485b30" alt="Kontextladung: CLAUDE.md und MCP werden beim Sitzungsstart geladen und bleiben in jeder Anfrage. Skills laden Beschreibungen beim Start, vollständigen Inhalt bei Aufruf. Subagents erhalten isolierten Kontext. Hooks laufen extern." width="720" height="410" data-path="images/context-loading.svg" />

<Tabs>
  <Tab title="CLAUDE.md">
    **Wann:** Sitzungsstart

    **Was lädt:** Vollständiger Inhalt aller CLAUDE.md-Dateien (verwaltet, Benutzer und Projektebenen).

    **Vererbung:** Claude liest CLAUDE.md-Dateien aus Ihrem Arbeitsverzeichnis bis zur Wurzel und entdeckt verschachtelte in Unterverzeichnissen, wenn es auf diese Dateien zugreift. Weitere Informationen finden Sie unter [How CLAUDE.md files load](/de/memory#how-claudemd-files-load).

    <Tip>Halten Sie CLAUDE.md unter \~500 Zeilen. Verschieben Sie Referenzmaterial zu Skills, die On-Demand geladen werden.</Tip>
  </Tab>

  <Tab title="Skills">
    Skills sind zusätzliche Funktionen in Claudes Toolkit. Sie können Referenzmaterial sein (wie ein API-Stilhandbuch) oder aufrufbare Workflows, die Sie mit `/<name>` auslösen (wie `/deploy`). Claude Code wird mit [gebündelten Skills](/de/skills#bundled-skills) wie `/simplify`, `/batch` und `/debug` ausgeliefert, die sofort funktionieren. Sie können auch Ihre eigenen erstellen. Claude verwendet Skills, wenn angemessen, oder Sie können einen direkt aufrufen.

    **Wann:** Hängt von der Konfiguration des Skills ab. Standardmäßig werden Beschreibungen beim Sitzungsstart geladen und vollständiger Inhalt bei Verwendung. Für nur-Benutzer-Skills (`disable-model-invocation: true`) wird nichts geladen, bis Sie sie aufrufen.

    **Was lädt:** Für modell-aufrufbare Skills sieht Claude Namen und Beschreibungen in jeder Anfrage. Wenn Sie einen Skill mit `/<name>` aufrufen oder Claude ihn automatisch lädt, wird der vollständige Inhalt in Ihre Konversation geladen.

    **Wie Claude Skills wählt:** Claude gleicht Ihre Aufgabe gegen Skill-Beschreibungen ab, um zu entscheiden, welche relevant sind. Wenn Beschreibungen vage oder überlappend sind, kann Claude den falschen Skill laden oder einen verpassen, der helfen würde. Um Claude zu sagen, einen bestimmten Skill zu verwenden, rufen Sie ihn mit `/<name>` auf. Skills mit `disable-model-invocation: true` sind für Claude unsichtbar, bis Sie sie aufrufen.

    **Kontextkosten:** Niedrig bis verwendet. Nur-Benutzer-Skills haben Null-Kosten bis aufgerufen.

    **In Subagents:** Skills funktionieren in Subagents anders. Anstelle von On-Demand-Laden werden Skills, die an einen Subagent übergeben werden, vollständig in seinen Kontext beim Start vorgeladen. Subagents erben Skills nicht von der Hauptsitzung; Sie müssen sie explizit angeben.

    <Tip>Verwenden Sie `disable-model-invocation: true` für Skills mit Nebenwirkungen. Dies spart Kontext und stellt sicher, dass nur Sie sie auslösen.</Tip>
  </Tab>

  <Tab title="MCP-Server">
    **Wann:** Sitzungsstart.

    **Was lädt:** Alle Tool-Definitionen und JSON-Schemas von verbundenen Servern.

    **Kontextkosten:** [Tool-Suche](/de/mcp#scale-with-mcp-tool-search) (standardmäßig aktiviert) lädt MCP-Tools bis zu 10% des Kontexts und verschiebt den Rest bis zur Notwendigkeit.

    **Zuverlässigkeitshinweis:** MCP-Verbindungen können während einer Sitzung stillschweigend fehlschlagen. Wenn ein Server die Verbindung trennt, verschwinden seine Tools ohne Warnung. Claude kann versuchen, ein Tool zu verwenden, das nicht mehr vorhanden ist. Wenn Sie bemerken, dass Claude ein MCP-Tool nicht verwenden kann, auf das es zuvor zugreifen konnte, überprüfen Sie die Verbindung mit `/mcp`.

    <Tip>Führen Sie `/mcp` aus, um Token-Kosten pro Server zu sehen. Trennen Sie Server, die Sie nicht aktiv verwenden.</Tip>
  </Tab>

  <Tab title="Subagents">
    **Wann:** On Demand, wenn Sie oder Claude einen für eine Aufgabe spawnt.

    **Was lädt:** Frischer, isolierter Kontext, der Folgendes enthält:

    * Der System-Prompt (geteilt mit Parent für Cache-Effizienz)
    * Vollständiger Inhalt von Skills, die im `skills:`-Feld des Agenten aufgelistet sind
    * CLAUDE.md und Git-Status (geerbt vom Parent)
    * Welcher Kontext auch immer der Lead-Agent im Prompt übergibt

    **Kontextkosten:** Isoliert von Hauptsitzung. Subagents erben Ihre Konversationshistorie oder aufgerufenen Skills nicht.

    <Tip>Verwenden Sie Subagents für Arbeit, die Ihren vollständigen Konversationskontext nicht benötigt. Ihre Isolation verhindert, dass Ihre Hauptsitzung aufgebläht wird.</Tip>
  </Tab>

  <Tab title="Hooks">
    **Wann:** Bei Auslösung. Hooks werden bei bestimmten Lebenszyklusereignissen ausgelöst, wie Tool-Ausführung, Sitzungsgrenzen, Prompt-Einreichung, Berechtigungsanfragen und Komprimierung. Siehe [Hooks](/de/hooks) für die vollständige Liste.

    **Was lädt:** Standardmäßig nichts. Hooks laufen als externe Skripte.

    **Kontextkosten:** Null, es sei denn, der Hook gibt Ausgabe zurück, die als Nachrichten zu Ihrer Konversation hinzugefügt wird.

    <Tip>Hooks sind ideal für Nebenwirkungen (Linting, Logging), die Claudes Kontext nicht beeinflussen müssen.</Tip>
  </Tab>
</Tabs>

## Weitere Informationen

Jede Funktion hat ihr eigenes Handbuch mit Setup-Anweisungen, Beispielen und Konfigurationsoptionen.

<CardGroup cols={2}>
  <Card title="CLAUDE.md" icon="file-lines" href="/de/memory">
    Speichern Sie Projektkontext, Konventionen und Anweisungen
  </Card>

  <Card title="Skills" icon="brain" href="/de/skills">
    Geben Sie Claude Fachkompetenz und wiederverwendbare Workflows
  </Card>

  <Card title="Subagents" icon="users" href="/de/sub-agents">
    Lagern Sie Arbeit in isoliertem Kontext aus
  </Card>

  <Card title="Agent teams" icon="network" href="/de/agent-teams">
    Koordinieren Sie mehrere Sitzungen, die parallel arbeiten
  </Card>

  <Card title="MCP" icon="plug" href="/de/mcp">
    Verbinden Sie Claude mit externen Diensten
  </Card>

  <Card title="Hooks" icon="bolt" href="/de/hooks-guide">
    Automatisieren Sie Workflows mit Hooks
  </Card>

  <Card title="Plugins" icon="puzzle-piece" href="/de/plugins">
    Bündeln und teilen Sie Feature-Sets
  </Card>

  <Card title="Marketplaces" icon="store" href="/de/plugin-marketplaces">
    Hosten und verteilen Sie Plugin-Sammlungen
  </Card>
</CardGroup>
