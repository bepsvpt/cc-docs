> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modellkonfiguration

> Erfahren Sie mehr über die Claude Code-Modellkonfiguration, einschließlich Modellaliase wie `opusplan`

## Verfügbare Modelle

Für die `model`-Einstellung in Claude Code können Sie konfigurieren:

* Einen **Modellalias**
* Einen **Modellnamen**
  * Anthropic API: Ein vollständiger **[Modellname](https://platform.claude.com/docs/de/about-claude/models/overview)**
  * Bedrock: ein Inference-Profil-ARN
  * Foundry: ein Bereitstellungsname
  * Vertex: ein Versionsname

### Modellaliase

Modellaliase bieten eine bequeme Möglichkeit, Modelleinstellungen auszuwählen, ohne sich genaue Versionsnummern merken zu müssen:

| Modellalias      | Verhalten                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`default`**    | Empfohlene Modelleinstellung, abhängig von Ihrem Kontotyp                                                                                                                      |
| **`sonnet`**     | Verwendet das neueste Sonnet-Modell (derzeit Sonnet 4.6) für tägliche Codierungsaufgaben                                                                                       |
| **`opus`**       | Verwendet das neueste Opus-Modell (derzeit Opus 4.6) für komplexe Reasoning-Aufgaben                                                                                           |
| **`haiku`**      | Verwendet das schnelle und effiziente Haiku-Modell für einfache Aufgaben                                                                                                       |
| **`sonnet[1m]`** | Verwendet Sonnet mit einem [1-Million-Token-Kontextfenster](https://platform.claude.com/docs/de/build-with-claude/context-windows#1m-token-context-window) für lange Sitzungen |
| **`opusplan`**   | Spezieller Modus, der `opus` während des Plan Mode verwendet und dann zu `sonnet` für die Ausführung wechselt                                                                  |

Aliase verweisen immer auf die neueste Version. Um eine bestimmte Version zu fixieren, verwenden Sie den vollständigen Modellnamen (z. B. `claude-opus-4-6`) oder setzen Sie die entsprechende Umgebungsvariable wie `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Einstellung Ihres Modells

Sie können Ihr Modell auf mehrere Arten konfigurieren, aufgelistet nach Priorität:

1. **Während der Sitzung** - Verwenden Sie `/model <alias|name>`, um Modelle während der Sitzung zu wechseln
2. **Beim Start** - Starten Sie mit `claude --model <alias|name>`
3. **Umgebungsvariable** - Setzen Sie `ANTHROPIC_MODEL=<alias|name>`
4. **Einstellungen** - Konfigurieren Sie dauerhaft in Ihrer Einstellungsdatei mit dem `model`-Feld.

Beispielverwendung:

```bash  theme={null}
# Start mit Opus
claude --model opus

# Wechsel zu Sonnet während der Sitzung
/model sonnet
```

Beispiel-Einstellungsdatei:

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Modellauswahl einschränken

Enterprise-Administratoren können `availableModels` in [verwalteten oder Richtlinieneinstellungen](/de/settings#settings-files) verwenden, um einzuschränken, welche Modelle Benutzer auswählen können.

Wenn `availableModels` gesetzt ist, können Benutzer nicht über `/model`, das `--model`-Flag, das Config-Tool oder die `ANTHROPIC_MODEL`-Umgebungsvariable zu Modellen wechseln, die nicht in der Liste enthalten sind.

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Standardmodell-Verhalten

Die Option „Standard" in der Modellauswahl wird von `availableModels` nicht beeinflusst. Sie bleibt immer verfügbar und stellt den Laufzeit-Standard des Systems dar, [basierend auf dem Abonnement-Tier des Benutzers](#default-model-setting).

Auch mit `availableModels: []` können Benutzer Claude Code weiterhin mit dem Standardmodell für ihren Tier verwenden.

### Kontrollieren Sie das Modell, auf dem Benutzer ausgeführt werden

Um die Modellerfahrung vollständig zu kontrollieren, verwenden Sie `availableModels` zusammen mit der `model`-Einstellung:

* **availableModels**: schränkt ein, zu welchen Modellen Benutzer wechseln können
* **model**: setzt die explizite Modellüberschreibung, die Vorrang vor dem Standard hat

Dieses Beispiel stellt sicher, dass alle Benutzer Sonnet 4.6 ausführen und nur zwischen Sonnet und Haiku wählen können:

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### Merge-Verhalten

Wenn `availableModels` auf mehreren Ebenen gesetzt ist, z. B. in Benutzereinstellungen und Projekteinstellungen, werden Arrays zusammengeführt und dedupliziert. Um eine strikte Allowlist durchzusetzen, setzen Sie `availableModels` in verwalteten oder Richtlinieneinstellungen, die die höchste Priorität haben.

## Spezielles Modellverhalten

### `default`-Modelleinstellung

Das Verhalten von `default` hängt von Ihrem Kontotyp ab:

* **Max und Team Premium**: Standard ist Opus 4.6
* **Pro und Team Standard**: Standard ist Sonnet 4.6
* **Enterprise**: Opus 4.6 ist verfügbar, aber nicht der Standard

Claude Code kann automatisch auf Sonnet zurückfallen, wenn Sie einen Nutzungsschwellenwert mit Opus erreichen.

### `opusplan`-Modelleinstellung

Der `opusplan`-Modellalias bietet einen automatisierten Hybrid-Ansatz:

* **Im Plan Mode** - Verwendet `opus` für komplexes Reasoning und Architekturentscheidungen
* **Im Execution Mode** - Wechselt automatisch zu `sonnet` für Code-Generierung und Implementierung

Dies gibt Ihnen das Beste aus beiden Welten: Opus's überlegenes Reasoning für die Planung und Sonnets Effizienz für die Ausführung.

### Anpassung des Aufwandsniveaus

[Aufwandsniveaus](https://platform.claude.com/docs/de/build-with-claude/effort) steuern adaptives Reasoning, das das Denken dynamisch basierend auf der Aufgabenkomplexität zuordnet. Niedrigerer Aufwand ist schneller und günstiger für unkomplizierte Aufgaben, während höherer Aufwand tieferes Reasoning für komplexe Probleme bietet.

Drei Ebenen sind verfügbar: **low**, **medium** und **high**. Opus 4.6 hat standardmäßig mittleren Aufwand für Max- und Team-Abonnenten.

**Aufwand einstellen:**

* **In `/model`**: Verwenden Sie die Pfeiltasten nach links/rechts, um den Aufwand-Schieberegler anzupassen, wenn Sie ein Modell auswählen
* **Umgebungsvariable**: Setzen Sie `CLAUDE_CODE_EFFORT_LEVEL=low|medium|high`
* **Einstellungen**: Setzen Sie `effortLevel` in Ihrer Einstellungsdatei

Der Aufwand wird auf Opus 4.6 und Sonnet 4.6 unterstützt. Der Aufwand-Schieberegler erscheint in `/model`, wenn ein unterstütztes Modell ausgewählt ist. Das aktuelle Aufwandsniveau wird auch neben dem Logo und Spinner angezeigt (z. B. „with low effort"), damit Sie bestätigen können, welche Einstellung aktiv ist, ohne `/model` zu öffnen.

Um adaptives Reasoning auf Opus 4.6 und Sonnet 4.6 zu deaktivieren und auf das vorherige feste Thinking-Budget zurückzukehren, setzen Sie `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Wenn deaktiviert, verwenden diese Modelle das feste Budget, das von `MAX_THINKING_TOKENS` gesteuert wird. Siehe [Umgebungsvariablen](/de/settings#environment-variables).

### Erweiterter Kontext

Opus 4.6 und Sonnet 4.6 unterstützen ein [1-Million-Token-Kontextfenster](https://platform.claude.com/docs/de/build-with-claude/context-windows#1m-token-context-window) für lange Sitzungen mit großen Codebases.

<Note>
  Das 1M-Kontextfenster befindet sich derzeit in der Beta-Phase. Funktionen, Preise und Verfügbarkeit können sich ändern.
</Note>

Erweiterter Kontext ist verfügbar für:

* **API- und Pay-as-you-go-Benutzer**: Vollzugriff auf 1M-Kontext
* **Pro-, Max-, Teams- und Enterprise-Abonnenten**: verfügbar mit [zusätzlicher Nutzung](https://support.claude.com/de/articles/12429409-extra-usage-for-paid-claude-plans) aktiviert

Um 1M-Kontext vollständig zu deaktivieren, setzen Sie `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Dies entfernt 1M-Modellvarianten aus der Modellauswahl. Siehe [Umgebungsvariablen](/de/settings#environment-variables).

Die Auswahl eines 1M-Modells ändert die Abrechnung nicht sofort. Ihre Sitzung verwendet Standardsätze, bis sie 200K Token Kontext überschreitet. Jenseits von 200K Token werden Anfragen mit [Long-Context-Preisen](https://platform.claude.com/docs/de/about-claude/pricing#long-context-pricing) und dedizierten [Rate Limits](https://platform.claude.com/docs/de/api/rate-limits#long-context-rate-limits) berechnet. Für Abonnenten werden Token jenseits von 200K als zusätzliche Nutzung statt durch das Abonnement abgerechnet.

Wenn Ihr Konto 1M-Kontext unterstützt, erscheint die Option in der Modellauswahl (`/model`) in den neuesten Versionen von Claude Code. Wenn Sie sie nicht sehen, versuchen Sie, Ihre Sitzung neu zu starten.

Sie können auch das `[1m]`-Suffix mit Modellaliasen oder vollständigen Modellnamen verwenden:

```bash  theme={null}
# Verwenden Sie den sonnet[1m]-Alias
/model sonnet[1m]

# Oder fügen Sie [1m] zu einem vollständigen Modellnamen hinzu
/model claude-sonnet-4-6[1m]
```

## Überprüfung Ihres aktuellen Modells

Sie können sehen, welches Modell Sie derzeit verwenden, auf mehrere Arten:

1. In der [Statuszeile](/de/statusline) (falls konfiguriert)
2. In `/status`, das auch Ihre Kontoinformationen anzeigt.

## Umgebungsvariablen

Sie können die folgenden Umgebungsvariablen verwenden, die vollständige **Modellnamen** (oder Äquivalente für Ihren API-Anbieter) sein müssen, um die Modellnamen zu steuern, auf die die Aliase verweisen.

| Umgebungsvariable                | Beschreibung                                                                                                          |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Das Modell, das für `opus` verwendet werden soll, oder für `opusplan`, wenn Plan Mode aktiv ist.                      |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Das Modell, das für `sonnet` verwendet werden soll, oder für `opusplan`, wenn Plan Mode nicht aktiv ist.              |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Das Modell, das für `haiku` verwendet werden soll, oder [Hintergrundfunktionalität](/de/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Das Modell, das für [subagents](/de/sub-agents) verwendet werden soll                                                 |

Hinweis: `ANTHROPIC_SMALL_FAST_MODEL` ist veraltet zugunsten von `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Modelle für Drittanbieter-Bereitstellungen fixieren

Beim Bereitstellen von Claude Code über [Bedrock](/de/amazon-bedrock), [Vertex AI](/de/google-vertex-ai) oder [Foundry](/de/microsoft-foundry) sollten Sie Modellversionen vor dem Rollout für Benutzer fixieren.

Ohne Fixierung verwendet Claude Code Modellaliase (`sonnet`, `opus`, `haiku`), die zur neuesten Version aufgelöst werden. Wenn Anthropic ein neues Modell veröffentlicht, werden Benutzer, deren Konten die neue Version nicht aktiviert haben, stillschweigend unterbrochen.

<Warning>
  Setzen Sie alle drei Modell-Umgebungsvariablen auf spezifische Versions-IDs als Teil Ihres anfänglichen Setups. Das Überspringen dieses Schritts bedeutet, dass ein Claude Code-Update Ihre Benutzer ohne Maßnahmen Ihrerseits unterbrechen kann.
</Warning>

Verwenden Sie die folgenden Umgebungsvariablen mit versionsspezifischen Modell-IDs für Ihren Anbieter:

| Anbieter  | Beispiel                                                                |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Wenden Sie das gleiche Muster auf `ANTHROPIC_DEFAULT_SONNET_MODEL` und `ANTHROPIC_DEFAULT_HAIKU_MODEL` an. Für aktuelle und ältere Modell-IDs über alle Anbieter hinweg siehe [Modellübersicht](https://platform.claude.com/docs/de/about-claude/models/overview). Um Benutzer auf eine neue Modellversion zu aktualisieren, aktualisieren Sie diese Umgebungsvariablen und stellen Sie erneut bereit.

<Note>
  Die `settings.availableModels`-Allowlist gilt weiterhin bei Verwendung von Drittanbieter-Anbietern. Die Filterung stimmt mit dem Modellalias (`opus`, `sonnet`, `haiku`) überein, nicht mit der anbieterspezifischen Modell-ID.
</Note>

### Modell-IDs pro Version überschreiben

Die oben genannten Umgebungsvariablen auf Familienebene konfigurieren eine Modell-ID pro Familienalias. Wenn Sie mehrere Versionen innerhalb derselben Familie verschiedenen Anbieter-IDs zuordnen müssen, verwenden Sie stattdessen die `modelOverrides`-Einstellung.

`modelOverrides` ordnet einzelne Anthropic-Modell-IDs den anbieterspezifischen Strings zu, die Claude Code an die API Ihres Anbieters sendet. Wenn ein Benutzer ein zugeordnetes Modell in der `/model`-Auswahl auswählt, verwendet Claude Code Ihren konfigurierten Wert statt des integrierten Standards.

Dies ermöglicht es Enterprise-Administratoren, jede Modellversion zu einem bestimmten Bedrock-Inference-Profil-ARN, Vertex AI-Versionsnamen oder Foundry-Bereitstellungsnamen für Governance, Kostenzuteilung oder regionales Routing zu leiten.

Setzen Sie `modelOverrides` in Ihrer [Einstellungsdatei](/de/settings#settings-files):

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Schlüssel müssen Anthropic-Modell-IDs sein, wie in der [Modellübersicht](https://platform.claude.com/docs/de/about-claude/models/overview) aufgelistet. Für datierte Modell-IDs fügen Sie das Datumssuffix genau so ein, wie es dort angezeigt wird. Unbekannte Schlüssel werden ignoriert.

Überschreibungen ersetzen die integrierten Modell-IDs, die jeden Eintrag in der `/model`-Auswahl unterstützen. Bei Bedrock haben Überschreibungen Vorrang vor allen Inference-Profilen, die Claude Code beim Start automatisch erkennt. Werte, die Sie direkt über `ANTHROPIC_MODEL`, `--model` oder die `ANTHROPIC_DEFAULT_*_MODEL`-Umgebungsvariablen bereitstellen, werden unverändert an den Anbieter übergeben und werden nicht durch `modelOverrides` transformiert.

`modelOverrides` funktioniert zusammen mit `availableModels`. Die Allowlist wird gegen die Anthropic-Modell-ID ausgewertet, nicht gegen den Überschreibungswert, daher ein Eintrag wie `"opus"` in `availableModels` weiterhin übereinstimmt, auch wenn Opus-Versionen ARNs zugeordnet sind.

### Prompt-Caching-Konfiguration

Claude Code verwendet automatisch [Prompt Caching](https://platform.claude.com/docs/de/build-with-claude/prompt-caching), um die Leistung zu optimieren und Kosten zu senken. Sie können Prompt Caching global oder für bestimmte Modell-Tiers deaktivieren:

| Umgebungsvariable               | Beschreibung                                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Setzen Sie auf `1`, um Prompt Caching für alle Modelle zu deaktivieren (hat Vorrang vor modellspezifischen Einstellungen) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Setzen Sie auf `1`, um Prompt Caching nur für Haiku-Modelle zu deaktivieren                                               |
| `DISABLE_PROMPT_CACHING_SONNET` | Setzen Sie auf `1`, um Prompt Caching nur für Sonnet-Modelle zu deaktivieren                                              |
| `DISABLE_PROMPT_CACHING_OPUS`   | Setzen Sie auf `1`, um Prompt Caching nur für Opus-Modelle zu deaktivieren                                                |

Diese Umgebungsvariablen geben Ihnen eine feinkörnige Kontrolle über das Prompt-Caching-Verhalten. Die globale `DISABLE_PROMPT_CACHING`-Einstellung hat Vorrang vor den modellspezifischen Einstellungen, sodass Sie das gesamte Caching bei Bedarf schnell deaktivieren können. Die modellspezifischen Einstellungen sind nützlich für selektive Kontrolle, z. B. beim Debuggen bestimmter Modelle oder bei der Arbeit mit Cloud-Anbietern, die möglicherweise unterschiedliche Caching-Implementierungen haben.
