> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modellkonfiguration

> Erfahren Sie mehr über die Claude Code-Modellkonfiguration, einschließlich Modellaliase wie `opusplan`

## Verfügbare Modelle

Für die `model`-Einstellung in Claude Code können Sie konfigurieren:

* Einen **Modellalias**
* Einen **Modellnamen**
  * Anthropic API: Einen vollständigen **[Modellnamen](https://platform.claude.com/docs/de/about-claude/models/overview)**
  * Bedrock: ein Inference-Profil-ARN
  * Foundry: einen Bereitstellungsnamen
  * Vertex: einen Versionsnamen

### Modellaliase

Modellaliase bieten eine bequeme Möglichkeit, Modelleinstellungen auszuwählen, ohne sich genaue Versionsnummern merken zu müssen:

| Modellalias      | Verhalten                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`default`**    | Spezieller Wert, der jede Modellüberschreibung löscht und auf das empfohlene Modell für Ihren Kontotyp zurückgesetzt wird. Ist selbst kein Modellalias                         |
| **`best`**       | Verwendet das leistungsfähigste verfügbare Modell, derzeit gleichwertig mit `opus`                                                                                             |
| **`sonnet`**     | Verwendet das neueste Sonnet-Modell (derzeit Sonnet 4.6) für tägliche Codierungsaufgaben                                                                                       |
| **`opus`**       | Verwendet das neueste Opus-Modell (derzeit Opus 4.6) für komplexe Reasoning-Aufgaben                                                                                           |
| **`haiku`**      | Verwendet das schnelle und effiziente Haiku-Modell für einfache Aufgaben                                                                                                       |
| **`sonnet[1m]`** | Verwendet Sonnet mit einem [1-Million-Token-Kontextfenster](https://platform.claude.com/docs/de/build-with-claude/context-windows#1m-token-context-window) für lange Sitzungen |
| **`opus[1m]`**   | Verwendet Opus mit einem [1-Million-Token-Kontextfenster](https://platform.claude.com/docs/de/build-with-claude/context-windows#1m-token-context-window) für lange Sitzungen   |
| **`opusplan`**   | Spezieller Modus, der `opus` während des Plan-Modus verwendet und dann zu `sonnet` für die Ausführung wechselt                                                                 |

Aliase verweisen immer auf die neueste Version. Um eine bestimmte Version zu fixieren, verwenden Sie den vollständigen Modellnamen (z. B. `claude-opus-4-6`) oder setzen Sie die entsprechende Umgebungsvariable wie `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Einstellung Ihres Modells

Sie können Ihr Modell auf mehrere Arten konfigurieren, aufgelistet nach Priorität:

1. **Während der Sitzung** - Verwenden Sie `/model <alias|name>`, um Modelle während der Sitzung zu wechseln
2. **Beim Start** - Starten Sie mit `claude --model <alias|name>`
3. **Umgebungsvariable** - Setzen Sie `ANTHROPIC_MODEL=<alias|name>`
4. **Einstellungen** - Konfigurieren Sie dauerhaft in Ihrer Einstellungsdatei mit dem `model`-Feld.

Beispielverwendung:

```bash theme={null}
# Mit Opus starten
claude --model opus

# Während der Sitzung zu Sonnet wechseln
/model sonnet
```

Beispiel-Einstellungsdatei:

```json theme={null}
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

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Standardmodell-Verhalten

Die Option „Standard" in der Modellauswahl wird von `availableModels` nicht beeinflusst. Sie bleibt immer verfügbar und stellt den Laufzeit-Standard des Systems dar, [basierend auf dem Abonnement-Tier des Benutzers](#default-model-setting).

Auch mit `availableModels: []` können Benutzer Claude Code weiterhin mit dem Standardmodell für ihren Tier verwenden.

### Kontrollieren Sie das Modell, auf dem Benutzer ausgeführt werden

Die `model`-Einstellung ist eine anfängliche Auswahl, keine Erzwingung. Sie legt fest, welches Modell aktiv ist, wenn eine Sitzung startet, aber Benutzer können weiterhin `/model` öffnen und „Standard" auswählen, das unabhängig davon auf den Systemstandard für ihren Tier aufgelöst wird, was `model` gesetzt ist.

Um die Modellerfahrung vollständig zu kontrollieren, kombinieren Sie drei Einstellungen:

* **`availableModels`**: schränkt ein, worauf Benutzer wechseln können
* **`model`**: legt die anfängliche Modellauswahl fest, wenn eine Sitzung startet
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**: steuern, worauf sich die Option „Standard" und die Aliase `sonnet`, `opus` und `haiku` auflösen

Dieses Beispiel startet Benutzer auf Sonnet 4.5, begrenzt die Auswahl auf Sonnet und Haiku und fixiert „Standard" auf Sonnet 4.5 statt auf die neueste Version:

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Ohne den `env`-Block würde ein Benutzer, der „Standard" in der Auswahl auswählt, die neueste Sonnet-Version erhalten und damit die Versionsfixierung in `model` und `availableModels` umgehen.

### Merge-Verhalten

Wenn `availableModels` auf mehreren Ebenen gesetzt ist, z. B. in Benutzereinstellungen und Projekteinstellungen, werden Arrays zusammengeführt und dedupliziert. Um eine strikte Zulassungsliste durchzusetzen, setzen Sie `availableModels` in verwalteten oder Richtlinieneinstellungen, die die höchste Priorität haben.

## Spezielles Modellverhalten

### `default`-Modelleinstellung

Das Verhalten von `default` hängt von Ihrem Kontotyp ab:

* **Max und Team Premium**: Standard ist Opus 4.6
* **Pro und Team Standard**: Standard ist Sonnet 4.6
* **Enterprise**: Opus 4.6 ist verfügbar, aber nicht der Standard

Claude Code kann automatisch auf Sonnet zurückfallen, wenn Sie einen Nutzungsschwellenwert mit Opus erreichen.

### `opusplan`-Modelleinstellung

Der `opusplan`-Modellalias bietet einen automatisierten Hybrid-Ansatz:

* **Im Plan-Modus** - Verwendet `opus` für komplexes Reasoning und Architekturentscheidungen
* **Im Ausführungsmodus** - Wechselt automatisch zu `sonnet` für Code-Generierung und Implementierung

Dies gibt Ihnen das Beste aus beiden Welten: Opus's überlegenes Reasoning für die Planung und Sonnets Effizienz für die Ausführung.

### Anpassung des Aufwandsniveaus

[Aufwandsniveaus](https://platform.claude.com/docs/de/build-with-claude/effort) steuern adaptives Reasoning, das das Denken dynamisch basierend auf der Aufgabenkomplexität zuordnet. Niedrigerer Aufwand ist schneller und günstiger für unkomplizierte Aufgaben, während höherer Aufwand tieferes Reasoning für komplexe Probleme bietet.

Drei Ebenen bleiben über Sitzungen hinweg erhalten: **low**, **medium** und **high**. Eine vierte Ebene, **max**, bietet das tiefste Reasoning ohne Einschränkung bei der Token-Ausgabe, daher sind Antworten langsamer und kosten mehr als bei `high`. `max` ist nur auf Opus 4.6 verfügbar und bleibt nicht über Sitzungen hinweg erhalten, außer durch die `CLAUDE_CODE_EFFORT_LEVEL`-Umgebungsvariable.

Opus 4.6 und Sonnet 4.6 haben standardmäßig mittleren Aufwand. Dies gilt für alle Anbieter, einschließlich Bedrock, Vertex AI und direktem API-Zugriff.

Medium ist die empfohlene Ebene für die meisten Codierungsaufgaben: Sie bietet ein Gleichgewicht zwischen Geschwindigkeit und Reasoning-Tiefe, und höhere Ebenen können dazu führen, dass das Modell Routinearbeiten überdenkt. Reservieren Sie `high` oder `max` für Aufgaben, die wirklich von tieferem Reasoning profitieren, wie z. B. schwierige Debugging-Probleme oder komplexe Architekturentscheidungen.

Für einmaliges tiefes Reasoning ohne Änderung Ihrer Sitzungseinstellung fügen Sie „ultrathink" in Ihren Prompt ein, um hohen Aufwand für diesen Durchgang auszulösen.

**Aufwand einstellen:**

* **`/effort`**: Führen Sie `/effort low`, `/effort medium`, `/effort high` oder `/effort max` aus, um die Ebene zu ändern, oder `/effort auto`, um auf den Modellstandard zurückzusetzen
* **In `/model`**: Verwenden Sie die Pfeiltasten nach links/rechts, um den Aufwand-Schieberegler anzupassen, wenn Sie ein Modell auswählen
* **`--effort`-Flag**: Übergeben Sie `low`, `medium`, `high` oder `max`, um die Ebene für eine einzelne Sitzung beim Starten von Claude Code festzulegen
* **Umgebungsvariable**: Setzen Sie `CLAUDE_CODE_EFFORT_LEVEL` auf `low`, `medium`, `high`, `max` oder `auto`
* **Einstellungen**: Setzen Sie `effortLevel` in Ihrer Einstellungsdatei auf `"low"`, `"medium"` oder `"high"`
* **Skill- und Subagent-Frontmatter**: Setzen Sie `effort` in einer [Skill](/de/skills#frontmatter-reference)- oder [Subagent](/de/sub-agents#supported-frontmatter-fields)-Markdown-Datei, um das Aufwandsniveau zu überschreiben, wenn dieser Skill oder Subagent ausgeführt wird

Die Umgebungsvariable hat Vorrang vor allen anderen Methoden, dann Ihre konfigurierte Ebene, dann der Modellstandard. Frontmatter-Aufwand gilt, wenn dieser Skill oder Subagent aktiv ist, und überschreibt die Sitzungsebene, aber nicht die Umgebungsvariable.

Der Aufwand wird auf Opus 4.6 und Sonnet 4.6 unterstützt. Der Aufwand-Schieberegler erscheint in `/model`, wenn ein unterstütztes Modell ausgewählt ist. Das aktuelle Aufwandsniveau wird auch neben dem Logo und dem Spinner angezeigt, z. B. „with low effort", damit Sie bestätigen können, welche Einstellung aktiv ist, ohne `/model` zu öffnen.

Um adaptives Reasoning auf Opus 4.6 und Sonnet 4.6 zu deaktivieren und zum vorherigen festen Thinking-Budget zurückzukehren, setzen Sie `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Wenn deaktiviert, verwenden diese Modelle das feste Budget, das von `MAX_THINKING_TOKENS` gesteuert wird. Siehe [Umgebungsvariablen](/de/env-vars).

### Erweiterter Kontext

Opus 4.6 und Sonnet 4.6 unterstützen ein [1-Million-Token-Kontextfenster](https://platform.claude.com/docs/de/build-with-claude/context-windows#1m-token-context-window) für lange Sitzungen mit großen Codebases.

Die Verfügbarkeit variiert je nach Modell und Plan. Bei Max-, Team- und Enterprise-Plänen wird Opus automatisch auf 1M-Kontext ohne zusätzliche Konfiguration aktualisiert. Dies gilt für beide Team Standard- und Team Premium-Plätze.

| Plan                     | Opus 4.6 mit 1M-Kontext                                                                                            | Sonnet 4.6 mit 1M-Kontext                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Max, Team und Enterprise | Im Abonnement enthalten                                                                                            | Erfordert [zusätzliche Nutzung](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                      | Erfordert [zusätzliche Nutzung](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) | Erfordert [zusätzliche Nutzung](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API und Pay-as-you-go    | Vollständiger Zugriff                                                                                              | Vollständiger Zugriff                                                                                              |

Um 1M-Kontext vollständig zu deaktivieren, setzen Sie `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Dies entfernt 1M-Modellvarianten aus der Modellauswahl. Siehe [Umgebungsvariablen](/de/env-vars).

Das 1M-Kontextfenster verwendet Standard-Modellpreise ohne Aufschlag für Token über 200K. Für Pläne, bei denen erweiterter Kontext in Ihrem Abonnement enthalten ist, bleibt die Nutzung von Ihrem Abonnement abgedeckt. Für Pläne, die über zusätzliche Nutzung auf erweiterten Kontext zugreifen, werden Token zur zusätzlichen Nutzung abgerechnet.

Wenn Ihr Konto 1M-Kontext unterstützt, erscheint die Option in der Modellauswahl (`/model`) in den neuesten Versionen von Claude Code. Wenn Sie sie nicht sehen, versuchen Sie, Ihre Sitzung neu zu starten.

Sie können auch das `[1m]`-Suffix mit Modellaliasen oder vollständigen Modellnamen verwenden:

```bash theme={null}
# Verwenden Sie den opus[1m]- oder sonnet[1m]-Alias
/model opus[1m]
/model sonnet[1m]

# Oder fügen Sie [1m] an einen vollständigen Modellnamen an
/model claude-opus-4-6[1m]
```

## Überprüfung Ihres aktuellen Modells

Sie können sehen, welches Modell Sie derzeit verwenden, auf mehrere Arten:

1. In der [Statuszeile](/de/statusline) (falls konfiguriert)
2. In `/status`, das auch Ihre Kontoinformationen anzeigt.

## Benutzerdefinierte Modelloption hinzufügen

Verwenden Sie `ANTHROPIC_CUSTOM_MODEL_OPTION`, um einen einzelnen benutzerdefinierten Eintrag zur `/model`-Auswahl hinzuzufügen, ohne die integrierten Aliase zu ersetzen. Dies ist nützlich für LLM-Gateway-Bereitstellungen oder zum Testen von Modell-IDs, die Claude Code standardmäßig nicht auflistet.

Dieses Beispiel setzt alle drei Variablen, um eine Gateway-gesteuerte Opus-Bereitstellung auswählbar zu machen:

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-6"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

Der benutzerdefinierte Eintrag erscheint am unteren Ende der `/model`-Auswahl. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` und `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` sind optional. Wenn weggelassen, wird die Modell-ID als Name verwendet und die Beschreibung wird standardmäßig auf `Custom model (<model-id>)` gesetzt.

Claude Code überspringt die Validierung für die Modell-ID, die in `ANTHROPIC_CUSTOM_MODEL_OPTION` gesetzt ist, daher können Sie jeden String verwenden, den Ihr API-Endpunkt akzeptiert.

## Umgebungsvariablen

Sie können die folgenden Umgebungsvariablen verwenden, die vollständige **Modellnamen** (oder Äquivalente für Ihren API-Anbieter) sein müssen, um die Modellnamen zu steuern, auf die die Aliase verweisen.

| Umgebungsvariable                | Beschreibung                                                                                                          |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Das Modell, das für `opus` verwendet werden soll, oder für `opusplan`, wenn Plan Mode aktiv ist.                      |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Das Modell, das für `sonnet` verwendet werden soll, oder für `opusplan`, wenn Plan Mode nicht aktiv ist.              |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Das Modell, das für `haiku` verwendet werden soll, oder [Hintergrundfunktionalität](/de/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Das Modell, das für [Subagents](/de/sub-agents) verwendet werden soll                                                 |

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

Um [erweiterten Kontext](#extended-context) für ein fixiertes Modell zu aktivieren, fügen Sie `[1m]` an die Modell-ID in `ANTHROPIC_DEFAULT_OPUS_MODEL` oder `ANTHROPIC_DEFAULT_SONNET_MODEL` an:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

Das `[1m]`-Suffix wendet das 1M-Kontextfenster auf alle Verwendungen dieses Alias an, einschließlich `opusplan`. Claude Code entfernt das Suffix, bevor die Modell-ID an Ihren Anbieter gesendet wird. Fügen Sie `[1m]` nur an, wenn das zugrunde liegende Modell 1M-Kontext unterstützt, z. B. Opus 4.6 oder Sonnet 4.6.

<Note>
  Die `settings.availableModels`-Zulassungsliste gilt weiterhin bei Verwendung von Drittanbieter-Anbietern. Die Filterung stimmt mit dem Modellalias (`opus`, `sonnet`, `haiku`) überein, nicht mit der anbieterspezifischen Modell-ID.
</Note>

### Modell-IDs pro Version überschreiben

Die oben genannten Umgebungsvariablen auf Familienebene konfigurieren eine Modell-ID pro Familienalias. Wenn Sie mehrere Versionen innerhalb der gleichen Familie auf unterschiedliche Anbieter-IDs abbilden müssen, verwenden Sie stattdessen die `modelOverrides`-Einstellung.

`modelOverrides` ordnet einzelne Anthropic-Modell-IDs den anbieterspezifischen Strings zu, die Claude Code an die API Ihres Anbieters sendet. Wenn ein Benutzer ein zugeordnetes Modell in der `/model`-Auswahl auswählt, verwendet Claude Code Ihren konfigurierten Wert anstelle des integrierten Standards.

Dies ermöglicht es Enterprise-Administratoren, jede Modellversion zu einem bestimmten Bedrock-Inference-Profil-ARN, Vertex AI-Versionsnamen oder Foundry-Bereitstellungsnamen für Governance, Kostenzuteilung oder regionales Routing zu leiten.

Setzen Sie `modelOverrides` in Ihrer [Einstellungsdatei](/de/settings#settings-files):

```json theme={null}
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

`modelOverrides` funktioniert zusammen mit `availableModels`. Die Zulassungsliste wird gegen die Anthropic-Modell-ID ausgewertet, nicht gegen den Überschreibungswert, daher ein Eintrag wie `"opus"` in `availableModels` stimmt weiterhin überein, auch wenn Opus-Versionen ARNs zugeordnet sind.

### Anpassung der Anzeige und Funktionen des fixierten Modells

Wenn Sie ein Modell bei einem Drittanbieter fixieren, erscheint die anbieterspezifische ID in der `/model`-Auswahl und Claude Code erkennt möglicherweise nicht, welche Funktionen das Modell unterstützt. Sie können den Anzeigenamen und die deklarierten Funktionen mit Begleit-Umgebungsvariablen für jedes fixierte Modell überschreiben.

Diese Variablen wirken sich nur auf Drittanbieter wie Bedrock, Vertex AI und Foundry aus. Sie haben keine Auswirkung bei direkter Verwendung der Anthropic API.

| Umgebungsvariable                                     | Beschreibung                                                                                                                     |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Anzeigename für das fixierte Opus-Modell in der `/model`-Auswahl. Standardmäßig die Modell-ID, wenn nicht gesetzt                |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Anzeige-Beschreibung für das fixierte Opus-Modell in der `/model`-Auswahl. Standardmäßig `Custom Opus model`, wenn nicht gesetzt |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Komma-getrennte Liste der Funktionen, die das fixierte Opus-Modell unterstützt                                                   |

Die gleichen `_NAME`-, `_DESCRIPTION`- und `_SUPPORTED_CAPABILITIES`-Suffixe sind für `ANTHROPIC_DEFAULT_SONNET_MODEL` und `ANTHROPIC_DEFAULT_HAIKU_MODEL` verfügbar.

Claude Code aktiviert Funktionen wie [Aufwandsniveaus](#adjust-effort-level) und [erweitertes Denken](/de/common-workflows#use-extended-thinking-thinking-mode) durch Abgleich der Modell-ID mit bekannten Mustern. Anbieterspezifische IDs wie Bedrock-ARNs oder benutzerdefinierte Bereitstellungsnamen stimmen oft nicht mit diesen Mustern überein, wodurch unterstützte Funktionen deaktiviert bleiben. Setzen Sie `_SUPPORTED_CAPABILITIES`, um Claude Code mitzuteilen, welche Funktionen das Modell tatsächlich unterstützt:

| Funktionswert          | Aktiviert                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| `effort`               | [Aufwandsniveaus](#adjust-effort-level) und der `/effort`-Befehl                             |
| `max_effort`           | Das `max`-Aufwandsniveau                                                                     |
| `thinking`             | [Erweitertes Denken](/de/common-workflows#use-extended-thinking-thinking-mode)               |
| `adaptive_thinking`    | Adaptives Reasoning, das das Denken dynamisch basierend auf der Aufgabenkomplexität zuordnet |
| `interleaved_thinking` | Denken zwischen Tool-Aufrufen                                                                |

Wenn `_SUPPORTED_CAPABILITIES` gesetzt ist, werden aufgelistete Funktionen aktiviert und nicht aufgelistete Funktionen werden für das entsprechende fixierte Modell deaktiviert. Wenn die Variable nicht gesetzt ist, greift Claude Code auf die integrierte Erkennung basierend auf der Modell-ID zurück.

Dieses Beispiel fixiert Opus auf ein benutzerdefiniertes Bedrock-Modell-ARN, setzt einen benutzerfreundlichen Namen und deklariert seine Funktionen:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.6 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Prompt-Caching-Konfiguration

Claude Code verwendet automatisch [Prompt-Caching](https://platform.claude.com/docs/de/build-with-claude/prompt-caching), um die Leistung zu optimieren und Kosten zu senken. Sie können Prompt-Caching global oder für bestimmte Modell-Tiers deaktivieren:

| Umgebungsvariable               | Beschreibung                                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Setzen Sie auf `1`, um Prompt-Caching für alle Modelle zu deaktivieren (hat Vorrang vor modellspezifischen Einstellungen) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Setzen Sie auf `1`, um Prompt-Caching nur für Haiku-Modelle zu deaktivieren                                               |
| `DISABLE_PROMPT_CACHING_SONNET` | Setzen Sie auf `1`, um Prompt-Caching nur für Sonnet-Modelle zu deaktivieren                                              |
| `DISABLE_PROMPT_CACHING_OPUS`   | Setzen Sie auf `1`, um Prompt-Caching nur für Opus-Modelle zu deaktivieren                                                |

Diese Umgebungsvariablen geben Ihnen eine feinkörnige Kontrolle über das Prompt-Caching-Verhalten. Die globale `DISABLE_PROMPT_CACHING`-Einstellung hat Vorrang vor den modellspezifischen Einstellungen, sodass Sie alle Caching schnell deaktivieren können, wenn nötig. Die modellspezifischen Einstellungen sind nützlich für selektive Kontrolle, z. B. beim Debuggen bestimmter Modelle oder bei der Arbeit mit Cloud-Anbietern, die möglicherweise unterschiedliche Caching-Implementierungen haben.
