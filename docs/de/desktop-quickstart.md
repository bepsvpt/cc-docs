> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Erste Schritte mit der Desktop-App

> Installieren Sie Claude Code auf dem Desktop und starten Sie Ihre erste Coding-Sitzung

Die Desktop-App bietet Ihnen Claude Code mit einer grafischen Benutzeroberfläche: visuelle Diff-Überprüfung, Live-App-Vorschau, GitHub-PR-Überwachung mit automatischem Merge, parallele Sitzungen mit Git-Worktree-Isolation, geplante Aufgaben und die Möglichkeit, Aufgaben remote auszuführen. Kein Terminal erforderlich.

Diese Seite führt Sie durch die Installation der App und den Start Ihrer ersten Sitzung. Wenn Sie bereits eingerichtet sind, siehe [Claude Code Desktop verwenden](/de/desktop) für die vollständige Referenz.

<Frame>
  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce" className="block dark:hidden" alt="Die Claude Code Desktop-Oberfläche mit der ausgewählten Registerkarte Code, mit einem Eingabefeld, einem Berechtigungsmodus-Selektor auf Berechtigungen erfragen, einem Modellwähler, einem Ordnerwähler und der Option Lokale Umgebung" width="2500" height="1376" data-path="images/desktop-code-tab-light.png" />

  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8" className="hidden dark:block" alt="Die Claude Code Desktop-Oberfläche im dunklen Modus mit der ausgewählten Registerkarte Code, mit einem Eingabefeld, einem Berechtigungsmodus-Selektor auf Berechtigungen erfragen, einem Modellwähler, einem Ordnerwähler und der Option Lokale Umgebung" width="2504" height="1374" data-path="images/desktop-code-tab-dark.png" />
</Frame>

Die Desktop-App hat drei Registerkarten:

* **Chat**: Allgemeine Konversation ohne Dateizugriff, ähnlich wie claude.ai.
* **Cowork**: Ein autonomer Hintergrund-Agent, der an Aufgaben in einer Cloud-VM mit eigener Umgebung arbeitet. Er kann unabhängig arbeiten, während Sie andere Dinge tun.
* **Code**: Ein interaktiver Coding-Assistent mit direktem Zugriff auf Ihre lokalen Dateien. Sie überprüfen und genehmigen jede Änderung in Echtzeit.

