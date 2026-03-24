> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Prompts nach Zeitplan ausführen

> Verwenden Sie /loop und die Cron-Planungstools, um Prompts wiederholt auszuführen, den Status abzurufen oder einmalige Erinnerungen innerhalb einer Claude Code-Sitzung zu setzen.

<Note>
  Geplante Aufgaben erfordern Claude Code v2.1.72 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

Geplante Aufgaben ermöglichen es Claude, einen Prompt automatisch in regelmäßigen Abständen erneut auszuführen. Verwenden Sie sie, um eine Bereitstellung abzurufen, einen PR zu überwachen, einen langwierigen Build zu überprüfen oder sich später in der Sitzung an etwas zu erinnern.

Aufgaben sind sitzungsbezogen: Sie existieren im aktuellen Claude Code-Prozess und sind weg, wenn Sie beenden. Für dauerhafte Planung, die Neustarts übersteht und ohne aktive Terminalsitzung läuft, siehe [Desktop-geplante Aufgaben](/de/desktop#schedule-recurring-tasks) oder [GitHub Actions](/de/github-actions).

## Planen Sie einen wiederkehrenden Prompt mit /loop

Die `/loop` [bundled skill](/de/skills#bundled-skills) ist der schnellste Weg, um einen wiederkehrenden Prompt zu planen. Übergeben Sie ein optionales Intervall und einen Prompt, und Claude richtet einen Cron-Job ein, der im Hintergrund läuft, während die Sitzung offen bleibt.

```text  theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude analysiert das Intervall, konvertiert es in einen Cron-Ausdruck, plant den Job und bestätigt die Häufigkeit und die Job-ID.

### Intervallsyntax

Intervalle sind optional. Sie können sie am Anfang, am Ende oder gar nicht verwenden.

| Form                         | Beispiel                              | Analysiertes Intervall    |
| :--------------------------- | :------------------------------------ | :------------------------ |
| Führendes Token              | `/loop 30m check the build`           | alle 30 Minuten           |
| Nachfolgende `every`-Klausel | `/loop check the build every 2 hours` | alle 2 Stunden            |
| Kein Intervall               | `/loop check the build`               | Standard: alle 10 Minuten |

Unterstützte Einheiten sind `s` für Sekunden, `m` für Minuten, `h` für Stunden und `d` für Tage. Sekunden werden auf die nächste Minute aufgerundet, da Cron eine Granularität von einer Minute hat. Intervalle, die nicht gleichmäßig in ihre Einheit aufgehen, wie `7m` oder `90m`, werden auf das nächste saubere Intervall gerundet und Claude teilt Ihnen mit, was es gewählt hat.

### Schleife über einen anderen Befehl

Der geplante Prompt kann selbst ein Befehl oder eine Skill-Invokation sein. Dies ist nützlich, um einen Workflow erneut auszuführen, den Sie bereits verpackt haben.

```text  theme={null}
/loop 20m /review-pr 1234
```

Jedes Mal, wenn der Job läuft, führt Claude `/review-pr 1234` aus, als hätten Sie es eingegeben.

## Setzen Sie eine einmalige Erinnerung

Für einmalige Erinnerungen beschreiben Sie, was Sie möchten, in natürlicher Sprache, anstatt `/loop` zu verwenden. Claude plant eine einmalige Aufgabe, die sich nach der Ausführung selbst löscht.

```text  theme={null}
remind me at 3pm to push the release branch
```

```text  theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude heftet die Ausführungszeit an eine bestimmte Minute und Stunde mit einem Cron-Ausdruck an und bestätigt, wann sie läuft.

## Verwalten Sie geplante Aufgaben

Bitten Sie Claude in natürlicher Sprache, Aufgaben aufzulisten oder zu stornieren, oder verweisen Sie direkt auf die zugrunde liegenden Tools.

```text  theme={null}
what scheduled tasks do I have?
```

```text  theme={null}
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

* Wiederkehrende Aufgaben läuft bis zu 10% ihrer Periode zu spät, begrenzt auf 15 Minuten. Ein stündlicher Job könnte überall von `:00` bis `:06` laufen.
* Einmalige Aufgaben, die für die Ober- oder Unterseite der Stunde geplant sind, läuft bis zu 90 Sekunden früh.

Der Offset wird von der Aufgaben-ID abgeleitet, daher erhält die gleiche Aufgabe immer den gleichen Offset. Wenn genaue Zeitangaben wichtig sind, wählen Sie eine Minute, die nicht `:00` oder `:30` ist, zum Beispiel `3 9 * * *` statt `0 9 * * *`, und der einmalige Jitter wird nicht angewendet.

### Ablauf nach drei Tagen

Wiederkehrende Aufgaben verfallen automatisch 3 Tage nach der Erstellung. Die Aufgabe läuft ein letztes Mal, dann löscht sie sich selbst. Dies begrenzt, wie lange eine vergessene Schleife laufen kann. Wenn Sie benötigen, dass eine wiederkehrende Aufgabe länger dauert, stornieren und erstellen Sie sie neu, bevor sie abläuft, oder verwenden Sie [Desktop-geplante Aufgaben](/de/desktop#schedule-recurring-tasks) für dauerhafte Planung.

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

Setzen Sie `CLAUDE_CODE_DISABLE_CRON=1` in Ihrer Umgebung, um den Scheduler vollständig zu deaktivieren. Die Cron-Tools und `/loop` werden nicht verfügbar, und alle bereits geplanten Aufgaben stoppen das Läufen. Siehe [Umgebungsvariablen](/de/env-vars) für die vollständige Liste der Deaktivierungsflags.

## Einschränkungen

Die sitzungsbezogene Planung hat inhärente Einschränkungen:

* Aufgaben läuft nur, während Claude Code läuft und untätig ist. Das Schließen des Terminals oder das Beenden der Sitzung storniert alles.
* Kein Aufholen für verpasste Läufe. Wenn die geplante Zeit einer Aufgabe verstreicht, während Claude mit einer langwierigen Anfrage beschäftigt ist, läuft sie einmal, wenn Claude untätig wird, nicht einmal pro verpasstem Intervall.
* Keine Persistenz über Neustarts hinweg. Das Neustarten von Claude Code löscht alle sitzungsbezogenen Aufgaben.

Für Cron-gesteuerte Automatisierung, die unbeaufsichtigt laufen muss, verwenden Sie einen [GitHub Actions-Workflow](/de/github-actions) mit einem `schedule`-Trigger, oder [Desktop-geplante Aufgaben](/de/desktop#schedule-recurring-tasks), wenn Sie einen grafischen Setup-Ablauf möchten.
