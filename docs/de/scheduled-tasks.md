> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Prompts nach Zeitplan ausführen

> Verwenden Sie /loop und die Cron-Planungstools, um Prompts wiederholt auszuführen, den Status abzurufen oder einmalige Erinnerungen innerhalb einer Claude Code-Sitzung zu setzen.

<Note>
  Geplante Aufgaben erfordern Claude Code v2.1.72 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

Geplante Aufgaben ermöglichen es Claude, einen Prompt automatisch in regelmäßigen Abständen erneut auszuführen. Verwenden Sie sie, um eine Bereitstellung abzurufen, einen PR zu überwachen, einen langwierigen Build zu überprüfen oder sich später in der Sitzung an etwas zu erinnern. Um auf Ereignisse zu reagieren, während sie geschehen, anstatt abzurufen, siehe [Kanäle](/de/channels): Ihr CI kann den Fehler direkt in die Sitzung übertragen.

Aufgaben sind sitzungsbezogen: Sie existieren im aktuellen Claude Code-Prozess und sind weg, wenn Sie beenden. Für dauerhafte Planung, die Neustarts übersteht, verwenden Sie [Routinen](/de/routines), [Desktop-geplante Aufgaben](/de/desktop-scheduled-tasks) oder [GitHub Actions](/de/github-actions).

## Vergleichen Sie Planungsoptionen

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Führen Sie einen Prompt wiederholt mit /loop aus

Die `/loop` [bundled skill](/de/commands) ist der schnellste Weg, um einen Prompt wiederholt auszuführen, während die Sitzung offen bleibt. Sowohl das Intervall als auch der Prompt sind optional, und das, was Sie bereitstellen, bestimmt, wie sich die Schleife verhält.