Chat und Cowork werden in den [Claude Desktop-Supportartikeln](https://support.claude.com/en/collections/16163169-claude-desktop) behandelt. Diese Seite konzentriert sich auf die Registerkarte **Code**.

<Note>
  Claude Code erfordert ein [Pro-, Max-, Teams- oder Enterprise-Abonnement](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing).
</Note>

## Installieren

<Steps>
  <Step title="App herunterladen">
    Laden Sie Claude für Ihre Plattform herunter.

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Universeller Build für Intel und Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Für x64-Prozessoren
      </Card>
    </CardGroup>

    Für Windows ARM64 [laden Sie hier herunter](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

    Linux wird derzeit nicht unterstützt.
  </Step>

  <Step title="Anmelden">
    Starten Sie Claude aus Ihrem Anwendungsordner (macOS) oder Startmenü (Windows). Melden Sie sich mit Ihrem Anthropic-Konto an.
  </Step>

  <Step title="Öffnen Sie die Registerkarte Code">
    Klicken Sie auf die Registerkarte **Code** oben in der Mitte. Wenn Sie beim Klicken auf „Code" aufgefordert werden, ein Upgrade durchzuführen, müssen Sie zunächst [ein bezahltes Abonnement abschließen](https://claude.com/pricing). Wenn Sie aufgefordert werden, sich online anzumelden, schließen Sie die Anmeldung ab und starten Sie die App neu. Wenn Sie einen 403-Fehler sehen, siehe [Authentifizierungsfehlersuche](/de/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

Die Desktop-App enthält Claude Code. Sie müssen Node.js oder die CLI nicht separat installieren. Um `claude` vom Terminal aus zu verwenden, installieren Sie die CLI separat. Siehe [Erste Schritte mit der CLI](/de/quickstart).

## Starten Sie Ihre erste Sitzung

Wählen Sie mit der geöffneten Registerkarte „Code" ein Projekt aus und geben Sie Claude etwas zu tun.

<Steps>
  <Step title="Wählen Sie eine Umgebung und einen Ordner">
    Wählen Sie **Lokal**, um Claude auf Ihrem Computer mit Ihren Dateien direkt auszuführen. Klicken Sie auf **Ordner auswählen** und wählen Sie Ihr Projektverzeichnis.

    <Tip>
      Beginnen Sie mit einem kleinen Projekt, das Sie gut kennen. Es ist die schnellste Möglichkeit zu sehen, was Claude Code kann. Unter Windows muss [Git](https://git-scm.com/downloads/win) für lokale Sitzungen installiert sein. Die meisten Macs enthalten Git standardmäßig.
    </Tip>

    Sie können auch auswählen:

    * **Remote**: Führen Sie Sitzungen auf der Cloud-Infrastruktur von Anthropic aus, die auch dann fortgesetzt werden, wenn Sie die App schließen. Remote-Sitzungen verwenden die gleiche Infrastruktur wie [Claude Code im Web](/de/claude-code-on-the-web).
    * **SSH**: Verbinden Sie sich über SSH mit einem Remote-Computer (Ihre eigenen Server, Cloud-VMs oder Dev-Container). Claude Code muss auf dem Remote-Computer installiert sein.
  </Step>

  <Step title="Wählen Sie ein Modell">
    Wählen Sie ein Modell aus der Dropdown-Liste neben der Schaltfläche „Senden". Siehe [Modelle](/de/model-config#available-models) für einen Vergleich von Opus, Sonnet und Haiku. Sie können das Modell nach dem Start der Sitzung nicht ändern.
  </Step>

  <Step title="Sagen Sie Claude, was zu tun ist">
    Geben Sie ein, was Claude tun soll:

    * `Find a TODO comment and fix it`
    * `Add tests for the main function`
    * `Create a CLAUDE.md with instructions for this codebase`

    Eine [Sitzung](/de/desktop#work-in-parallel-with-sessions) ist eine Konversation mit Claude über Ihren Code. Jede Sitzung verfolgt ihren eigenen Kontext und ihre Änderungen, sodass Sie an mehreren Aufgaben arbeiten können, ohne dass sie sich gegenseitig beeinflussen.
  </Step>

  <Step title="Überprüfen und akzeptieren Sie Änderungen">
    Standardmäßig startet die Registerkarte „Code" im [Modus „Berechtigungen erfragen"](/de/desktop#choose-a-permission-mode), in dem Claude Änderungen vorschlägt und auf Ihre Genehmigung wartet, bevor er sie anwendet. Sie sehen:

    1. Eine [Diff-Ansicht](/de/desktop#review-changes-with-diff-view), die genau zeigt, was sich in jeder Datei ändern wird
    2. Schaltflächen „Akzeptieren"/„Ablehnen", um jede Änderung zu genehmigen oder abzulehnen
    3. Echtzeit-Updates, während Claude Ihre Anfrage bearbeitet

    Wenn Sie eine Änderung ablehnen, fragt Claude, wie Sie anders vorgehen möchten. Ihre Dateien werden erst geändert, wenn Sie sie akzeptieren.
  </Step>
</Steps>

## Was nun?

Sie haben Ihre erste Bearbeitung vorgenommen. Für die vollständige Referenz zu allem, was Desktop kann, siehe [Claude Code Desktop verwenden](/de/desktop). Hier sind einige Dinge, die Sie als Nächstes versuchen können.

**Unterbrechen und lenken.** Sie können Claude jederzeit unterbrechen. Wenn es den falschen Weg geht, klicken Sie auf die Stoppschaltfläche oder geben Sie Ihre Korrektur ein und drücken Sie **Eingabe**. Claude stoppt, was es tut, und passt sich basierend auf Ihrer Eingabe an. Sie müssen nicht warten, bis es fertig ist, oder von vorne anfangen.

**Geben Sie Claude mehr Kontext.** Geben Sie `@filename` im Eingabefeld ein, um eine bestimmte Datei in die Konversation zu ziehen, fügen Sie Bilder und PDFs mit der Schaltfläche „Anhang" an, oder ziehen Sie Dateien direkt in das Eingabefeld. Je mehr Kontext Claude hat, desto besser sind die Ergebnisse. Siehe [Dateien und Kontext zu Eingaben hinzufügen](/de/desktop#add-files-and-context-to-prompts).

**Verwenden Sie Skills für wiederholbare Aufgaben.** Geben Sie `/` ein oder klicken Sie auf **+** → **Slash commands**, um [integrierte Befehle](/de/commands), [benutzerdefinierte Skills](/de/skills) und Plugin-Skills zu durchsuchen. Skills sind wiederverwendbare Eingaben, die Sie aufrufen können, wenn Sie sie benötigen, wie Code-Review-Checklisten oder Bereitstellungsschritte.

**Überprüfen Sie Änderungen vor dem Commit.** Nachdem Claude Dateien bearbeitet hat, wird ein `+12 -1`-Indikator angezeigt. Klicken Sie darauf, um die [Diff-Ansicht](/de/desktop#review-changes-with-diff-view) zu öffnen, überprüfen Sie Änderungen Datei für Datei und kommentieren Sie bestimmte Zeilen. Claude liest Ihre Kommentare und überarbeitet. Klicken Sie auf **Code überprüfen**, um Claude die Diffs selbst auswerten zu lassen und Inline-Vorschläge zu hinterlassen.

**Passen Sie an, wie viel Kontrolle Sie haben.** Ihr [Berechtigungsmodus](/de/desktop#choose-a-permission-mode) steuert das Gleichgewicht. „Berechtigungen erfragen" (Standard) erfordert Genehmigung vor jeder Bearbeitung. „Auto-Akzeptanz" akzeptiert Dateibearbeitungen automatisch für schnellere Iteration. Der Plan Mode lässt Claude einen Ansatz planen, ohne Dateien zu berühren, was vor einem großen Refactoring nützlich ist.

**Fügen Sie Plugins für mehr Funktionen hinzu.** Klicken Sie auf die Schaltfläche **+** neben dem Eingabefeld und wählen Sie **Plugins**, um [Plugins](/de/desktop#install-plugins) zu durchsuchen und zu installieren, die Skills, Agents, MCP servers und mehr hinzufügen.

**Zeigen Sie eine Vorschau Ihrer App an.** Klicken Sie auf das Dropdown-Menü **Vorschau**, um Ihren Dev-Server direkt im Desktop auszuführen. Claude kann die laufende App anzeigen, Endpunkte testen, Protokolle überprüfen und auf das, was es sieht, iterieren. Siehe [Zeigen Sie eine Vorschau Ihrer App an](/de/desktop#preview-your-app).

**Verfolgen Sie Ihren Pull Request.** Nachdem Sie einen PR geöffnet haben, überwacht Claude Code die CI-Prüfungsergebnisse und kann Fehler automatisch beheben oder den PR zusammenführen, sobald alle Prüfungen bestanden sind. Siehe [Überwachen Sie den Pull-Request-Status](/de/desktop#monitor-pull-request-status).

**Setzen Sie Claude auf einen Zeitplan.** Richten Sie [geplante Aufgaben](/de/desktop#schedule-recurring-tasks) ein, um Claude automatisch regelmäßig auszuführen: eine tägliche Code-Überprüfung jeden Morgen, eine wöchentliche Abhängigkeitsprüfung oder eine Zusammenfassung, die von Ihren verbundenen Tools abruft.

**Skalieren Sie auf, wenn Sie bereit sind.** Öffnen Sie [parallele Sitzungen](/de/desktop#work-in-parallel-with-sessions) aus der Seitenleiste, um an mehreren Aufgaben gleichzeitig zu arbeiten, jede in ihrem eigenen Git-Worktree. Senden Sie [langfristige Arbeit in die Cloud](/de/desktop#run-long-running-tasks-remotely), damit sie auch dann fortgesetzt wird, wenn Sie die App schließen, oder [setzen Sie eine Sitzung im Web oder in Ihrer IDE fort](/de/desktop#continue-in-another-surface), wenn eine Aufgabe länger als erwartet dauert. [Verbinden Sie externe Tools](/de/desktop#extend-claude-code) wie GitHub, Slack und Linear, um Ihren Workflow zusammenzubringen.

## Kommen Sie von der CLI?

Desktop führt die gleiche Engine wie die CLI mit einer grafischen Benutzeroberfläche aus. Sie können beide gleichzeitig auf dem gleichen Projekt ausführen, und sie teilen die Konfiguration (CLAUDE.md-Dateien, MCP servers, hooks, Skills und Einstellungen). Für einen vollständigen Vergleich von Funktionen, Flag-Äquivalenten und was in Desktop nicht verfügbar ist, siehe [CLI-Vergleich](/de/desktop#coming-from-the-cli).

## Was kommt als Nächstes

* [Claude Code Desktop verwenden](/de/desktop): Berechtigungsmodi, parallele Sitzungen, Diff-Ansicht, Konnektoren und Enterprise-Konfiguration
* [Fehlerbehebung](/de/desktop#troubleshooting): Lösungen für häufige Fehler und Setup-Probleme
* [Best Practices](/de/best-practices): Tipps zum Schreiben effektiver Eingaben und zum Herausholen des Besten aus Claude Code
* [Häufige Workflows](/de/common-workflows): Tutorials zum Debuggen, Refactoring, Testen und mehr
