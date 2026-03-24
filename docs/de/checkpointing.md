> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Verfolgen, zurückspulen und fassen Sie Claudes Bearbeitungen und Konversation zusammen, um den Sitzungsstatus zu verwalten.

Claude Code verfolgt automatisch Claudes Dateibearbeitungen während Sie arbeiten, sodass Sie Änderungen schnell rückgängig machen und zu vorherigen Zuständen zurückspulen können, falls etwas schiefgeht.

## Wie Checkpointing funktioniert

Während Sie mit Claude arbeiten, erfasst Checkpointing automatisch den Zustand Ihres Codes vor jeder Bearbeitung. Dieses Sicherheitsnetz ermöglicht es Ihnen, ehrgeizige, großflächige Aufgaben zu verfolgen, da Sie immer zu einem vorherigen Code-Zustand zurückkehren können.

### Automatische Verfolgung

Claude Code verfolgt alle Änderungen, die von seinen Datei-Bearbeitungswerkzeugen vorgenommen werden:

* Jede Benutzereingabe erstellt einen neuen Checkpoint
* Checkpoints bleiben über Sitzungen hinweg erhalten, sodass Sie auf sie in fortgesetzten Konversationen zugreifen können
* Werden automatisch zusammen mit Sitzungen nach 30 Tagen bereinigt (konfigurierbar)

### Zurückspulen und zusammenfassen

Drücken Sie `Esc` zweimal (`Esc` + `Esc`) oder verwenden Sie den `/rewind` Befehl, um das Zurückspul-Menü zu öffnen. Eine scrollbare Liste zeigt jede Ihrer Eingaben aus der Sitzung. Wählen Sie den Punkt aus, auf den Sie einwirken möchten, und wählen Sie dann eine Aktion:

* **Code und Konversation wiederherstellen**: Setzt sowohl Code als auch Konversation auf diesen Punkt zurück
* **Konversation wiederherstellen**: Zurückspulen zu dieser Nachricht, während der aktuelle Code beibehalten wird
* **Code wiederherstellen**: Dateiänderungen rückgängig machen, während die Konversation beibehalten wird
* **Von hier aus zusammenfassen**: Komprimieren Sie die Konversation von diesem Punkt an in eine Zusammenfassung und geben Sie Kontextfensterplatz frei
* **Abbrechen**: Kehren Sie zur Nachrichtenliste zurück, ohne Änderungen vorzunehmen

Nach dem Wiederherstellen der Konversation oder dem Zusammenfassen wird die ursprüngliche Eingabe aus der ausgewählten Nachricht in das Eingabefeld wiederhergestellt, sodass Sie sie erneut senden oder bearbeiten können.

#### Wiederherstellen vs. zusammenfassen

Die drei Wiederherstellungsoptionen setzen den Zustand zurück: Sie machen Code-Änderungen, Konversationsverlauf oder beides rückgängig. „Von hier aus zusammenfassen" funktioniert anders:

* Nachrichten vor der ausgewählten Nachricht bleiben intakt
* Die ausgewählte Nachricht und alle nachfolgenden Nachrichten werden durch eine kompakte KI-generierte Zusammenfassung ersetzt
* Keine Dateien auf der Festplatte werden geändert
* Die ursprünglichen Nachrichten bleiben im Sitzungstranskript erhalten, sodass Claude die Details bei Bedarf referenzieren kann

Dies ähnelt `/compact`, ist aber gezielt: Anstatt die gesamte Konversation zusammenzufassen, behalten Sie frühen Kontext in vollem Detail und komprimieren nur die Teile, die Platz verbrauchen. Sie können optionale Anweisungen eingeben, um zu lenken, worauf sich die Zusammenfassung konzentriert.

<Note>
  Zusammenfassen hält Sie in derselben Sitzung und komprimiert Kontext. Wenn Sie abzweigen und einen anderen Ansatz versuchen möchten, während Sie die ursprüngliche Sitzung intakt bewahren, verwenden Sie stattdessen [fork](/de/how-claude-code-works#resume-or-fork-sessions) (`claude --continue --fork-session`).
</Note>

## Häufige Anwendungsfälle

Checkpoints sind besonders nützlich, wenn:

* **Alternativen erkunden**: Versuchen Sie verschiedene Implementierungsansätze, ohne Ihren Ausgangspunkt zu verlieren
* **Fehler beheben**: Machen Sie schnell Änderungen rückgängig, die Fehler eingeführt oder Funktionalität unterbrochen haben
* **Funktionen iterieren**: Experimentieren Sie mit Variationen, da Sie zu funktionierenden Zuständen zurückkehren können
* **Kontextplatz freigeben**: Fassen Sie eine ausführliche Debugging-Sitzung von der Mitte an zusammen, während Sie Ihre ursprünglichen Anweisungen intakt halten

## Einschränkungen

### Bash-Befehlsänderungen werden nicht verfolgt

Checkpointing verfolgt keine Dateien, die durch Bash-Befehle geändert werden. Wenn Claude Code beispielsweise ausführt:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Diese Dateiänderungen können nicht durch Zurückspulen rückgängig gemacht werden. Nur direkte Dateibearbeitungen, die durch Claudes Datei-Bearbeitungswerkzeuge vorgenommen werden, werden verfolgt.

### Externe Änderungen werden nicht verfolgt

Checkpointing verfolgt nur Dateien, die in der aktuellen Sitzung bearbeitet wurden. Manuelle Änderungen, die Sie an Dateien außerhalb von Claude Code vornehmen, und Bearbeitungen aus anderen gleichzeitigen Sitzungen werden normalerweise nicht erfasst, es sei denn, sie ändern zufällig dieselben Dateien wie die aktuelle Sitzung.

### Kein Ersatz für Versionskontrolle

Checkpoints sind für schnelle, sitzungsebene Wiederherstellung konzipiert. Für permanente Versionshistorie und Zusammenarbeit:

* Verwenden Sie weiterhin Versionskontrolle (z. B. Git) für Commits, Branches und langfristige Historie
* Checkpoints ergänzen, ersetzen aber nicht ordnungsgemäße Versionskontrolle
* Denken Sie an Checkpoints als „lokales Rückgängigmachen" und Git als „permanente Historie"

## Siehe auch

* [Interaktiver Modus](/de/interactive-mode) - Tastaturkürzel und Sitzungssteuerungen
* [Integrierte Befehle](/de/commands) - Zugriff auf Checkpoints mit `/rewind`
* [CLI-Referenz](/de/cli-reference) - Befehlszeilenoptionen
