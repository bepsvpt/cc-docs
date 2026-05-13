> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ausgabestile

> Passen Sie Claude Code für Anwendungsfälle über Softwareentwicklung hinaus an

Ausgabestile ändern, wie Claude antwortet, nicht was Claude weiß. Sie ändern die Systemaufforderung, um Rolle, Ton und Ausgabeformat festzulegen, während die Kernfunktionen wie das Ausführen von Skripten, das Lesen und Schreiben von Dateien sowie das Nachverfolgen von TODOs erhalten bleiben. Verwenden Sie einen, wenn Sie sich in jedem Durchgang immer wieder nach derselben Stimme oder demselben Format erkundigen, oder wenn Sie möchten, dass Claude als etwas anderes als ein Softwareentwickler fungiert.

Für Anweisungen zu Ihrem Projekt, Konventionen oder Ihrer Codebasis verwenden Sie stattdessen [CLAUDE.md](/de/memory).

## Integrierte Ausgabestile

Der **Standard**-Ausgabestil von Claude Code ist die vorhandene Systemaufforderung, die Ihnen helfen soll, Softwareentwicklungsaufgaben effizient zu bewältigen.

Es gibt drei zusätzliche integrierte Ausgabestile:

* **Proaktiv**: Claude führt sofort aus, trifft vernünftige Annahmen statt bei Routineentscheidungen zu pausieren, und bevorzugt Handeln gegenüber Planung. Dies wendet die gleiche Anleitung wie [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode) an, ohne Ihren Berechtigungsmodus zu ändern, sodass Sie vor der Ausführung von Tools weiterhin Berechtigungsaufforderungen sehen.

* **Explanatory**: Bietet pädagogische „Insights" zwischen der Unterstützung bei Softwareentwicklungsaufgaben. Hilft Ihnen, Implementierungsentscheidungen und Codebase-Muster zu verstehen.

* **Learning**: Kollaborativer, Lern-durch-Tun-Modus, in dem Claude nicht nur „Insights" beim Codieren teilt, sondern Sie auch auffordert, kleine, strategische Codestücke selbst beizutragen. Claude Code fügt `TODO(human)`-Marker in Ihren Code ein, damit Sie diese implementieren können.

## Wie Ausgabestile funktionieren

Ausgabestile ändern direkt die Systemaufforderung von Claude Code.

* Benutzerdefinierte Ausgabestile schließen Anweisungen zum Codieren aus (z. B. Überprüfung von Code mit Tests), es sei denn, `keep-coding-instructions` ist true.
* Alle Ausgabestile haben ihre eigenen benutzerdefinierten Anweisungen am Ende der Systemaufforderung hinzugefügt.
* Alle Ausgabestile lösen Erinnerungen für Claude aus, um die Ausgabestil-Anweisungen während des Gesprächs einzuhalten.

Die Tokennutzung hängt vom Stil ab. Das Hinzufügen von Anweisungen zur Systemaufforderung erhöht die Eingabe-Token, obwohl Prompt Caching diese Kosten nach der ersten Anfrage in einer Sitzung reduziert. Die integrierten Explanatory- und Learning-Stile erzeugen absichtlich längere Antworten als Standard, was die Ausgabe-Token erhöht. Bei benutzerdefinierten Stilen hängt die Tokennutzung für die Ausgabe davon ab, was Ihre Anweisungen Claude zu produzieren sagen.

## Ändern Sie Ihren Ausgabestil

Führen Sie `/config` aus und wählen Sie **Output style**, um einen Stil aus einem Menü auszuwählen. Ihre Auswahl wird in `.claude/settings.local.json` auf der [lokalen Projektebene](/de/settings) gespeichert.

Um einen Stil ohne Menü festzulegen, bearbeiten Sie das Feld `outputStyle` direkt in einer Einstellungsdatei:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Da der Ausgabestil in der Systemaufforderung beim Sitzungsstart festgelegt wird, werden Änderungen beim nächsten Start einer neuen Sitzung wirksam. Dies hält die Systemaufforderung während eines Gesprächs stabil, sodass Prompt Caching die Latenz und Kosten reduzieren kann.

