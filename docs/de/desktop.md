> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code Desktop verwenden

> Nutzen Sie Claude Code Desktop optimal: parallele Sitzungen mit Git-Isolation, visuelle Diff-Überprüfung, App-Vorschau, PR-Überwachung, Berechtigungsmodi, Konnektoren und Unternehmenskonfiguration.

Die Registerkarte „Code" in der Claude Desktop-App ermöglicht es Ihnen, Claude Code über eine grafische Benutzeroberfläche statt über das Terminal zu verwenden.

Desktop bietet diese Funktionen zusätzlich zur Standard-Claude-Code-Erfahrung:

* [Visuelle Diff-Überprüfung](#review-changes-with-diff-view) mit Inline-Kommentaren
* [Live-App-Vorschau](#preview-your-app) mit Dev-Servern
* [GitHub-PR-Überwachung](#monitor-pull-request-status) mit automatischer Fehlerbehebung und automatischem Merge
* [Parallele Sitzungen](#work-in-parallel-with-sessions) mit automatischer Git-Worktree-Isolation
* [Geplante Aufgaben](#schedule-recurring-tasks), die Claude nach einem wiederkehrenden Zeitplan ausführen
* [Konnektoren](#connect-external-tools) für GitHub, Slack, Linear und mehr
* Lokale, [SSH](#ssh-sessions)- und [Cloud](#run-long-running-tasks-remotely)-Umgebungen

<Tip>
  Neu bei Desktop? Beginnen Sie mit [Erste Schritte](/de/desktop-quickstart), um die App zu installieren und Ihre erste Bearbeitung vorzunehmen.
</Tip>

Diese Seite behandelt [Arbeiten mit Code](#work-with-code), [Verwalten von Sitzungen](#manage-sessions), [Erweitern von Claude Code](#extend-claude-code), [Geplante Aufgaben](#schedule-recurring-tasks) und [Konfiguration](#environment-configuration). Sie enthält auch einen [CLI-Vergleich](#coming-from-the-cli) und [Fehlerbehebung](#troubleshooting).

## Sitzung starten

Bevor Sie Ihre erste Nachricht senden, konfigurieren Sie vier Dinge im Eingabebereich:

* **Umgebung**: Wählen Sie, wo Claude ausgeführt wird. Wählen Sie **Lokal** für Ihren Computer, **Remote** für von Anthropic gehostete Cloud-Sitzungen oder eine [**SSH-Verbindung**](#ssh-sessions) für einen von Ihnen verwalteten Remote-Computer. Siehe [Umgebungskonfiguration](#environment-configuration).
* **Projektordner**: Wählen Sie den Ordner oder das Repository aus, in dem Claude arbeitet. Für Remote-Sitzungen können Sie [mehrere Repositories](#run-long-running-tasks-remotely) hinzufügen.
* **Modell**: Wählen Sie ein [Modell](/de/model-config#available-models) aus dem Dropdown neben der Schaltfläche „Senden". Das Modell wird gesperrt, sobald die Sitzung startet.
* **Berechtigungsmodus**: Wählen Sie, wie viel Autonomie Claude aus dem [Moduswahlschalter](#choose-a-permission-mode) hat. Sie können dies während der Sitzung ändern.

Geben Sie Ihre Aufgabe ein und drücken Sie **Eingabe**, um zu starten. Jede Sitzung verfolgt ihren eigenen Kontext und Änderungen unabhängig.

## Arbeiten mit Code

Geben Sie Claude den richtigen Kontext, kontrollieren Sie, wie viel es eigenständig tut, und überprüfen Sie, was es geändert hat.

### Verwenden Sie das Eingabefeld

Geben Sie ein, was Claude tun soll, und drücken Sie **Eingabe**, um zu senden. Claude liest Ihre Projektdateien, nimmt Änderungen vor und führt Befehle basierend auf Ihrem [Berechtigungsmodus](#choose-a-permission-mode) aus. Sie können Claude jederzeit unterbrechen: Klicken Sie auf die Stoppschaltfläche oder geben Sie Ihre Korrektur ein und drücken Sie **Eingabe**. Claude stoppt, was es tut, und passt sich basierend auf Ihrer Eingabe an.

Die Schaltfläche **+** neben dem Eingabefeld gibt Ihnen Zugriff auf Dateianhänge, [Skills](#use-skills), [Konnektoren](#connect-external-tools) und [Plugins](#install-plugins).

### Fügen Sie Dateien und Kontext zu Eingaben hinzu

Das Eingabefeld unterstützt zwei Möglichkeiten, um externen Kontext einzubinden:

* **@mention-Dateien**: Geben Sie `@` gefolgt von einem Dateinamen ein, um eine Datei zum Gesprächskontext hinzuzufügen. Claude kann diese Datei dann lesen und referenzieren.
* **Dateien anhängen**: Hängen Sie Bilder, PDFs und andere Dateien an Ihre Eingabe an, indem Sie die Schaltfläche „Anhängen" verwenden, oder ziehen Sie Dateien direkt in die Eingabe. Dies ist nützlich zum Teilen von Screenshots von Fehlern, Design-Mockups oder Referenzdokumenten.

### Wählen Sie einen Berechtigungsmodus

Berechtigungsmodi kontrollieren, wie viel Autonomie Claude während einer Sitzung hat: ob es vor dem Bearbeiten von Dateien, dem Ausführen von Befehlen oder beidem fragt. Sie können Modi jederzeit mit dem Moduswahlschalter neben der Schaltfläche „Senden" wechseln. Beginnen Sie mit „Berechtigungen erfragen", um genau zu sehen, was Claude tut, und wechseln Sie dann zu „Bearbeitungen automatisch akzeptieren" oder „Plan Mode", wenn Sie sich wohler fühlen.

| Modus                                     | Einstellungsschlüssel | Verhalten                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Berechtigungen erfragen**               | `default`             | Claude fragt vor dem Bearbeiten von Dateien oder dem Ausführen von Befehlen. Sie sehen einen Diff und können jede Änderung akzeptieren oder ablehnen. Empfohlen für neue Benutzer.                                                                                                                                                       |
| **Bearbeitungen automatisch akzeptieren** | `acceptEdits`         | Claude akzeptiert Dateibearbeitungen automatisch, fragt aber immer noch vor dem Ausführen von Terminal-Befehlen. Verwenden Sie dies, wenn Sie Dateiänderungen vertrauen und schnellere Iterationen wünschen.                                                                                                                             |
| **Plan Mode**                             | `plan`                | Claude analysiert Ihren Code und erstellt einen Plan, ohne Dateien zu ändern oder Befehle auszuführen. Gut für komplexe Aufgaben, bei denen Sie den Ansatz zuerst überprüfen möchten.                                                                                                                                                    |
| **Berechtigungen umgehen**                | `bypassPermissions`   | Claude läuft ohne Berechtigungsaufforderungen, äquivalent zu `--dangerously-skip-permissions` in der CLI. Aktivieren Sie dies in Ihren Einstellungen → Claude Code unter „Bypass-Berechtigungsmodus zulassen". Verwenden Sie dies nur in sandboxierten Containern oder VMs. Enterprise-Administratoren können diese Option deaktivieren. |

Der Berechtigungsmodus `dontAsk` ist nur in der [CLI](/de/permissions#permission-modes) verfügbar.

<Tip title="Best Practice">
  Beginnen Sie komplexe Aufgaben im Plan Mode, damit Claude einen Ansatz abbildet, bevor Änderungen vorgenommen werden. Sobald Sie den Plan genehmigen, wechseln Sie zu 'Bearbeitungen automatisch akzeptieren" oder „Berechtigungen erfragen", um ihn auszuführen. Siehe [Zuerst erkunden, dann planen, dann codieren](/de/best-practices#explore-first-then-plan-then-code) für mehr zu diesem Workflow.
</Tip>

Remote-Sitzungen unterstützen „Bearbeitungen automatisch akzeptieren" und „Plan Mode". „Berechtigungen erfragen" ist nicht verfügbar, da Remote-Sitzungen Dateibearbeitungen standardmäßig automatisch akzeptieren, und „Berechtigungen umgehen" ist nicht verfügbar, da die Remote-Umgebung bereits sandboxed ist.

Enterprise-Administratoren können einschränken, welche Berechtigungsmodi verfügbar sind. Siehe [Unternehmenskonfiguration](#enterprise-configuration) für Details.

### Vorschau Ihrer App

Claude kann einen Dev-Server starten und einen eingebetteten Browser öffnen, um seine Änderungen zu überprüfen. Dies funktioniert sowohl für Frontend-Web-Apps als auch für Backend-Server: Claude kann API-Endpunkte testen, Server-Protokolle anzeigen und Probleme, die er findet, iterieren. In den meisten Fällen startet Claude den Server automatisch nach dem Bearbeiten von Projektdateien. Sie können Claude auch jederzeit bitten, eine Vorschau anzuzeigen. Standardmäßig [überprüft Claude automatisch](#auto-verify-changes) Änderungen nach jeder Bearbeitung.

Aus dem Vorschau-Panel können Sie:

* Direkt im eingebetteten Browser mit Ihrer laufenden App interagieren
* Beobachten, wie Claude seine eigenen Änderungen automatisch überprüft: Es macht Screenshots, inspiziert das DOM, klickt auf Elemente, füllt Formulare aus und behebt Probleme, die es findet
* Server aus dem Dropdown **Vorschau** in der Sitzungs-Symbolleiste starten oder stoppen
* Cookies und lokalen Speicher über Server-Neustarts hinweg beibehalten, indem Sie **Sitzungen beibehalten** im Dropdown auswählen, damit Sie sich während der Entwicklung nicht erneut anmelden müssen
* Die Server-Konfiguration bearbeiten oder alle Server auf einmal stoppen

Claude erstellt die anfängliche Server-Konfiguration basierend auf Ihrem Projekt. Wenn Ihre App einen benutzerdefinierten Dev-Befehl verwendet, bearbeiten Sie `.claude/launch.json`, um Ihr Setup zu entsprechen. Siehe [Vorschau-Server konfigurieren](#configure-preview-servers) für die vollständige Referenz.

Um gespeicherte Sitzungsdaten zu löschen, schalten Sie **Vorschau-Sitzungen beibehalten** in Einstellungen → Claude Code aus. Um die Vorschau vollständig zu deaktivieren, schalten Sie **Vorschau** in Einstellungen → Claude Code aus.

### Überprüfen Sie Änderungen mit der Diff-Ansicht

Nachdem Claude Änderungen an Ihrem Code vorgenommen hat, können Sie mit der Diff-Ansicht Änderungen dateiweise überprüfen, bevor Sie einen Pull Request erstellen.

Wenn Claude Dateien ändert, wird ein Diff-Statistik-Indikator angezeigt, der die Anzahl der hinzugefügten und entfernten Zeilen anzeigt, z. B. `+12 -1`. Klicken Sie auf diesen Indikator, um den Diff-Viewer zu öffnen, der eine Dateiliste auf der linken Seite und die Änderungen für jede Datei auf der rechten Seite anzeigt.

Um Kommentare zu bestimmten Zeilen hinzuzufügen, klicken Sie auf eine beliebige Zeile im Diff, um ein Kommentarfeld zu öffnen. Geben Sie Ihr Feedback ein und drücken Sie **Eingabe**, um den Kommentar hinzuzufügen. Nach dem Hinzufügen von Kommentaren zu mehreren Zeilen senden Sie alle Kommentare auf einmal:

* **macOS**: drücken Sie **Cmd+Eingabe**
* **Windows**: drücken Sie **Strg+Eingabe**

Claude liest Ihre Kommentare und nimmt die angeforderten Änderungen vor, die als neuer Diff angezeigt werden, den Sie überprüfen können.

### Überprüfen Sie Ihren Code

Klicken Sie in der Diff-Ansicht auf **Code überprüfen** in der oberen rechten Symbolleiste, um Claude zu bitten, die Änderungen vor dem Commit zu bewerten. Claude untersucht die aktuellen Diffs und hinterlässt Kommentare direkt in der Diff-Ansicht. Sie können auf jeden Kommentar antworten oder Claude bitten, zu überarbeiten.

Die Überprüfung konzentriert sich auf hochwertige Probleme: Kompilierungsfehler, definitive Logikfehler, Sicherheitslücken und offensichtliche Fehler. Sie kennzeichnet keine Stil-, Formatierungs-, bereits vorhandenen Probleme oder etwas, das ein Linter erfassen würde.

### Überwachen Sie den Pull-Request-Status

Nachdem Sie einen Pull Request öffnen, wird eine CI-Statusleiste in der Sitzung angezeigt. Claude Code verwendet die GitHub CLI, um Prüfergebnisse abzurufen und Fehler anzuzeigen.

* **Automatische Fehlerbehebung**: Wenn aktiviert, versucht Claude automatisch, fehlgeschlagene CI-Prüfungen zu beheben, indem die Fehlerausgabe gelesen und iteriert wird.
* **Automatisches Merge**: Wenn aktiviert, führt Claude den PR zusammen, sobald alle Prüfungen bestanden sind. Die Merge-Methode ist Squash. Das automatische Merge muss [in Ihren GitHub-Repository-Einstellungen aktiviert sein](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository), damit dies funktioniert.

Verwenden Sie die Umschalter **Automatische Fehlerbehebung** und **Automatisches Merge** in der CI-Statusleiste, um eine der beiden Optionen zu aktivieren. Claude Code sendet auch eine Desktop-Benachrichtigung, wenn CI abgeschlossen ist.

<Note>
  Die PR-Überwachung erfordert, dass die [GitHub CLI (`gh`)](https://cli.github.com/) auf Ihrem Computer installiert und authentifiziert ist. Wenn `gh` nicht installiert ist, fordert Desktop Sie auf, es beim ersten Versuch, einen PR zu erstellen, zu installieren.
</Note>

## Verwalten Sie Sitzungen

Jede Sitzung ist ein unabhängiges Gespräch mit eigenem Kontext und Änderungen. Sie können mehrere Sitzungen parallel ausführen oder Arbeit in die Cloud senden.

### Arbeiten Sie parallel mit Sitzungen

Klicken Sie auf **+ Neue Sitzung** in der Seitenleiste, um an mehreren Aufgaben parallel zu arbeiten. Für Git-Repositories erhält jede Sitzung ihre eigene isolierte Kopie Ihres Projekts mit [Git Worktrees](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), sodass Änderungen in einer Sitzung andere Sitzungen nicht beeinflussen, bis Sie sie committen.

Worktrees werden standardmäßig in `<project-root>/.claude/worktrees/` gespeichert. Sie können dies in Einstellungen → Claude Code unter „Worktree-Speicherort" in ein benutzerdefiniertes Verzeichnis ändern. Sie können auch ein Branch-Präfix festlegen, das jedem Worktree-Branch-Namen vorangestellt wird, was nützlich ist, um von Claude erstellte Branches organisiert zu halten. Um einen Worktree zu entfernen, wenn Sie fertig sind, fahren Sie mit der Maus über die Sitzung in der Seitenleiste und klicken Sie auf das Archiv-Symbol.

<Note>
  Die Sitzungsisolation erfordert [Git](https://git-scm.com/downloads). Die meisten Macs enthalten Git standardmäßig. Führen Sie `git --version` im Terminal aus, um zu überprüfen. Unter Windows ist Git erforderlich, damit die Registerkarte „Code" funktioniert: [Laden Sie Git für Windows herunter](https://git-scm.com/downloads/win), installieren Sie es und starten Sie die App neu. Wenn Sie auf Git-Fehler stoßen, versuchen Sie eine Cowork-Sitzung, um Ihr Setup zu beheben.
</Note>

Verwenden Sie das Filtersymbol oben in der Seitenleiste, um Sitzungen nach Status (Aktiv, Archiviert) und Umgebung (Lokal, Cloud) zu filtern. Um eine Sitzung umzubenennen oder die Kontextnutzung zu überprüfen, klicken Sie auf den Sitzungstitel in der Symbolleiste oben in der aktiven Sitzung. Wenn der Kontext voll wird, fasst Claude das Gespräch automatisch zusammen und arbeitet weiter. Sie können auch `/compact` eingeben, um die Zusammenfassung früher auszulösen und Kontextraum freizugeben. Siehe [das Kontextfenster](/de/how-claude-code-works#the-context-window) für Details, wie die Komprimierung funktioniert.

### Führen Sie lange laufende Aufgaben remote aus

Für große Refaktorierungen, Test-Suites, Migrationen oder andere lange laufende Aufgaben wählen Sie **Remote** statt **Lokal**, wenn Sie eine Sitzung starten. Remote-Sitzungen laufen auf Anthropics Cloud-Infrastruktur und werden fortgesetzt, auch wenn Sie die App schließen oder Ihren Computer herunterfahren. Überprüfen Sie jederzeit den Fortschritt oder lenken Sie Claude in eine andere Richtung. Sie können Remote-Sitzungen auch von [claude.ai/code](https://claude.ai/code) oder der Claude iOS-App aus überwachen.

Remote-Sitzungen unterstützen auch mehrere Repositories. Nach Auswahl einer Cloud-Umgebung klicken Sie auf die Schaltfläche **+** neben dem Repo-Pill, um zusätzliche Repositories zur Sitzung hinzuzufügen. Jedes Repo erhält seinen eigenen Branch-Wahlschalter. Dies ist nützlich für Aufgaben, die mehrere Codebases umfassen, z. B. das Aktualisieren einer gemeinsamen Bibliothek und ihrer Consumer.

Siehe [Claude Code im Web](/de/claude-code-on-the-web) für mehr darüber, wie Remote-Sitzungen funktionieren.

### Fortsetzen auf einer anderen Oberfläche

Das Menü **Fortsetzen in**, das über das VS Code-Symbol unten rechts in der Sitzungs-Symbolleiste zugänglich ist, ermöglicht es Ihnen, Ihre Sitzung auf eine andere Oberfläche zu verschieben:

* **Claude Code im Web**: sendet Ihre lokale Sitzung, um remote weiter zu laufen. Desktop pusht Ihren Branch, generiert eine Zusammenfassung des Gesprächs und erstellt eine neue Remote-Sitzung mit dem vollständigen Kontext. Sie können dann wählen, die lokale Sitzung zu archivieren oder zu behalten. Dies erfordert einen sauberen Arbeitsbaum und ist nicht für SSH-Sitzungen verfügbar.
* **Ihre IDE**: öffnet Ihr Projekt in einer unterstützten IDE im aktuellen Arbeitsverzeichnis.

## Erweitern Sie Claude Code

Verbinden Sie externe Dienste, fügen Sie wiederverwendbare Workflows hinzu, passen Sie Claudes Verhalten an und konfigurieren Sie Vorschau-Server.

### Verbinden Sie externe Tools

Für lokale und [SSH](#ssh-sessions)-Sitzungen klicken Sie auf die Schaltfläche **+** neben dem Eingabefeld und wählen Sie **Konnektoren**, um Integrationen wie Google Calendar, Slack, GitHub, Linear, Notion und mehr hinzuzufügen. Sie können Konnektoren vor oder während einer Sitzung hinzufügen. Konnektoren sind nicht für Remote-Sitzungen verfügbar.

Um Konnektoren zu verwalten oder zu trennen, gehen Sie zu Einstellungen → Konnektoren in der Desktop-App oder wählen Sie **Konnektoren verwalten** aus dem Konnektoren-Menü im Eingabefeld.

Nach der Verbindung kann Claude Ihren Kalender lesen, Nachrichten senden, Probleme erstellen und direkt mit Ihren Tools interagieren. Sie können Claude fragen, welche Konnektoren in Ihrer Sitzung konfiguriert sind.

Konnektoren sind [MCP-Server](/de/mcp) mit einem grafischen Setup-Ablauf. Verwenden Sie sie für schnelle Integration mit unterstützten Diensten. Für Integrationen, die nicht in Konnektoren aufgelistet sind, fügen Sie MCP-Server manuell über [Einstellungsdateien](/de/mcp#installing-mcp-servers) hinzu. Sie können auch [benutzerdefinierte Konnektoren erstellen](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Verwenden Sie Skills

[Skills](/de/skills) erweitern, was Claude tun kann. Claude lädt sie automatisch, wenn relevant, oder Sie können eine direkt aufrufen: Geben Sie `/` im Eingabefeld ein oder klicken Sie auf die Schaltfläche **+** und wählen Sie **Slash-Befehle**, um zu sehen, was verfügbar ist. Dies umfasst [integrierte Befehle](/de/commands), Ihre [benutzerdefinierten Skills](/de/skills#create-custom-skills), Projekt-Skills aus Ihrer Codebasis und Skills aus allen [installierten Plugins](/de/plugins). Wählen Sie einen aus und er wird im Eingabefeld hervorgehoben angezeigt. Geben Sie Ihre Aufgabe danach ein und senden Sie wie gewohnt.

### Installieren Sie Plugins

[Plugins](/de/plugins) sind wiederverwendbare Pakete, die Skills, Agents, hooks, MCP-Server und LSP-Konfigurationen zu Claude Code hinzufügen. Sie können Plugins aus der Desktop-App installieren, ohne das Terminal zu verwenden.

Für lokale und [SSH](#ssh-sessions)-Sitzungen klicken Sie auf die Schaltfläche **+** neben dem Eingabefeld und wählen Sie **Plugins**, um Ihre installierten Plugins und deren Befehle zu sehen. Um ein Plugin hinzuzufügen, wählen Sie **Plugin hinzufügen** aus dem Untermenü, um den Plugin-Browser zu öffnen, der verfügbare Plugins aus Ihren konfigurierten [Marketplaces](/de/plugin-marketplaces) einschließlich des offiziellen Anthropic-Marketplace anzeigt. Wählen Sie **Plugins verwalten**, um Plugins zu aktivieren, zu deaktivieren oder zu deinstallieren.

Plugins können auf Ihr Benutzerkonto, ein bestimmtes Projekt oder nur lokal beschränkt sein. Plugins sind nicht für Remote-Sitzungen verfügbar. Für die vollständige Plugin-Referenz einschließlich der Erstellung eigener Plugins siehe [Plugins](/de/plugins).

### Konfigurieren Sie Vorschau-Server

Claude erkennt automatisch Ihr Dev-Server-Setup und speichert die Konfiguration in `.claude/launch.json` im Stammverzeichnis des Ordners, den Sie beim Starten der Sitzung ausgewählt haben. Die Vorschau verwendet diesen Ordner als Arbeitsverzeichnis. Wenn Sie also einen übergeordneten Ordner ausgewählt haben, werden Unterordner mit ihren eigenen Dev-Servern nicht automatisch erkannt. Um mit dem Server eines Unterordners zu arbeiten, starten Sie entweder eine Sitzung direkt in diesem Ordner oder fügen Sie eine Konfiguration manuell hinzu.

Um anzupassen, wie Ihr Server startet, z. B. um `yarn dev` statt `npm run dev` zu verwenden oder den Port zu ändern, bearbeiten Sie die Datei manuell oder klicken Sie auf **Konfiguration bearbeiten** im Dropdown „Vorschau", um sie in Ihrem Code-Editor zu öffnen. Die Datei unterstützt JSON mit Kommentaren.

```json  theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Sie können mehrere Konfigurationen definieren, um verschiedene Server aus demselben Projekt auszuführen, z. B. ein Frontend und eine API. Siehe die [Beispiele](#examples) unten.

#### Automatische Überprüfung von Änderungen

Wenn `autoVerify` aktiviert ist, überprüft Claude automatisch Code-Änderungen nach dem Bearbeiten von Dateien. Es macht Screenshots, prüft auf Fehler und bestätigt, dass Änderungen funktionieren, bevor es seine Antwort abschließt.

Die automatische Überprüfung ist standardmäßig aktiviert. Deaktivieren Sie sie pro Projekt, indem Sie `"autoVerify": false` zu `.claude/launch.json` hinzufügen, oder schalten Sie sie aus dem Dropdown **Vorschau** um.

```json  theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Wenn deaktiviert, sind Vorschau-Tools immer noch verfügbar und Sie können Claude jederzeit bitten, zu überprüfen. Die automatische Überprüfung macht es automatisch nach jeder Bearbeitung.

#### Konfigurationsfelder

Jeder Eintrag im Array `configurations` akzeptiert die folgenden Felder:

| Feld                | Typ       | Beschreibung                                                                                                                                                                                                                                                       |
| ------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`              | string    | Ein eindeutiger Bezeichner für diesen Server                                                                                                                                                                                                                       |
| `runtimeExecutable` | string    | Der auszuführende Befehl, z. B. `npm`, `yarn` oder `node`                                                                                                                                                                                                          |
| `runtimeArgs`       | string\[] | An `runtimeExecutable` übergebene Argumente, z. B. `["run", "dev"]`                                                                                                                                                                                                |
| `port`              | number    | Der Port, auf dem Ihr Server lauscht. Standardmäßig 3000                                                                                                                                                                                                           |
| `cwd`               | string    | Arbeitsverzeichnis relativ zu Ihrem Projektstammverzeichnis. Standardmäßig das Projektstammverzeichnis. Verwenden Sie `${workspaceFolder}`, um das Projektstammverzeichnis explizit zu referenzieren                                                               |
| `env`               | object    | Zusätzliche Umgebungsvariablen als Schlüssel-Wert-Paare, z. B. `{ "NODE_ENV": "development" }`. Legen Sie hier keine Geheimnisse ab, da diese Datei in Ihr Repo committed wird. Geheimnisse, die in Ihrem Shell-Profil festgelegt sind, werden automatisch geerbt. |
| `autoPort`          | boolean   | Wie Port-Konflikte behandelt werden. Siehe unten                                                                                                                                                                                                                   |
| `program`           | string    | Ein mit `node` auszuführendes Skript. Siehe [wann `program` vs `runtimeExecutable` verwendet werden](#when-to-use-program-vs-runtimeexecutable)                                                                                                                    |
| `args`              | string\[] | An `program` übergebene Argumente. Wird nur verwendet, wenn `program` gesetzt ist                                                                                                                                                                                  |

##### Wann `program` vs `runtimeExecutable` verwendet werden

Verwenden Sie `runtimeExecutable` mit `runtimeArgs`, um einen Dev-Server über einen Package Manager zu starten. Zum Beispiel `"runtimeExecutable": "npm"` mit `"runtimeArgs": ["run", "dev"]` führt `npm run dev` aus.

Verwenden Sie `program`, wenn Sie ein eigenständiges Skript haben, das Sie direkt mit `node` ausführen möchten. Zum Beispiel `"program": "server.js"` führt `node server.js` aus. Übergeben Sie zusätzliche Flags mit `args`.

#### Port-Konflikte

Das Feld `autoPort` kontrolliert, was passiert, wenn Ihr bevorzugter Port bereits verwendet wird:

* **`true`**: Claude findet und verwendet automatisch einen freien Port. Geeignet für die meisten Dev-Server.
* **`false`**: Claude schlägt mit einem Fehler fehl. Verwenden Sie dies, wenn Ihr Server einen bestimmten Port verwenden muss, z. B. für OAuth-Callbacks oder CORS-Allowlists.
* **Nicht gesetzt (Standard)**: Claude fragt, ob der Server diesen genauen Port benötigt, und speichert dann Ihre Antwort.

Wenn Claude einen anderen Port wählt, übergibt es den zugewiesenen Port an Ihren Server über die Umgebungsvariable `PORT`.

#### Beispiele

Diese Konfigurationen zeigen häufige Setups für verschiedene Projekttypen:

<Tabs>
  <Tab title="Next.js">
    Diese Konfiguration führt eine Next.js-App mit Yarn auf Port 3000 aus:

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Für ein Monorepo mit einem Frontend und einem API-Server definieren Sie mehrere Konfigurationen. Das Frontend verwendet `autoPort: true`, sodass es einen freien Port wählt, wenn 3000 belegt ist, während der API-Server Port 8080 genau benötigt:

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Um ein Node.js-Skript direkt auszuführen, statt einen Package-Manager-Befehl zu verwenden, verwenden Sie das Feld `program`:

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Planen Sie wiederkehrende Aufgaben

Geplante Aufgaben starten automatisch zu einer von Ihnen gewählten Zeit und Häufigkeit eine neue lokale Sitzung. Verwenden Sie sie für wiederkehrende Arbeiten wie tägliche Code-Überprüfungen, Abhängigkeitsaktualisierungsprüfungen oder morgendliche Briefings, die von Ihrem Kalender und Posteingang abrufen.

Aufgaben laufen auf Ihrem Computer, daher muss die Desktop-App offen und Ihr Computer wach sein, damit sie ausgelöst werden. Siehe [Wie geplante Aufgaben ausgeführt werden](#how-scheduled-tasks-run) für Details zu verpassten Läufen und Aufholverhalten.

<Note>
  Standardmäßig laufen geplante Aufgaben gegen den aktuellen Zustand Ihres Arbeitsverzeichnisses, einschließlich nicht committeter Änderungen. Aktivieren Sie den Worktree-Umschalter in der Eingabe, um jedem Lauf seinen eigenen isolierten Git-Worktree zu geben, genauso wie [parallele Sitzungen](#work-in-parallel-with-sessions) funktionieren.
</Note>

Um eine geplante Aufgabe zu erstellen, klicken Sie auf **Zeitplan** in der Seitenleiste und dann auf **+ Neue Aufgabe**. Konfigurieren Sie diese Felder:

| Feld         | Beschreibung                                                                                                                                                                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name         | Bezeichner für die Aufgabe. Wird in Kleinbuchstaben Kebab-Case konvertiert und als Ordnername auf der Festplatte verwendet. Muss eindeutig über Ihre Aufgaben sein.                                                                                                       |
| Beschreibung | Kurze Zusammenfassung, die in der Aufgabenliste angezeigt wird.                                                                                                                                                                                                           |
| Eingabe      | Die Anweisungen, die an Claude gesendet werden, wenn die Aufgabe ausgeführt wird. Schreiben Sie dies genauso, wie Sie jede Nachricht im Eingabefeld schreiben würden. Die Eingabe enthält auch Steuerelemente für Modell, Berechtigungsmodus, Arbeitsordner und Worktree. |
| Häufigkeit   | Wie oft die Aufgabe ausgeführt wird. Siehe [Häufigkeitsoptionen](#frequency-options) unten.                                                                                                                                                                               |

Sie können auch eine Aufgabe erstellen, indem Sie in einer beliebigen Sitzung beschreiben, was Sie möchten. Zum Beispiel: „Richten Sie eine tägliche Code-Überprüfung ein, die jeden Morgen um 9 Uhr ausgeführt wird."

### Häufigkeitsoptionen

* **Manuell**: kein Zeitplan, läuft nur, wenn Sie auf **Jetzt ausführen** klicken. Nützlich zum Speichern einer Eingabe, die Sie bei Bedarf auslösen
* **Stündlich**: läuft jede Stunde. Jede Aufgabe erhält einen festen Versatz von bis zu 10 Minuten von der vollen Stunde, um API-Verkehr zu staffeln
* **Täglich**: zeigt einen Zeitwahlschalter, Standard ist 9:00 Uhr Ortszeit
* **Wochentage**: wie täglich, aber überspringt Samstag und Sonntag
* **Wöchentlich**: zeigt einen Zeitwahlschalter und einen Tageswahlschalter

Für Intervalle, die der Wahlschalter nicht anbietet (alle 15 Minuten, erste des Monats usw.), bitten Sie Claude in einer beliebigen Desktop-Sitzung, den Zeitplan festzulegen. Verwenden Sie einfache Sprache; zum Beispiel: „Planen Sie eine Aufgabe, um alle Tests alle 6 Stunden auszuführen."

### Wie geplante Aufgaben ausgeführt werden

Geplante Aufgaben laufen lokal auf Ihrem Computer. Desktop überprüft den Zeitplan jede Minute, während die App offen ist, und startet eine neue Sitzung, wenn eine Aufgabe fällig ist, unabhängig von manuellen Sitzungen, die Sie offen haben. Jede Aufgabe erhält eine feste Verzögerung von bis zu 10 Minuten nach der geplanten Zeit, um API-Verkehr zu staffeln. Die Verzögerung ist deterministisch: dieselbe Aufgabe startet immer mit demselben Versatz.

Wenn eine Aufgabe ausgelöst wird, erhalten Sie eine Desktop-Benachrichtigung und eine neue Sitzung wird unter einem Abschnitt **Geplant** in der Seitenleiste angezeigt. Öffnen Sie sie, um zu sehen, was Claude getan hat, Änderungen zu überprüfen oder auf Berechtigungsaufforderungen zu antworten. Die Sitzung funktioniert wie jede andere: Claude kann Dateien bearbeiten, Befehle ausführen, Commits erstellen und Pull Requests öffnen.

Aufgaben laufen nur, während die Desktop-App läuft und Ihr Computer wach ist. Wenn Ihr Computer durch eine geplante Zeit schläft, wird der Lauf übersprungen. Um Idle-Sleep zu verhindern, aktivieren Sie **Computer wach halten** in Einstellungen unter **Desktop-App → Allgemein**. Das Schließen des Laptop-Deckels setzt ihn immer noch in den Schlafmodus.

### Verpasste Läufe

Wenn die App startet oder Ihr Computer aufwacht, überprüft Desktop, ob jede Aufgabe in den letzten sieben Tagen Läufe verpasst hat. Wenn ja, startet Desktop genau einen Aufhollauf für die zuletzt verpasste Zeit und verwirft alles Ältere. Eine täglich geplante Aufgabe, die sechs Tage verpasst hat, läuft einmal beim Aufwachen. Desktop zeigt eine Benachrichtigung, wenn ein Aufhollauf startet.

Beachten Sie dies beim Schreiben von Eingaben. Eine für 9 Uhr geplante Aufgabe könnte um 23 Uhr ausgeführt werden, wenn Ihr Computer den ganzen Tag schläft. Wenn das Timing wichtig ist, fügen Sie Schutzmaßnahmen zur Eingabe selbst hinzu, zum Beispiel: „Überprüfen Sie nur die heutigen Commits. Wenn es nach 17 Uhr ist, überspringen Sie die Überprüfung und posten Sie einfach eine Zusammenfassung dessen, was verpasst wurde."

### Berechtigungen für geplante Aufgaben

Jede Aufgabe hat ihren eigenen Berechtigungsmodus, den Sie beim Erstellen oder Bearbeiten der Aufgabe festlegen. Erlaubnisregeln aus `~/.claude/settings.json` gelten auch für geplante Aufgabensitzungen. Wenn eine Aufgabe im Ask-Modus läuft und ein Tool ausführen muss, für das sie keine Berechtigung hat, stellt sich der Lauf hin, bis Sie ihn genehmigen. Die Sitzung bleibt offen in der Seitenleiste, damit Sie später antworten können.

Um Stalls zu vermeiden, klicken Sie auf **Jetzt ausführen**, nachdem Sie eine Aufgabe erstellt haben, achten Sie auf Berechtigungsaufforderungen und wählen Sie „Immer zulassen" für jede aus. Zukünftige Läufe dieser Aufgabe genehmigen automatisch dieselben Tools ohne Aufforderung. Sie können diese Genehmigungen auf der Detailseite der Aufgabe überprüfen und widerrufen.

### Verwalten Sie geplante Aufgaben

Klicken Sie auf eine Aufgabe in der Liste **Zeitplan**, um ihre Detailseite zu öffnen. Von hier aus können Sie:

* **Jetzt ausführen**: Starten Sie die Aufgabe sofort, ohne auf die nächste geplante Zeit zu warten
* **Wiederholungen umschalten**: Pausieren oder fortsetzen Sie geplante Läufe, ohne die Aufgabe zu löschen
* **Bearbeiten**: Ändern Sie die Eingabe, Häufigkeit, den Ordner oder andere Einstellungen
* **Verlauf überprüfen**: Sehen Sie jeden vergangenen Lauf, einschließlich solcher, die übersprungen wurden, weil Ihr Computer schläft
* **Erlaubte Berechtigungen überprüfen**: Sehen Sie und widerrufen Sie gespeicherte Tool-Genehmigungen für diese Aufgabe aus dem Panel **Immer zulassen**
* **Löschen**: Entfernen Sie die Aufgabe und archivieren Sie alle Sitzungen, die sie erstellt hat

Sie können Aufgaben auch verwalten, indem Sie Claude in einer beliebigen Desktop-Sitzung bitten. Zum Beispiel: „Pausieren Sie meine Aufgabe zur Abhängigkeitsprüfung", „Löschen Sie die Aufgabe zur Standup-Vorbereitung" oder „Zeigen Sie mir meine geplanten Aufgaben."

Um die Eingabe einer Aufgabe auf der Festplatte zu bearbeiten, öffnen Sie `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (oder unter [`CLAUDE_CONFIG_DIR`](/de/env-vars), falls gesetzt). Die Datei verwendet YAML-Frontmatter für `name` und `description`, mit der Eingabe als Body. Änderungen treten beim nächsten Lauf in Kraft. Zeitplan, Ordner, Modell und aktivierter Zustand sind nicht in dieser Datei: Ändern Sie sie über das Bearbeitungsformular oder bitten Sie Claude.

## Umgebungskonfiguration

Die Umgebung, die Sie beim [Starten einer Sitzung](#start-a-session) wählen, bestimmt, wo Claude ausgeführt wird und wie Sie sich verbinden:

* **Lokal**: läuft auf Ihrem Computer mit direktem Zugriff auf Ihre Dateien
* **Remote**: läuft auf Anthropics Cloud-Infrastruktur. Sitzungen werden fortgesetzt, auch wenn Sie die App schließen.
* **SSH**: läuft auf einem Remote-Computer, mit dem Sie sich über SSH verbinden, z. B. Ihre eigenen Server, Cloud-VMs oder Dev-Container

### Lokale Sitzungen

Lokale Sitzungen erben Umgebungsvariablen aus Ihrer Shell. Wenn Sie zusätzliche Variablen benötigen, legen Sie sie in Ihrem Shell-Profil fest, z. B. `~/.zshrc` oder `~/.bashrc`, und starten Sie die Desktop-App neu. Siehe [Umgebungsvariablen](/de/env-vars) für die vollständige Liste der unterstützten Variablen.

[Erweitertes Denken](/de/common-workflows#use-extended-thinking-thinking-mode) ist standardmäßig aktiviert, was die Leistung bei komplexen Denkaufgaben verbessert, aber zusätzliche Token verwendet. Um das Denken vollständig zu deaktivieren, setzen Sie `MAX_THINKING_TOKENS=0` in Ihrem Shell-Profil. Bei Opus wird `MAX_THINKING_TOKENS` ignoriert, außer für `0`, da adaptive Argumentation die Denktiefe steuert.

### Remote-Sitzungen

Remote-Sitzungen werden im Hintergrund fortgesetzt, auch wenn Sie die App schließen. Die Nutzung wird auf Ihre [Abonnementplanlimits](/de/costs) angerechnet, ohne separate Compute-Gebühren.

Sie können benutzerdefinierte Cloud-Umgebungen mit verschiedenen Netzwerkzugriffsstufen und Umgebungsvariablen erstellen. Wählen Sie das Umgebungs-Dropdown beim Starten einer Remote-Sitzung und wählen Sie **Umgebung hinzufügen**. Siehe [Cloud-Umgebungen](/de/claude-code-on-the-web#cloud-environment) für Details zur Konfiguration von Netzwerkzugriff und Umgebungsvariablen.

### SSH-Sitzungen

SSH-Sitzungen ermöglichen es Ihnen, Claude Code auf einem Remote-Computer auszuführen, während Sie die Desktop-App als Ihre Schnittstelle verwenden. Dies ist nützlich für die Arbeit mit Codebases, die auf Cloud-VMs, Dev-Containern oder Servern mit spezifischer Hardware oder Abhängigkeiten leben.

Um eine SSH-Verbindung hinzuzufügen, klicken Sie auf das Umgebungs-Dropdown vor dem Starten einer Sitzung und wählen Sie **+ SSH-Verbindung hinzufügen**. Der Dialog fragt nach:

* **Name**: ein freundlicher Bezeichner für diese Verbindung
* **SSH-Host**: `user@hostname` oder ein in `~/.ssh/config` definierter Host
* **SSH-Port**: Standard ist 22, wenn leer gelassen, oder verwendet den Port aus Ihrer SSH-Konfiguration
* **Identity File**: Pfad zu Ihrem privaten Schlüssel, z. B. `~/.ssh/id_rsa`. Lassen Sie leer, um den Standardschlüssel oder Ihre SSH-Konfiguration zu verwenden.

Nach dem Hinzufügen wird die Verbindung im Umgebungs-Dropdown angezeigt. Wählen Sie sie aus, um eine Sitzung auf diesem Computer zu starten. Claude läuft auf dem Remote-Computer mit Zugriff auf seine Dateien und Tools.

Claude Code muss auf dem Remote-Computer installiert sein. Nach der Verbindung unterstützen SSH-Sitzungen Berechtigungsmodi, Konnektoren, Plugins und MCP-Server.

## Unternehmenskonfiguration

Organisationen in Teams- oder Enterprise-Plänen können das Verhalten der Desktop-App durch Admin-Konsolen-Steuerelemente, verwaltete Einstellungsdateien und Geräteverwaltungsrichtlinien verwalten.

### Admin-Konsolen-Steuerelemente

Diese Einstellungen werden über die [Admin-Einstellungskonsole](https://claude.ai/admin-settings/claude-code) konfiguriert:

* **Aktivieren oder deaktivieren Sie die Registerkarte „Code"**: Kontrollieren Sie, ob Benutzer in Ihrer Organisation auf Claude Code in der Desktop-App zugreifen können
* **Deaktivieren Sie den Bypass-Berechtigungsmodus**: Verhindern Sie, dass Benutzer in Ihrer Organisation den Bypass-Berechtigungsmodus aktivieren
* **Deaktivieren Sie Claude Code im Web**: Aktivieren oder deaktivieren Sie Remote-Sitzungen für Ihre Organisation

### Verwaltete Einstellungen

Verwaltete Einstellungen überschreiben Projekt- und Benutzereinstellungen und gelten, wenn Desktop CLI-Sitzungen startet. Sie können diese Schlüssel in der [verwalteten Einstellungsdatei](/de/settings#settings-precedence) Ihrer Organisation oder remote über die Admin-Konsole festlegen.

| Schlüssel                      | Beschreibung                                                                                                                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode` | auf `"disable"` setzen, um Benutzer daran zu hindern, den Bypass-Berechtigungsmodus zu aktivieren. Siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings). |

Für die vollständige Liste der verwalteten Einstellungen einschließlich `allowManagedPermissionRulesOnly` und `allowManagedHooksOnly` siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings).

Remote-verwaltete Einstellungen, die über die Admin-Konsole hochgeladen werden, gelten derzeit nur für CLI- und IDE-Sitzungen. Für Desktop-spezifische Einschränkungen verwenden Sie die Admin-Konsolen-Steuerelemente oben.

### Geräteverwaltungsrichtlinien

IT-Teams können die Desktop-App über MDM auf macOS oder Gruppenrichtlinie unter Windows verwalten. Verfügbare Richtlinien umfassen das Aktivieren oder Deaktivieren der Claude-Code-Funktion, das Steuern von Auto-Updates und das Festlegen einer benutzerdefinierten Bereitstellungs-URL.

* **macOS**: Konfigurieren Sie über die Präferenzdomäne `com.anthropic.Claude` mit Tools wie Jamf oder Kandji
* **Windows**: Konfigurieren Sie über die Registrierung unter `SOFTWARE\Policies\Claude`

### Authentifizierung und SSO

Enterprise-Organisationen können SSO für alle Benutzer verlangen. Siehe [Authentifizierung](/de/authentication) für Plan-Level-Details und [Einrichten von SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) für SAML- und OIDC-Konfiguration.

### Datenbehandlung

Claude Code verarbeitet Ihren Code lokal in lokalen Sitzungen oder auf Anthropics Cloud-Infrastruktur in Remote-Sitzungen. Gespräche und Code-Kontext werden an Anthropics API zur Verarbeitung gesendet. Siehe [Datenbehandlung](/de/data-usage) für Details zu Datenspeicherung, Datenschutz und Compliance.

### Bereitstellung

Desktop kann über Enterprise-Bereitstellungstools verteilt werden:

* **macOS**: Verteilen Sie über MDM wie Jamf oder Kandji mit dem `.dmg`-Installer
* **Windows**: Stellen Sie über MSIX-Paket oder `.exe`-Installer bereit. Siehe [Claude Desktop für Windows bereitstellen](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) für Enterprise-Bereitstellungsoptionen einschließlich stiller Installation

Für Netzwerkkonfiguration wie Proxy-Einstellungen, Firewall-Allowlisting und LLM-Gateways siehe [Netzwerkkonfiguration](/de/network-config).

Für die vollständige Enterprise-Konfigurationsreferenz siehe das [Enterprise-Konfigurationshandbuch](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Kommen Sie von der CLI?

Wenn Sie bereits die Claude Code CLI verwenden, führt Desktop dieselbe zugrunde liegende Engine mit einer grafischen Benutzeroberfläche aus. Sie können beide gleichzeitig auf demselben Computer ausführen, sogar auf demselben Projekt. Jede behält separate Sitzungsverlauf, aber sie teilen Konfiguration und Projektgedächtnis über CLAUDE.md-Dateien.

Um eine CLI-Sitzung in Desktop zu verschieben, führen Sie `/desktop` im Terminal aus. Claude speichert Ihre Sitzung und öffnet sie in der Desktop-App, dann beendet die CLI. Dieser Befehl ist nur auf macOS und Windows verfügbar.

<Tip>
  Wann Desktop vs CLI verwendet werden: Verwenden Sie Desktop, wenn Sie visuelle Diff-Überprüfung, Dateianhänge oder Sitzungsverwaltung in einer Seitenleiste möchten. Verwenden Sie die CLI, wenn Sie Scripting, Automatisierung, Drittanbieter oder ein Terminal-Workflow bevorzugen.
</Tip>

### CLI-Flag-Äquivalente

Diese Tabelle zeigt das Desktop-App-Äquivalent für häufige CLI-Flags. Flags, die nicht aufgelistet sind, haben kein Desktop-Äquivalent, da sie für Scripting oder Automatisierung konzipiert sind.

| CLI                                     | Desktop-Äquivalent                                                                                                                                                                 |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                        | Modell-Dropdown neben der Schaltfläche „Senden", vor dem Starten einer Sitzung                                                                                                     |
| `--resume`, `--continue`                | Klicken Sie auf eine Sitzung in der Seitenleiste                                                                                                                                   |
| `--permission-mode`                     | Moduswahlschalter neben der Schaltfläche „Senden"                                                                                                                                  |
| `--dangerously-skip-permissions`        | Bypass-Berechtigungsmodus. Aktivieren Sie in Einstellungen → Claude Code → „Bypass-Berechtigungsmodus zulassen". Enterprise-Administratoren können diese Einstellung deaktivieren. |
| `--add-dir`                             | Fügen Sie mehrere Repos mit der Schaltfläche **+** in Remote-Sitzungen hinzu                                                                                                       |
| `--allowedTools`, `--disallowedTools`   | nicht in Desktop verfügbar                                                                                                                                                         |
| `--verbose`                             | nicht verfügbar. Überprüfen Sie Systemprotokolle: Console.app auf macOS, Event Viewer → Windows Logs → Application unter Windows                                                   |
| `--print`, `--output-format`            | nicht verfügbar. Desktop ist nur interaktiv.                                                                                                                                       |
| `ANTHROPIC_MODEL` Umgebungsvariable     | Modell-Dropdown neben der Schaltfläche „Senden"                                                                                                                                    |
| `MAX_THINKING_TOKENS` Umgebungsvariable | in Shell-Profil festlegen; gilt für lokale Sitzungen. Siehe [Umgebungskonfiguration](#environment-configuration).                                                                  |

### Gemeinsame Konfiguration

Desktop und CLI lesen dieselben Konfigurationsdateien, daher wird Ihr Setup übertragen:

* **[CLAUDE.md](/de/memory)-Dateien** in Ihrem Projekt werden von beiden verwendet
* **[MCP-Server](/de/mcp)**, die in `~/.claude.json` oder `.mcp.json` konfiguriert sind, funktionieren in beiden
* **[Hooks](/de/hooks)** und **[Skills](/de/skills)**, die in Einstellungen definiert sind, gelten für beide
* **[Einstellungen](/de/settings)** in `~/.claude.json` und `~/.claude/settings.json` werden geteilt. Berechtigungsregeln, erlaubte Tools und andere Einstellungen in `settings.json` gelten für Desktop-Sitzungen.
* **Modelle**: Sonnet, Opus und Haiku sind in beiden verfügbar. Wählen Sie in Desktop das Modell aus dem Dropdown neben der Schaltfläche „Senden" vor dem Starten einer Sitzung. Sie können das Modell während einer aktiven Sitzung nicht ändern.

<Note>
  **MCP-Server: Desktop-Chat-App vs Claude Code**: MCP-Server, die für die Claude Desktop-Chat-App in `claude_desktop_config.json` konfiguriert sind, sind separat von Claude Code und werden nicht auf der Registerkarte „Code" angezeigt. Um MCP-Server in Claude Code zu verwenden, konfigurieren Sie sie in `~/.claude.json` oder der `.mcp.json`-Datei Ihres Projekts. Siehe [MCP-Konfiguration](/de/mcp#installing-mcp-servers) für Details.
</Note>

### Funktionsvergleich

Diese Tabelle vergleicht Kernfunktionen zwischen CLI und Desktop. Für eine vollständige Liste der CLI-Flags siehe die [CLI-Referenz](/de/cli-reference).

| Funktion                                               | CLI                                                       | Desktop                                                                                                                |
| ------------------------------------------------------ | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Berechtigungsmodi                                      | alle Modi einschließlich `dontAsk`                        | Berechtigungen erfragen, Bearbeitungen automatisch akzeptieren, Plan Mode und Bypass-Berechtigungen über Einstellungen |
| `--dangerously-skip-permissions`                       | CLI-Flag                                                  | Bypass-Berechtigungsmodus. Aktivieren Sie in Einstellungen → Claude Code → „Bypass-Berechtigungsmodus zulassen"        |
| [Drittanbieter-Provider](/de/third-party-integrations) | Bedrock, Vertex, Foundry                                  | nicht verfügbar. Desktop verbindet sich direkt mit Anthropics API.                                                     |
| [MCP-Server](/de/mcp)                                  | in Einstellungsdateien konfigurieren                      | Konnektoren-UI für lokale und SSH-Sitzungen oder Einstellungsdateien                                                   |
| [Plugins](/de/plugins)                                 | `/plugin`-Befehl                                          | Plugin-Manager-UI                                                                                                      |
| @mention-Dateien                                       | textbasiert                                               | mit Autovervollständigung                                                                                              |
| Dateianhänge                                           | nicht verfügbar                                           | Bilder, PDFs                                                                                                           |
| Sitzungsisolation                                      | [`--worktree`](/de/cli-reference)-Flag                    | automatische Worktrees                                                                                                 |
| Mehrere Sitzungen                                      | separate Terminals                                        | Seitenleisten-Tabs                                                                                                     |
| Wiederkehrende Aufgaben                                | Cron-Jobs, CI-Pipelines                                   | [geplante Aufgaben](#schedule-recurring-tasks)                                                                         |
| Scripting und Automatisierung                          | [`--print`](/de/cli-reference), [Agent SDK](/de/headless) | nicht verfügbar                                                                                                        |

### Was ist nicht in Desktop verfügbar

Die folgenden Funktionen sind nur in der CLI oder VS Code-Erweiterung verfügbar:

* **Drittanbieter-Provider**: Desktop verbindet sich direkt mit Anthropics API. Verwenden Sie stattdessen die [CLI](/de/quickstart) mit Bedrock, Vertex oder Foundry.
* **Linux**: Die Desktop-App ist nur auf macOS und Windows verfügbar.
* **Inline-Code-Vorschläge**: Desktop bietet keine Autovervollständigungs-ähnlichen Vorschläge. Es funktioniert durch Gesprächseingaben und explizite Code-Änderungen.
* **Agent-Teams**: Multi-Agent-Orchestrierung ist über die [CLI](/de/agent-teams) und [Agent SDK](/de/headless) verfügbar, nicht in Desktop.

## Fehlerbehebung

### Überprüfen Sie Ihre Version

Um zu sehen, welche Version der Desktop-App Sie ausführen:

* **macOS**: Klicken Sie auf **Claude** in der Menüleiste und dann auf **Über Claude**
* **Windows**: Klicken Sie auf **Hilfe** und dann auf **Über**

Klicken Sie auf die Versionsnummer, um sie in Ihre Zwischenablage zu kopieren.

### 403 oder Authentifizierungsfehler auf der Registerkarte „Code"

Wenn Sie `Error 403: Forbidden` oder andere Authentifizierungsfehler bei der Verwendung der Registerkarte „Code" sehen:

1. Melden Sie sich aus dem App-Menü ab und wieder an. Dies ist die häufigste Lösung.
2. Überprüfen Sie, ob Sie ein aktives bezahltes Abonnement haben: Pro, Max, Teams oder Enterprise.
3. Wenn die CLI funktioniert, aber Desktop nicht, beenden Sie die Desktop-App vollständig, nicht nur das Fenster schließen, und öffnen Sie sie dann erneut und melden Sie sich an.
4. Überprüfen Sie Ihre Internetverbindung und Proxy-Einstellungen.

### Leerer oder hängender Bildschirm beim Start

Wenn die App öffnet, aber einen leeren oder nicht reagierenden Bildschirm anzeigt:

1. Starten Sie die App neu.
2. Überprüfen Sie auf ausstehende Updates. Die App wird beim Start automatisch aktualisiert.
3. Überprüfen Sie unter Windows den Event Viewer auf Absturzprotokolle unter **Windows Logs → Application**.

### „Fehler beim Laden der Sitzung"

Wenn Sie `Failed to load session` sehen, existiert der ausgewählte Ordner möglicherweise nicht mehr, ein Git-Repository benötigt möglicherweise Git LFS, das nicht installiert ist, oder Dateiberechtigungen verhindern möglicherweise den Zugriff. Versuchen Sie, einen anderen Ordner auszuwählen oder die App neu zu starten.

### Sitzung findet installierte Tools nicht

Wenn Claude Tools wie `npm`, `node` oder andere CLI-Befehle nicht finden kann, überprüfen Sie, dass die Tools in Ihrem regulären Terminal funktionieren, überprüfen Sie, dass Ihr Shell-Profil PATH richtig einrichtet, und starten Sie die Desktop-App neu, um Umgebungsvariablen neu zu laden.

### Git- und Git LFS-Fehler

Unter Windows ist Git erforderlich, damit die Registerkarte „Code" lokale Sitzungen startet. Wenn Sie „Git is required" sehen, installieren Sie [Git für Windows](https://git-scm.com/downloads/win) und starten Sie die App neu.

Wenn Sie „Git LFS is required by this repository but is not installed" sehen, installieren Sie Git LFS von [git-lfs.com](https://git-lfs.com/), führen Sie `git lfs install` aus und starten Sie die App neu.

### MCP-Server funktionieren nicht unter Windows

Wenn MCP-Server-Umschalter nicht reagieren oder Server unter Windows keine Verbindung herstellen, überprüfen Sie, dass der Server in Ihren Einstellungen richtig konfiguriert ist, starten Sie die App neu, überprüfen Sie, dass der Server-Prozess im Task Manager läuft, und überprüfen Sie Server-Protokolle auf Verbindungsfehler.

### App wird nicht beendet

* **macOS**: drücken Sie Cmd+Q. Wenn die App nicht reagiert, verwenden Sie Force Quit mit Cmd+Option+Esc, wählen Sie Claude und klicken Sie auf Force Quit.
* **Windows**: verwenden Sie Task Manager mit Strg+Umschalt+Esc, um den Claude-Prozess zu beenden.

### Windows-spezifische Probleme

* **PATH nicht aktualisiert nach Installation**: Öffnen Sie ein neues Terminal-Fenster. PATH-Updates gelten nur für neue Terminal-Sitzungen.
* **Fehler bei gleichzeitiger Installation**: Wenn Sie einen Fehler über eine andere Installation sehen, die läuft, aber es gibt keine, versuchen Sie, das Installationsprogramm als Administrator auszuführen.
* **ARM64**: Windows ARM64-Geräte werden vollständig unterstützt.

### Cowork-Registerkarte auf Intel-Macs nicht verfügbar

Die Cowork-Registerkarte erfordert Apple Silicon (M1 oder später) auf macOS. Unter Windows ist Cowork auf allen unterstützten Hardware verfügbar. Die Registerkarten „Chat" und „Code" funktionieren normal auf Intel-Macs.

### „Branch existiert noch nicht" beim Öffnen in CLI

Remote-Sitzungen können Branches erstellen, die auf Ihrem lokalen Computer nicht existieren. Klicken Sie auf den Branch-Namen in der Sitzungs-Symbolleiste, um ihn zu kopieren, und rufen Sie ihn dann lokal ab:

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Immer noch stecken?

* Suchen Sie oder melden Sie einen Fehler auf [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Besuchen Sie das [Claude Support Center](https://support.claude.com/)

Wenn Sie einen Fehler melden, geben Sie Ihre Desktop-App-Version, Ihr Betriebssystem, die genaue Fehlermeldung und relevante Protokolle an. Überprüfen Sie auf macOS Console.app. Überprüfen Sie unter Windows Event Viewer → Windows Logs → Application.
