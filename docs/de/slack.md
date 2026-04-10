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

# Claude Code in Slack

> Delegieren Sie Codierungsaufgaben direkt aus Ihrem Slack-Arbeitsbereich

Claude Code in Slack bringt die Leistung von Claude Code direkt in Ihren Slack-Arbeitsbereich. Wenn Sie `@Claude` mit einer Codierungsaufgabe erwähnen, erkennt Claude automatisch die Absicht und erstellt eine Claude Code-Sitzung im Web, sodass Sie Entwicklungsarbeiten delegieren können, ohne Ihre Team-Gespräche zu verlassen.

Diese Integration basiert auf der bestehenden Claude for Slack-App, fügt aber intelligentes Routing zu Claude Code im Web für codierungsbezogene Anfragen hinzu.

## Anwendungsfälle

* **Fehleruntersuchung und -behebung**: Bitten Sie Claude, Fehler zu untersuchen und zu beheben, sobald sie in Slack-Kanälen gemeldet werden.
* **Schnelle Code-Reviews und Änderungen**: Lassen Sie Claude kleine Funktionen implementieren oder Code basierend auf Team-Feedback umgestalten.
* **Kollaboratives Debugging**: Wenn Team-Diskussionen wichtigen Kontext bieten (z. B. Fehlerreproduzierungen oder Benutzerberichte), kann Claude diese Informationen nutzen, um seinen Debugging-Ansatz zu informieren.
* **Parallele Aufgabenausführung**: Starten Sie Codierungsaufgaben in Slack, während Sie andere Arbeiten fortsetzen, und erhalten Sie Benachrichtigungen nach Abschluss.

## Voraussetzungen

Bevor Sie Claude Code in Slack verwenden, stellen Sie sicher, dass Sie über Folgendes verfügen:

| Anforderung             | Details                                                                              |
| :---------------------- | :----------------------------------------------------------------------------------- |
| Claude Plan             | Pro, Max, Team oder Enterprise mit Claude Code-Zugriff (Premium-Plätze)              |
| Claude Code im Web      | Der Zugriff auf [Claude Code im Web](/de/claude-code-on-the-web) muss aktiviert sein |
| GitHub-Konto            | Mit Claude Code im Web verbunden mit mindestens einem authentifizierten Repository   |
| Slack-Authentifizierung | Ihr Slack-Konto ist über die Claude-App mit Ihrem Claude-Konto verknüpft             |

## Einrichten von Claude Code in Slack

