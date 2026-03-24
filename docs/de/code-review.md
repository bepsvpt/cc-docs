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

Um Claude in Ihrer eigenen CI-Infrastruktur statt dieses verwalteten Dienstes auszuführen, siehe [GitHub Actions](/de/github-actions) oder [GitLab CI/CD](/de/gitlab-ci-cd).

Diese Seite behandelt:

* [Wie Reviews funktionieren](#how-reviews-work)
* [Setup](#set-up-code-review)
* [Anpassung von Reviews](#customize-reviews) mit `CLAUDE.md` und `REVIEW.md`
* [Preisgestaltung](#pricing)

## Wie Reviews funktionieren

Sobald ein Administrator [Code Review aktiviert](#set-up-code-review) für Ihre Organisation, werden Reviews ausgelöst, wenn ein PR geöffnet wird, bei jedem Push oder auf manuelle Anfrage, je nach konfiguriertem Verhalten des Repositorys. Das Kommentieren von `@claude review` [startet Reviews auf einem PR](#manually-trigger-reviews) in jedem Modus.

Wenn ein Review ausgeführt wird, analysieren mehrere Agenten parallel den Diff und den umgebenden Code auf Anthropic-Infrastruktur. Jeder Agent sucht nach einer anderen Klasse von Problemen, dann überprüft ein Verifizierungsschritt Kandidaten gegen das tatsächliche Codeverhalten, um falsch positive Ergebnisse zu filtern. Die Ergebnisse werden dedupliziert, nach Schweregrad eingestuft und als Inline-Kommentare auf den spezifischen Zeilen veröffentlicht, auf denen Probleme gefunden wurden. Wenn keine Probleme gefunden werden, veröffentlicht Claude einen kurzen Bestätigungskommentar auf dem PR.

Reviews skalieren in den Kosten mit PR-Größe und Komplexität und werden im Durchschnitt in 20 Minuten abgeschlossen. Administratoren können Review-Aktivität und Ausgaben über das [Analytics-Dashboard](#view-usage) überwachen.

### Schweregrad-Stufen

Jede Erkenntnis wird mit einer Schweregrad-Stufe gekennzeichnet:

| Marker | Schweregrad       | Bedeutung                                                                                   |
| :----- | :---------------- | :------------------------------------------------------------------------------------------ |
| 🔴     | Normal            | Ein Fehler, der vor dem Zusammenführen behoben werden sollte                                |
| 🟡     | Nit               | Ein kleineres Problem, das behoben werden sollte, aber nicht blockierend ist                |
| 🟣     | Bereits vorhanden | Ein Fehler, der in der Codebasis vorhanden ist, aber nicht durch diesen PR eingeführt wurde |

Erkenntnisse enthalten einen ausklappbaren erweiterten Reasoning-Bereich, den Sie erweitern können, um zu verstehen, warum Claude das Problem gekennzeichnet hat und wie es das Problem überprüft hat.

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
    * **Manual**: Reviews werden nur gestartet, wenn jemand `@claude review` auf einem PR [kommentiert](#manually-trigger-reviews); nachfolgende Pushes zu diesem PR werden dann automatisch überprüft

    Das Überprüfen bei jedem Push führt die meisten Reviews durch und kostet am meisten. Der manuelle Modus ist nützlich für Repositorys mit hohem Datenverkehr, bei denen Sie bestimmte PRs in die Überprüfung aufnehmen möchten, oder um nur mit der Überprüfung Ihrer PRs zu beginnen, wenn sie bereit sind.
  </Step>
</Steps>

Die Repositorys-Tabelle zeigt auch die durchschnittlichen Kosten pro Review für jedes Repo basierend auf der letzten Aktivität. Verwenden Sie das Zeilenaktionsmenü, um Code Review pro Repository ein- oder auszuschalten, oder um ein Repository vollständig zu entfernen.

Um das Setup zu überprüfen, öffnen Sie einen Test-PR. Wenn Sie einen automatischen Trigger gewählt haben, wird eine Check-Run namens **Claude Code Review** innerhalb weniger Minuten angezeigt. Wenn Sie Manual gewählt haben, kommentieren Sie `@claude review` auf dem PR, um die erste Überprüfung zu starten. Wenn keine Check-Run angezeigt wird, bestätigen Sie, dass das Repository in Ihren Admin-Einstellungen aufgelistet ist und die Claude GitHub App Zugriff darauf hat.

## Manuelles Auslösen von Reviews

Kommentieren Sie `@claude review` auf einem Pull Request, um eine Überprüfung zu starten und diesen PR für Push-ausgelöste Reviews in Zukunft zu aktivieren. Dies funktioniert unabhängig vom konfigurierten Trigger des Repositorys: Verwenden Sie es, um bestimmte PRs im manuellen Modus in die Überprüfung aufzunehmen, oder um eine sofortige Neuüberprüfung in anderen Modi zu erhalten. In jedem Fall werden Pushes zu diesem PR von da an überprüft.

Damit der Kommentar eine Überprüfung auslöst:

* Veröffentlichen Sie ihn als Top-Level-PR-Kommentar, nicht als Inline-Kommentar auf einer Diff-Zeile
* Setzen Sie `@claude review` an den Anfang des Kommentars
* Sie müssen Owner-, Member- oder Collaborator-Zugriff auf das Repository haben
* Der PR muss offen sein und kein Entwurf

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

```markdown  theme={null}
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

Code Review wird basierend auf der Token-Nutzung abgerechnet. Reviews kosten durchschnittlich \$15-25, skalierend mit PR-Größe, Codebasis-Komplexität und wie viele Probleme eine Überprüfung erfordern. Code Review Nutzung wird separat über [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) abgerechnet und zählt nicht gegen die in Ihrem Plan enthaltene Nutzung.

Der Review-Trigger, den Sie wählen, beeinflusst die Gesamtkosten:

* **Once after PR creation**: wird einmal pro PR ausgeführt
* **After every push**: wird bei jedem Push ausgeführt, multipliziert die Kosten mit der Anzahl der Pushes
* **Manual**: keine Reviews, bis jemand `@claude review` auf einem PR [kommentiert](#manually-trigger-reviews)

In jedem Modus führt das Kommentieren von `@claude review` [den PR in Push-ausgelöste Reviews auf](#manually-trigger-reviews), sodass zusätzliche Kosten pro Push nach diesem Kommentar anfallen.

Kosten erscheinen auf Ihrer Anthropic-Rechnung, unabhängig davon, ob Ihre Organisation AWS Bedrock oder Google Vertex AI für andere Claude Code Funktionen verwendet. Um eine monatliche Ausgabenbegrenzung für Code Review festzulegen, gehen Sie zu [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) und konfigurieren Sie das Limit für den Claude Code Review Service.

Überwachen Sie die Ausgaben über das wöchentliche Kostendiagramm in [analytics](#view-usage) oder die durchschnittliche Kostenspalte pro Repo in den Admin-Einstellungen.

## Verwandte Ressourcen

Code Review ist so konzipiert, dass es neben dem Rest von Claude Code funktioniert. Wenn Sie Reviews lokal ausführen möchten, bevor Sie einen PR öffnen, eine selbst gehostete Einrichtung benötigen oder tiefer verstehen möchten, wie `CLAUDE.md` Claudes Verhalten über Tools hinweg prägt, sind diese Seiten gute nächste Schritte:

* [Plugins](/de/discover-plugins): durchsuchen Sie den Plugin-Marktplatz, einschließlich eines `code-review` Plugins zum Ausführen von On-Demand-Reviews lokal vor dem Pushen
* [GitHub Actions](/de/github-actions): führen Sie Claude in Ihren eigenen GitHub Actions Workflows aus für benutzerdefinierte Automatisierung über Code Review hinaus
* [GitLab CI/CD](/de/gitlab-ci-cd): selbst gehostete Claude-Integration für GitLab-Pipelines
* [Memory](/de/memory): wie `CLAUDE.md` Dateien über Claude Code funktionieren
* [Analytics](/de/analytics): verfolgen Sie Claude Code Nutzung über Code Review hinaus
