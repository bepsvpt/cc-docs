> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Beschleunigen Sie Antworten mit dem Schnellmodus

> Erhalten Sie schnellere Opus 4.6-Antworten in Claude Code durch Aktivierung des Schnellmodus.

<Note>
  Der Schnellmodus befindet sich in [Forschungsvorschau](#research-preview). Die Funktion, Preisgestaltung und Verfügbarkeit können sich basierend auf Feedback ändern.
</Note>

Der Schnellmodus ist eine Hochgeschwindigkeitskonfiguration für Claude Opus 4.6, die das Modell 2,5x schneller macht, allerdings zu höheren Kosten pro Token. Aktivieren Sie ihn mit `/fast`, wenn Sie Geschwindigkeit für interaktive Arbeiten wie schnelle Iteration oder Live-Debugging benötigen, und deaktivieren Sie ihn, wenn Kosten wichtiger sind als Latenz.

Der Schnellmodus ist kein anderes Modell. Er verwendet denselben Opus 4.6 mit einer anderen API-Konfiguration, die Geschwindigkeit über Kosteneffizienz priorisiert. Sie erhalten identische Qualität und Funktionen, nur schnellere Antworten.

<Note>
  Der Schnellmodus erfordert Claude Code v2.1.36 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

Was Sie wissen sollten:

* Verwenden Sie `/fast`, um den Schnellmodus in Claude Code CLI ein- oder auszuschalten. Auch über `/fast` in der Claude Code VS Code Extension verfügbar.
* Die Preisgestaltung für den Schnellmodus auf Opus 4.6 beginnt bei \$30/150 MTok. Der Schnellmodus ist bis 23:59 Uhr PT am 16. Februar mit 50 % Rabatt für alle Pläne verfügbar.
* Verfügbar für alle Claude Code-Benutzer mit Abonnementplänen (Pro/Max/Team/Enterprise) und Claude Console.
* Für Claude Code-Benutzer mit Abonnementplänen (Pro/Max/Team/Enterprise) ist der Schnellmodus nur über zusätzliche Nutzung verfügbar und nicht in den Abonnement-Ratenlimits enthalten.

Diese Seite behandelt, wie Sie [den Schnellmodus aktivieren](#toggle-fast-mode), seine [Kostenabwägung](#understand-the-cost-tradeoff), [wann Sie ihn verwenden](#decide-when-to-use-fast-mode), [Anforderungen](#requirements), [Opt-in pro Sitzung](#require-per-session-opt-in) und [Ratenlimit-Verhalten](#handle-rate-limits).

## Schnellmodus aktivieren

Aktivieren Sie den Schnellmodus auf eine dieser Weisen:

* Geben Sie `/fast` ein und drücken Sie Tab, um ihn ein- oder auszuschalten
* Setzen Sie `"fastMode": true` in Ihrer [Benutzereinstellungsdatei](/de/settings)

Standardmäßig bleibt der Schnellmodus über Sitzungen hinweg erhalten. Administratoren können den Schnellmodus so konfigurieren, dass er sich bei jeder Sitzung zurückgesetzt wird. Weitere Informationen finden Sie unter [Opt-in pro Sitzung erforderlich](#require-per-session-opt-in).

Für die beste Kosteneffizienz aktivieren Sie den Schnellmodus am Anfang einer Sitzung, anstatt ihn mitten in einem Gespräch zu wechseln. Weitere Informationen finden Sie unter [Kostenabwägung verstehen](#understand-the-cost-tradeoff).

Wenn Sie den Schnellmodus aktivieren:

* Wenn Sie sich auf einem anderen Modell befinden, wechselt Claude Code automatisch zu Opus 4.6
* Sie sehen eine Bestätigungsmeldung: „Fast mode ON"
* Ein kleines `↯`-Symbol wird neben der Eingabeaufforderung angezeigt, während der Schnellmodus aktiv ist
* Führen Sie `/fast` jederzeit erneut aus, um zu überprüfen, ob der Schnellmodus aktiviert oder deaktiviert ist

Wenn Sie den Schnellmodus mit `/fast` erneut deaktivieren, bleiben Sie auf Opus 4.6. Das Modell wird nicht auf Ihr vorheriges Modell zurückgesetzt. Um zu einem anderen Modell zu wechseln, verwenden Sie `/model`.

## Kostenabwägung verstehen

Der Schnellmodus hat höhere Pro-Token-Preise als Standard-Opus 4.6:

| Modus                              | Eingabe (MTok) | Ausgabe (MTok) |
| ---------------------------------- | -------------- | -------------- |
| Schnellmodus auf Opus 4.6 (\<200K) | \$30           | \$150          |
| Schnellmodus auf Opus 4.6 (>200K)  | \$60           | \$225          |

Der Schnellmodus ist mit dem erweiterten Kontextfenster mit 1M Token kompatibel.

Wenn Sie mitten in einem Gespräch in den Schnellmodus wechseln, zahlen Sie den vollständigen Schnellmodus-Preis für nicht zwischengespeicherte Eingabe-Token für den gesamten Gesprächskontext. Dies kostet mehr, als wenn Sie den Schnellmodus von Anfang an aktiviert hätten.

## Entscheiden Sie, wann Sie den Schnellmodus verwenden

Der Schnellmodus ist am besten für interaktive Arbeiten geeignet, bei denen die Antwortlatenz wichtiger ist als die Kosten:

* Schnelle Iteration bei Code-Änderungen
* Live-Debugging-Sitzungen
* Zeitkritische Arbeiten mit engen Fristen

Der Standardmodus ist besser für:

* Lange autonome Aufgaben, bei denen Geschwindigkeit weniger wichtig ist
* Batch-Verarbeitung oder CI/CD-Pipelines
* Kostenempfindliche Arbeitslasten

### Schnellmodus vs. Anstrengungsstufe

Der Schnellmodus und die Anstrengungsstufe beeinflussen beide die Antwortgeschwindigkeit, aber auf unterschiedliche Weise:

| Einstellung                      | Auswirkung                                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Schnellmodus**                 | Gleiche Modellqualität, niedrigere Latenz, höhere Kosten                                          |
| **Niedrigere Anstrengungsstufe** | Weniger Denkzeit, schnellere Antworten, möglicherweise niedrigere Qualität bei komplexen Aufgaben |

Sie können beide kombinieren: Verwenden Sie den Schnellmodus mit einer niedrigeren [Anstrengungsstufe](/de/model-config#adjust-effort-level) für maximale Geschwindigkeit bei einfachen Aufgaben.

## Anforderungen

Der Schnellmodus erfordert alle folgenden Voraussetzungen:

* **Nicht auf Cloud-Anbietern von Drittanbietern verfügbar**: Der Schnellmodus ist nicht auf Amazon Bedrock, Google Vertex AI oder Microsoft Azure Foundry verfügbar. Der Schnellmodus ist über die Anthropic Console API und für Claude-Abonnementpläne mit zusätzlicher Nutzung verfügbar.
* **Zusätzliche Nutzung aktiviert**: Ihr Konto muss zusätzliche Nutzung aktiviert haben, die eine Abrechnung über die in Ihrem Plan enthaltene Nutzung hinaus ermöglicht. Aktivieren Sie dies für einzelne Konten in Ihren [Console-Abrechnungseinstellungen](https://platform.claude.com/settings/organization/billing). Für Teams und Enterprise muss ein Administrator die zusätzliche Nutzung für die Organisation aktivieren.

<Note>
  Die Nutzung des Schnellmodus wird direkt zur zusätzlichen Nutzung abgerechnet, auch wenn Sie noch Nutzung in Ihrem Plan haben. Dies bedeutet, dass Schnellmodus-Token nicht gegen die in Ihrem Plan enthaltene Nutzung angerechnet werden und vom ersten Token an zum Schnellmodus-Tarif berechnet werden.
</Note>

* **Admin-Aktivierung für Teams und Enterprise**: Der Schnellmodus ist standardmäßig für Teams- und Enterprise-Organisationen deaktiviert. Ein Administrator muss den Schnellmodus explizit [aktivieren](#enable-fast-mode-for-your-organization), bevor Benutzer darauf zugreifen können.

<Note>
  Wenn Ihr Administrator den Schnellmodus für Ihre Organisation nicht aktiviert hat, zeigt der Befehl `/fast` „Fast mode has been disabled by your organization." an.
</Note>

### Schnellmodus für Ihre Organisation aktivieren

Administratoren können den Schnellmodus aktivieren in:

* **Console** (API-Kunden): [Claude Code-Einstellungen](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Teams und Enterprise): [Admin-Einstellungen > Claude Code](https://claude.ai/admin-settings/claude-code)

Eine weitere Option zum vollständigen Deaktivieren des Schnellmodus ist das Setzen von `CLAUDE_CODE_DISABLE_FAST_MODE=1`. Siehe [Umgebungsvariablen](/de/env-vars).

### Opt-in pro Sitzung erforderlich

Standardmäßig bleibt der Schnellmodus über Sitzungen hinweg erhalten: Wenn ein Benutzer den Schnellmodus aktiviert, bleibt er in zukünftigen Sitzungen aktiviert. Administratoren in [Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise)- oder [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise)-Plänen können dies verhindern, indem sie `fastModePerSessionOptIn` in [verwalteten Einstellungen](/de/settings#settings-files) oder [servergesteuerten Einstellungen](/de/server-managed-settings) auf `true` setzen. Dies führt dazu, dass jede Sitzung mit deaktiviertem Schnellmodus beginnt und Benutzer ihn explizit mit `/fast` aktivieren müssen.

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

Dies ist nützlich zur Kostenkontrolle in Organisationen, in denen Benutzer mehrere gleichzeitige Sitzungen ausführen. Benutzer können den Schnellmodus immer noch mit `/fast` aktivieren, wenn sie Geschwindigkeit benötigen, aber er wird zu Beginn jeder neuen Sitzung zurückgesetzt. Die Schnellmodus-Einstellung des Benutzers wird immer noch gespeichert, sodass das Entfernen dieser Einstellung das standardmäßige persistente Verhalten wiederherstellt.

## Ratenlimits handhaben

Der Schnellmodus hat separate Ratenlimits vom Standard-Opus 4.6. Wenn Sie das Ratenlimit des Schnellmodus erreichen oder keine zusätzlichen Nutzungsguthaben mehr haben:

1. Der Schnellmodus fällt automatisch auf Standard-Opus 4.6 zurück
2. Das `↯`-Symbol wird grau, um die Abkühlung anzuzeigen
3. Sie arbeiten weiterhin mit Standard-Geschwindigkeit und -Preisen
4. Wenn die Abkühlung abläuft, wird der Schnellmodus automatisch wieder aktiviert

Um den Schnellmodus manuell zu deaktivieren, anstatt auf die Abkühlung zu warten, führen Sie `/fast` erneut aus.

## Forschungsvorschau

Der Schnellmodus ist eine Forschungsvorschau-Funktion. Dies bedeutet:

* Die Funktion kann sich basierend auf Feedback ändern
* Verfügbarkeit und Preisgestaltung können sich ändern
* Die zugrunde liegende API-Konfiguration kann sich weiterentwickeln

Melden Sie Probleme oder Feedback über Ihre üblichen Anthropic-Supportkanäle.

## Siehe auch

* [Modellkonfiguration](/de/model-config): Wechseln Sie Modelle und passen Sie Anstrengungsstufen an
* [Kosten effektiv verwalten](/de/costs): Verfolgen Sie die Token-Nutzung und reduzieren Sie Kosten
* [Statuszeilen-Konfiguration](/de/statusline): Zeigen Sie Modell- und Kontextinformationen an
