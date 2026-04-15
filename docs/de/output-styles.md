> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ausgabestile

> Passen Sie Claude Code für Anwendungsfälle über Softwareentwicklung hinaus an

Ausgabestile ermöglichen es Ihnen, Claude Code als jeden Agententyp zu verwenden, während Sie seine Kernfunktionen wie das Ausführen lokaler Skripte, das Lesen/Schreiben von Dateien und das Nachverfolgen von TODOs beibehalten.

## Integrierte Ausgabestile

Der **Standard**-Ausgabestil von Claude Code ist die vorhandene Systemaufforderung, die Ihnen helfen soll, Softwareentwicklungsaufgaben effizient zu bewältigen.

Es gibt zwei zusätzliche integrierte Ausgabestile, die sich auf das Unterrichten der Codebasis und der Funktionsweise von Claude konzentrieren:

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

Sie können diese Dateien auf Benutzerebene (`~/.claude/output-styles`) oder Projektebene (`.claude/output-styles`) speichern.

### Frontmatter

Ausgabestil-Dateien unterstützen Frontmatter zum Angeben von Metadaten:

| Frontmatter                | Zweck                                                                                              | Standard                   |
| :------------------------- | :------------------------------------------------------------------------------------------------- | :------------------------- |
| `name`                     | Name des Ausgabestils, falls nicht der Dateiname                                                   | Wird vom Dateinamen geerbt |
| `description`              | Beschreibung des Ausgabestils, angezeigt in der `/config`-Auswahl                                  | Keine                      |
| `keep-coding-instructions` | Ob die Teile der Systemaufforderung von Claude Code bezüglich Codierung beibehalten werden sollen. | false                      |

## Vergleiche mit verwandten Funktionen

### Ausgabestile vs. CLAUDE.md vs. --append-system-prompt

Ausgabestile schalten die Teile der Standard-Systemaufforderung von Claude Code, die spezifisch für Softwareentwicklung sind, vollständig aus. Weder CLAUDE.md noch `--append-system-prompt` bearbeiten die Standard-Systemaufforderung von Claude Code. CLAUDE.md fügt den Inhalt als Benutzernachricht *nach* der Standard-Systemaufforderung von Claude Code hinzu. `--append-system-prompt` hängt den Inhalt an die Systemaufforderung an.

### Ausgabestile vs. [Agents](/de/sub-agents)

Ausgabestile beeinflussen direkt die Hauptagentenschleife und beeinflussen nur die Systemaufforderung. Agents werden aufgerufen, um bestimmte Aufgaben zu bewältigen, und können zusätzliche Einstellungen wie das zu verwendende Modell, die verfügbaren Tools und einen Kontext darüber enthalten, wann der Agent verwendet werden soll.

### Ausgabestile vs. [Skills](/de/skills)

Ausgabestile ändern, wie Claude antwortet (Formatierung, Ton, Struktur), und sind immer aktiv, sobald sie ausgewählt sind. Skills sind aufgabenspezifische Aufforderungen, die Sie mit `/skill-name` aufrufen oder die Claude automatisch lädt, wenn relevant. Verwenden Sie Ausgabestile für konsistente Formatierungspräferenzen; verwenden Sie Skills für wiederverwendbare Workflows und Aufgaben.
