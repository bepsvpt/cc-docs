> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Verfolgen Sie automatisch die Änderungen von Claude und machen Sie unerwünschte Änderungen schnell rückgängig.

Claude Code verfolgt automatisch die Dateiänderungen von Claude während der Arbeit und ermöglicht es Ihnen, Änderungen schnell rückgängig zu machen und zu vorherigen Zuständen zurückzukehren, wenn etwas schiefgeht.

## Wie Checkpointing funktioniert

Während Sie mit Claude arbeiten, erfasst Checkpointing automatisch den Zustand Ihres Codes vor jeder Änderung. Dieses Sicherheitsnetz ermöglicht es Ihnen, ehrgeizige, großflächige Aufgaben zu verfolgen, da Sie immer zu einem vorherigen Code-Zustand zurückkehren können.

### Automatische Verfolgung

Claude Code verfolgt alle Änderungen, die von seinen Datei-Bearbeitungswerkzeugen vorgenommen werden:

* Jede Benutzereingabe erstellt einen neuen Checkpoint
* Checkpoints bleiben über Sitzungen hinweg erhalten, sodass Sie auf sie in fortgesetzten Gesprächen zugreifen können
* Werden automatisch zusammen mit Sitzungen nach 30 Tagen bereinigt (konfigurierbar)

### Änderungen rückgängig machen

Drücken Sie `Esc` zweimal (`Esc` + `Esc`) oder verwenden Sie den `/rewind` Befehl, um das Rewind-Menü zu öffnen. Sie können wählen, um wiederherzustellen:

* **Nur Gespräch**: Zurückspulen zu einer Benutzernachricht, während Code-Änderungen beibehalten werden
* **Nur Code**: Dateiänderungen rückgängig machen, während das Gespräch beibehalten wird
* **Sowohl Code als auch Gespräch**: Beide zu einem früheren Punkt in der Sitzung wiederherstellen

## Häufige Anwendungsfälle

Checkpoints sind besonders nützlich, wenn:

* **Alternativen erkunden**: Versuchen Sie verschiedene Implementierungsansätze, ohne Ihren Ausgangspunkt zu verlieren
* **Von Fehlern wiederherstellen**: Machen Sie schnell Änderungen rückgängig, die Fehler eingeführt oder Funktionalität unterbrochen haben
* **Funktionen iterieren**: Experimentieren Sie mit Variationen, da Sie zu funktionierenden Zuständen zurückkehren können

## Einschränkungen

### Bash-Befehlsänderungen werden nicht verfolgt

Checkpointing verfolgt keine Dateien, die durch Bash-Befehle geändert werden. Wenn Claude Code beispielsweise ausführt:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Diese Dateiänderungen können nicht durch Rewind rückgängig gemacht werden. Nur direkte Dateiänderungen, die durch Claudes Datei-Bearbeitungswerkzeuge vorgenommen werden, werden verfolgt.

### Externe Änderungen werden nicht verfolgt

Checkpointing verfolgt nur Dateien, die in der aktuellen Sitzung bearbeitet wurden. Manuelle Änderungen, die Sie an Dateien außerhalb von Claude Code vornehmen, und Änderungen aus anderen gleichzeitigen Sitzungen werden normalerweise nicht erfasst, es sei denn, sie ändern zufällig dieselben Dateien wie die aktuelle Sitzung.

### Kein Ersatz für Versionskontrolle

Checkpoints sind für schnelle, sitzungsebene Wiederherstellung konzipiert. Für permanente Versionsverlauf und Zusammenarbeit:

* Verwenden Sie weiterhin Versionskontrolle (z. B. Git) für Commits, Branches und langfristige Verlauf
* Checkpoints ergänzen, ersetzen aber nicht ordnungsgemäße Versionskontrolle
* Denken Sie an Checkpoints als „lokales Rückgängigmachen" und Git als „permanente Verlauf"

## Siehe auch

* [Interaktiver Modus](/de/interactive-mode) - Tastaturkürzel und Sitzungssteuerungen
* [Integrierte Befehle](/de/interactive-mode#built-in-commands) - Zugriff auf Checkpoints mit `/rewind`
* [CLI-Referenz](/de/cli-reference) - Befehlszeilenoptionen