<Steps>
  <Step title="Installieren Sie die Claude-App in Slack">
    Ein Workspace-Administrator muss die Claude-App aus dem Slack App Marketplace installieren. Besuchen Sie den [Slack App Marketplace](https://slack.com/marketplace/A08SF47R6P4) und klicken Sie auf „Zu Slack hinzufügen", um den Installationsprozess zu starten.
  </Step>

  <Step title="Verbinden Sie Ihr Claude-Konto">
    Nach der Installation der App authentifizieren Sie Ihr individuelles Claude-Konto:

    1. Öffnen Sie die Claude-App in Slack, indem Sie auf „Claude" in Ihrem Apps-Bereich klicken
    2. Navigieren Sie zur Registerkarte „App Home"
    3. Klicken Sie auf „Verbinden", um Ihr Slack-Konto mit Ihrem Claude-Konto zu verknüpfen
    4. Schließen Sie den Authentifizierungsfluss in Ihrem Browser ab
  </Step>

  <Step title="Konfigurieren Sie Claude Code im Web">
    Stellen Sie sicher, dass Ihr Claude Code im Web ordnungsgemäß konfiguriert ist:

    * Besuchen Sie [claude.ai/code](https://claude.ai/code) und melden Sie sich mit dem gleichen Konto an, das Sie mit Slack verbunden haben
    * Verbinden Sie Ihr GitHub-Konto, falls noch nicht geschehen
    * Authentifizieren Sie mindestens ein Repository, mit dem Claude arbeiten soll
  </Step>

  <Step title="Wählen Sie Ihren Routing-Modus">
    Nach dem Verbinden Ihrer Konten konfigurieren Sie, wie Claude Ihre Nachrichten in Slack verarbeitet. Navigieren Sie zur Claude App Home in Slack, um die Einstellung **Routing Mode** zu finden.

    | Modus           | Verhalten                                                                                                                                                                                                                                                                        |
    | :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | **Nur Code**    | Claude leitet alle @mentions zu Claude Code-Sitzungen weiter. Am besten für Teams, die Claude in Slack ausschließlich für Entwicklungsaufgaben verwenden.                                                                                                                        |
    | **Code + Chat** | Claude analysiert jede Nachricht und leitet intelligent zwischen Claude Code (für Codierungsaufgaben) und Claude Chat (für Schreiben, Analyse und allgemeine Fragen) weiter. Am besten für Teams, die einen einzigen @Claude-Einstiegspunkt für alle Arten von Arbeiten möchten. |

    <Note>
      Im Code + Chat-Modus können Sie, wenn Claude eine Nachricht zu Chat leitet, aber Sie wollten eine Codierungssitzung, auf „Als Code erneut versuchen" klicken, um stattdessen eine Claude Code-Sitzung zu erstellen. Wenn es zu Code weitergeleitet wird, aber Sie wollten eine Chat-Sitzung, können Sie diese Option in diesem Thread wählen.
    </Note>
  </Step>
</Steps>

## Wie es funktioniert

### Automatische Erkennung

Wenn Sie @Claude in einem Slack-Kanal oder Thread erwähnen, analysiert Claude automatisch Ihre Nachricht, um festzustellen, ob es sich um eine Codierungsaufgabe handelt. Wenn Claude Codierungsabsicht erkennt, leitet es Ihre Anfrage stattdessen zu Claude Code im Web weiter, anstatt als regulärer Chat-Assistent zu antworten.

Sie können Claude auch explizit anweisen, eine Anfrage als Codierungsaufgabe zu behandeln, auch wenn es diese nicht automatisch erkennt.

<Note>
  Claude Code in Slack funktioniert nur in Kanälen (öffentlich oder privat). Es funktioniert nicht in direkten Nachrichten (DMs).
</Note>

### Kontexterfassung

**Aus Threads**: Wenn Sie Claude in einem Thread @erwähnen, sammelt es Kontext aus allen Nachrichten in diesem Thread, um das vollständige Gespräch zu verstehen.

**Aus Kanälen**: Wenn es direkt in einem Kanal erwähnt wird, schaut Claude sich aktuelle Kanalnachrichten auf relevanten Kontext an.

Dieser Kontext hilft Claude, das Problem zu verstehen, das entsprechende Repository auszuwählen und seinen Ansatz zur Aufgabe zu informieren.

<Warning>
  Wenn @Claude in Slack aufgerufen wird, erhält Claude Zugriff auf den Gesprächskontext, um Ihre Anfrage besser zu verstehen. Claude kann Anweisungen aus anderen Nachrichten im Kontext befolgen, daher sollten Benutzer sicherstellen, dass sie Claude nur in vertrauenswürdigen Slack-Gesprächen verwenden.
</Warning>

### Sitzungsfluss

1. **Initiierung**: Sie @erwähnen Claude mit einer Codierungsanfrage
2. **Erkennung**: Claude analysiert Ihre Nachricht und erkennt Codierungsabsicht
3. **Sitzungserstellung**: Eine neue Claude Code-Sitzung wird auf claude.ai/code erstellt
4. **Fortschritts-Updates**: Claude veröffentlicht Status-Updates in Ihrem Slack-Thread, während die Arbeit fortschreitet
5. **Abschluss**: Nach Abschluss @erwähnt Claude Sie mit einer Zusammenfassung und Aktionsschaltflächen
6. **Überprüfung**: Klicken Sie auf „Sitzung anzeigen", um das vollständige Transkript zu sehen, oder auf „PR erstellen", um einen Pull Request zu öffnen

## Benutzeroberflächenelemente

### App Home

Die Registerkarte „App Home" zeigt Ihren Verbindungsstatus an und ermöglicht es Ihnen, Ihr Claude-Konto von Slack zu verbinden oder zu trennen.

### Nachrichtenaktionen

* **Sitzung anzeigen**: Öffnet die vollständige Claude Code-Sitzung in Ihrem Browser, wo Sie alle durchgeführten Arbeiten sehen, die Sitzung fortsetzen oder zusätzliche Anfragen stellen können.
* **PR erstellen**: Erstellt einen Pull Request direkt aus den Änderungen der Sitzung.
* **Als Code erneut versuchen**: Wenn Claude zunächst als Chat-Assistent antwortet, aber Sie wollten eine Codierungssitzung, klicken Sie auf diese Schaltfläche, um die Anfrage als Claude Code-Aufgabe erneut zu versuchen.
* **Repository ändern**: Ermöglicht es Ihnen, ein anderes Repository auszuwählen, wenn Claude falsch gewählt hat.

### Repository-Auswahl

Claude wählt automatisch ein Repository basierend auf dem Kontext aus Ihrem Slack-Gespräch aus. Wenn mehrere Repositories zutreffen könnten, zeigt Claude möglicherweise ein Dropdown-Menü an, mit dem Sie das richtige auswählen können.

## Zugriff und Berechtigungen

### Zugriff auf Benutzerebene

| Zugriffstyp           | Anforderung                                                                        |
| :-------------------- | :--------------------------------------------------------------------------------- |
| Claude Code-Sitzungen | Jeder Benutzer führt Sitzungen unter seinem eigenen Claude-Konto aus               |
| Nutzung & Ratenlimits | Sitzungen werden gegen die individuellen Plan-Limits des Benutzers angerechnet     |
| Repository-Zugriff    | Benutzer können nur auf Repositories zugreifen, die sie persönlich verbunden haben |
| Sitzungsverlauf       | Sitzungen erscheinen in Ihrem Claude Code-Verlauf auf claude.ai/code               |

### Berechtigungen für Workspace-Administratoren

Slack-Workspace-Administratoren kontrollieren, ob die Claude-App im Workspace installiert werden kann. Einzelne Benutzer authentifizieren sich dann mit ihren eigenen Claude-Konten, um die Integration zu verwenden.

## Was wo zugänglich ist

**In Slack**: Sie sehen Status-Updates, Abschluss-Zusammenfassungen und Aktionsschaltflächen. Das vollständige Transkript wird beibehalten und ist immer zugänglich.

**Im Web**: Die vollständige Claude Code-Sitzung mit vollständiger Gesprächsverlauf, alle Code-Änderungen, Dateivorgänge und die Möglichkeit, die Sitzung fortzusetzen oder Pull Requests zu erstellen.

## Best Practices

### Schreiben effektiver Anfragen

* **Seien Sie spezifisch**: Geben Sie Dateinamen, Funktionsnamen oder Fehlermeldungen an, wenn relevant.
* **Geben Sie Kontext**: Erwähnen Sie das Repository oder Projekt, wenn es nicht aus dem Gespräch klar ist.
* **Definieren Sie Erfolg**: Erklären Sie, wie „fertig" aussieht – sollte Claude Tests schreiben? Dokumentation aktualisieren? Einen PR erstellen?
* **Verwenden Sie Threads**: Antworten Sie in Threads, wenn Sie über Fehler oder Funktionen diskutieren, damit Claude den vollständigen Kontext sammeln kann.

### Wann Slack vs. Web verwenden

**Verwenden Sie Slack, wenn**: Kontext bereits in einer Slack-Diskussion vorhanden ist, Sie eine Aufgabe asynchron starten möchten oder mit Teamkollegen zusammenarbeiten, die Sichtbarkeit benötigen.

**Verwenden Sie das Web direkt, wenn**: Sie Dateien hochladen müssen, Echtzeit-Interaktion während der Entwicklung möchten oder an längeren, komplexeren Aufgaben arbeiten.

## Fehlerbehebung

### Sitzungen starten nicht

1. Überprüfen Sie, ob Ihr Claude-Konto in der Claude App Home verbunden ist
2. Überprüfen Sie, ob Sie Claude Code im Web-Zugriff aktiviert haben
3. Stellen Sie sicher, dass Sie mindestens ein GitHub-Repository mit Claude Code verbunden haben

### Repository wird nicht angezeigt

1. Verbinden Sie das Repository in Claude Code im Web unter [claude.ai/code](https://claude.ai/code)
2. Überprüfen Sie Ihre GitHub-Berechtigungen für dieses Repository
3. Versuchen Sie, Ihr GitHub-Konto zu trennen und erneut zu verbinden

### Falsches Repository ausgewählt

1. Klicken Sie auf die Schaltfläche „Repository ändern", um ein anderes Repository auszuwählen
2. Geben Sie den Repository-Namen in Ihrer Anfrage an, um eine genauere Auswahl zu erhalten

### Authentifizierungsfehler

1. Trennen Sie Ihr Claude-Konto in der App Home und verbinden Sie es erneut
2. Stellen Sie sicher, dass Sie in Ihrem Browser mit dem richtigen Claude-Konto angemeldet sind
3. Überprüfen Sie, ob Ihr Claude-Plan Claude Code-Zugriff umfasst

### Sitzungsablauf

1. Sitzungen bleiben in Ihrem Claude Code-Verlauf im Web zugänglich
2. Sie können vergangene Sitzungen von [claude.ai/code](https://claude.ai/code) aus fortsetzen oder referenzieren

## Aktuelle Einschränkungen

* **Nur GitHub**: Unterstützt derzeit nur Repositories auf GitHub.
* **Ein PR gleichzeitig**: Jede Sitzung kann einen Pull Request erstellen.
* **Ratenlimits gelten**: Sitzungen verwenden die Ratenlimits Ihres individuellen Claude-Plans.
* **Web-Zugriff erforderlich**: Benutzer müssen Claude Code im Web-Zugriff haben; diejenigen ohne erhalten nur Standard-Claude-Chat-Antworten.

## Verwandte Ressourcen

<CardGroup>
  <Card title="Claude Code im Web" icon="globe" href="/de/claude-code-on-the-web">
    Erfahren Sie mehr über Claude Code im Web
  </Card>

  <Card title="Claude für Slack" icon="slack" href="https://claude.com/claude-and-slack">
    Allgemeine Claude for Slack-Dokumentation
  </Card>

  <Card title="Slack App Marketplace" icon="store" href="https://slack.com/marketplace/A08SF47R6P4">
    Installieren Sie die Claude-App aus dem Slack Marketplace
  </Card>

  <Card title="Claude Help Center" icon="circle-question" href="https://support.claude.com">
    Erhalten Sie zusätzliche Unterstützung
  </Card>
</CardGroup>
