> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude mit Skills erweitern

> Erstellen, verwalten und teilen Sie Skills, um Claudes Funktionen in Claude Code zu erweitern. Umfasst benutzerdefinierte Befehle und gebündelte Skills.

Skills erweitern das, was Claude tun kann. Erstellen Sie eine `SKILL.md`-Datei mit Anweisungen, und Claude fügt sie zu seinem Toolkit hinzu. Claude verwendet Skills, wenn sie relevant sind, oder Sie können einen direkt mit `/skill-name` aufrufen.

Erstellen Sie einen Skill, wenn Sie immer wieder das gleiche Playbook, die gleiche Checkliste oder ein mehrstufiges Verfahren in den Chat einfügen, oder wenn ein Abschnitt von CLAUDE.md zu einem Verfahren statt zu einer Tatsache geworden ist. Im Gegensatz zu CLAUDE.md-Inhalten wird der Body eines Skills nur geladen, wenn er verwendet wird, sodass lange Referenzmaterialien fast nichts kosten, bis Sie sie benötigen.

<Note>
  Für integrierte Befehle wie `/help` und `/compact` sowie gebündelte Skills wie `/debug` und `/simplify` siehe die [Befehlsreferenz](/de/commands).

  **Benutzerdefinierte Befehle wurden in Skills zusammengeführt.** Eine Datei unter `.claude/commands/deploy.md` und ein Skill unter `.claude/skills/deploy/SKILL.md` erstellen beide `/deploy` und funktionieren auf die gleiche Weise. Ihre vorhandenen `.claude/commands/`-Dateien funktionieren weiterhin. Skills fügen optionale Funktionen hinzu: ein Verzeichnis für unterstützende Dateien, Frontmatter zum [Steuern, wer einen Skill aufruft](#control-who-invokes-a-skill), und die Möglichkeit für Claude, sie automatisch zu laden, wenn sie relevant sind.
</Note>

Claude Code Skills folgen dem [Agent Skills](https://agentskills.io) offenen Standard, der über mehrere KI-Tools funktioniert. Claude Code erweitert den Standard mit zusätzlichen Funktionen wie [Invocation Control](#control-who-invokes-a-skill), [Subagent-Ausführung](#run-skills-in-a-subagent) und [dynamischer Kontexteinspritzung](#inject-dynamic-context).

## Gebündelte Skills

Claude Code wird mit einer Reihe von gebündelten Skills ausgeliefert, die in jeder Sitzung verfügbar sind, einschließlich `/simplify`, `/batch`, `/debug`, `/loop` und `/claude-api`. Im Gegensatz zu den meisten integrierten Befehlen, die direkt feste Logik ausführen, sind gebündelte Skills prompt-basiert: Sie geben Claude ein detailliertes Playbook und lassen es die Arbeit mit seinen Tools orchestrieren. Sie rufen sie auf die gleiche Weise auf wie jeden anderen Skill, indem Sie `/` gefolgt vom Skill-Namen eingeben.

Gebündelte Skills sind in der [Befehlsreferenz](/de/commands) neben integrierten Befehlen aufgelistet und mit **Skill** in der Spalte „Zweck" gekennzeichnet.

## Erste Schritte

### Erstellen Sie Ihren ersten Skill

Dieses Beispiel erstellt einen Skill, der Claude beibringt, Code mit visuellen Diagrammen und Analogien zu erklären. Da er Standard-Frontmatter verwendet, kann Claude ihn automatisch laden, wenn Sie fragen, wie etwas funktioniert, oder Sie können ihn direkt mit `/explain-code` aufrufen.

<Steps>
  <Step title="Erstellen Sie das Skill-Verzeichnis">
    Erstellen Sie ein Verzeichnis für den Skill in Ihrem persönlichen Skills-Ordner. Persönliche Skills sind über alle Ihre Projekte hinweg verfügbar.

    ```bash theme={null}
    mkdir -p ~/.claude/skills/explain-code
    ```
  </Step>

  <Step title="Schreiben Sie SKILL.md">
    Jeder Skill benötigt eine `SKILL.md`-Datei mit zwei Teilen: YAML-Frontmatter (zwischen `---`-Markierungen), das Claude mitteilt, wann der Skill verwendet werden soll, und Markdown-Inhalt mit Anweisungen, die Claude befolgt, wenn der Skill aufgerufen wird. Das Verzeichnisname wird zum `/slash-command`, und die `description` hilft Claude zu entscheiden, wann der Skill automatisch geladen werden soll.

    Erstellen Sie `~/.claude/skills/explain-code/SKILL.md`:

    ```yaml theme={null}
    ---
    description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
    ---

    When explaining code, always include:

    1. **Start with an analogy**: Compare the code to something from everyday life
    2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
    3. **Walk through the code**: Explain step-by-step what happens
    4. **Highlight a gotcha**: What's a common mistake or misconception?

    Keep explanations conversational. For complex concepts, use multiple analogies.
    ```
  </Step>

  <Step title="Testen Sie den Skill">
    Sie können ihn auf zwei Arten testen:

    **Lassen Sie Claude ihn automatisch aufrufen**, indem Sie etwas eingeben, das der Beschreibung entspricht:

    ```text theme={null}
    How does this code work?
    ```

    **Oder rufen Sie ihn direkt auf** mit dem Skill-Namen:

    ```text theme={null}
    /explain-code src/auth/login.ts
    ```

    In beiden Fällen sollte Claude eine Analogie und ein ASCII-Diagramm in seiner Erklärung enthalten.
  </Step>
</Steps>

### Wo Skills leben

Wo Sie einen Skill speichern, bestimmt, wer ihn verwenden kann:

| Ort         | Pfad                                                          | Gilt für                            |
| :---------- | :------------------------------------------------------------ | :---------------------------------- |
| Unternehmen | Siehe [verwaltete Einstellungen](/de/settings#settings-files) | Alle Benutzer in Ihrer Organisation |
| Persönlich  | `~/.claude/skills/<skill-name>/SKILL.md`                      | Alle Ihre Projekte                  |
| Projekt     | `.claude/skills/<skill-name>/SKILL.md`                        | Nur dieses Projekt                  |
| Plugin      | `<plugin>/skills/<skill-name>/SKILL.md`                       | Wo das Plugin aktiviert ist         |

Wenn Skills auf verschiedenen Ebenen denselben Namen haben, gewinnt Unternehmen gegenüber Persönlich, und Persönlich gewinnt gegenüber Projekt. Plugin-Skills verwenden einen `plugin-name:skill-name`-Namespace, sodass sie nicht mit anderen Ebenen in Konflikt geraten können. Wenn Sie Dateien in `.claude/commands/` haben, funktionieren diese auf die gleiche Weise, aber wenn ein Skill und ein Befehl denselben Namen haben, hat der Skill Vorrang.

#### Live-Änderungserkennung

Claude Code überwacht Skill-Verzeichnisse auf Dateiänderungen. Das Hinzufügen, Bearbeiten oder Entfernen eines Skills unter `~/.claude/skills/`, dem Projekt `.claude/skills/` oder einem `.claude/skills/` in einem `--add-dir`-Verzeichnis wird in der aktuellen Sitzung wirksam, ohne Claude Code neu zu starten. Das Erstellen eines Skill-Verzeichnisses auf oberster Ebene, das nicht vorhanden war, als die Sitzung gestartet wurde, erfordert einen Neustart von Claude Code, damit das neue Verzeichnis überwacht werden kann.

#### Automatische Erkennung aus verschachtelten Verzeichnissen

Wenn Sie mit Dateien in Unterverzeichnissen arbeiten, erkennt Claude Code automatisch Skills aus verschachtelten `.claude/skills/`-Verzeichnissen. Wenn Sie beispielsweise eine Datei in `packages/frontend/` bearbeiten, sucht Claude Code auch nach Skills in `packages/frontend/.claude/skills/`. Dies unterstützt Monorepo-Setups, bei denen Pakete ihre eigenen Skills haben.

Jeder Skill ist ein Verzeichnis mit `SKILL.md` als Einstiegspunkt:

```text theme={null}
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

Die `SKILL.md` enthält die Hauptanweisungen und ist erforderlich. Andere Dateien sind optional und ermöglichen es Ihnen, leistungsfähigere Skills zu erstellen: Vorlagen für Claude zum Ausfüllen, Beispielausgaben, die das erwartete Format zeigen, Scripts, die Claude ausführen kann, oder detaillierte Referenzdokumentation. Verweisen Sie auf diese Dateien von Ihrer `SKILL.md` aus, damit Claude weiß, was sie enthalten und wann sie geladen werden sollen. Siehe [Unterstützende Dateien hinzufügen](#add-supporting-files) für weitere Details.

<Note>
  Dateien in `.claude/commands/` funktionieren weiterhin und unterstützen das gleiche [Frontmatter](#frontmatter-reference). Skills werden empfohlen, da sie zusätzliche Funktionen wie unterstützende Dateien unterstützen.
</Note>

#### Skills aus zusätzlichen Verzeichnissen

Das Flag `--add-dir` [gewährt Dateizugriff](/de/permissions#additional-directories-grant-file-access-not-configuration) statt Konfigurationserkennung, aber Skills sind eine Ausnahme: `.claude/skills/` in einem hinzugefügten Verzeichnis wird automatisch geladen. Siehe [Live-Änderungserkennung](#live-change-detection) für die Aufnahme von Änderungen während einer Sitzung.

Andere `.claude/`-Konfigurationen wie Subagenten, Befehle und Ausgabestile werden nicht aus zusätzlichen Verzeichnissen geladen. Siehe die [Ausnahmetabelle](/de/permissions#additional-directories-grant-file-access-not-configuration) für die vollständige Liste dessen, was geladen wird und was nicht, sowie die empfohlenen Wege zum Teilen von Konfigurationen über Projekte hinweg.

<Note>
  CLAUDE.md-Dateien aus `--add-dir`-Verzeichnissen werden standardmäßig nicht geladen. Um sie zu laden, setzen Sie `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. Siehe [Aus zusätzlichen Verzeichnissen laden](/de/memory#load-from-additional-directories).
</Note>

## Skills konfigurieren

Skills werden durch YAML-Frontmatter oben in `SKILL.md` und den Markdown-Inhalt, der folgt, konfiguriert.

### Arten von Skill-Inhalten

Skill-Dateien können beliebige Anweisungen enthalten, aber das Nachdenken darüber, wie Sie sie aufrufen möchten, hilft zu leiten, was Sie einbeziehen:

**Referenzinhalt** fügt Wissen hinzu, das Claude auf Ihre aktuelle Arbeit anwendet. Konventionen, Muster, Stilhandbücher, Domänenwissen. Dieser Inhalt wird inline ausgeführt, sodass Claude ihn neben Ihrem Gesprächskontext verwenden kann.

```yaml theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Task-Inhalt** gibt Claude Schritt-für-Schritt-Anweisungen für eine bestimmte Aktion, wie Bereitstellungen, Commits oder Code-Generierung. Dies sind oft Aktionen, die Sie direkt mit `/skill-name` aufrufen möchten, anstatt Claude entscheiden zu lassen, wann sie ausgeführt werden. Fügen Sie `disable-model-invocation: true` hinzu, um zu verhindern, dass Claude sie automatisch auslöst.

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

Ihre `SKILL.md` kann alles enthalten, aber das Nachdenken darüber, wie Sie den Skill aufrufen möchten (von Ihnen, von Claude oder von beiden) und wo Sie ihn ausführen möchten (inline oder in einem Subagent) hilft zu leiten, was Sie einbeziehen. Für komplexe Skills können Sie auch [unterstützende Dateien hinzufügen](#add-supporting-files), um den Hauptskill fokussiert zu halten.

### Frontmatter-Referenz

Über den Markdown-Inhalt hinaus können Sie das Skill-Verhalten mit YAML-Frontmatter-Feldern zwischen `---`-Markierungen oben in Ihrer `SKILL.md`-Datei konfigurieren:

```yaml theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

Alle Felder sind optional. Nur `description` wird empfohlen, damit Claude weiß, wann der Skill verwendet werden soll.

| Feld                       | Erforderlich | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                |
| :------------------------- | :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | Nein         | Anzeigename für den Skill. Falls weggelassen, wird der Verzeichnisname verwendet. Nur Kleinbuchstaben, Zahlen und Bindestriche (max. 64 Zeichen).                                                                                                                                                                                                                                                           |
| `description`              | Empfohlen    | Was der Skill tut und wann er verwendet werden soll. Claude verwendet dies, um zu entscheiden, wann der Skill angewendet werden soll. Falls weggelassen, wird der erste Absatz des Markdown-Inhalts verwendet. Front-load den wichtigsten Anwendungsfall: Der kombinierte Text `description` und `when_to_use` wird in der Skill-Auflistung bei 1.536 Zeichen gekürzt, um die Kontextnutzung zu reduzieren. |
| `when_to_use`              | Nein         | Zusätzlicher Kontext für den Zeitpunkt, zu dem Claude den Skill aufrufen sollte, z. B. Trigger-Phrasen oder Beispielanfragen. An `description` in der Skill-Auflistung angehängt und zählt zur 1.536-Zeichen-Obergrenze.                                                                                                                                                                                    |
| `argument-hint`            | Nein         | Hinweis, der während der Autovervollständigung angezeigt wird, um erwartete Argumente anzuzeigen. Beispiel: `[issue-number]` oder `[filename] [format]`.                                                                                                                                                                                                                                                    |
| `arguments`                | Nein         | Benannte positionelle Argumente für [`$name`-Substitution](#available-string-substitutions) im Skill-Inhalt. Akzeptiert eine durch Leerzeichen getrennte Zeichenkette oder eine YAML-Liste. Namen werden in Reihenfolge auf Argumentpositionen abgebildet.                                                                                                                                                  |
| `disable-model-invocation` | Nein         | Setzen Sie auf `true`, um zu verhindern, dass Claude diesen Skill automatisch lädt. Verwenden Sie für Workflows, die Sie manuell mit `/name` auslösen möchten. Verhindert auch, dass der Skill [in Subagenten vorgeladen wird](/de/sub-agents#preload-skills-into-subagents). Standard: `false`.                                                                                                            |
| `user-invocable`           | Nein         | Setzen Sie auf `false`, um aus dem `/`-Menü auszublenden. Verwenden Sie für Hintergrundwissen, das Benutzer nicht direkt aufrufen sollten. Standard: `true`.                                                                                                                                                                                                                                                |
| `allowed-tools`            | Nein         | Tools, die Claude ohne Genehmigung verwenden kann, wenn dieser Skill aktiv ist. Akzeptiert eine durch Leerzeichen getrennte Zeichenkette oder eine YAML-Liste.                                                                                                                                                                                                                                              |
| `model`                    | Nein         | Modell, das verwendet werden soll, wenn dieser Skill aktiv ist. Die Überschreibung gilt für den Rest des aktuellen Zuges und wird nicht in den Einstellungen gespeichert; das Sitzungsmodell wird bei Ihrer nächsten Eingabe fortgesetzt. Akzeptiert die gleichen Werte wie [`/model`](/de/model-config) oder `inherit`, um das aktive Modell beizubehalten.                                                |
| `effort`                   | Nein         | [Anstrengungsstufe](/de/model-config#adjust-effort-level) wenn dieser Skill aktiv ist. Überschreibt die Anstrengungsstufe der Sitzung. Standard: erbt von Sitzung. Optionen: `low`, `medium`, `high`, `xhigh`, `max`; verfügbare Stufen hängen vom Modell ab.                                                                                                                                               |
| `context`                  | Nein         | Setzen Sie auf `fork`, um in einem verzweigten Subagent-Kontext ausgeführt zu werden.                                                                                                                                                                                                                                                                                                                       |
| `agent`                    | Nein         | Welcher Subagent-Typ verwendet werden soll, wenn `context: fork` gesetzt ist.                                                                                                                                                                                                                                                                                                                               |
| `hooks`                    | Nein         | Hooks, die auf den Lebenszyklus dieses Skills beschränkt sind. Siehe [Hooks in Skills und Agenten](/de/hooks#hooks-in-skills-and-agents) für das Konfigurationsformat.                                                                                                                                                                                                                                      |
| `paths`                    | Nein         | Glob-Muster, die begrenzen, wann dieser Skill aktiviert wird. Akzeptiert eine kommagetrennte Zeichenkette oder eine YAML-Liste. Wenn gesetzt, lädt Claude den Skill automatisch nur, wenn mit Dateien arbeitet, die den Mustern entsprechen. Verwendet das gleiche Format wie [pfadspezifische Regeln](/de/memory#path-specific-rules).                                                                     |
| `shell`                    | Nein         | Shell, die für `` !`command` `` und ` ```! ` Blöcke in diesem Skill verwendet werden soll. Akzeptiert `bash` (Standard) oder `powershell`. Das Setzen von `powershell` führt Inline-Shell-Befehle über PowerShell unter Windows aus. Erfordert `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.                                                                                                                         |

#### Verfügbare String-Substitutionen

Skills unterstützen String-Substitution für dynamische Werte im Skill-Inhalt:

| Variable               | Beschreibung                                                                                                                                                                                                                                                                                                                  |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | Alle Argumente, die beim Aufrufen des Skills übergeben werden. Wenn `$ARGUMENTS` nicht im Inhalt vorhanden ist, werden Argumente als `ARGUMENTS: <value>` angehängt.                                                                                                                                                          |
| `$ARGUMENTS[N]`        | Greifen Sie auf ein bestimmtes Argument nach 0-basiertem Index zu, z. B. `$ARGUMENTS[0]` für das erste Argument.                                                                                                                                                                                                              |
| `$N`                   | Kurzform für `$ARGUMENTS[N]`, z. B. `$0` für das erste Argument oder `$1` für das zweite.                                                                                                                                                                                                                                     |
| `$name`                | Benanntes Argument, das in der [`arguments`](#frontmatter-reference)-Frontmatter-Liste deklariert ist. Namen werden in Reihenfolge auf Positionen abgebildet, daher wird mit `arguments: [issue, branch]` der Platzhalter `$issue` zum ersten Argument erweitert und `$branch` zum zweiten.                                   |
| `${CLAUDE_SESSION_ID}` | Die aktuelle Sitzungs-ID. Nützlich zum Protokollieren, Erstellen sitzungsspezifischer Dateien oder Korrelieren der Skill-Ausgabe mit Sitzungen.                                                                                                                                                                               |
| `${CLAUDE_EFFORT}`     | Die aktuelle Anstrengungsstufe: `low`, `medium`, `high`, `xhigh` oder `max`. Verwenden Sie dies, um Skill-Anweisungen an die aktive Anstrengungseinstellung anzupassen.                                                                                                                                                       |
| `${CLAUDE_SKILL_DIR}`  | Das Verzeichnis, das die `SKILL.md`-Datei des Skills enthält. Für Plugin-Skills ist dies das Skill-Unterverzeichnis im Plugin, nicht das Plugin-Root. Verwenden Sie dies in Bash-Injektionsbefehlen, um auf Scripts oder Dateien zu verweisen, die mit dem Skill gebündelt sind, unabhängig vom aktuellen Arbeitsverzeichnis. |

Indizierte Argumente verwenden Shell-ähnliche Anführungszeichen, daher müssen Sie mehrteilige Werte in Anführungszeichen setzen, um sie als einzelnes Argument zu übergeben. Zum Beispiel macht `/my-skill "hello world" second` `$0` zu `hello world` und `$1` zu `second`. Der `$ARGUMENTS`-Platzhalter wird immer zur vollständigen Argumentzeichenkette erweitert, wie eingegeben.

**Beispiel mit Substitutionen:**

```yaml theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Unterstützende Dateien hinzufügen

Skills können mehrere Dateien in ihrem Verzeichnis enthalten. Dies hält `SKILL.md` auf das Wesentliche konzentriert, während Claude detailliertes Referenzmaterial nur bei Bedarf abrufen kann. Große Referenzdokumente, API-Spezifikationen oder Beispielsammlungen müssen nicht jedes Mal geladen werden, wenn der Skill ausgeführt wird.

```text theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

Verweisen Sie auf unterstützende Dateien von `SKILL.md` aus, damit Claude weiß, was jede Datei enthält und wann sie geladen werden soll:

```markdown theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>Halten Sie `SKILL.md` unter 500 Zeilen. Verschieben Sie detailliertes Referenzmaterial in separate Dateien.</Tip>

### Steuern Sie, wer einen Skill aufruft

Standardmäßig können sowohl Sie als auch Claude jeden Skill aufrufen. Sie können `/skill-name` eingeben, um ihn direkt aufzurufen, und Claude kann ihn automatisch laden, wenn er für Ihr Gespräch relevant ist. Zwei Frontmatter-Felder ermöglichen es Ihnen, dies einzuschränken:

* **`disable-model-invocation: true`**: Nur Sie können den Skill aufrufen. Verwenden Sie dies für Workflows mit Nebenwirkungen oder die Sie zeitlich steuern möchten, wie `/commit`, `/deploy` oder `/send-slack-message`. Sie möchten nicht, dass Claude bereitstellt, weil Ihr Code bereit aussieht.

* **`user-invocable: false`**: Nur Claude kann den Skill aufrufen. Verwenden Sie dies für Hintergrundwissen, das nicht als Befehl umsetzbar ist. Ein `legacy-system-context`-Skill erklärt, wie ein altes System funktioniert. Claude sollte dies kennen, wenn es relevant ist, aber `/legacy-system-context` ist keine aussagekräftige Aktion für Benutzer.

Dieses Beispiel erstellt einen Deploy-Skill, den nur Sie auslösen können. Das `disable-model-invocation: true`-Feld verhindert, dass Claude ihn automatisch ausführt:

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

Hier ist, wie die beiden Felder Aufrufe und Kontextladung beeinflussen:

| Frontmatter                      | Sie können aufrufen | Claude kann aufrufen | Wann in Kontext geladen                                                            |
| :------------------------------- | :------------------ | :------------------- | :--------------------------------------------------------------------------------- |
| (Standard)                       | Ja                  | Ja                   | Beschreibung immer im Kontext, vollständiger Skill wird beim Aufrufen geladen      |
| `disable-model-invocation: true` | Ja                  | Nein                 | Beschreibung nicht im Kontext, vollständiger Skill wird geladen, wenn Sie aufrufen |
| `user-invocable: false`          | Nein                | Ja                   | Beschreibung immer im Kontext, vollständiger Skill wird beim Aufrufen geladen      |

<Note>
  In einer regulären Sitzung werden Skill-Beschreibungen in den Kontext geladen, damit Claude weiß, was verfügbar ist, aber vollständiger Skill-Inhalt wird nur beim Aufrufen geladen. [Subagenten mit vorgeladenen Skills](/de/sub-agents#preload-skills-into-subagents) funktionieren anders: Der vollständige Skill-Inhalt wird beim Start eingespritzt.
</Note>

### Skill-Inhalts-Lebenszyklus

Wenn Sie oder Claude einen Skill aufrufen, wird der gerenderte `SKILL.md`-Inhalt als einzelne Nachricht in das Gespräch eingegeben und bleibt dort für den Rest der Sitzung. Claude Code liest die Skill-Datei bei späteren Zügen nicht erneut, daher schreiben Sie Anleitung, die während einer Aufgabe gelten sollte, als stehende Anweisungen statt als einmalige Schritte.

[Auto-Komprimierung](/de/how-claude-code-works#when-context-fills-up) trägt aufgerufene Skills innerhalb eines Token-Budgets weiter. Wenn das Gespräch zusammengefasst wird, um Kontext freizugeben, hängt Claude Code die neueste Aufrufe jedes Skills nach der Zusammenfassung wieder an und behält die ersten 5.000 Token jedes Skills. Wieder angehängte Skills teilen sich ein kombiniertes Budget von 25.000 Token. Claude Code füllt dieses Budget ab dem zuletzt aufgerufenen Skill, sodass ältere Skills vollständig gelöscht werden können, wenn Sie viele in einer Sitzung aufgerufen haben.

Wenn ein Skill das Verhalten nach der ersten Antwort nicht mehr zu beeinflussen scheint, ist der Inhalt normalerweise immer noch vorhanden und das Modell wählt andere Tools oder Ansätze. Stärken Sie die `description` und Anweisungen des Skills, damit das Modell es weiterhin bevorzugt, oder verwenden Sie [Hooks](/de/hooks), um Verhalten deterministisch zu erzwingen. Wenn der Skill groß ist oder Sie mehrere andere danach aufgerufen haben, rufen Sie ihn nach der Komprimierung erneut auf, um den vollständigen Inhalt wiederherzustellen.

### Tools für einen Skill vorab genehmigen

Das `allowed-tools`-Feld gewährt Berechtigung für die aufgelisteten Tools, während der Skill aktiv ist, sodass Claude sie verwenden kann, ohne Sie um Genehmigung zu bitten. Es schränkt nicht ein, welche Tools verfügbar sind: Jedes Tool bleibt aufrufbar, und Ihre [Berechtigungseinstellungen](/de/permissions) regeln weiterhin Tools, die nicht aufgelistet sind.

Dieser Skill lässt Claude Git-Befehle ohne Genehmigung pro Verwendung ausführen, wenn Sie ihn aufrufen:

```yaml theme={null}
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

Um einen Skill daran zu hindern, bestimmte Tools zu verwenden, fügen Sie stattdessen Ablehnungsregeln in Ihren [Berechtigungseinstellungen](/de/permissions) hinzu.

### Argumente an Skills übergeben

Sowohl Sie als auch Claude können Argumente beim Aufrufen eines Skills übergeben. Argumente sind über den `$ARGUMENTS`-Platzhalter verfügbar.

Dieser Skill behebt ein GitHub-Problem nach Nummer. Der `$ARGUMENTS`-Platzhalter wird durch alles ersetzt, was dem Skill-Namen folgt:

```yaml theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

Wenn Sie `/fix-issue 123` ausführen, erhält Claude „Fix GitHub issue 123 following our coding standards..."

Wenn Sie einen Skill mit Argumenten aufrufen, aber der Skill `$ARGUMENTS` nicht enthält, hängt Claude Code `ARGUMENTS: <your input>` am Ende des Skill-Inhalts an, damit Claude immer noch sieht, was Sie eingegeben haben.

Um auf einzelne Argumente nach Position zuzugreifen, verwenden Sie `$ARGUMENTS[N]` oder die kürzere Form `$N`:

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

Wenn Sie `/migrate-component SearchBar React Vue` ausführen, wird `$ARGUMENTS[0]` durch `SearchBar`, `$ARGUMENTS[1]` durch `React` und `$ARGUMENTS[2]` durch `Vue` ersetzt. Der gleiche Skill mit der `$N`-Kurzform:

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## Fortgeschrittene Muster

### Dynamischen Kontext einspritzen

Die `` !`<command>` `` Syntax führt Shell-Befehle aus, bevor der Skill-Inhalt an Claude gesendet wird. Die Befehlsausgabe ersetzt den Platzhalter, sodass Claude tatsächliche Daten erhält, nicht den Befehl selbst.

Dieser Skill fasst einen Pull Request zusammen, indem er Live-PR-Daten mit der GitHub CLI abruft. Die `` !`gh pr diff` `` und andere Befehle werden zuerst ausgeführt, und ihre Ausgabe wird in den Prompt eingefügt:

```yaml theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

Wenn dieser Skill ausgeführt wird:

1. Jeder `` !`<command>` `` wird sofort ausgeführt (bevor Claude etwas sieht)
2. Die Ausgabe ersetzt den Platzhalter im Skill-Inhalt
3. Claude erhält den vollständig gerenderten Prompt mit tatsächlichen PR-Daten

Dies ist Vorverarbeitung, nicht etwas, das Claude ausführt. Claude sieht nur das Endergebnis.

Für mehrzeilige Befehle verwenden Sie einen Codeblock, der mit ` ```! ` statt der Inline-Form geöffnet wird:

````markdown theme={null}
## Environment
```!
node --version
npm --version
git status --short
```
````

Um dieses Verhalten für Skills und benutzerdefinierte Befehle aus Benutzer-, Projekt-, Plugin- oder [zusätzlichen Verzeichnis](#skills-from-additional-directories)-Quellen zu deaktivieren, setzen Sie `"disableSkillShellExecution": true` in [Einstellungen](/de/settings). Jeder Befehl wird stattdessen durch `[shell command execution disabled by policy]` ersetzt. Gebündelte und verwaltete Skills sind nicht betroffen. Diese Einstellung ist am nützlichsten in [verwalteten Einstellungen](/de/permissions#managed-settings), wo Benutzer sie nicht überschreiben können.

<Tip>
  Um [erweitertes Denken](/de/common-workflows#use-extended-thinking-thinking-mode) in einem Skill zu aktivieren, fügen Sie das Wort „ultrathink" irgendwo in Ihren Skill-Inhalt ein.
</Tip>

### Skills in einem Subagent ausführen

Fügen Sie `context: fork` zu Ihrem Frontmatter hinzu, wenn Sie möchten, dass ein Skill isoliert ausgeführt wird. Der Skill-Inhalt wird zum Prompt, der den Subagent antreibt. Er hat keinen Zugriff auf Ihren Gesprächsverlauf.

<Warning>
  `context: fork` macht nur Sinn für Skills mit expliziten Anweisungen. Wenn Ihr Skill Richtlinien wie „verwenden Sie diese API-Konventionen" ohne eine Aufgabe enthält, erhält der Subagent die Richtlinien, aber keinen umsetzbaren Prompt, und gibt ohne aussagekräftige Ausgabe zurück.
</Warning>

Skills und [Subagenten](/de/sub-agents) funktionieren in zwei Richtungen zusammen:

| Ansatz                     | System-Prompt                           | Aufgabe                      | Lädt auch                      |
| :------------------------- | :-------------------------------------- | :--------------------------- | :----------------------------- |
| Skill mit `context: fork`  | Vom Agent-Typ (`Explore`, `Plan`, etc.) | SKILL.md-Inhalt              | CLAUDE.md                      |
| Subagent mit `skills`-Feld | Subagent-Markdown-Body                  | Claudes Delegationsnachricht | Vorgeladene Skills + CLAUDE.md |

Mit `context: fork` schreiben Sie die Aufgabe in Ihren Skill und wählen einen Agent-Typ aus, um sie auszuführen. Für das Inverse (Definieren eines benutzerdefinierten Subagenten, der Skills als Referenzmaterial verwendet), siehe [Subagenten](/de/sub-agents#preload-skills-into-subagents).

#### Beispiel: Research-Skill mit Explore-Agent

Dieser Skill führt Recherchen in einem verzweigten Explore-Agent aus. Der Skill-Inhalt wird zur Aufgabe, und der Agent bietet schreibgeschützte Tools, die für die Codebase-Erkundung optimiert sind:

```yaml theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

Wenn dieser Skill ausgeführt wird:

1. Ein neuer isolierter Kontext wird erstellt
2. Der Subagent erhält den Skill-Inhalt als seinen Prompt („Research \$ARGUMENTS thoroughly...")
3. Das `agent`-Feld bestimmt die Ausführungsumgebung (Modell, Tools und Berechtigungen)
4. Ergebnisse werden zusammengefasst und an Ihr Hauptgespräch zurückgegeben

Das `agent`-Feld gibt an, welche Subagent-Konfiguration verwendet werden soll. Optionen umfassen integrierte Agenten (`Explore`, `Plan`, `general-purpose`) oder jeden benutzerdefinierten Subagenten aus `.claude/agents/`. Falls weggelassen, wird `general-purpose` verwendet.

### Beschränken Sie Claudes Skill-Zugriff

Standardmäßig kann Claude jeden Skill aufrufen, der nicht `disable-model-invocation: true` gesetzt hat. Skills, die `allowed-tools` definieren, gewähren Claude Zugriff auf diese Tools ohne Genehmigung pro Verwendung, wenn der Skill aktiv ist. Ihre [Berechtigungseinstellungen](/de/permissions) regeln weiterhin das Baseline-Genehmigungsverhalten für alle anderen Tools. Einige integrierte Befehle sind auch über das Skill-Tool verfügbar, einschließlich `/init`, `/review` und `/security-review`. Andere integrierte Befehle wie `/compact` sind nicht verfügbar.

Drei Möglichkeiten, um zu steuern, welche Skills Claude aufrufen kann:

**Deaktivieren Sie alle Skills**, indem Sie das Skill-Tool in `/permissions` ablehnen:

```text theme={null}
# Add to deny rules:
Skill
```

**Erlauben oder verweigern Sie bestimmte Skills** mit [Berechtigungsregeln](/de/permissions):

```text theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Berechtigungssyntax: `Skill(name)` für exakte Übereinstimmung, `Skill(name *)` für Präfixübereinstimmung mit beliebigen Argumenten.

**Verstecken Sie einzelne Skills**, indem Sie `disable-model-invocation: true` zu ihrem Frontmatter hinzufügen. Dies entfernt den Skill vollständig aus Claudes Kontext.

<Note>
  Das `user-invocable`-Feld steuert nur die Menüsichtbarkeit, nicht den Skill-Tool-Zugriff. Verwenden Sie `disable-model-invocation: true`, um die programmgesteuerte Aufrufe zu blockieren.
</Note>

## Skills teilen

Skills können je nach Ihrer Zielgruppe in verschiedenen Bereichen verteilt werden:

* **Projekt-Skills**: Committen Sie `.claude/skills/` zur Versionskontrolle
* **Plugins**: Erstellen Sie ein `skills/`-Verzeichnis in Ihrem [Plugin](/de/plugins)
* **Verwaltet**: Stellen Sie organisationsweit über [verwaltete Einstellungen](/de/settings#settings-files) bereit

### Visuelle Ausgabe generieren

Skills können Scripts in jeder Sprache bündeln und ausführen, was Claude Funktionen gibt, die über das hinausgehen, was in einem einzelnen Prompt möglich ist. Ein leistungsstarkes Muster ist die Generierung visueller Ausgabe: interaktive HTML-Dateien, die in Ihrem Browser geöffnet werden, um Daten zu erkunden, zu debuggen oder Berichte zu erstellen.

Dieses Beispiel erstellt einen Codebase-Explorer: eine interaktive Baumansicht, in der Sie Verzeichnisse erweitern und reduzieren, Dateigröße auf einen Blick sehen und Dateitypen nach Farbe identifizieren können.

Erstellen Sie das Skill-Verzeichnis:

```bash theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Erstellen Sie `~/.claude/skills/codebase-visualizer/SKILL.md`. Die Beschreibung teilt Claude mit, wann dieser Skill aktiviert werden soll, und die Anweisungen teilen Claude mit, das gebündelte Script auszuführen:

````yaml theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

Erstellen Sie `~/.claude/skills/codebase-visualizer/scripts/visualize.py`. Dieses Script scannt einen Verzeichnisbaum und generiert eine eigenständige HTML-Datei mit:

* Eine **Zusammenfassungs-Seitenleiste**, die Dateianzahl, Verzeichnisanzahl, Gesamtgröße und Anzahl der Dateitypen anzeigt
* Ein **Balkendiagramm**, das die Codebasis nach Dateityp aufschlüsselt (Top 8 nach Größe)
* Einen **zusammenklappbaren Baum**, in dem Sie Verzeichnisse erweitern und reduzieren können, mit farbcodierten Dateityp-Indikatoren

Das Script erfordert Python, verwendet aber nur integrierte Bibliotheken, daher müssen keine Pakete installiert werden:

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

Um zu testen, öffnen Sie Claude Code in einem beliebigen Projekt und fragen Sie „Visualize this codebase." Claude führt das Script aus, generiert `codebase-map.html` und öffnet es in Ihrem Browser.

Dieses Muster funktioniert für jede visuelle Ausgabe: Abhängigkeitsgraphen, Test-Coverage-Berichte, API-Dokumentation oder Datenbankschema-Visualisierungen. Das gebündelte Script erledigt die schwere Arbeit, während Claude die Orchestrierung übernimmt.

## Fehlerbehebung

### Skill wird nicht ausgelöst

Wenn Claude Ihren Skill nicht verwendet, wenn erwartet:

1. Überprüfen Sie, ob die Beschreibung Schlüsselwörter enthält, die Benutzer natürlicherweise sagen würden
2. Überprüfen Sie, ob der Skill in `What skills are available?` angezeigt wird
3. Versuchen Sie, Ihre Anfrage umzuformulieren, um die Beschreibung besser zu treffen
4. Rufen Sie ihn direkt mit `/skill-name` auf, wenn der Skill vom Benutzer aufgerufen werden kann

### Skill wird zu oft ausgelöst

Wenn Claude Ihren Skill verwendet, wenn Sie das nicht möchten:

1. Machen Sie die Beschreibung spezifischer
2. Fügen Sie `disable-model-invocation: true` hinzu, wenn Sie nur manuelle Aufrufe möchten

### Skill-Beschreibungen werden gekürzt

Skill-Beschreibungen werden in den Kontext geladen, damit Claude weiß, was verfügbar ist. Alle Skill-Namen sind immer enthalten, aber wenn Sie viele Skills haben, werden Beschreibungen gekürzt, um in das Zeichenbudget zu passen, was die Schlüsselwörter entfernen kann, die Claude benötigt, um Ihre Anfrage zu erfüllen. Das Budget skaliert dynamisch bei 1% des Kontextfensters, mit einem Fallback von 8.000 Zeichen.

Um das Limit zu erhöhen, setzen Sie die Umgebungsvariable `SLASH_COMMAND_TOOL_CHAR_BUDGET`. Oder kürzen Sie Beschreibungen an der Quelle: Front-load den wichtigsten Anwendungsfall, da jeder Eintrag unabhängig vom Budget auf 1.536 Zeichen begrenzt ist.

## Verwandte Ressourcen

* **[Debuggen Sie Ihre Konfiguration](/de/debug-your-config)**: Diagnostizieren Sie, warum ein Skill nicht angezeigt oder ausgelöst wird
* **[Subagenten](/de/sub-agents)**: Delegieren Sie Aufgaben an spezialisierte Agenten
* **[Plugins](/de/plugins)**: Packen und verteilen Sie Skills mit anderen Erweiterungen
* **[Hooks](/de/hooks)**: Automatisieren Sie Workflows um Tool-Ereignisse
* **[Memory](/de/memory)**: Verwalten Sie CLAUDE.md-Dateien für persistenten Kontext
* **[Befehle](/de/commands)**: Referenz für integrierte Befehle und gebündelte Skills
* **[Berechtigungen](/de/permissions)**: Steuern Sie Tool- und Skill-Zugriff