## Erstellen Sie einen benutzerdefinierten Ausgabestil

Benutzerdefinierte Ausgabestile sind Markdown-Dateien mit Frontmatter und dem Text, der zur Systemaufforderung hinzugefügt wird:

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

Sie können diese Dateien auf drei Ebenen speichern:

* Benutzer: `~/.claude/output-styles`
* Projekt: `.claude/output-styles`
* Verwaltete Richtlinie: `.claude/output-styles` im [Verzeichnis für verwaltete Einstellungen](/de/settings#settings-files)

[Plugins](/de/plugins-reference) können auch Ausgabestile in einem `output-styles/`-Verzeichnis bereitstellen.

### Frontmatter

Ausgabestil-Dateien unterstützen Frontmatter zum Angeben von Metadaten:

| Frontmatter                | Zweck                                                                                                                                                                                                                                                                          | Standard                   |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------- |
| `name`                     | Name des Ausgabestils, falls nicht der Dateiname                                                                                                                                                                                                                               | Wird vom Dateinamen geerbt |
| `description`              | Beschreibung des Ausgabestils, angezeigt in der `/config`-Auswahl                                                                                                                                                                                                              | Keine                      |
| `keep-coding-instructions` | Ob die Teile der Systemaufforderung von Claude Code bezüglich Codierung beibehalten werden sollen.                                                                                                                                                                             | false                      |
| `force-for-plugin`         | Nur Plugin-Ausgabestile: Wenden Sie diesen Stil automatisch an, wenn das Plugin aktiviert ist, ohne dass Benutzer ihn auswählen müssen. Überschreibt die `outputStyle`-Einstellung des Benutzers. Wenn mehrere aktivierte Plugins dies festlegen, gewinnt das zuerst geladene. | false                      |

## Vergleiche mit verwandten Funktionen

### Ausgabestile vs. CLAUDE.md vs. --append-system-prompt

Wählen Sie basierend darauf, ob Claude seine Rolle als Coding-Assistent aufgeben oder seine Standardrolle behalten und mehr lernen soll. Ausgabestile ersetzen die Softwareentwicklungsteile von Claude Codes Systemaufforderung durch Ihre eigene Rolle und Stimme, verwenden Sie also einen, wenn Claude eine andere Identität annehmen soll, wie ein Schreib-Editor oder ein Datenanalyse-Assistent. CLAUDE.md und `--append-system-prompt` behalten beide Claude Codes Standardidentität bei und ergänzen sie, verwenden Sie sie also, wenn Claude ein Coding-Assistent bleiben soll, der auch Ihre Projektkonventionen oder zusätzliche Anweisungen befolgt.

Die Mechanismen unterscheiden sich ebenfalls. Ausgabestile bearbeiten die Systemaufforderung direkt. CLAUDE.md fügt seinen Inhalt als Benutzernachricht nach der Systemaufforderung hinzu. `--append-system-prompt` hängt Inhalte an das Ende der Systemaufforderung an, ohne etwas zu entfernen.

### Ausgabestile vs. [Agents](/de/sub-agents)

Verwenden Sie einen Ausgabestil, um zu ändern, wie die Hauptkonversation in jeder Sitzung antwortet. Verwenden Sie einen [Subagent](/de/sub-agents), wenn Sie einen separat definierten Helper möchten, an den die Hauptkonversation delegiert. Ausgabestile beeinflussen nur die Systemaufforderung der Hauptagentenschleife. Agents bewältigen spezifische Aufgaben und können ihr eigenes Modell, Tools und einen Kontext darüber haben, wann sie aufgerufen werden sollen.

### Ausgabestile vs. [Skills](/de/skills)

Ausgabestile ändern, wie Claude antwortet (Formatierung, Ton, Struktur), und sind immer aktiv, sobald sie ausgewählt sind. Skills sind aufgabenspezifische Aufforderungen, die Sie mit `/skill-name` aufrufen oder die Claude automatisch lädt, wenn relevant. Verwenden Sie Ausgabestile für konsistente Formatierungspräferenzen; verwenden Sie Skills für wiederverwendbare Workflows und Aufgaben.
