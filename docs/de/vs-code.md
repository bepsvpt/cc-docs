> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code in VS Code verwenden

> Installieren und konfigurieren Sie die Claude Code-Erweiterung für VS Code. Erhalten Sie KI-Codierungshilfe mit Inline-Diffs, @-Erwähnungen, Planüberprüfung und Tastaturkürzeln.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="VS Code-Editor mit dem geöffneten Claude Code-Erweiterungspanel auf der rechten Seite, das ein Gespräch mit Claude zeigt" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

Die VS Code-Erweiterung bietet eine native grafische Benutzeroberfläche für Claude Code, die direkt in Ihre IDE integriert ist. Dies ist die empfohlene Methode zur Verwendung von Claude Code in VS Code.

Mit der Erweiterung können Sie Claudes Pläne überprüfen und bearbeiten, bevor Sie sie akzeptieren, Bearbeitungen automatisch akzeptieren, während sie vorgenommen werden, @-Erwähnungen von Dateien mit bestimmten Zeilenbereichen aus Ihrer Auswahl hinzufügen, auf Gesprächsverlauf zugreifen und mehrere Gespräche in separaten Registerkarten oder Fenstern öffnen.

## Voraussetzungen

Stellen Sie vor der Installation sicher, dass Sie Folgendes haben:

