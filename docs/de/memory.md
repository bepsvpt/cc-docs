> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wie Claude sich Ihr Projekt merkt

> Geben Sie Claude persistente Anweisungen mit CLAUDE.md-Dateien, und lassen Sie Claude automatisch Erkenntnisse mit Auto-Memory sammeln.

Jede Claude Code-Sitzung beginnt mit einem frischen Context Window. Zwei Mechanismen tragen Wissen über Sitzungen hinweg:

* **CLAUDE.md-Dateien**: Anweisungen, die Sie schreiben, um Claude persistenten Kontext zu geben
* **Auto-Memory**: Notizen, die Claude selbst basierend auf Ihren Korrektionen und Vorlieben schreibt

Diese Seite behandelt folgende Themen:

* [CLAUDE.md-Dateien schreiben und organisieren](#claude-md-files)
* [Regeln auf bestimmte Dateitypen beschränken](#organize-rules-with-claude/rules/) mit `.claude/rules/`
* [Auto-Memory konfigurieren](#auto-memory), damit Claude automatisch Notizen macht
* [Fehlerbehebung](#troubleshoot-memory-issues), wenn Anweisungen nicht befolgt werden

## CLAUDE.md vs. Auto-Memory

Claude Code hat zwei komplementäre Memory-Systeme. Beide werden zu Beginn jeder Konversation geladen. Claude behandelt sie als Kontext, nicht als erzwungene Konfiguration. Je spezifischer und prägnanter Ihre Anweisungen sind, desto konsistenter folgt Claude ihnen.

|                     | CLAUDE.md-Dateien                               | Auto-Memory                                                           |
| :------------------ | :---------------------------------------------- | :-------------------------------------------------------------------- |
| **Wer schreibt es** | Sie                                             | Claude                                                                |
| **Was es enthält**  | Anweisungen und Regeln                          | Erkenntnisse und Muster                                               |
| **Umfang**          | Projekt, Benutzer oder Organisation             | Pro Worktree                                                          |
| **Geladen in**      | Jede Sitzung                                    | Jede Sitzung (erste 200 Zeilen)                                       |
| **Verwenden für**   | Coding-Standards, Workflows, Projektarchitektur | Build-Befehle, Debugging-Erkenntnisse, Vorlieben, die Claude entdeckt |

Verwenden Sie CLAUDE.md-Dateien, wenn Sie Claudes Verhalten lenken möchten. Auto-Memory lässt Claude aus Ihren Korrektionen lernen, ohne manuelle Anstrengung.

Subagents können auch ihre eigene Auto-Memory pflegen. Weitere Informationen finden Sie unter [Subagent-Konfiguration](/de/sub-agents#enable-persistent-memory).

## CLAUDE.md-Dateien

CLAUDE.md-Dateien sind Markdown-Dateien, die Claude persistente Anweisungen für ein Projekt, Ihren persönlichen Workflow oder Ihre gesamte Organisation geben. Sie schreiben diese Dateien in Klartext; Claude liest sie zu Beginn jeder Sitzung.

### Wählen Sie, wo Sie CLAUDE.md-Dateien ablegen

CLAUDE.md-Dateien können sich an mehreren Orten befinden, jeder mit einem anderen Umfang. Spezifischere Orte haben Vorrang vor breiteren.

| Umfang                    | Ort                                                                                                                                                                     | Zweck                                                   | Anwendungsbeispiele                                                             | Geteilt mit                            |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------- |
| **Verwaltete Richtlinie** | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux und WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Organisationsweite Anweisungen, verwaltet von IT/DevOps | Unternehmens-Coding-Standards, Sicherheitsrichtlinien, Compliance-Anforderungen | Alle Benutzer in der Organisation      |
| **Projektanweisungen**    | `./CLAUDE.md` oder `./.claude/CLAUDE.md`                                                                                                                                | Team-gemeinsame Anweisungen für das Projekt             | Projektarchitektur, Coding-Standards, häufige Workflows                         | Team-Mitglieder über Versionskontrolle |
| **Benutzeranweisungen**   | `~/.claude/CLAUDE.md`                                                                                                                                                   | Persönliche Vorlieben für alle Projekte                 | Code-Styling-Vorlieben, persönliche Tooling-Shortcuts                           | Nur Sie (alle Projekte)                |

CLAUDE.md-Dateien in der Verzeichnishierarchie über dem Arbeitsverzeichnis werden beim Start vollständig geladen. CLAUDE.md-Dateien in Unterverzeichnissen werden bei Bedarf geladen, wenn Claude Dateien in diesen Verzeichnissen liest. Weitere Informationen finden Sie unter [Wie CLAUDE.md-Dateien geladen werden](#how-claude-md-files-load).

Für große Projekte können Sie Anweisungen in themaspezifische Dateien aufteilen, indem Sie [Projektregeln](#organize-rules-with-claude/rules/) verwenden. Regeln ermöglichen es Ihnen, Anweisungen auf bestimmte Dateitypen oder Unterverzeichnisse zu beschränken.

### Richten Sie eine Projekt-CLAUDE.md ein

Eine Projekt-CLAUDE.md kann entweder in `./CLAUDE.md` oder `./.claude/CLAUDE.md` gespeichert werden. Erstellen Sie diese Datei und fügen Sie Anweisungen hinzu, die für jeden gelten, der am Projekt arbeitet: Build- und Test-Befehle, Coding-Standards, architektonische Entscheidungen, Namenskonventionen und häufige Workflows. Diese Anweisungen werden über Versionskontrolle mit Ihrem Team geteilt, daher konzentrieren Sie sich auf projektweite Standards statt auf persönliche Vorlieben.

<Tip>
  Führen Sie `/init` aus, um automatisch eine Start-CLAUDE.md zu generieren. Claude analysiert Ihre Codebasis und erstellt eine Datei mit Build-Befehlen, Test-Anweisungen und Projektkonventionen, die es entdeckt. Wenn bereits eine CLAUDE.md vorhanden ist, schlägt `/init` Verbesserungen vor, statt sie zu überschreiben. Verfeinern Sie sie von dort aus mit Anweisungen, die Claude nicht selbst entdecken würde.

  Setzen Sie `CLAUDE_CODE_NEW_INIT=true`, um einen interaktiven mehrstufigen Ablauf zu aktivieren. `/init` fragt, welche Artefakte eingerichtet werden sollen: CLAUDE.md-Dateien, Skills und Hooks. Es erkundet dann Ihre Codebasis mit einem Subagent, füllt Lücken durch Folgefragen aus und präsentiert einen überprüfbaren Vorschlag, bevor Dateien geschrieben werden.
</Tip>

### Schreiben Sie effektive Anweisungen

CLAUDE.md-Dateien werden zu Beginn jeder Sitzung in das Context Window geladen und verbrauchen Token zusammen mit Ihrer Konversation. Da sie Kontext statt erzwungene Konfiguration sind, beeinflusst die Art, wie Sie Anweisungen schreiben, wie zuverlässig Claude ihnen folgt. Spezifische, prägnante, gut strukturierte Anweisungen funktionieren am besten.

**Größe**: Ziel unter 200 Zeilen pro CLAUDE.md-Datei. Längere Dateien verbrauchen mehr Kontext und reduzieren die Einhaltung. Wenn Ihre Anweisungen zu groß werden, teilen Sie sie mit [Importen](#import-additional-files) oder [`.claude/rules/`](#organize-rules-with-claude/rules/)-Dateien auf.

**Struktur**: Verwenden Sie Markdown-Header und Aufzählungszeichen, um verwandte Anweisungen zu gruppieren. Claude scannt die Struktur genauso wie Leser: organisierte Abschnitte sind leichter zu befolgen als dichte Absätze.

**Spezifität**: Schreiben Sie Anweisungen, die konkret genug sind, um überprüft zu werden. Zum Beispiel:

* „Verwenden Sie 2-Leerzeichen-Einrückung" statt „Formatieren Sie Code ordnungsgemäß"
* „Führen Sie `npm test` vor dem Commit aus" statt „Testen Sie Ihre Änderungen"
* „API-Handler befinden sich in `src/api/handlers/`" statt „Halten Sie Dateien organisiert"

**Konsistenz**: Wenn zwei Regeln sich widersprechen, kann Claude eine willkürlich auswählen. Überprüfen Sie Ihre CLAUDE.md-Dateien, verschachtelte CLAUDE.md-Dateien in Unterverzeichnissen und [`.claude/rules/`](#organize-rules-with-claude/rules/) regelmäßig, um veraltete oder widersprüchliche Anweisungen zu entfernen. In Monorepos verwenden Sie [`claudeMdExcludes`](#exclude-specific-claude-md-files), um CLAUDE.md-Dateien von anderen Teams zu überspringen, die für Ihre Arbeit nicht relevant sind.

### Importieren Sie zusätzliche Dateien

CLAUDE.md-Dateien können zusätzliche Dateien mit der Syntax `@path/to/import` importieren. Importierte Dateien werden erweitert und beim Start zusammen mit der CLAUDE.md, die sie referenziert, in den Kontext geladen.

Sowohl relative als auch absolute Pfade sind zulässig. Relative Pfade werden relativ zur Datei aufgelöst, die den Import enthält, nicht zum Arbeitsverzeichnis. Importierte Dateien können rekursiv andere Dateien importieren, mit einer maximalen Tiefe von fünf Hops.

Um eine README, package.json und einen Workflow-Leitfaden einzubeziehen, referenzieren Sie sie mit der `@`-Syntax überall in Ihrer CLAUDE.md:

```text  theme={null}
Siehe @README für Projektübersicht und @package.json für verfügbare npm-Befehle für dieses Projekt.

# Zusätzliche Anweisungen
- Git-Workflow @docs/git-instructions.md
```

Für persönliche Vorlieben, die Sie nicht einchecken möchten, importieren Sie eine Datei aus Ihrem Home-Verzeichnis. Der Import geht in die gemeinsame CLAUDE.md, aber die Datei, auf die er verweist, bleibt auf Ihrem Computer:

```text  theme={null}
# Individuelle Vorlieben
- @~/.claude/my-project-instructions.md
```

<Warning>
  Wenn Claude Code zum ersten Mal externe Importe in einem Projekt antrifft, zeigt es einen Genehmigungsdialog an, der die Dateien auflistet. Wenn Sie ablehnen, bleiben die Importe deaktiviert und der Dialog wird nicht erneut angezeigt.
</Warning>

Für einen strukturierteren Ansatz zur Organisation von Anweisungen siehe [`.claude/rules/`](#organize-rules-with-claude/rules/).

### AGENTS.md

Claude Code liest `CLAUDE.md`, nicht `AGENTS.md`. Wenn Ihr Repository bereits `AGENTS.md` für andere Coding-Agenten verwendet, erstellen Sie eine `CLAUDE.md`, die es importiert, damit beide Tools die gleichen Anweisungen lesen, ohne sie zu duplizieren. Sie können auch Claude-spezifische Anweisungen unter dem Import hinzufügen. Claude lädt die importierte Datei beim Sitzungsstart und hängt dann den Rest an:

```markdown CLAUDE.md theme={null}
@AGENTS.md

## Claude Code

Verwenden Sie Plan Mode für Änderungen unter `src/billing/`.
```

### Wie CLAUDE.md-Dateien geladen werden

Claude Code liest CLAUDE.md-Dateien, indem es die Verzeichnisstruktur von Ihrem aktuellen Arbeitsverzeichnis aus durchläuft und jedes Verzeichnis unterwegs überprüft. Das bedeutet, wenn Sie Claude Code in `foo/bar/` ausführen, lädt es Anweisungen aus `foo/bar/CLAUDE.md` und `foo/CLAUDE.md`.

Claude entdeckt auch CLAUDE.md-Dateien in Unterverzeichnissen unter Ihrem aktuellen Arbeitsverzeichnis. Statt sie beim Start zu laden, werden sie eingebunden, wenn Claude Dateien in diesen Unterverzeichnissen liest.

Wenn Sie in einem großen Monorepo arbeiten, in dem CLAUDE.md-Dateien anderer Teams aufgegriffen werden, verwenden Sie [`claudeMdExcludes`](#exclude-specific-claude-md-files), um sie zu überspringen.

Block-Level-HTML-Kommentare (`<!-- maintainer notes -->`) in CLAUDE.md-Dateien werden vor der Injektion in Claudes Kontext entfernt. Verwenden Sie sie, um Notizen für menschliche Betreuer zu hinterlassen, ohne Kontext-Token darauf zu verschwenden. Kommentare innerhalb von Code-Blöcken werden beibehalten. Wenn Sie eine CLAUDE.md-Datei direkt mit dem Read-Tool öffnen, bleiben Kommentare sichtbar.

#### Laden aus zusätzlichen Verzeichnissen

Das Flag `--add-dir` gibt Claude Zugriff auf zusätzliche Verzeichnisse außerhalb Ihres Hauptarbeitsverzeichnisses. Standardmäßig werden CLAUDE.md-Dateien aus diesen Verzeichnissen nicht geladen.

Um auch CLAUDE.md-Dateien aus zusätzlichen Verzeichnissen zu laden, einschließlich `CLAUDE.md`, `.claude/CLAUDE.md` und `.claude/rules/*.md`, setzen Sie die Umgebungsvariable `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash  theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Organisieren Sie Regeln mit `.claude/rules/`

Für größere Projekte können Sie Anweisungen in mehrere Dateien mit dem Verzeichnis `.claude/rules/` organisieren. Dies hält Anweisungen modular und leichter für Teams zu pflegen. Regeln können auch [auf bestimmte Dateipfade beschränkt werden](#path-specific-rules), sodass sie nur in den Kontext geladen werden, wenn Claude mit übereinstimmenden Dateien arbeitet, was Rauschen reduziert und Kontextraum spart.

<Note>
  Regeln werden in jeder Sitzung oder beim Öffnen übereinstimmender Dateien in den Kontext geladen. Für aufgabenspezifische Anweisungen, die nicht ständig im Kontext sein müssen, verwenden Sie stattdessen [Skills](/de/skills), die nur geladen werden, wenn Sie sie aufrufen oder wenn Claude bestimmt, dass sie für Ihren Prompt relevant sind.
</Note>

#### Richten Sie Regeln ein

Platzieren Sie Markdown-Dateien im Verzeichnis `.claude/rules/` Ihres Projekts. Jede Datei sollte ein Thema abdecken, mit einem beschreibenden Dateinamen wie `testing.md` oder `api-design.md`. Alle `.md`-Dateien werden rekursiv entdeckt, sodass Sie Regeln in Unterverzeichnisse wie `frontend/` oder `backend/` organisieren können:

```text  theme={null}
your-project/
├── .claude/
│   ├── CLAUDE.md           # Hauptprojektanweisungen
│   └── rules/
│       ├── code-style.md   # Code-Style-Richtlinien
│       ├── testing.md      # Test-Konventionen
│       └── security.md     # Sicherheitsanforderungen
```

Regeln ohne [`paths`-Frontmatter](#path-specific-rules) werden beim Start mit der gleichen Priorität wie `.claude/CLAUDE.md` geladen.

#### Pfadspezifische Regeln

Regeln können mit YAML-Frontmatter mit dem Feld `paths` auf bestimmte Dateien beschränkt werden. Diese bedingten Regeln gelten nur, wenn Claude mit Dateien arbeitet, die den angegebenen Mustern entsprechen.

```markdown  theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# API-Entwicklungsregeln

- Alle API-Endpunkte müssen Eingabevalidierung enthalten
- Verwenden Sie das Standard-Fehlerantwortformat
- Fügen Sie OpenAPI-Dokumentationskommentare ein
```

Regeln ohne ein `paths`-Feld werden bedingungslos geladen und gelten für alle Dateien. Pfadgebundene Regeln werden ausgelöst, wenn Claude Dateien liest, die dem Muster entsprechen, nicht bei jedem Tool-Einsatz.

Verwenden Sie Glob-Muster im Feld `paths`, um Dateien nach Erweiterung, Verzeichnis oder einer beliebigen Kombination zu vergleichen:

| Muster                 | Passt zu                                          |
| ---------------------- | ------------------------------------------------- |
| `**/*.ts`              | Alle TypeScript-Dateien in jedem Verzeichnis      |
| `src/**/*`             | Alle Dateien unter dem Verzeichnis `src/`         |
| `*.md`                 | Markdown-Dateien im Projektstamm                  |
| `src/components/*.tsx` | React-Komponenten in einem bestimmten Verzeichnis |

Sie können mehrere Muster angeben und Klammer-Expansion verwenden, um mehrere Erweiterungen in einem Muster zu vergleichen:

```markdown  theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Teilen Sie Regeln über Projekte hinweg mit Symlinks

Das Verzeichnis `.claude/rules/` unterstützt Symlinks, sodass Sie einen gemeinsamen Satz von Regeln pflegen und in mehrere Projekte verlinken können. Symlinks werden aufgelöst und normal geladen, und zirkuläre Symlinks werden erkannt und elegant behandelt.

Dieses Beispiel verlinkt sowohl ein gemeinsames Verzeichnis als auch eine einzelne Datei:

```bash  theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### Benutzerebenen-Regeln

Persönliche Regeln in `~/.claude/rules/` gelten für jedes Projekt auf Ihrem Computer. Verwenden Sie sie für Vorlieben, die nicht projektspezifisch sind:

```text  theme={null}
~/.claude/rules/
├── preferences.md    # Ihre persönlichen Coding-Vorlieben
└── workflows.md      # Ihre bevorzugten Workflows
```

Benutzerebenen-Regeln werden vor Projektregeln geladen, was Projektregeln höhere Priorität gibt.

### Verwalten Sie CLAUDE.md für große Teams

Für Organisationen, die Claude Code über Teams bereitstellen, können Sie Anweisungen zentralisieren und steuern, welche CLAUDE.md-Dateien geladen werden.

#### Stellen Sie organisationsweite CLAUDE.md bereit

Organisationen können eine zentral verwaltete CLAUDE.md bereitstellen, die für alle Benutzer auf einem Computer gilt. Diese Datei kann nicht durch individuelle Einstellungen ausgeschlossen werden.

<Steps>
  <Step title="Erstellen Sie die Datei am Ort der verwalteten Richtlinie">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux und WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Stellen Sie mit Ihrem Konfigurationsverwaltungssystem bereit">
    Verwenden Sie MDM, Group Policy, Ansible oder ähnliche Tools, um die Datei über Entwicklermaschinen zu verteilen. Weitere Informationen finden Sie unter [verwaltete Einstellungen](/de/permissions#managed-settings) für andere organisationsweite Konfigurationsoptionen.
  </Step>
</Steps>

Eine verwaltete CLAUDE.md und [verwaltete Einstellungen](/de/settings#settings-files) dienen unterschiedlichen Zwecken. Verwenden Sie Einstellungen für technische Durchsetzung und CLAUDE.md für Verhaltensanleitung:

| Anliegen                                                | Konfigurieren in                                                  |
| :------------------------------------------------------ | :---------------------------------------------------------------- |
| Blockieren Sie bestimmte Tools, Befehle oder Dateipfade | Verwaltete Einstellungen: `permissions.deny`                      |
| Erzwingen Sie Sandbox-Isolation                         | Verwaltete Einstellungen: `sandbox.enabled`                       |
| Umgebungsvariablen und API-Provider-Routing             | Verwaltete Einstellungen: `env`                                   |
| Authentifizierungsmethode und Organisationssperre       | Verwaltete Einstellungen: `forceLoginMethod`, `forceLoginOrgUUID` |
| Code-Style und Qualitätsrichtlinien                     | Verwaltete CLAUDE.md                                              |
| Datenbehandlung und Compliance-Erinnerungen             | Verwaltete CLAUDE.md                                              |
| Verhaltensanweisungen für Claude                        | Verwaltete CLAUDE.md                                              |

Einstellungsregeln werden vom Client unabhängig davon durchgesetzt, was Claude entscheidet zu tun. CLAUDE.md-Anweisungen prägen Claudes Verhalten, sind aber keine harte Durchsetzungsebene.

#### Schließen Sie bestimmte CLAUDE.md-Dateien aus

In großen Monorepos können Vorgänger-CLAUDE.md-Dateien Anweisungen enthalten, die für Ihre Arbeit nicht relevant sind. Die Einstellung `claudeMdExcludes` ermöglicht es Ihnen, bestimmte Dateien nach Pfad oder Glob-Muster zu überspringen.

Dieses Beispiel schließt eine CLAUDE.md auf oberster Ebene und ein Regelverzeichnis aus einem übergeordneten Ordner aus. Fügen Sie es zu `.claude/settings.local.json` hinzu, damit der Ausschluss lokal auf Ihrem Computer bleibt:

```json  theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Muster werden mit Glob-Syntax gegen absolute Dateipfade abgeglichen. Sie können `claudeMdExcludes` auf jeder [Einstellungsebene](/de/settings#settings-files) konfigurieren: Benutzer, Projekt, lokal oder verwaltete Richtlinie. Arrays werden über Ebenen hinweg zusammengeführt.

CLAUDE.md-Dateien mit verwalteter Richtlinie können nicht ausgeschlossen werden. Dies stellt sicher, dass organisationsweite Anweisungen unabhängig von individuellen Einstellungen immer gelten.

## Auto-Memory

Auto-Memory lässt Claude Wissen über Sitzungen hinweg sammeln, ohne dass Sie etwas schreiben müssen. Claude speichert Notizen für sich selbst, während es arbeitet: Build-Befehle, Debugging-Erkenntnisse, Architektur-Notizen, Code-Style-Vorlieben und Workflow-Gewohnheiten. Claude speichert nicht jede Sitzung etwas. Es entscheidet, was es sich merken sollte, basierend darauf, ob die Information in einer zukünftigen Konversation nützlich wäre.

<Note>
  Auto-Memory erfordert Claude Code v2.1.59 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

### Aktivieren oder deaktivieren Sie Auto-Memory

Auto-Memory ist standardmäßig aktiviert. Um es umzuschalten, öffnen Sie `/memory` in einer Sitzung und verwenden Sie den Auto-Memory-Schalter, oder setzen Sie `autoMemoryEnabled` in Ihren Projekteinstellungen:

```json  theme={null}
{
  "autoMemoryEnabled": false
}
```

Um Auto-Memory über eine Umgebungsvariable zu deaktivieren, setzen Sie `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Speicherort

Jedes Projekt erhält sein eigenes Memory-Verzeichnis unter `~/.claude/projects/<project>/memory/`. Der Pfad `<project>` wird aus dem Git-Repository abgeleitet, sodass alle Worktrees und Unterverzeichnisse innerhalb desselben Repos ein Auto-Memory-Verzeichnis teilen. Außerhalb eines Git-Repos wird stattdessen das Projektstammverzeichnis verwendet.

Um Auto-Memory an einem anderen Ort zu speichern, setzen Sie `autoMemoryDirectory` in Ihren Benutzer- oder lokalen Einstellungen:

```json  theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

Diese Einstellung wird von Richtlinien-, lokalen und Benutzereinstellungen akzeptiert. Sie wird nicht von Projekteinstellungen (`.claude/settings.json`) akzeptiert, um zu verhindern, dass ein gemeinsames Projekt Auto-Memory-Schreibvorgänge an sensible Orte umleitet.

Das Verzeichnis enthält einen `MEMORY.md`-Einstiegspunkt und optionale Themadateien:

```text  theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Prägnanter Index, geladen in jede Sitzung
├── debugging.md       # Detaillierte Notizen zu Debugging-Mustern
├── api-conventions.md # API-Design-Entscheidungen
└── ...                # Alle anderen Themadateien, die Claude erstellt
```

`MEMORY.md` fungiert als Index des Memory-Verzeichnisses. Claude liest und schreibt Dateien in diesem Verzeichnis während Ihrer Sitzung und verwendet `MEMORY.md`, um den Überblick zu behalten, was wo gespeichert ist.

Auto-Memory ist maschinenlokal. Alle Worktrees und Unterverzeichnisse innerhalb desselben Git-Repositories teilen ein Auto-Memory-Verzeichnis. Dateien werden nicht über Maschinen oder Cloud-Umgebungen hinweg geteilt.

### Wie es funktioniert

Die ersten 200 Zeilen von `MEMORY.md` werden zu Beginn jeder Konversation geladen. Inhalte über Zeile 200 werden nicht beim Sitzungsstart geladen. Claude hält `MEMORY.md` prägnant, indem es detaillierte Notizen in separate Themadateien verschiebt.

Diese 200-Zeilen-Grenze gilt nur für `MEMORY.md`. CLAUDE.md-Dateien werden unabhängig von der Länge vollständig geladen, obwohl kürzere Dateien bessere Einhaltung erzeugen.

Themadateien wie `debugging.md` oder `patterns.md` werden nicht beim Start geladen. Claude liest sie bei Bedarf mit seinen Standard-Datei-Tools, wenn es die Informationen benötigt.

Claude liest und schreibt Memory-Dateien während Ihrer Sitzung. Wenn Sie „Writing memory" oder „Recalled memory" in der Claude Code-Schnittstelle sehen, aktualisiert oder liest Claude aktiv aus `~/.claude/projects/<project>/memory/`.

### Überprüfen und bearbeiten Sie Ihr Memory

Auto-Memory-Dateien sind einfaches Markdown, das Sie jederzeit bearbeiten oder löschen können. Führen Sie [`/memory`](#view-and-edit-with-memory) aus, um Memory-Dateien innerhalb einer Sitzung zu durchsuchen und zu öffnen.

## Anzeigen und Bearbeiten mit `/memory`

Der Befehl `/memory` listet alle CLAUDE.md- und Regelsdateien auf, die in Ihrer aktuellen Sitzung geladen sind, ermöglicht es Ihnen, Auto-Memory ein- oder auszuschalten, und bietet einen Link zum Öffnen des Auto-Memory-Ordners. Wählen Sie eine beliebige Datei aus, um sie in Ihrem Editor zu öffnen.

Wenn Sie Claude bitten, sich etwas zu merken, wie „immer pnpm verwenden, nicht npm" oder „denken Sie daran, dass die API-Tests eine lokale Redis-Instanz erfordern", speichert Claude es in Auto-Memory. Um Anweisungen stattdessen zu CLAUDE.md hinzuzufügen, bitten Sie Claude direkt, wie „fügen Sie dies zu CLAUDE.md hinzu", oder bearbeiten Sie die Datei selbst über `/memory`.

## Fehlerbehebung bei Memory-Problemen

Dies sind die häufigsten Probleme mit CLAUDE.md und Auto-Memory, zusammen mit Schritten zum Debuggen.

### Claude folgt meiner CLAUDE.md nicht

CLAUDE.md-Inhalte werden als Benutzernachricht nach dem System-Prompt bereitgestellt, nicht als Teil des System-Prompts selbst. Claude liest ihn und versucht, ihm zu folgen, aber es gibt keine Garantie für strikte Einhaltung, besonders bei vagen oder widersprüchlichen Anweisungen.

Zum Debuggen:

* Führen Sie `/memory` aus, um zu überprüfen, dass Ihre CLAUDE.md-Dateien geladen werden. Wenn eine Datei nicht aufgelistet ist, kann Claude sie nicht sehen.
* Überprüfen Sie, dass die relevante CLAUDE.md an einem Ort ist, der für Ihre Sitzung geladen wird (siehe [Wählen Sie, wo Sie CLAUDE.md-Dateien ablegen](#choose-where-to-put-claude-md-files)).
* Machen Sie Anweisungen spezifischer. „Verwenden Sie 2-Leerzeichen-Einrückung" funktioniert besser als „formatieren Sie Code schön".
* Suchen Sie nach widersprüchlichen Anweisungen über CLAUDE.md-Dateien hinweg. Wenn zwei Dateien unterschiedliche Anleitungen für das gleiche Verhalten geben, kann Claude eine willkürlich auswählen.

Für Anweisungen, die Sie auf System-Prompt-Ebene haben möchten, verwenden Sie [`--append-system-prompt`](/de/cli-reference#system-prompt-flags). Dies muss bei jeder Invokation übergeben werden, daher ist es besser für Skripte und Automatisierung als für interaktive Nutzung geeignet.

<Tip>
  Verwenden Sie den [`InstructionsLoaded`-Hook](/de/hooks#instructionsloaded), um genau zu protokollieren, welche Anweisungsdateien geladen sind, wann sie geladen werden und warum. Dies ist nützlich zum Debuggen von pfadspezifischen Regeln oder Lazy-Loading-Dateien in Unterverzeichnissen.
</Tip>

### Ich weiß nicht, was Auto-Memory gespeichert hat

Führen Sie `/memory` aus und wählen Sie den Auto-Memory-Ordner aus, um zu durchsuchen, was Claude gespeichert hat. Alles ist einfaches Markdown, das Sie lesen, bearbeiten oder löschen können.

### Meine CLAUDE.md ist zu groß

Dateien über 200 Zeilen verbrauchen mehr Kontext und können die Einhaltung reduzieren. Verschieben Sie detaillierte Inhalte in separate Dateien, auf die mit `@path`-Importen verwiesen wird (siehe [Importieren Sie zusätzliche Dateien](#import-additional-files)), oder teilen Sie Ihre Anweisungen über `.claude/rules/`-Dateien auf.

### Anweisungen scheinen nach `/compact` verloren zu gehen

CLAUDE.md übersteht Komprimierung vollständig. Nach `/compact` liest Claude Ihre CLAUDE.md neu von der Festplatte und injiziert sie frisch in die Sitzung. Wenn eine Anweisung nach der Komprimierung verschwunden ist, wurde sie nur in der Konversation gegeben, nicht in CLAUDE.md geschrieben. Fügen Sie sie zu CLAUDE.md hinzu, um sie über Sitzungen hinweg zu erhalten.

Weitere Informationen finden Sie unter [Schreiben Sie effektive Anweisungen](#write-effective-instructions) für Anleitungen zu Größe, Struktur und Spezifität.

## Verwandte Ressourcen

* [Skills](/de/skills): Verpacken Sie wiederholbare Workflows, die bei Bedarf geladen werden
* [Einstellungen](/de/settings): Konfigurieren Sie Claude Code-Verhalten mit Einstellungsdateien
* [Verwalten Sie Sitzungen](/de/sessions): Verwalten Sie Kontext, setzen Sie Konversationen fort und führen Sie parallele Sitzungen aus
* [Subagent-Memory](/de/sub-agents#enable-persistent-memory): Lassen Sie Subagents ihre eigene Auto-Memory pflegen
