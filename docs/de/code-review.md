> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Richten Sie automatisierte PR-Reviews ein, die Logikfehler, Sicherheitslücken und Regressionen durch Multi-Agent-Analyse Ihrer vollständigen Codebasis erkennen

<Note>
  Code Review befindet sich in der Forschungsvorschau und ist für [Teams und Enterprise](https://claude.ai/admin-settings/claude-code) Abonnements verfügbar. Es ist nicht verfügbar für Organisationen mit aktiviertem [Zero Data Retention](/de/zero-data-retention).
</Note>

Code Review analysiert Ihre GitHub Pull Requests und veröffentlicht Erkenntnisse als Inline-Kommentare auf den Codezeilen, auf denen Probleme gefunden wurden. Eine Flotte spezialisierter Agenten untersucht die Codeänderungen im Kontext Ihrer vollständigen Codebasis und sucht nach Logikfehlern, Sicherheitslücken, fehlerhaften Grenzfällen und subtilen Regressionen.

Erkenntnisse werden nach Schweregrad gekennzeichnet und genehmigen oder blockieren Ihren PR nicht, sodass bestehende Review-Workflows intakt bleiben. Sie können anpassen, was Claude kennzeichnet, indem Sie eine `CLAUDE.md` oder `REVIEW.md` Datei zu Ihrem Repository hinzufügen.

Um Claude in Ihrer eigenen CI-Infrastruktur statt in diesem verwalteten Service auszuführen, siehe [GitHub Actions](/de/github-actions) oder [GitLab CI/CD](/de/gitlab-ci-cd).

Diese Seite behandelt:

* [Wie Reviews funktionieren](#how-reviews-work)
* [Setup](#set-up-code-review)
* [Anpassung von Reviews](#customize-reviews) mit `CLAUDE.md` und `REVIEW.md`
* [Preisgestaltung](#pricing)

## Wie Reviews funktionieren

Sobald ein Administrator Code Review für Ihre Organisation [aktiviert](#set-up-code-review), werden Reviews automatisch ausgeführt, wenn ein Pull Request geöffnet oder aktualisiert wird. Mehrere Agenten analysieren parallel den Diff und den umgebenden Code auf Anthropic-Infrastruktur. Jeder Agent sucht nach einer anderen Klasse von Problemen, dann überprüft ein Verifizierungsschritt Kandidaten gegen das tatsächliche Codeverhalten, um falsch positive Ergebnisse herauszufiltern. Die Ergebnisse werden dedupliziert, nach Schweregrad eingestuft und als Inline-Kommentare auf den spezifischen Zeilen veröffentlicht, auf denen Probleme gefunden wurden. Wenn keine Probleme gefunden werden, veröffentlicht Claude einen kurzen Bestätigungskommentar auf dem PR.

Reviews skalieren in den Kosten mit PR-Größe und -Komplexität und werden im Durchschnitt in 20 Minuten abgeschlossen. Administratoren können Review-Aktivität und Ausgaben über das [Analytics-Dashboard](#view-usage) überwachen.

### Schweregrad-Stufen

Jede Erkenntnis wird mit einer Schweregrad-Stufe gekennzeichnet:

| Marker | Schweregrad       | Bedeutung                                                                                   |
| :----- | :---------------- | :------------------------------------------------------------------------------------------ |
| 🔴     | Normal            | Ein Fehler, der vor dem Zusammenführen behoben werden sollte                                |
| 🟡     | Nit               | Ein kleineres Problem, das behoben werden sollte, aber nicht blockierend ist                |
| 🟣     | Bereits vorhanden | Ein Fehler, der in der Codebasis vorhanden ist, aber nicht durch diesen PR eingeführt wurde |

Erkenntnisse enthalten einen ausklappbaren erweiterten Reasoning-Bereich, den Sie erweitern können, um zu verstehen, warum Claude das Problem gekennzeichnet hat und wie es das Problem überprüft hat.

### Was Code Review überprüft

Standardmäßig konzentriert sich Code Review auf Korrektheit: Fehler, die die Produktion unterbrechen würden, nicht auf Formatierungspräferenzen oder fehlende Testabdeckung. Sie können erweitern, was es überprüft, indem Sie [Anleitungsdateien](#customize-reviews) zu Ihrem Repository hinzufügen.

## Code Review einrichten

Ein Administrator aktiviert Code Review einmal für die Organisation und wählt aus, welche Repositories einbezogen werden sollen.

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

  <Step title="Wählen Sie Repositories aus">
    Wählen Sie aus, welche Repositories für Code Review aktiviert werden sollen. Wenn Sie ein Repository nicht sehen, stellen Sie sicher, dass Sie der Claude GitHub App während der Installation Zugriff darauf gewährt haben. Sie können später weitere Repositories hinzufügen.
  </Step>

  <Step title="Legen Sie Review-Trigger pro Repo fest">
    Nach Abschluss des Setups zeigt der Code Review Bereich Ihre Repositories in einer Tabelle an. Verwenden Sie für jedes Repository das Dropdown-Menü, um auszuwählen, wann Reviews ausgeführt werden:

    * **Nach PR-Erstellung nur**: Review wird einmal ausgeführt, wenn ein PR geöffnet oder als bereit zur Überprüfung markiert wird
    * **Nach jedem Push zum PR-Branch**: Review wird bei jedem Push ausgeführt, erkennt neue Probleme, während sich der PR entwickelt, und löst Threads automatisch auf, wenn Sie gekennzeichnete Probleme beheben

    Das Überprüfen bei jedem Push führt zu mehr Reviews und höheren Kosten. Beginnen Sie mit der PR-Erstellung nur und wechseln Sie zu On-Push für Repos, in denen Sie kontinuierliche Abdeckung und automatische Thread-Bereinigung wünschen.
  </Step>
</Steps>

Die Repositories-Tabelle zeigt auch die durchschnittlichen Kosten pro Review für jedes Repo basierend auf der letzten Aktivität. Verwenden Sie das Zeilenaktionsmenü, um Code Review pro Repository ein- oder auszuschalten, oder um ein Repository vollständig zu entfernen.

Um das Setup zu überprüfen, öffnen Sie einen Test-PR. Ein Check Run mit dem Namen **Claude Code Review** wird innerhalb weniger Minuten angezeigt. Wenn dies nicht der Fall ist, bestätigen Sie, dass das Repository in Ihren Admin-Einstellungen aufgeführt ist und die Claude GitHub App Zugriff darauf hat.

## Reviews anpassen

Code Review liest zwei Dateien aus Ihrem Repository, um zu steuern, was es kennzeichnet. Beide sind zusätzlich zu den standardmäßigen Korrektheitsprüfungen:

* **`CLAUDE.md`**: gemeinsame Projektanweisungen, die Claude Code für alle Aufgaben verwendet, nicht nur für Reviews. Verwenden Sie es, wenn die Anleitung auch für interaktive Claude Code Sitzungen gilt.
* **`REVIEW.md`**: nur Review-Anleitung, die ausschließlich während Code Reviews gelesen wird. Verwenden Sie es für Regeln, die streng damit zu tun haben, was während der Überprüfung gekennzeichnet oder übersprungen werden soll, und würde Ihre allgemeine `CLAUDE.md` nicht überladen.

### CLAUDE.md

Code Review liest Ihre Repository-`CLAUDE.md` Dateien und behandelt neu eingeführte Verstöße als Nit-Level-Erkenntnisse. Dies funktioniert bidirektional: Wenn Ihr PR Code so ändert, dass eine `CLAUDE.md` Aussage veraltet wird, kennzeichnet Claude, dass die Dokumentation aktualisiert werden muss.

Claude liest `CLAUDE.md` Dateien auf jeder Ebene Ihrer Verzeichnishierarchie, sodass Regeln in einer Unterverzeichnis-`CLAUDE.md` nur auf Dateien unter diesem Pfad angewendet werden. Weitere Informationen zur Funktionsweise von `CLAUDE.md` finden Sie in der [Memory-Dokumentation](/de/memory).

Für Review-spezifische Anleitung, die Sie nicht auf allgemeine Claude Code Sitzungen angewendet haben möchten, verwenden Sie stattdessen [`REVIEW.md`](#review-md).

### REVIEW\.md

Fügen Sie eine `REVIEW.md` Datei zu Ihrem Repository-Root für Review-spezifische Regeln hinzu. Verwenden Sie es zum Kodieren von:

* Unternehmens- oder Team-Stilrichtlinien: "frühe Returns gegenüber verschachtelten Bedingungen bevorzugen"
* Sprach- oder Framework-spezifische Konventionen, die nicht von Lintern abgedeckt werden
* Dinge, die Claude immer kennzeichnen sollte: "jede neue API-Route muss einen Integrationstest haben"
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

| Bereich                    | Was es zeigt                                                                                                |
| :------------------------- | :---------------------------------------------------------------------------------------------------------- |
| PRs überprüft              | Tägliche Anzahl der überprüften Pull Requests über den ausgewählten Zeitraum                                |
| Kosten wöchentlich         | Wöchentliche Ausgaben für Code Review                                                                       |
| Feedback                   | Anzahl der Review-Kommentare, die automatisch aufgelöst wurden, weil ein Entwickler das Problem behoben hat |
| Repository-Aufschlüsselung | Pro-Repo-Anzahl der überprüften PRs und aufgelösten Kommentare                                              |

Die Repositories-Tabelle in Admin-Einstellungen zeigt auch durchschnittliche Kosten pro Review für jedes Repo.

## Preisgestaltung

Code Review wird basierend auf der Token-Nutzung abgerechnet. Reviews kosten durchschnittlich \$15-25, skalierend mit PR-Größe, Codebasis-Komplexität und wie viele Probleme Verifizierung erfordern. Code Review Nutzung wird separat über [zusätzliche Nutzung](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) abgerechnet und zählt nicht gegen die in Ihrem Plan enthaltene Nutzung.

Der Review-Trigger, den Sie wählen, beeinflusst die Gesamtkosten:

* **Nach PR-Erstellung nur**: wird einmal pro PR ausgeführt
* **Nach jedem Push**: wird bei jedem Commit ausgeführt, multipliziert die Kosten mit der Anzahl der Pushes

Kosten erscheinen auf Ihrer Anthropic-Rechnung, unabhängig davon, ob Ihre Organisation AWS Bedrock oder Google Vertex AI für andere Claude Code Funktionen verwendet. Um eine monatliche Ausgabenbegrenzung für Code Review festzulegen, gehen Sie zu [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) und konfigurieren Sie das Limit für den Claude Code Review Service.

Überwachen Sie Ausgaben über das wöchentliche Kostendiagramm in [Analytics](#view-usage) oder die durchschnittliche Kostenspalte pro Repo in Admin-Einstellungen.

## Verwandte Ressourcen

Code Review ist so konzipiert, dass es neben dem Rest von Claude Code funktioniert. Wenn Sie Reviews lokal ausführen möchten, bevor Sie einen PR öffnen, eine selbst gehostete Einrichtung benötigen oder tiefer verstehen möchten, wie `CLAUDE.md` Claudes Verhalten über Tools hinweg prägt, sind diese Seiten gute nächste Schritte:

* [Plugins](/de/discover-plugins): Durchsuchen Sie den Plugin-Marktplatz, einschließlich eines `code-review` Plugins zum Ausführen von On-Demand-Reviews lokal vor dem Pushen
* [GitHub Actions](/de/github-actions): Führen Sie Claude in Ihren eigenen GitHub Actions Workflows für benutzerdefinierte Automatisierung über Code Review hinaus aus
* [GitLab CI/CD](/de/gitlab-ci-cd): Selbst gehostete Claude-Integration für GitLab-Pipelines
* [Memory](/de/memory): Wie `CLAUDE.md` Dateien über Claude Code funktionieren
* [Analytics](/de/analytics): Verfolgen Sie Claude Code Nutzung über Code Review hinaus