* VS Code 1.98.0 oder höher
* Ein Anthropic-Konto (Sie melden sich an, wenn Sie die Erweiterung zum ersten Mal öffnen). Wenn Sie einen Drittanbieter wie Amazon Bedrock oder Google Vertex AI verwenden, siehe stattdessen [Drittanbieter verwenden](#use-third-party-providers).

<Tip>
  Die Erweiterung enthält die CLI (Befehlszeilenschnittstelle), auf die Sie über das integrierte Terminal von VS Code für erweiterte Funktionen zugreifen können. Siehe [VS Code-Erweiterung vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) für Details.
</Tip>

## Installieren Sie die Erweiterung

Klicken Sie auf den Link für Ihre IDE, um direkt zu installieren:

* [Für VS Code installieren](vscode:extension/anthropic.claude-code)
* [Für Cursor installieren](cursor:extension/anthropic.claude-code)

Oder drücken Sie in VS Code `Cmd+Shift+X` (Mac) oder `Ctrl+Shift+X` (Windows/Linux), um die Ansicht „Erweiterungen" zu öffnen, suchen Sie nach „Claude Code" und klicken Sie auf **Installieren**.

<Note>Wenn die Erweiterung nach der Installation nicht angezeigt wird, starten Sie VS Code neu oder führen Sie „Developer: Reload Window" aus der Befehlspalette aus.</Note>

## Erste Schritte

Nach der Installation können Sie Claude Code über die VS Code-Benutzeroberfläche verwenden:

<Steps>
  <Step title="Öffnen Sie das Claude Code-Panel">
    In VS Code zeigt das Spark-Symbol Claude Code an: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Spark-Symbol" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    Die schnellste Möglichkeit, Claude zu öffnen, besteht darin, auf das Spark-Symbol in der **Editor-Symbolleiste** (obere rechte Ecke des Editors) zu klicken. Das Symbol wird nur angezeigt, wenn Sie eine Datei geöffnet haben.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="VS Code-Editor mit dem Spark-Symbol in der Editor-Symbolleiste" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Weitere Möglichkeiten zum Öffnen von Claude Code:

    * **Aktivitätsleiste**: Klicken Sie auf das Spark-Symbol in der linken Seitenleiste, um die Sitzungsliste zu öffnen. Klicken Sie auf eine beliebige Sitzung, um sie als vollständige Editor-Registerkarte zu öffnen, oder starten Sie eine neue. Dieses Symbol ist immer in der Aktivitätsleiste sichtbar.
    * **Befehlspalette**: `Cmd+Shift+P` (Mac) oder `Ctrl+Shift+P` (Windows/Linux), geben Sie „Claude Code" ein und wählen Sie eine Option wie „In neuer Registerkarte öffnen"
    * **Statusleiste**: Klicken Sie auf **✱ Claude Code** in der unteren rechten Ecke des Fensters. Dies funktioniert auch, wenn keine Datei geöffnet ist.

    Wenn Sie das Panel zum ersten Mal öffnen, wird eine **Learn Claude Code**-Checkliste angezeigt. Arbeiten Sie jedes Element durch, indem Sie auf **Show me** klicken, oder schließen Sie es mit dem X. Um es später erneut zu öffnen, deaktivieren Sie **Hide Onboarding** in den VS Code-Einstellungen unter Extensions → Claude Code.

    Sie können das Claude-Panel ziehen, um es überall in VS Code zu repositionieren. Siehe [Passen Sie Ihren Workflow an](#customize-your-workflow) für Details.
  </Step>

  <Step title="Senden Sie eine Eingabeaufforderung">
    Bitten Sie Claude, Ihnen bei Ihrem Code oder Ihren Dateien zu helfen, sei es zum Erklären, wie etwas funktioniert, zum Debuggen eines Problems oder zum Vornehmen von Änderungen.

    <Tip>Claude sieht Ihren ausgewählten Text automatisch. Drücken Sie `Option+K` (Mac) / `Alt+K` (Windows/Linux), um auch eine @-Erwähnungsreferenz (wie `@file.ts#5-10`) in Ihre Eingabeaufforderung einzufügen.</Tip>

    Hier ist ein Beispiel für eine Frage zu einer bestimmten Zeile in einer Datei:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="VS Code-Editor mit den Zeilen 2-3, die in einer Python-Datei ausgewählt sind, und das Claude Code-Panel zeigt eine Frage zu diesen Zeilen mit einer @-Erwähnungsreferenz" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Überprüfen Sie Änderungen">
    Wenn Claude eine Datei bearbeiten möchte, zeigt es einen Vergleich nebeneinander zwischen dem Original und den vorgeschlagenen Änderungen an und fordert dann die Genehmigung an. Sie können akzeptieren, ablehnen oder Claude sagen, was stattdessen zu tun ist.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code zeigt einen Diff von Claudes vorgeschlagenen Änderungen mit einer Genehmigungsaufforderung, die fragt, ob die Bearbeitung vorgenommen werden soll" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Weitere Ideen, was Sie mit Claude Code tun können, finden Sie unter [Häufige Workflows](/de/common-workflows).

<Tip>
  Führen Sie „Claude Code: Open Walkthrough" aus der Befehlspalette aus, um eine geführte Tour durch die Grundlagen zu erhalten.
</Tip>

## Verwenden Sie das Eingabefeld

Das Eingabefeld unterstützt mehrere Funktionen:

* **Genehmigungsmodi**: Klicken Sie auf den Modusindikator am unteren Rand des Eingabefelds, um Modi zu wechseln. Im normalen Modus fragt Claude vor jeder Aktion um Genehmigung. Im Plan Mode beschreibt Claude, was es tun wird, und wartet auf Genehmigung, bevor es Änderungen vornimmt. VS Code öffnet den Plan automatisch als vollständiges Markdown-Dokument, in dem Sie Inline-Kommentare hinzufügen können, um Feedback zu geben, bevor Claude beginnt. Im Auto-Accept-Modus nimmt Claude Bearbeitungen vor, ohne zu fragen. Legen Sie den Standard in den VS Code-Einstellungen unter `claudeCode.initialPermissionMode` fest.
* **Befehlsmenü**: Klicken Sie auf `/` oder geben Sie `/` ein, um das Befehlsmenü zu öffnen. Zu den Optionen gehören das Anhängen von Dateien, das Wechseln von Modellen, das Umschalten von Extended Thinking und das Anzeigen der Plannutzung (`/usage`). Der Abschnitt „Customize" bietet Zugriff auf MCP servers, hooks, memory, permissions und plugins. Elemente mit einem Terminal-Symbol werden im integrierten Terminal geöffnet.
* **Kontextindikator**: Das Eingabefeld zeigt, wie viel von Claudes context window Sie verwenden. Claude komprimiert automatisch bei Bedarf, oder Sie können `/compact` manuell ausführen.
* **Extended Thinking**: Ermöglicht Claude, mehr Zeit für die Überlegung komplexer Probleme aufzuwenden. Aktivieren Sie es über das Befehlsmenü (`/`). Siehe [Extended Thinking](/de/common-workflows#use-extended-thinking-thinking-mode) für Details.
* **Mehrzeilige Eingabe**: Drücken Sie `Shift+Enter`, um eine neue Zeile hinzuzufügen, ohne zu senden. Dies funktioniert auch in der „Other"-Freitexteingabe von Frage-Dialogen.

### Referenzdateien und -ordner

Verwenden Sie @-Erwähnungen, um Claude Kontext über bestimmte Dateien oder Ordner zu geben. Wenn Sie `@` gefolgt von einem Datei- oder Ordnernamen eingeben, liest Claude diesen Inhalt und kann Fragen dazu beantworten oder Änderungen daran vornehmen. Claude Code unterstützt Fuzzy Matching, sodass Sie Teilnamen eingeben können, um das zu finden, was Sie benötigen:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Für große PDFs können Sie Claude bitten, bestimmte Seiten statt der gesamten Datei zu lesen: eine einzelne Seite, einen Bereich wie Seiten 1-10 oder einen offenen Bereich wie Seite 3 und darüber hinaus.

Wenn Sie Text im Editor auswählen, kann Claude Ihren hervorgehobenen Code automatisch sehen. Die Fußzeile des Eingabefelds zeigt, wie viele Zeilen ausgewählt sind. Drücken Sie `Option+K` (Mac) / `Alt+K` (Windows/Linux), um eine @-Erwähnung mit dem Dateipfad und den Zeilennummern einzufügen (z. B. `@app.ts#5-10`). Klicken Sie auf den Auswahlindikator, um umzuschalten, ob Claude Ihren hervorgehobenen Text sehen kann – das Symbol mit durchgestrichenem Auge bedeutet, dass die Auswahl vor Claude verborgen ist.

Sie können auch `Shift` gedrückt halten, während Sie Dateien in das Eingabefeld ziehen, um sie als Anhänge hinzuzufügen. Klicken Sie auf das X bei einem Anhang, um ihn aus dem Kontext zu entfernen.

### Frühere Gespräche fortsetzen

Klicken Sie auf das Dropdown-Menü oben im Claude Code-Panel, um auf Ihren Gesprächsverlauf zuzugreifen. Sie können nach Schlüsselwort suchen oder nach Zeit durchsuchen (Heute, Gestern, Letzte 7 Tage usw.). Klicken Sie auf ein beliebiges Gespräch, um es mit dem vollständigen Nachrichtenverlauf fortzusetzen. Bewegen Sie den Mauszeiger über eine Sitzung, um Umbenennungs- und Entfernungsaktionen anzuzeigen: Benennen Sie um, um ihr einen beschreibenden Titel zu geben, oder entfernen Sie sie, um sie aus der Liste zu löschen. Weitere Informationen zum Fortsetzen von Sitzungen finden Sie unter [Häufige Workflows](/de/common-workflows#resume-previous-conversations).

### Fortsetzen von Remote-Sitzungen von Claude.ai

Wenn Sie [Claude Code im Web](/de/claude-code-on-the-web) verwenden, können Sie diese Remote-Sitzungen direkt in VS Code fortsetzen. Dies erfordert die Anmeldung mit **Claude.ai Subscription**, nicht Anthropic Console.

<Steps>
  <Step title="Öffnen Sie Frühere Gespräche">
    Klicken Sie auf das Dropdown-Menü **Past Conversations** oben im Claude Code-Panel.
  </Step>

  <Step title="Wählen Sie die Remote-Registerkarte">
    Der Dialog zeigt zwei Registerkarten: Local und Remote. Klicken Sie auf **Remote**, um Sitzungen von claude.ai anzuzeigen.
  </Step>

  <Step title="Wählen Sie eine Sitzung zum Fortsetzen">
    Durchsuchen oder suchen Sie Ihre Remote-Sitzungen. Klicken Sie auf eine beliebige Sitzung, um sie herunterzuladen und das Gespräch lokal fortzusetzen.
  </Step>
</Steps>

<Note>
  Nur Web-Sitzungen, die mit einem GitHub-Repository gestartet wurden, werden auf der Remote-Registerkarte angezeigt. Das Fortsetzen lädt den Gesprächsverlauf lokal; Änderungen werden nicht mit claude.ai synchronisiert.
</Note>

## Passen Sie Ihren Workflow an

Sobald Sie einsatzbereit sind, können Sie das Claude-Panel repositionieren, mehrere Sitzungen ausführen oder zum Terminal-Modus wechseln.

### Wählen Sie, wo Claude lebt

Sie können das Claude-Panel ziehen, um es überall in VS Code zu repositionieren. Greifen Sie die Registerkarte oder Titelleiste des Panels und ziehen Sie es zu:

* **Sekundäre Seitenleiste**: die rechte Seite des Fensters. Hält Claude sichtbar, während Sie codieren.
* **Primäre Seitenleiste**: die linke Seitenleiste mit Symbolen für Explorer, Search usw.
* **Editor-Bereich**: öffnet Claude als Registerkarte neben Ihren Dateien. Nützlich für Nebenaufgaben.

<Tip>
  Verwenden Sie die Seitenleiste für Ihre Haupt-Claude-Sitzung und öffnen Sie zusätzliche Registerkarten für Nebenaufgaben. Claude merkt sich Ihren bevorzugten Ort. Das Symbol der Sitzungsliste in der Aktivitätsleiste ist separat vom Claude-Panel: Die Sitzungsliste ist immer in der Aktivitätsleiste sichtbar, während das Claude-Panel-Symbol nur dort angezeigt wird, wenn das Panel an der linken Seitenleiste angedockt ist.
</Tip>

### Führen Sie mehrere Gespräche aus

Verwenden Sie **Open in New Tab** oder **Open in New Window** aus der Befehlspalette, um zusätzliche Gespräche zu starten. Jedes Gespräch behält seinen eigenen Verlauf und Kontext bei, sodass Sie parallel an verschiedenen Aufgaben arbeiten können.

Bei Verwendung von Registerkarten zeigt ein kleiner farbiger Punkt auf dem Spark-Symbol den Status an: Blau bedeutet, dass eine Genehmigungsanfrage ausstehend ist, Orange bedeutet, dass Claude fertig ist, während die Registerkarte verborgen war.

### Wechseln Sie zum Terminal-Modus

Standardmäßig öffnet die Erweiterung ein grafisches Chat-Panel. Wenn Sie die CLI-ähnliche Benutzeroberfläche bevorzugen, öffnen Sie die [Use Terminal-Einstellung](vscode://settings/claudeCode.useTerminal) und aktivieren Sie das Kontrollkästchen.

Sie können auch VS Code-Einstellungen öffnen (`Cmd+,` auf Mac oder `Ctrl+,` auf Windows/Linux), zu Extensions → Claude Code gehen und **Use Terminal** aktivieren.

## Verwalten Sie Plugins

Die VS Code-Erweiterung enthält eine grafische Benutzeroberfläche zum Installieren und Verwalten von [plugins](/de/plugins). Geben Sie `/plugins` in das Eingabefeld ein, um die Benutzeroberfläche **Manage plugins** zu öffnen.

### Installieren Sie Plugins

Der Plugin-Dialog zeigt zwei Registerkarten: **Plugins** und **Marketplaces**.

Auf der Registerkarte 'Plugins":

* **Installed plugins** werden oben mit Umschaltern angezeigt, um sie zu aktivieren oder zu deaktivieren
* **Available plugins** aus Ihren konfigurierten Marketplaces werden unten angezeigt
* Suchen Sie, um Plugins nach Name oder Beschreibung zu filtern
* Klicken Sie auf **Install** bei einem beliebigen verfügbaren Plugin

Wenn Sie ein Plugin installieren, wählen Sie den Installationsumfang:

* **Install for you**: verfügbar in allen Ihren Projekten (Benutzerumfang)
* **Install for this project**: geteilt mit Projektmitarbeitern (Projektumfang)
* **Install locally**: nur für Sie, nur in diesem Repository (lokaler Umfang)

### Verwalten Sie Marketplaces

Wechseln Sie zur Registerkarte **Marketplaces**, um Plugin-Quellen hinzuzufügen oder zu entfernen:

* Geben Sie ein GitHub-Repo, eine URL oder einen lokalen Pfad ein, um einen neuen Marketplace hinzuzufügen
* Klicken Sie auf das Aktualisierungssymbol, um die Plugin-Liste eines Marketplace zu aktualisieren
* Klicken Sie auf das Papierkorbsymbol, um einen Marketplace zu entfernen

Nach dem Vornehmen von Änderungen fordert ein Banner Sie auf, Claude Code neu zu starten, um die Aktualisierungen anzuwenden.

<Note>
  Die Plugin-Verwaltung in VS Code verwendet unter der Haube die gleichen CLI-Befehle. Plugins und Marketplaces, die Sie in der Erweiterung konfigurieren, sind auch in der CLI verfügbar, und umgekehrt.
</Note>

Weitere Informationen zum Plugin-System finden Sie unter [Plugins](/de/plugins) und [Plugin marketplaces](/de/plugin-marketplaces).

## Automatisieren Sie Browser-Aufgaben mit Chrome

Verbinden Sie Claude mit Ihrem Chrome-Browser, um Web-Apps zu testen, mit Konsolenprotokollen zu debuggen und Browser-Workflows zu automatisieren, ohne VS Code zu verlassen. Dies erfordert die [Claude in Chrome-Erweiterung](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) Version 1.0.36 oder höher.

Geben Sie `@browser` in das Eingabefeld ein, gefolgt von dem, was Claude tun soll:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

Sie können auch das Anhang-Menü öffnen, um bestimmte Browser-Tools wie das Öffnen einer neuen Registerkarte oder das Lesen von Seiteninhalten auszuwählen.

Claude öffnet neue Registerkarten für Browser-Aufgaben und teilt den Anmeldestatus Ihres Browsers, sodass es auf jede Website zugreifen kann, bei der Sie bereits angemeldet sind.

Anweisungen zum Einrichten, die vollständige Liste der Funktionen und Fehlerbehebung finden Sie unter [Claude Code mit Chrome verwenden](/de/chrome).

## VS Code-Befehle und Tastaturkürzel

Öffnen Sie die Befehlspalette (`Cmd+Shift+P` auf Mac oder `Ctrl+Shift+P` auf Windows/Linux) und geben Sie „Claude Code" ein, um alle verfügbaren VS Code-Befehle für die Claude Code-Erweiterung anzuzeigen.

Einige Tastaturkürzel hängen davon ab, welches Panel „fokussiert" ist (Tastatureingabe empfängt). Wenn sich Ihr Cursor in einer Codedatei befindet, ist der Editor fokussiert. Wenn sich Ihr Cursor im Eingabefeld von Claude befindet, ist Claude fokussiert. Verwenden Sie `Cmd+Esc` / `Ctrl+Esc`, um zwischen ihnen zu wechseln.

<Note>
  Dies sind VS Code-Befehle zum Steuern der Erweiterung. Nicht alle integrierten Claude Code-Befehle sind in der Erweiterung verfügbar. Siehe [VS Code-Erweiterung vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) für Details.
</Note>

| Befehl                     | Tastaturkürzel                                           | Beschreibung                                                                                            |
| -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Fokus zwischen Editor und Claude umschalten                                                             |
| Open in Side Bar           | -                                                        | Öffnen Sie Claude in der linken Seitenleiste                                                            |
| Open in Terminal           | -                                                        | Öffnen Sie Claude im Terminal-Modus                                                                     |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Öffnen Sie ein neues Gespräch als Editor-Registerkarte                                                  |
| Open in New Window         | -                                                        | Öffnen Sie ein neues Gespräch in einem separaten Fenster                                                |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Starten Sie ein neues Gespräch (erfordert, dass Claude fokussiert ist)                                  |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Fügen Sie eine Referenz zur aktuellen Datei und Auswahl ein (erfordert, dass der Editor fokussiert ist) |
| Show Logs                  | -                                                        | Zeigen Sie Erweiterungs-Debug-Protokolle an                                                             |
| Logout                     | -                                                        | Melden Sie sich von Ihrem Anthropic-Konto ab                                                            |

## Konfigurieren Sie Einstellungen

Die Erweiterung hat zwei Arten von Einstellungen:

* **Extension settings** in VS Code: Steuern Sie das Verhalten der Erweiterung in VS Code. Öffnen Sie mit `Cmd+,` (Mac) oder `Ctrl+,` (Windows/Linux), dann gehen Sie zu Extensions → Claude Code. Sie können auch `/` eingeben und **General Config** auswählen, um Einstellungen zu öffnen.
* **Claude Code settings** in `~/.claude/settings.json`: Geteilt zwischen der Erweiterung und CLI. Verwenden Sie für zulässige Befehle, Umgebungsvariablen, hooks und MCP servers. Siehe [Settings](/de/settings) für Details.

<Tip>
  Fügen Sie `"$schema": "https://json.schemastore.org/claude-code-settings.json"` zu Ihrer `settings.json` hinzu, um Autovervollständigung und Inline-Validierung für alle verfügbaren Einstellungen direkt in VS Code zu erhalten.
</Tip>

### Extension-Einstellungen

| Einstellung                       | Standard  | Beschreibung                                                                                                                                |
| --------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default` | Modell für neue Gespräche. Ändern Sie pro Sitzung mit `/model`.                                                                             |
| `useTerminal`                     | `false`   | Starten Sie Claude im Terminal-Modus statt im grafischen Panel                                                                              |
| `initialPermissionMode`           | `default` | Steuert Genehmigungsaufforderungen: `default` (jedes Mal fragen), `plan`, `acceptEdits` oder `bypassPermissions`                            |
| `preferredLocation`               | `panel`   | Wo Claude öffnet: `sidebar` (rechts) oder `panel` (neue Registerkarte)                                                                      |
| `autosave`                        | `true`    | Speichern Sie Dateien automatisch, bevor Claude sie liest oder schreibt                                                                     |
| `useCtrlEnterToSend`              | `false`   | Verwenden Sie Ctrl/Cmd+Enter statt Enter, um Eingabeaufforderungen zu senden                                                                |
| `enableNewConversationShortcut`   | `true`    | Aktivieren Sie Cmd/Ctrl+N, um ein neues Gespräch zu starten                                                                                 |
| `hideOnboarding`                  | `false`   | Blenden Sie die Onboarding-Checkliste aus (Abschlusskappe-Symbol)                                                                           |
| `respectGitIgnore`                | `true`    | Schließen Sie .gitignore-Muster aus Dateisuchvorgängen aus                                                                                  |
| `environmentVariables`            | `[]`      | Legen Sie Umgebungsvariablen für den Claude-Prozess fest. Verwenden Sie stattdessen Claude Code-Einstellungen für gemeinsame Konfiguration. |
| `disableLoginPrompt`              | `false`   | Überspringen Sie Authentifizierungsaufforderungen (für Setups von Drittanbietern)                                                           |
| `allowDangerouslySkipPermissions` | `false`   | Umgehen Sie alle Genehmigungsaufforderungen. **Verwenden Sie mit äußerster Vorsicht.**                                                      |
| `claudeProcessWrapper`            | -         | Ausführbarer Pfad, der zum Starten des Claude-Prozesses verwendet wird                                                                      |

## VS Code-Erweiterung vs. Claude Code CLI

Claude Code ist sowohl als VS Code-Erweiterung (grafisches Panel) als auch als CLI (Befehlszeilenschnittstelle im Terminal) verfügbar. Einige Funktionen sind nur in der CLI verfügbar. Wenn Sie eine CLI-only-Funktion benötigen, führen Sie `claude` im integrierten Terminal von VS Code aus.

| Funktion            | CLI                                            | VS Code-Erweiterung                                                                                   |
| ------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Commands and skills | [Alle](/de/interactive-mode#built-in-commands) | Teilmenge (geben Sie `/` ein, um verfügbare anzuzeigen)                                               |
| MCP server config   | Ja                                             | Teilweise (fügen Sie Server über CLI hinzu; verwalten Sie vorhandene Server mit `/mcp` im Chat-Panel) |
| Checkpoints         | Ja                                             | Ja                                                                                                    |
| `!` bash shortcut   | Ja                                             | Nein                                                                                                  |
| Tab completion      | Ja                                             | Nein                                                                                                  |

### Zurückspulen mit Checkpoints

Die VS Code-Erweiterung unterstützt Checkpoints, die Claudes Dateibearbeitungen verfolgen und es Ihnen ermöglichen, zu einem vorherigen Zustand zurückzuspulen. Bewegen Sie den Mauszeiger über eine beliebige Nachricht, um die Zurückspul-Schaltfläche anzuzeigen, und wählen Sie dann aus drei Optionen:

* **Fork conversation from here**: Starten Sie einen neuen Gesprächszweig von dieser Nachricht aus, während Sie alle Codeänderungen intakt halten
* **Rewind code to here**: Setzen Sie Dateiänderungen auf diesen Punkt im Gespräch zurück, während Sie den vollständigen Gesprächsverlauf behalten
* **Fork conversation and rewind code**: Starten Sie einen neuen Gesprächszweig und setzen Sie Dateiänderungen auf diesen Punkt zurück

Vollständige Details zur Funktionsweise von Checkpoints und deren Einschränkungen finden Sie unter [Checkpointing](/de/checkpointing).

### Führen Sie CLI in VS Code aus

Um die CLI zu verwenden und in VS Code zu bleiben, öffnen Sie das integrierte Terminal (`` Ctrl+` `` auf Windows/Linux oder `` Cmd+` `` auf Mac) und führen Sie `claude` aus. Die CLI wird automatisch mit Ihrer IDE für Funktionen wie Diff-Anzeige und Diagnosefreigabe integriert.

Wenn Sie ein externes Terminal verwenden, führen Sie `/ide` in Claude Code aus, um es mit VS Code zu verbinden.

### Wechseln Sie zwischen Erweiterung und CLI

Die Erweiterung und CLI teilen den gleichen Gesprächsverlauf. Um ein Erweiterungsgespräch in der CLI fortzusetzen, führen Sie `claude --resume` im Terminal aus. Dies öffnet eine interaktive Auswahl, in der Sie Ihr Gespräch suchen und auswählen können.

### Beziehen Sie Terminal-Ausgabe in Eingabeaufforderungen ein

Referenzieren Sie Terminal-Ausgabe in Ihren Eingabeaufforderungen mit `@terminal:name`, wobei `name` der Titel des Terminals ist. Dies ermöglicht Claude, Befehlsausgabe, Fehlermeldungen oder Protokolle zu sehen, ohne zu kopieren und einzufügen.

### Überwachen Sie Hintergrundprozesse

Wenn Claude lange laufende Befehle ausführt, zeigt die Erweiterung den Fortschritt in der Statusleiste an. Die Sichtbarkeit für Hintergrundaufgaben ist jedoch im Vergleich zur CLI begrenzt. Für bessere Sichtbarkeit lassen Sie Claude den Befehl ausgeben, damit Sie ihn im integrierten Terminal von VS Code ausführen können.

### Verbinden Sie sich mit externen Tools mit MCP

MCP (Model Context Protocol) servers geben Claude Zugriff auf externe Tools, Datenbanken und APIs.

Um einen MCP server hinzuzufügen, öffnen Sie das integrierte Terminal (`` Ctrl+` `` oder `` Cmd+` ``) und führen Sie aus:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Nach der Konfiguration bitten Sie Claude, die Tools zu verwenden (z. B. „Review PR #456").

Um MCP servers zu verwalten, ohne VS Code zu verlassen, geben Sie `/mcp` im Chat-Panel ein. Der MCP-Verwaltungsdialog ermöglicht es Ihnen, Server zu aktivieren oder zu deaktivieren, sich erneut mit einem Server zu verbinden und OAuth-Authentifizierung zu verwalten. Siehe die [MCP-Dokumentation](/de/mcp) für verfügbare servers.

## Arbeiten Sie mit Git

Claude Code wird mit Git integriert, um Versionskontroll-Workflows direkt in VS Code zu unterstützen. Bitten Sie Claude, Änderungen zu committen, Pull Requests zu erstellen oder über Branches zu arbeiten.

### Erstellen Sie Commits und Pull Requests

Claude kann Änderungen bereitstellen, Commit-Nachrichten schreiben und Pull Requests basierend auf Ihrer Arbeit erstellen:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Beim Erstellen von Pull Requests generiert Claude Beschreibungen basierend auf den tatsächlichen Codeänderungen und kann Kontext über Tests oder Implementierungsentscheidungen hinzufügen.

### Verwenden Sie Git Worktrees für parallele Aufgaben

Verwenden Sie das Flag `--worktree` (`-w`), um Claude in einem isolierten Worktree mit seinen eigenen Dateien und Branch zu starten:

```bash  theme={null}
claude --worktree feature-auth
```

Jeder Worktree behält einen unabhängigen Dateizustand bei, während er die Git-Historie teilt. Dies verhindert, dass Claude-Instanzen sich gegenseitig beeinflussen, wenn sie an verschiedenen Aufgaben arbeiten. Weitere Details finden Sie unter [Führen Sie parallele Claude Code-Sitzungen mit Git Worktrees aus](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

## Verwenden Sie Drittanbieter

Standardmäßig verbindet sich Claude Code direkt mit der API von Anthropic. Wenn Ihre Organisation Amazon Bedrock, Google Vertex AI oder Microsoft Foundry verwendet, um auf Claude zuzugreifen, konfigurieren Sie die Erweiterung, um stattdessen Ihren Anbieter zu verwenden:

<Steps>
  <Step title="Deaktivieren Sie die Anmeldungsaufforderung">
    Öffnen Sie die [Disable Login Prompt-Einstellung](vscode://settings/claudeCode.disableLoginPrompt) und aktivieren Sie das Kontrollkästchen.

    Sie können auch VS Code-Einstellungen öffnen (`Cmd+,` auf Mac oder `Ctrl+,` auf Windows/Linux), nach 'Claude Code login" suchen und **Disable Login Prompt** aktivieren.
  </Step>

  <Step title="Konfigurieren Sie Ihren Anbieter">
    Folgen Sie dem Setup-Leitfaden für Ihren Anbieter:

    * [Claude Code auf Amazon Bedrock](/de/amazon-bedrock)
    * [Claude Code auf Google Vertex AI](/de/google-vertex-ai)
    * [Claude Code auf Microsoft Foundry](/de/microsoft-foundry)

    Diese Leitfäden behandeln die Konfiguration Ihres Anbieters in `~/.claude/settings.json`, was sicherstellt, dass Ihre Einstellungen zwischen der VS Code-Erweiterung und der CLI geteilt werden.
  </Step>
</Steps>

## Sicherheit und Datenschutz

Ihr Code bleibt privat. Claude Code verarbeitet Ihren Code, um Unterstützung zu bieten, verwendet ihn aber nicht zum Trainieren von Modellen. Weitere Informationen zur Datenbehandlung und zum Deaktivieren der Protokollierung finden Sie unter [Data and privacy](/de/data-usage).

Mit aktivierten Auto-Edit-Berechtigungen kann Claude Code VS Code-Konfigurationsdateien (wie `settings.json` oder `tasks.json`) ändern, die VS Code möglicherweise automatisch ausführt. Um das Risiko bei der Arbeit mit nicht vertrauenswürdigem Code zu verringern:

* Aktivieren Sie [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) für nicht vertrauenswürdige Workspaces
* Verwenden Sie den manuellen Genehmigungsmodus statt Auto-Accept für Bearbeitungen
* Überprüfen Sie Änderungen sorgfältig, bevor Sie sie akzeptieren

## Beheben Sie häufige Probleme

### Erweiterung wird nicht installiert

* Stellen Sie sicher, dass Sie eine kompatible Version von VS Code haben (1.98.0 oder später)
* Überprüfen Sie, dass VS Code die Berechtigung zum Installieren von Erweiterungen hat
* Versuchen Sie, direkt vom [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) zu installieren

### Spark-Symbol nicht sichtbar

Das Spark-Symbol wird in der **Editor-Symbolleiste** (oben rechts des Editors) angezeigt, wenn Sie eine Datei geöffnet haben. Wenn Sie es nicht sehen:

1. **Öffnen Sie eine Datei**: Das Symbol erfordert, dass eine Datei geöffnet ist. Nur einen Ordner zu öffnen reicht nicht aus.
2. **Überprüfen Sie die VS Code-Version**: Erfordert 1.98.0 oder höher (Help → About)
3. **Starten Sie VS Code neu**: Führen Sie 'Developer: Reload Window" aus der Befehlspalette aus
4. **Deaktivieren Sie konfliktverursachende Erweiterungen**: Deaktivieren Sie vorübergehend andere KI-Erweiterungen (Cline, Continue usw.)
5. **Überprüfen Sie die Workspace-Vertrauenswürdigkeit**: Die Erweiterung funktioniert nicht im Restricted Mode

Alternativ klicken Sie auf „✱ Claude Code" in der **Statusleiste** (untere rechte Ecke). Dies funktioniert auch ohne eine geöffnete Datei. Sie können auch die **Befehlspalette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) verwenden und „Claude Code" eingeben.

### Claude Code antwortet nie

Wenn Claude Code nicht auf Ihre Eingabeaufforderungen antwortet:

1. **Überprüfen Sie Ihre Internetverbindung**: Stellen Sie sicher, dass Sie eine stabile Internetverbindung haben
2. **Starten Sie ein neues Gespräch**: Versuchen Sie, ein neues Gespräch zu starten, um zu sehen, ob das Problem weiterhin besteht
3. **Versuchen Sie die CLI**: Führen Sie `claude` vom Terminal aus, um detailliertere Fehlermeldungen zu erhalten

Wenn Probleme weiterhin bestehen, [melden Sie ein Problem auf GitHub](https://github.com/anthropics/claude-code/issues) mit Details zum Fehler.

## Deinstallieren Sie die Erweiterung

So deinstallieren Sie die Claude Code-Erweiterung:

1. Öffnen Sie die Ansicht „Erweiterungen" (`Cmd+Shift+X` auf Mac oder `Ctrl+Shift+X` auf Windows/Linux)
2. Suchen Sie nach „Claude Code"
3. Klicken Sie auf **Uninstall**

Um auch Erweiterungsdaten zu entfernen und alle Einstellungen zurückzusetzen:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Weitere Hilfe finden Sie im [Troubleshooting-Leitfaden](/de/troubleshooting).

## Nächste Schritte

Jetzt, da Sie Claude Code in VS Code eingerichtet haben:

* [Erkunden Sie häufige Workflows](/de/common-workflows), um das Beste aus Claude Code herauszuholen
* [Richten Sie MCP servers ein](/de/mcp), um Claudes Funktionen mit externen Tools zu erweitern. Fügen Sie Server über die CLI hinzu und verwalten Sie sie dann mit `/mcp` im Chat-Panel.
* [Konfigurieren Sie Claude Code-Einstellungen](/de/settings), um zulässige Befehle, hooks und mehr anzupassen. Diese Einstellungen werden zwischen der Erweiterung und CLI geteilt.