| Was Sie bereitstellen     | Beispiel                    | Was passiert                                                                                                       |
| :------------------------ | :-------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| Intervall und Prompt      | `/loop 5m check the deploy` | Ihr Prompt läuft nach einem [festen Zeitplan](#run-on-a-fixed-interval)                                            |
| Nur Prompt                | `/loop check the deploy`    | Ihr Prompt läuft in einem [Intervall, das Claude wählt](#let-claude-choose-the-interval) bei jeder Iteration       |
| Nur Intervall oder nichts | `/loop`                     | Der [integrierte Wartungs-Prompt](#run-the-built-in-maintenance-prompt) läuft, oder Ihr `loop.md`, falls vorhanden |

Sie können auch einen anderen Befehl als Prompt übergeben, zum Beispiel `/loop 20m /review-pr 1234`, um einen verpackten Workflow bei jeder Iteration erneut auszuführen.

### Führen Sie nach einem festen Intervall aus

Wenn Sie ein Intervall angeben, konvertiert Claude es in einen Cron-Ausdruck, plant den Job und bestätigt die Häufigkeit und die Job-ID.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Das Intervall kann dem Prompt als einfaches Token wie `30m` vorangehen oder als Klausel wie `every 2 hours` folgen. Unterstützte Einheiten sind `s` für Sekunden, `m` für Minuten, `h` für Stunden und `d` für Tage.

Sekunden werden auf die nächste Minute aufgerundet, da Cron eine Granularität von einer Minute hat. Intervalle, die nicht gleichmäßig in einen sauberen Cron-Schritt abgebildet werden, wie `7m` oder `90m`, werden auf das nächste Intervall gerundet, das dies tut, und Claude teilt Ihnen mit, was es gewählt hat.

### Lassen Sie Claude das Intervall wählen

Wenn Sie das Intervall weglassen, wählt Claude stattdessen dynamisch eines, anstatt nach einem festen Cron-Zeitplan zu laufen. Nach jeder Iteration wählt es eine Verzögerung zwischen einer Minute und einer Stunde basierend auf dem, was es beobachtet hat: kurze Wartezeiten, während ein Build fertig wird oder ein PR aktiv ist, längere Wartezeiten, wenn nichts ansteht. Die gewählte Verzögerung und der Grund dafür werden am Ende jeder Iteration gedruckt.

Das folgende Beispiel überprüft CI und Überprüfungskommentare, wobei Claude länger zwischen Iterationen wartet, sobald der PR ruhig wird:

```text theme={null}
/loop check whether CI passed and address any review comments
```

Wenn Sie einen dynamischen `/loop`-Zeitplan anfordern, kann Claude das [Monitor-Tool](/de/tools-reference#monitor-tool) direkt verwenden. Monitor führt ein Hintergrundskript aus und streamt jede Ausgabezeile zurück, was das Abrufen ganz vermeidet und oft token-effizienter und reaktiver ist als das erneute Ausführen eines Prompts in einem Intervall.

Eine dynamisch geplante Schleife erscheint in Ihrer [geplanten Aufgabenliste](#manage-scheduled-tasks) wie jede andere Aufgabe, sodass Sie sie auf die gleiche Weise auflisten oder stornieren können. Die [Jitter-Regeln](#jitter) gelten nicht dafür, aber die [sieben-Tage-Ablauf](#seven-day-expiry) tut es: die Schleife endet automatisch sieben Tage nach dem Start.

<Note>
  Bei Bedrock, Vertex AI und Microsoft Foundry läuft ein Prompt ohne Intervall stattdessen nach einem festen 10-Minuten-Zeitplan.
</Note>

### Führen Sie den integrierten Wartungs-Prompt aus

Wenn Sie den Prompt weglassen, verwendet Claude stattdessen einen integrierten Wartungs-Prompt. Bei jeder Iteration arbeitet es folgende Punkte in dieser Reihenfolge durch:

* Fortsetzen unvollendeter Arbeiten aus dem Gespräch
* Kümmern Sie sich um den Pull Request des aktuellen Branches: Überprüfungskommentare, fehlgeschlagene CI-Läufe, Merge-Konflikte
* Führen Sie Bereinigungsdurchläufe durch, wie Fehlersuche oder Vereinfachung, wenn nichts anderes ansteht

Claude startet keine neuen Initiativen außerhalb dieses Umfangs, und irreversible Aktionen wie Pushing oder Löschen erfolgen nur, wenn sie etwas fortsetzen, das das Transkript bereits autorisiert hat.

```text theme={null}
/loop
```

Ein einfaches `/loop` führt diesen Prompt in einem [dynamisch gewählten Intervall](#let-claude-choose-the-interval) aus. Fügen Sie ein Intervall hinzu, zum Beispiel `/loop 15m`, um es stattdessen nach einem festen Zeitplan auszuführen. Um den integrierten Prompt durch Ihren eigenen Standard zu ersetzen, siehe [Passen Sie den Standard-Prompt mit loop.md an](#customize-the-default-prompt-with-loop-md).

<Note>
  Bei Bedrock, Vertex AI und Microsoft Foundry druckt `/loop` ohne Prompt die Nutzungsmeldung aus, anstatt die Wartungsschleife zu starten.
</Note>

### Passen Sie den Standard-Prompt mit loop.md an

Eine `loop.md`-Datei ersetzt den integrierten Wartungs-Prompt durch Ihre eigenen Anweisungen. Sie definiert einen einzelnen Standard-Prompt für einfaches `/loop`, nicht eine Liste separater geplanter Aufgaben, und wird ignoriert, wenn Sie einen Prompt in der Befehlszeile angeben. Um zusätzliche Prompts daneben zu planen, verwenden Sie `/loop <prompt>` oder [fragen Sie Claude direkt](#manage-scheduled-tasks).

Claude sucht die Datei an zwei Orten und verwendet die erste, die er findet.

| Pfad                | Umfang                                                                  |
| :------------------ | :---------------------------------------------------------------------- |
| `.claude/loop.md`   | Projektebene. Hat Vorrang, wenn beide Dateien vorhanden sind.           |
| `~/.claude/loop.md` | Benutzerebene. Gilt in jedem Projekt, das sein eigenes nicht definiert. |

Die Datei ist einfaches Markdown ohne erforderliche Struktur. Schreiben Sie sie so, als würden Sie den `/loop`-Prompt direkt eingeben. Das folgende Beispiel hält einen Release-Branch gesund:

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

Änderungen an `loop.md` treten bei der nächsten Iteration in Kraft, sodass Sie die Anweisungen verfeinern können, während eine Schleife läuft. Wenn keine `loop.md` an einem der beiden Orte vorhanden ist, fällt die Schleife auf den integrierten Wartungs-Prompt zurück. Halten Sie die Datei prägnant: Inhalte über 25.000 Bytes werden gekürzt.

## Setzen Sie eine einmalige Erinnerung

Für einmalige Erinnerungen beschreiben Sie, was Sie möchten, in natürlicher Sprache, anstatt `/loop` zu verwenden. Claude plant eine einmalige Aufgabe, die sich nach der Ausführung selbst löscht.

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude heftet die Ausführungszeit an eine bestimmte Minute und Stunde mit einem Cron-Ausdruck an und bestätigt, wann sie läuft.

## Verwalten Sie geplante Aufgaben

Bitten Sie Claude in natürlicher Sprache, Aufgaben aufzulisten oder zu stornieren, oder verweisen Sie direkt auf die zugrunde liegenden Tools.

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

Unter der Haube verwendet Claude diese Tools:

| Tool         | Zweck                                                                                                                                         |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `CronCreate` | Planen Sie eine neue Aufgabe. Akzeptiert einen 5-Feld-Cron-Ausdruck, den auszuführenden Prompt und ob er wiederkehrend ist oder einmal läuft. |
| `CronList`   | Listet alle geplanten Aufgaben mit ihren IDs, Zeitplänen und Prompts auf.                                                                     |
| `CronDelete` | Stornieren Sie eine Aufgabe nach ID.                                                                                                          |

Jede geplante Aufgabe hat eine 8-stellige ID, die Sie an `CronDelete` übergeben können. Eine Sitzung kann gleichzeitig bis zu 50 geplante Aufgaben enthalten.

## Wie geplante Aufgaben ausgeführt werden

Der Scheduler überprüft jede Sekunde auf fällige Aufgaben und reiht sie mit niedriger Priorität ein. Ein geplanter Prompt läuft zwischen Ihren Zügen, nicht während Claude mitten in einer Antwort ist. Wenn Claude beschäftigt ist, wenn eine Aufgabe fällig wird, wartet der Prompt, bis der aktuelle Zug endet.

Alle Zeiten werden in Ihrer lokalen Zeitzone interpretiert. Ein Cron-Ausdruck wie `0 9 * * *` bedeutet 9 Uhr, wo immer Sie Claude Code ausführen, nicht UTC.

### Jitter

Um zu vermeiden, dass jede Sitzung die API zum gleichen Wanduhrzeitpunkt trifft, fügt der Scheduler einen kleinen deterministischen Offset zu Ausführungszeiten hinzu:

* Wiederkehrende Aufgaben laufen bis zu 10% ihrer Periode zu spät, begrenzt auf 15 Minuten. Ein stündlicher Job könnte überall von `:00` bis `:06` laufen.
* Einmalige Aufgaben, die für die Ober- oder Unterseite der Stunde geplant sind, laufen bis zu 90 Sekunden früh.

Der Offset wird von der Aufgaben-ID abgeleitet, daher erhält die gleiche Aufgabe immer den gleichen Offset. Wenn genaue Zeitangaben wichtig sind, wählen Sie eine Minute, die nicht `:00` oder `:30` ist, zum Beispiel `3 9 * * *` statt `0 9 * * *`, und der einmalige Jitter wird nicht angewendet.

### Ablauf nach sieben Tagen

Wiederkehrende Aufgaben verfallen automatisch 7 Tage nach der Erstellung. Die Aufgabe läuft ein letztes Mal, dann löscht sie sich selbst. Dies begrenzt, wie lange eine vergessene Schleife laufen kann. Wenn Sie benötigen, dass eine wiederkehrende Aufgabe länger dauert, stornieren und erstellen Sie sie neu, bevor sie abläuft, oder verwenden Sie [Routinen](/de/routines) oder [Desktop-geplante Aufgaben](/de/desktop-scheduled-tasks) für dauerhafte Planung.

## Cron-Ausdrucksreferenz

`CronCreate` akzeptiert Standard-5-Feld-Cron-Ausdrücke: `minute hour day-of-month month day-of-week`. Alle Felder unterstützen Wildcards (`*`), einzelne Werte (`5`), Schritte (`*/15`), Bereiche (`1-5`) und kommagetrennte Listen (`1,15,30`).

| Beispiel       | Bedeutung                     |
| :------------- | :---------------------------- |
| `*/5 * * * *`  | Alle 5 Minuten                |
| `0 * * * *`    | Jede Stunde zur vollen Stunde |
| `7 * * * *`    | Jede Stunde um 7 Minuten nach |
| `0 9 * * *`    | Jeden Tag um 9 Uhr lokal      |
| `0 9 * * 1-5`  | Wochentags um 9 Uhr lokal     |
| `30 14 15 3 *` | 15. März um 14:30 Uhr lokal   |

Der Wochentag verwendet `0` oder `7` für Sonntag bis `6` für Samstag. Erweiterte Syntax wie `L`, `W`, `?` und Namensaliase wie `MON` oder `JAN` werden nicht unterstützt.

Wenn sowohl der Tag des Monats als auch der Wochentag eingeschränkt sind, stimmt ein Datum überein, wenn eines der Felder übereinstimmt. Dies folgt der Standard-Vixie-Cron-Semantik.

## Deaktivieren Sie geplante Aufgaben

Setzen Sie `CLAUDE_CODE_DISABLE_CRON=1` in Ihrer Umgebung, um den Scheduler vollständig zu deaktivieren. Die Cron-Tools und `/loop` werden nicht verfügbar, und alle bereits geplanten Aufgaben stoppen das Laufen. Siehe [Umgebungsvariablen](/de/env-vars) für die vollständige Liste der Deaktivierungsflags.

## Einschränkungen

Die sitzungsbezogene Planung hat inhärente Einschränkungen:

* Aufgaben laufen nur, während Claude Code läuft und untätig ist. Das Schließen des Terminals oder das Beenden der Sitzung storniert alles.
* Kein Aufholen für verpasste Läufe. Wenn die geplante Zeit einer Aufgabe verstreicht, während Claude mit einer langwierigen Anfrage beschäftigt ist, läuft sie einmal, wenn Claude untätig wird, nicht einmal pro verpasstem Intervall.
* Keine Persistenz über Neustarts hinweg. Das Neustarten von Claude Code löscht alle sitzungsbezogenen Aufgaben.

Für Cron-gesteuerte Automatisierung, die unbeaufsichtigt laufen muss:

* [Routinen](/de/routines): Laufen auf von Anthropic verwalteter Infrastruktur nach Zeitplan, über API-Aufruf oder bei GitHub-Ereignissen
* [GitHub Actions](/de/github-actions): Verwenden Sie einen `schedule`-Trigger in CI
* [Desktop-geplante Aufgaben](/de/desktop-scheduled-tasks): Laufen lokal auf Ihrem Computer
