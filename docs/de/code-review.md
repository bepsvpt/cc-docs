> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Richten Sie automatisierte PR-Reviews ein, die Logikfehler, Sicherheitslücken und Regressionen durch Multi-Agent-Analyse Ihrer vollständigen Codebasis erkennen

<Note>
  Code Review befindet sich in der Forschungsvorschau und ist für [Teams und Enterprise](https://claude.ai/admin-settings/claude-code) Abonnements verfügbar. Es ist nicht verfügbar für Organisationen mit [Zero Data Retention](/de/zero-data-retention) aktiviert.
</Note>

Code Review analysiert Ihre GitHub Pull Requests und veröffentlicht Erkenntnisse als Inline-Kommentare auf den Codezeilen, auf denen Probleme gefunden wurden. Eine Flotte spezialisierter Agenten untersucht die Codeänderungen im Kontext Ihrer vollständigen Codebasis und sucht nach Logikfehlern, Sicherheitslücken, fehlerhaften Grenzfällen und subtilen Regressionen.

Erkenntnisse werden nach Schweregrad gekennzeichnet und genehmigen oder blockieren Ihren PR nicht, sodass bestehende Review-Workflows intakt bleiben. Sie können anpassen, was Claude kennzeichnet, indem Sie eine `CLAUDE.md` oder `REVIEW.md` Datei zu Ihrem Repository hinzufügen.

Um Claude in Ihrer eigenen CI-Infrastruktur statt dieses verwalteten Dienstes auszuführen, siehe [GitHub Actions](/de/github-actions) oder [GitLab CI/CD](/de/gitlab-ci-cd). Für Repositorys auf einer selbst gehosteten GitHub-Instanz siehe [GitHub Enterprise Server](/de/github-enterprise-server).

Diese Seite behandelt:

* [Wie Reviews funktionieren](#how-reviews-work)
* [Setup](#set-up-code-review)
* [Manuelles Auslösen von Reviews](#manually-trigger-reviews) mit `@claude review` und `@claude review once`
* [Anpassung von Reviews](#customize-reviews) mit `CLAUDE.md` und `REVIEW.md`
* [Preisgestaltung](#pricing)
* [Fehlerbehebung](#troubleshooting) fehlgeschlagener Ausführungen und fehlender Kommentare

## Wie Reviews funktionieren

Sobald ein Administrator [Code Review aktiviert](#set-up-code-review) für Ihre Organisation, werden Reviews ausgelöst, wenn ein PR geöffnet wird, bei jedem Push oder auf manuelle Anfrage, je nach konfiguriertem Verhalten des Repositorys. Das Kommentieren von `@claude review` [startet Reviews auf einem PR](#manually-trigger-reviews) in jedem Modus.

Wenn ein Review ausgeführt wird, analysieren mehrere Agenten parallel den Diff und den umgebenden Code auf Anthropic-Infrastruktur. Jeder Agent sucht nach einer anderen Klasse von Problemen, dann überprüft ein Verifizierungsschritt Kandidaten gegen das tatsächliche Codeverhalten, um falsch positive Ergebnisse zu filtern. Die Ergebnisse werden dedupliziert, nach Schweregrad eingestuft und als Inline-Kommentare auf den spezifischen Zeilen veröffentlicht, auf denen Probleme gefunden wurden. Wenn keine Probleme gefunden werden, veröffentlicht Claude einen kurzen Bestätigungskommentar auf dem PR.

Reviews skalieren in den Kosten mit PR-Größe und Komplexität und werden im Durchschnitt in 20 Minuten abgeschlossen. Administratoren können Review-Aktivität und Ausgaben über das [Analytics-Dashboard](#view-usage) überwachen.

### Schweregrad-Stufen

Jede Erkenntnis wird mit einer Schweregrad-Stufe gekennzeichnet:

| Marker | Schweregrad       | Bedeutung                                                                                   |
| :----- | :---------------- | :------------------------------------------------------------------------------------------ |
| 🔴     | Wichtig           | Ein Fehler, der vor dem Zusammenführen behoben werden sollte                                |
| 🟡     | Nit               | Ein kleineres Problem, das behoben werden sollte, aber nicht blockierend ist                |
| 🟣     | Bereits vorhanden | Ein Fehler, der in der Codebasis vorhanden ist, aber nicht durch diesen PR eingeführt wurde |

Erkenntnisse enthalten einen ausklappbaren erweiterten Reasoning-Bereich, den Sie erweitern können, um zu verstehen, warum Claude das Problem gekennzeichnet hat und wie es das Problem überprüft hat.

### Check-Run-Ausgabe

Neben den Inline-Review-Kommentaren füllt jedes Review die **Claude Code Review** Check-Run auf, die neben Ihren CI-Checks angezeigt wird. Erweitern Sie ihren **Details**-Link, um eine Zusammenfassung aller Erkenntnisse an einem Ort zu sehen, sortiert nach Schweregrad:

| Schweregrad | Datei:Zeile               | Problem                                                                                   |
| ----------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| 🔴 Wichtig  | `src/auth/session.ts:142` | Token-Aktualisierung läuft parallel mit Logout, wodurch veraltete Sitzungen aktiv bleiben |
| 🟡 Nit      | `src/auth/session.ts:88`  | `parseExpiry` gibt stillschweigend 0 bei fehlerhafter Eingabe zurück                      |

Jede Erkenntnis wird auch als Anmerkung auf der Registerkarte **Files changed** angezeigt, direkt auf den relevanten Diff-Zeilen markiert. Wichtige Erkenntnisse werden mit einem roten Marker gerendert, Nits mit einer gelben Warnung und bereits vorhandene Fehler mit einer grauen Benachrichtigung. Anmerkungen und die Schweregrad-Tabelle werden unabhängig von Inline-Review-Kommentaren in die Check-Run geschrieben, sodass sie verfügbar bleiben, auch wenn GitHub einen Inline-Kommentar auf einer Zeile ablehnt, die sich verschoben hat.

Die Check-Run wird immer mit einer neutralen Schlussfolgerung abgeschlossen, sodass sie das Zusammenführen durch Branch-Schutzregeln niemals blockiert. Wenn Sie Zusammenführungen auf Code Review-Erkenntnisse beschränken möchten, lesen Sie die Schweregrad-Aufschlüsselung aus der Check-Run-Ausgabe in Ihrem eigenen CI. Die letzte Zeile des Details-Texts ist ein maschinenlesbarer Kommentar, den Ihr Workflow mit `gh` und jq analysieren kann:

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

Dies gibt ein JSON-Objekt mit Zählungen pro Schweregrad zurück, zum Beispiel `{"normal": 2, "nit": 1, "pre_existing": 0}`. Der `normal`-Schlüssel enthält die Anzahl der Wichtig-Erkenntnisse; ein Wert ungleich Null bedeutet, dass Claude mindestens einen Fehler gefunden hat, der vor dem Zusammenführen behoben werden sollte.

### Was Code Review überprüft

Standardmäßig konzentriert sich Code Review auf Korrektheit: Fehler, die die Produktion unterbrechen würden, nicht auf Formatierungspräferenzen oder fehlende Testabdeckung. Sie können erweitern, was es überprüft, indem Sie [Anleitungsdateien hinzufügen](#customize-reviews) zu Ihrem Repository.

## Code Review einrichten

Ein Administrator aktiviert Code Review einmal für die Organisation und wählt aus, welche Repositorys einbezogen werden sollen.

<Steps>
  <Step title="Öffnen Sie die Claude Code Admin-Einstellungen">
    Gehen Sie zu [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) und finden Sie den Code Review Bereich. Sie benötigen Admin-Zugriff auf Ihre Claude-Organisation und die Berechtigung, GitHub Apps in Ihrer GitHub-Organisation zu installieren.
  </Step>

  <Step title="Setup starten">
    Klicken Sie auf **Setup**. Dies startet den GitHub App-Installationsablauf.
  </Step>

  <Step title="Installieren Sie die Claude GitHub App">
    Folgen Sie den Aufforderungen, um die Claude GitHub App in Ihrer GitHub-Organisation zu installieren. Die App fordert diese Repository-Berechtigungen an:

    * **Contents**: Lesen und Schreiben
    * **Issues**: Lesen und Schreiben
    * **Pull requests**: Lesen und Schreiben

    Code Review verwendet Lesezugriff auf Inhalte und Schreibzugriff auf Pull Requests. Der breitere Berechtigungssatz unterstützt auch [GitHub Actions](/de/github-actions), wenn Sie diese später aktivieren.
  </Step>

  <Step title="Wählen Sie Repositorys aus">
    Wählen Sie aus, welche Repositorys für Code Review aktiviert werden sollen. Wenn Sie ein Repository nicht sehen, stellen Sie sicher, dass Sie der Claude GitHub App während der Installation Zugriff darauf gewährt haben. Sie können später weitere Repositorys hinzufügen.
  </Step>

  <Step title="Legen Sie Review-Trigger pro Repo fest">
    Nach Abschluss des Setups zeigt der Code Review Bereich Ihre Repositorys in einer Tabelle an. Verwenden Sie für jedes Repository das Dropdown-Menü **Review Behavior**, um auszuwählen, wann Reviews ausgeführt werden:

    * **Once after PR creation**: Review wird einmal ausgeführt, wenn ein PR geöffnet oder als bereit zur Überprüfung markiert wird
    * **After every push**: Review wird bei jedem Push zum PR-Branch ausgeführt, erkennt neue Probleme, während sich der PR entwickelt, und löst Threads automatisch auf, wenn Sie gekennzeichnete Probleme beheben
    * **Manual**: Reviews werden nur gestartet, wenn jemand [kommentiert `@claude review` oder `@claude review once` auf einem PR](#manually-trigger-reviews); `@claude review` abonniert den PR auch für Reviews bei nachfolgenden Pushes

    Das Überprüfen bei jedem Push führt die meisten Reviews durch und kostet am meisten. Der manuelle Modus ist nützlich für Repositorys mit hohem Datenverkehr, bei denen Sie bestimmte PRs in die Überprüfung aufnehmen möchten, oder um nur mit der Überprüfung Ihrer PRs zu beginnen, wenn sie bereit sind.
  </Step>
</Steps>

Die Repositorys-Tabelle zeigt auch die durchschnittlichen Kosten pro Review für jedes Repo basierend auf der letzten Aktivität. Verwenden Sie das Zeilenaktionsmenü, um Code Review pro Repository ein- oder auszuschalten, oder um ein Repository vollständig zu entfernen.

Um das Setup zu überprüfen, öffnen Sie einen Test-PR. Wenn Sie einen automatischen Trigger gewählt haben, wird eine Check-Run namens **Claude Code Review** innerhalb weniger Minuten angezeigt. Wenn Sie Manual gewählt haben, kommentieren Sie `@claude review` auf dem PR, um die erste Überprüfung zu starten. Wenn keine Check-Run angezeigt wird, bestätigen Sie, dass das Repository in Ihren Admin-Einstellungen aufgelistet ist und die Claude GitHub App Zugriff darauf hat.

## Manuelles Auslösen von Reviews

Zwei Kommentarbefehle starten eine Überprüfung auf Anfrage. Beide funktionieren unabhängig vom konfigurierten Trigger des Repositorys, sodass Sie sie verwenden können, um bestimmte PRs im manuellen Modus in die Überprüfung aufzunehmen oder um eine sofortige Neuüberprüfung in anderen Modi zu erhalten.

| Befehl                | Was er tut                                                                           |
| :-------------------- | :----------------------------------------------------------------------------------- |
| `@claude review`      | Startet eine Überprüfung und abonniert den PR für Push-ausgelöste Reviews in Zukunft |
| `@claude review once` | Startet eine einzelne Überprüfung, ohne den PR für zukünftige Pushes zu abonnieren   |

Verwenden Sie `@claude review once`, wenn Sie Feedback zum aktuellen Zustand eines PR möchten, aber nicht möchten, dass jeder nachfolgende Push eine Überprüfung verursacht. Dies ist nützlich für langfristige PRs mit häufigen Pushes oder wenn Sie eine einmalige zweite Meinung möchten, ohne das Review-Verhalten des PR zu ändern.

Damit einer der beiden Befehle eine Überprüfung auslöst:

* Veröffentlichen Sie ihn als Top-Level-PR-Kommentar, nicht als Inline-Kommentar auf einer Diff-Zeile
* Setzen Sie den Befehl an den Anfang des Kommentars, mit `once` auf der gleichen Zeile, wenn Sie die One-Shot-Form verwenden
* Sie müssen Owner-, Member- oder Collaborator-Zugriff auf das Repository haben
* Der PR muss offen sein

Im Gegensatz zu automatischen Triggern werden manuelle Trigger auf Entwurfs-PRs ausgeführt, da eine explizite Anfrage signalisiert, dass Sie die Überprüfung jetzt möchten, unabhängig vom Entwurfsstatus.

Wenn bereits eine Überprüfung auf diesem PR läuft, wird die Anfrage in die Warteschlange eingereiht, bis die laufende Überprüfung abgeschlossen ist. Sie können den Fortschritt über die Check-Run auf dem PR überwachen.

## Anpassung von Reviews

Code Review liest zwei Dateien aus Ihrem Repository, um zu steuern, was es kennzeichnet. Beide sind zusätzlich zu den standardmäßigen Korrektheitsprüfungen:

* **`CLAUDE.md`**: gemeinsame Projektanweisungen, die Claude Code für alle Aufgaben verwendet, nicht nur für Reviews. Verwenden Sie es, wenn Anleitungen auch für interaktive Claude Code Sitzungen gelten.
* **`REVIEW.md`**: Review-spezifische Anleitungen, die ausschließlich während Code Reviews gelesen werden. Verwenden Sie es für Regeln, die streng damit zu tun haben, was während der Überprüfung gekennzeichnet oder übersprungen werden soll, und würden Ihre allgemeine `CLAUDE.md` überladen.

### CLAUDE.md

Code Review liest Ihre Repository-`CLAUDE.md` Dateien und behandelt neu eingeführte Verstöße als Nit-Level-Erkenntnisse. Dies funktioniert bidirektional: Wenn Ihr PR Code auf eine Weise ändert, die eine `CLAUDE.md` Aussage veraltet macht, kennzeichnet Claude, dass die Dokumentation aktualisiert werden muss.

Claude liest `CLAUDE.md` Dateien auf jeder Ebene Ihrer Verzeichnishierarchie, sodass Regeln in einer Unterverzeichnis-`CLAUDE.md` nur auf Dateien unter diesem Pfad angewendet werden. Weitere Informationen zur Funktionsweise von `CLAUDE.md` finden Sie in der [Memory-Dokumentation](/de/memory).

Für Review-spezifische Anleitungen, die Sie nicht auf allgemeine Claude Code Sitzungen angewendet haben möchten, verwenden Sie stattdessen [`REVIEW.md`](#review-md).

### REVIEW\.md

Fügen Sie eine `REVIEW.md` Datei zu Ihrem Repository-Root hinzu, um Review-spezifische Regeln zu erstellen. Verwenden Sie es zum Kodieren von:

* Unternehmens- oder Team-Stilrichtlinien: "frühe Returns gegenüber verschachtelten Bedingungen bevorzugen"
* Sprach- oder Framework-spezifische Konventionen, die nicht von Lintern abgedeckt werden
* Dinge, die Claude immer kennzeichnen sollte: "jede neue API-Route muss einen Integrationtest haben"
* Dinge, die Claude überspringen sollte: "keine Kommentare zur Formatierung in generiertem Code unter `/gen/`"

Beispiel `REVIEW.md`:

```markdown theme={null}
# Code Review Richtlinien

## Immer überprüfen
- Neue API-Endpunkte haben entsprechende Integrationstests
- Datenbankmigrationen sind rückwärtskompatibel
- Fehlermeldungen geben keine internen Details an Benutzer preis

## Stil
- `match` Anweisungen gegenüber verketteten `isinstance` Überprüfungen bevorzugen
- Strukturiertes Logging verwenden, nicht f-String-Interpolation in Log-Aufrufen

## Überspringen
- Generierte Dateien unter `src/gen/`
- Nur Formatierungsänderungen in `*.lock` Dateien
```

Claude erkennt `REVIEW.md` automatisch im Repository-Root. Keine Konfiguration erforderlich.

## Nutzung anzeigen

Gehen Sie zu [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review), um Code Review Aktivität in Ihrer Organisation zu sehen. Das Dashboard zeigt:

| Bereich              | Was es zeigt                                                                                                |
| :------------------- | :---------------------------------------------------------------------------------------------------------- |
| PRs reviewed         | Tägliche Anzahl der überprüften Pull Requests über den ausgewählten Zeitraum                                |
| Cost weekly          | Wöchentliche Ausgaben für Code Review                                                                       |
| Feedback             | Anzahl der Review-Kommentare, die automatisch aufgelöst wurden, weil ein Entwickler das Problem behoben hat |
| Repository breakdown | Pro-Repo-Anzahl der überprüften PRs und aufgelösten Kommentare                                              |

Die Repositorys-Tabelle in den Admin-Einstellungen zeigt auch die durchschnittlichen Kosten pro Review für jedes Repo.

## Preisgestaltung

Code Review wird basierend auf der Token-Nutzung abgerechnet. Jede Überprüfung kostet durchschnittlich \$15-25, skalierend mit PR-Größe, Codebasis-Komplexität und wie viele Probleme eine Überprüfung erfordern. Code Review Nutzung wird separat über [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) abgerechnet und zählt nicht gegen die in Ihrem Plan enthaltene Nutzung.

Der Review-Trigger, den Sie wählen, beeinflusst die Gesamtkosten:

* **Once after PR creation**: wird einmal pro PR ausgeführt
* **After every push**: wird bei jedem Push ausgeführt, multipliziert die Kosten mit der Anzahl der Pushes
* **Manual**: keine Reviews, bis jemand `@claude review` auf einem PR kommentiert

In jedem Modus führt das Kommentieren von `@claude review` [den PR in Push-ausgelöste Reviews auf](#manually-trigger-reviews), sodass zusätzliche Kosten pro Push nach diesem Kommentar anfallen. Um eine einzelne Überprüfung auszuführen, ohne sich für zukünftige Pushes zu abonnieren, kommentieren Sie stattdessen `@claude review once`.

Kosten erscheinen auf Ihrer Anthropic-Rechnung, unabhängig davon, ob Ihre Organisation AWS Bedrock oder Google Vertex AI für andere Claude Code Funktionen verwendet. Um eine monatliche Ausgabenbegrenzung für Code Review festzulegen, gehen Sie zu [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) und konfigurieren Sie das Limit für den Claude Code Review Service.

Überwachen Sie die Ausgaben über das wöchentliche Kostendiagramm in [analytics](#view-usage) oder die durchschnittliche Kostenspalte pro Repo in den Admin-Einstellungen.

## Fehlerbehebung

Review-Ausführungen sind Best-Effort. Eine fehlgeschlagene Ausführung blockiert Ihren PR niemals, aber sie wird auch nicht automatisch erneut versucht. Dieser Abschnitt behandelt, wie Sie sich von einer fehlgeschlagenen Ausführung erholen und wo Sie nachschauen können, wenn die Check-Run Probleme meldet, die Sie nicht finden können.

### Auslösen einer fehlgeschlagenen oder abgelaufenen Überprüfung erneut

Wenn die Review-Infrastruktur auf einen internen Fehler trifft oder ihr Zeitlimit überschreitet, wird die Check-Run mit einem Titel von **Code review encountered an error** oder **Code review timed out** abgeschlossen. Die Schlussfolgerung ist immer noch neutral, sodass nichts Ihre Zusammenführung blockiert, aber keine Erkenntnisse werden veröffentlicht.

Um die Überprüfung erneut auszuführen, kommentieren Sie `@claude review once` auf dem PR. Dies startet eine neue Überprüfung, ohne den PR für zukünftige Pushes zu abonnieren. Wenn der PR bereits für Push-ausgelöste Reviews abonniert ist, startet das Pushen eines neuen Commits auch eine neue Überprüfung.

Die Schaltfläche **Re-run** in Githubs Checks-Registerkarte löst Code Review nicht erneut aus. Verwenden Sie stattdessen den Kommentarbefehl oder einen neuen Push.

### Finden Sie Probleme, die nicht als Inline-Kommentare angezeigt werden

Wenn der Check-Run-Titel besagt, dass Probleme gefunden wurden, aber Sie keine Inline-Review-Kommentare auf dem Diff sehen, schauen Sie an diesen anderen Stellen, wo Erkenntnisse angezeigt werden:

* **Check-Run Details**: Klicken Sie auf **Details** neben der Claude Code Review Check-Run auf der Registerkarte Checks. Die Schweregrad-Tabelle listet jede Erkenntnis mit ihrer Datei, Zeile und Zusammenfassung auf, unabhängig davon, ob der Inline-Kommentar akzeptiert wurde.
* **Files changed Anmerkungen**: Öffnen Sie die Registerkarte **Files changed** auf dem PR. Erkenntnisse werden als Anmerkungen gerendert, die direkt an den Diff-Zeilen angebracht sind, getrennt von Review-Kommentaren.
* **Review-Text**: Wenn Sie zum PR gepusht haben, während eine Überprüfung lief, können einige Erkenntnisse auf Zeilen verweisen, die nicht mehr im aktuellen Diff vorhanden sind. Diese werden unter einer **Additional findings** Überschrift im Review-Text angezeigt, anstatt als Inline-Kommentare.

## Verwandte Ressourcen

Code Review ist so konzipiert, dass es neben dem Rest von Claude Code funktioniert. Wenn Sie Reviews lokal ausführen möchten, bevor Sie einen PR öffnen, eine selbst gehostete Einrichtung benötigen oder tiefer verstehen möchten, wie `CLAUDE.md` Claudes Verhalten über Tools hinweg prägt, sind diese Seiten gute nächste Schritte:

* [Plugins](/de/discover-plugins): durchsuchen Sie den Plugin-Marktplatz, einschließlich eines `code-review` Plugins zum Ausführen von On-Demand-Reviews lokal vor dem Pushen
* [GitHub Actions](/de/github-actions): führen Sie Claude in Ihren eigenen GitHub Actions Workflows aus für benutzerdefinierte Automatisierung über Code Review hinaus
* [GitLab CI/CD](/de/gitlab-ci-cd): selbst gehostete Claude-Integration für GitLab-Pipelines
* [Memory](/de/memory): wie `CLAUDE.md` Dateien über Claude Code funktionieren
* [Analytics](/de/analytics): verfolgen Sie Claude Code Nutzung über Code Review hinaus
