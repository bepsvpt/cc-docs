> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Berechtigungen konfigurieren

> Kontrollieren Sie, worauf Claude Code zugreifen kann und was es mit granularen Berechtigungsregeln, Modi und verwalteten Richtlinien tun kann.

Claude Code unterstützt granulare Berechtigungen, sodass Sie genau angeben können, was der Agent tun darf und was nicht. Berechtigungseinstellungen können in die Versionskontrolle eingecheckt und an alle Entwickler in Ihrer Organisation verteilt werden, sowie von einzelnen Entwicklern angepasst werden.

## Berechtigungssystem

Claude Code verwendet ein gestuftes Berechtigungssystem, um Leistung und Sicherheit auszugleichen:

| Werkzeugtyp   | Beispiel                     | Genehmigung erforderlich | Verhalten „Ja, nicht mehr fragen"           |
| :------------ | :--------------------------- | :----------------------- | :------------------------------------------ |
| Nur Lesen     | Dateilesevorgänge, Grep      | Nein                     | N/A                                         |
| Bash-Befehle  | Shell-Ausführung             | Ja                       | Dauerhaft pro Projektverzeichnis und Befehl |
| Dateiänderung | Dateien bearbeiten/schreiben | Ja                       | Bis zum Ende der Sitzung                    |

## Berechtigungen verwalten

Sie können Claude Code's Werkzeugberechtigungen mit `/permissions` anzeigen und verwalten. Diese Benutzeroberfläche listet alle Berechtigungsregeln und die settings.json-Dateien auf, aus denen sie stammen.

* **Allow**-Regeln ermöglichen Claude Code, das angegebene Werkzeug ohne manuelle Genehmigung zu verwenden.
* **Ask**-Regeln fordern eine Bestätigung auf, wenn Claude Code versucht, das angegebene Werkzeug zu verwenden.
* **Deny**-Regeln verhindern, dass Claude Code das angegebene Werkzeug verwendet.

Regeln werden in dieser Reihenfolge ausgewertet: **deny -> ask -> allow**. Die erste übereinstimmende Regel gewinnt, daher haben Deny-Regeln immer Vorrang.

## Berechtigungsmodi

Claude Code unterstützt mehrere Berechtigungsmodi, die steuern, wie Werkzeuge genehmigt werden. Legen Sie den `defaultMode` in Ihren [Einstellungsdateien](/de/settings#settings-files) fest:

| Modus               | Beschreibung                                                                                                                |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Standardverhalten: fordert Genehmigung bei der ersten Verwendung jedes Werkzeugs auf                                        |
| `acceptEdits`       | Akzeptiert automatisch Dateiberechtigungen für die Sitzung                                                                  |
| `plan`              | Plan Mode: Claude kann Dateien analysieren, aber nicht ändern oder Befehle ausführen                                        |
| `dontAsk`           | Verweigert Werkzeuge automatisch, es sei denn, sie sind vorab über `/permissions` oder `permissions.allow`-Regeln genehmigt |
| `bypassPermissions` | Überspringt alle Berechtigungsaufforderungen (erfordert sichere Umgebung, siehe Warnung unten)                              |

<Warning>
  Der Modus `bypassPermissions` deaktiviert alle Berechtigungsprüfungen. Verwenden Sie diesen nur in isolierten Umgebungen wie Containern oder VMs, in denen Claude Code keinen Schaden anrichten kann. Administratoren können diesen Modus verhindern, indem sie `disableBypassPermissionsMode` in [verwalteten Einstellungen](#managed-settings) auf `"disable"` setzen.
</Warning>

## Berechtigungsregelsyntax

Berechtigungsregeln folgen dem Format `Tool` oder `Tool(specifier)`.

### Alle Verwendungen eines Werkzeugs abgleichen

Um alle Verwendungen eines Werkzeugs abzugleichen, verwenden Sie einfach den Werkzeugnamen ohne Klammern:

| Regel      | Effekt                             |
| :--------- | :--------------------------------- |
| `Bash`     | Gleicht alle Bash-Befehle ab       |
| `WebFetch` | Gleicht alle Web-Fetch-Anfragen ab |
| `Read`     | Gleicht alle Dateilesevorgänge ab  |

`Bash(*)` ist gleichwertig mit `Bash` und gleicht alle Bash-Befehle ab.

### Verwenden Sie Spezifizierer für granulare Kontrolle

Fügen Sie einen Spezifizierer in Klammern hinzu, um bestimmte Werkzeugverwendungen abzugleichen:

| Regel                          | Effekt                                                         |
| :----------------------------- | :------------------------------------------------------------- |
| `Bash(npm run build)`          | Gleicht den genauen Befehl `npm run build` ab                  |
| `Read(./.env)`                 | Gleicht das Lesen der `.env`-Datei im aktuellen Verzeichnis ab |
| `WebFetch(domain:example.com)` | Gleicht Fetch-Anfragen an example.com ab                       |

### Wildcard-Muster

Bash-Regeln unterstützen Glob-Muster mit `*`. Platzhalter können an jeder Position im Befehl erscheinen. Diese Konfiguration ermöglicht npm- und git-Commit-Befehle, blockiert aber git push:

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

Das Leerzeichen vor `*` ist wichtig: `Bash(ls *)` gleicht `ls -la` ab, aber nicht `lsof`, während `Bash(ls*)` beide abgleicht. Die veraltete `:*`-Suffixsyntax ist gleichwertig mit ` *`, wird aber nicht mehr empfohlen.

## Werkzeugspezifische Berechtigungsregeln

### Bash

Bash-Berechtigungsregeln unterstützen Wildcard-Abgleich mit `*`. Platzhalter können an jeder Position im Befehl erscheinen, einschließlich am Anfang, in der Mitte oder am Ende:

* `Bash(npm run build)` gleicht den genauen Bash-Befehl `npm run build` ab
* `Bash(npm run test *)` gleicht Bash-Befehle ab, die mit `npm run test` beginnen
* `Bash(npm *)` gleicht jeden Befehl ab, der mit `npm ` beginnt
* `Bash(* install)` gleicht jeden Befehl ab, der mit ` install` endet
* `Bash(git * main)` gleicht Befehle wie `git checkout main`, `git merge main` ab

Wenn `*` am Ende mit einem Leerzeichen davor erscheint (wie `Bash(ls *)`), wird eine Wortgrenze erzwungen, die erfordert, dass dem Präfix ein Leerzeichen oder das Ende der Zeichenkette folgt. Zum Beispiel gleicht `Bash(ls *)` `ls -la` ab, aber nicht `lsof`. Im Gegensatz dazu gleicht `Bash(ls*)` ohne Leerzeichen sowohl `ls -la` als auch `lsof` ab, da es keine Wortgrenzbeschränkung gibt.

<Tip>
  Claude Code ist sich Shell-Operatoren (wie `&&`) bewusst, daher gibt eine Präfixabgleichregel wie `Bash(safe-cmd *)` ihm nicht die Berechtigung, den Befehl `safe-cmd && other-cmd` auszuführen.
</Tip>

<Warning>
  Bash-Berechtigungsmuster, die versuchen, Befehlsargumente einzuschränken, sind fragil. Zum Beispiel beabsichtigt `Bash(curl http://github.com/ *)`, curl auf GitHub-URLs zu beschränken, wird aber Variationen nicht abgleichen wie:

  * Optionen vor URL: `curl -X GET http://github.com/...`
  * Anderes Protokoll: `curl https://github.com/...`
  * Umleitungen: `curl -L http://bit.ly/xyz` (leitet zu github um)
  * Variablen: `URL=http://github.com && curl $URL`
  * Zusätzliche Leerzeichen: `curl  http://github.com`

  Für zuverlässigere URL-Filterung sollten Sie erwägen:

  * **Bash-Netzwerkwerkzeuge einschränken**: Verwenden Sie Deny-Regeln, um `curl`, `wget` und ähnliche Befehle zu blockieren, verwenden Sie dann das WebFetch-Werkzeug mit `WebFetch(domain:github.com)`-Berechtigung für zulässige Domänen
  * **PreToolUse-Hooks verwenden**: Implementieren Sie einen Hook, der URLs in Bash-Befehlen validiert und nicht zulässige Domänen blockiert
  * Claude Code über Ihre zulässigen curl-Muster über CLAUDE.md informieren

  Beachten Sie, dass die alleinige Verwendung von WebFetch keinen Netzwerkzugriff verhindert. Wenn Bash zulässig ist, kann Claude immer noch `curl`, `wget` oder andere Werkzeuge verwenden, um auf jede URL zuzugreifen.
</Warning>

### Read und Edit

`Edit`-Regeln gelten für alle integrierten Werkzeuge, die Dateien bearbeiten. Claude versucht nach besten Kräften, `Read`-Regeln auf alle integrierten Werkzeuge anzuwenden, die Dateien lesen, wie Grep und Glob.

Read- und Edit-Regeln folgen beide der [gitignore](https://git-scm.com/docs/gitignore)-Spezifikation mit vier unterschiedlichen Mustertypen:

| Muster               | Bedeutung                                  | Beispiel                         | Gleicht ab                     |
| -------------------- | ------------------------------------------ | -------------------------------- | ------------------------------ |
| `//path`             | **Absoluter** Pfad vom Dateisystem-Root    | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`             | Pfad vom **Home**-Verzeichnis              | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`              | Pfad **relativ zum Projekt-Root**          | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` oder `./path` | Pfad **relativ zum aktuellen Verzeichnis** | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  Ein Muster wie `/Users/alice/file` ist KEIN absoluter Pfad. Es ist relativ zum Projekt-Root. Verwenden Sie `//Users/alice/file` für absolute Pfade.
</Warning>

Beispiele:

* `Edit(/docs/**)`: Bearbeitungen in `<project>/docs/` (NICHT `/docs/` und NICHT `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: liest die `.zshrc` Ihres Home-Verzeichnisses
* `Edit(//tmp/scratch.txt)`: bearbeitet den absoluten Pfad `/tmp/scratch.txt`
* `Read(src/**)`: liest aus `<current-directory>/src/`

<Note>
  In gitignore-Mustern gleicht `*` Dateien in einem einzelnen Verzeichnis ab, während `**` rekursiv über Verzeichnisse hinweg abgleicht. Um allen Dateizugriff zu ermöglichen, verwenden Sie einfach den Werkzeugnamen ohne Klammern: `Read`, `Edit` oder `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` gleicht Fetch-Anfragen an example.com ab

### MCP

* `mcp__puppeteer` gleicht jedes Werkzeug ab, das vom `puppeteer`-Server bereitgestellt wird (Name in Claude Code konfiguriert)
* `mcp__puppeteer__*` Wildcard-Syntax, die auch alle Werkzeuge vom `puppeteer`-Server abgleicht
* `mcp__puppeteer__puppeteer_navigate` gleicht das `puppeteer_navigate`-Werkzeug ab, das vom `puppeteer`-Server bereitgestellt wird

### Agent (subagents)

Verwenden Sie `Agent(AgentName)`-Regeln, um zu steuern, welche [subagents](/de/sub-agents) Claude verwenden kann:

* `Agent(Explore)` gleicht den Explore-Subagent ab
* `Agent(Plan)` gleicht den Plan-Subagent ab
* `Agent(my-custom-agent)` gleicht einen benutzerdefinierten Subagent namens `my-custom-agent` ab

Fügen Sie diese Regeln zum `deny`-Array in Ihren Einstellungen hinzu oder verwenden Sie das `--disallowedTools`-CLI-Flag, um bestimmte Agenten zu deaktivieren. Um den Explore-Agenten zu deaktivieren:

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Berechtigungen mit Hooks erweitern

[Claude Code hooks](/de/hooks-guide) bieten eine Möglichkeit, benutzerdefinierte Shell-Befehle zu registrieren, um die Berechtigungsevaluierung zur Laufzeit durchzuführen. Wenn Claude Code einen Werkzeugaufruf tätigt, werden PreToolUse-Hooks vor dem Berechtigungssystem ausgeführt, und die Hook-Ausgabe kann bestimmen, ob der Werkzeugaufruf anstelle des Berechtigungssystems genehmigt oder abgelehnt wird.

## Arbeitsverzeichnisse

Standardmäßig hat Claude Zugriff auf Dateien in dem Verzeichnis, in dem es gestartet wurde. Sie können diesen Zugriff erweitern:

* **Beim Start**: Verwenden Sie das CLI-Argument `--add-dir <path>`
* **Während der Sitzung**: Verwenden Sie den Befehl `/add-dir`
* **Persistente Konfiguration**: Fügen Sie zu `additionalDirectories` in [Einstellungsdateien](/de/settings#settings-files) hinzu

Dateien in zusätzlichen Verzeichnissen folgen den gleichen Berechtigungsregeln wie das ursprüngliche Arbeitsverzeichnis: Sie werden lesbar ohne Aufforderungen, und Dateiberechtigungen folgen dem aktuellen Berechtigungsmodus.

## Wie Berechtigungen mit Sandboxing interagieren

Berechtigungen und [Sandboxing](/de/sandboxing) sind komplementäre Sicherheitsebenen:

* **Berechtigungen** steuern, welche Werkzeuge Claude Code verwenden kann und auf welche Dateien oder Domänen es zugreifen kann. Sie gelten für alle Werkzeuge (Bash, Read, Edit, WebFetch, MCP und andere).
* **Sandboxing** bietet OS-Ebenen-Durchsetzung, die den Zugriff des Bash-Werkzeugs auf das Dateisystem und das Netzwerk einschränkt. Es gilt nur für Bash-Befehle und ihre untergeordneten Prozesse.

Verwenden Sie beide für Defense-in-Depth:

* Berechtigungs-Deny-Regeln blockieren Claude daran, überhaupt zu versuchen, auf eingeschränkte Ressourcen zuzugreifen
* Sandbox-Einschränkungen verhindern, dass Bash-Befehle Ressourcen außerhalb definierter Grenzen erreichen, selbst wenn eine Prompt-Injection Claude's Entscheidungsfindung umgeht
* Dateisystem-Einschränkungen in der Sandbox verwenden Read- und Edit-Deny-Regeln, nicht separate Sandbox-Konfiguration
* Netzwerk-Einschränkungen kombinieren WebFetch-Berechtigungsregeln mit der `allowedDomains`-Liste der Sandbox

## Verwaltete Einstellungen

Für Organisationen, die eine zentralisierte Kontrolle über die Claude Code-Konfiguration benötigen, können Administratoren verwaltete Einstellungen bereitstellen, die nicht von Benutzer- oder Projekteinstellungen überschrieben werden können. Diese Richtlinieneinstellungen folgen dem gleichen Format wie reguläre Einstellungsdateien und können über MDM/OS-Ebenen-Richtlinien, verwaltete Einstellungsdateien oder [servergesteuerte Einstellungen](/de/server-managed-settings) bereitgestellt werden. Siehe [Einstellungsdateien](/de/settings#settings-files) für Bereitstellungsmechanismen und Dateispeicherorte.

### Nur verwaltete Einstellungen

Einige Einstellungen sind nur in verwalteten Einstellungen wirksam:

| Einstellung                               | Beschreibung                                                                                                                                                                                                                                                                              |
| :---------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | Auf `"disable"` setzen, um den Modus `bypassPermissions` und das Flag `--dangerously-skip-permissions` zu verhindern                                                                                                                                                                      |
| `allowManagedPermissionRulesOnly`         | Wenn `true`, verhindert, dass Benutzer- und Projekteinstellungen `allow`-, `ask`- oder `deny`-Berechtigungsregeln definieren. Nur Regeln in verwalteten Einstellungen gelten                                                                                                              |
| `allowManagedHooksOnly`                   | Wenn `true`, verhindert das Laden von Benutzer-, Projekt- und Plugin-Hooks. Nur verwaltete Hooks und SDK-Hooks sind zulässig                                                                                                                                                              |
| `allowManagedMcpServersOnly`              | Wenn `true`, werden nur `allowedMcpServers` aus verwalteten Einstellungen berücksichtigt. `deniedMcpServers` wird immer noch aus allen Quellen zusammengeführt. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                   |
| `blockedMarketplaces`                     | Blocklist von Marketplace-Quellen. Blockierte Quellen werden vor dem Download überprüft, sodass sie das Dateisystem nie berühren. Siehe [verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                |
| `sandbox.network.allowManagedDomainsOnly` | Wenn `true`, werden nur `allowedDomains` und `WebFetch(domain:...)`-Allow-Regeln aus verwalteten Einstellungen berücksichtigt. Nicht zulässige Domänen werden automatisch blockiert, ohne den Benutzer zu fragen. Verweigerte Domänen werden immer noch aus allen Quellen zusammengeführt |
| `strictKnownMarketplaces`                 | Steuert, welche Plugin-Marketplaces Benutzer hinzufügen können. Siehe [verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                  |
| `allow_remote_sessions`                   | Wenn `true`, ermöglicht Benutzern, [Remote Control](/de/remote-control) und [Web-Sitzungen](/de/claude-code-on-the-web) zu starten. Standardmäßig `true`. Auf `false` setzen, um Remote-Sitzungszugriff zu verhindern                                                                     |

## Einstellungspriorität

Berechtigungsregeln folgen der gleichen [Einstellungspriorität](/de/settings#settings-precedence) wie alle anderen Claude Code-Einstellungen:

1. **Verwaltete Einstellungen**: können von keiner anderen Ebene überschrieben werden, einschließlich Befehlszeilenargumenten
2. **Befehlszeilenargumente**: temporäre Sitzungsüberschreibungen
3. **Lokale Projekteinstellungen** (`.claude/settings.local.json`)
4. **Gemeinsame Projekteinstellungen** (`.claude/settings.json`)
5. **Benutzereinstellungen** (`~/.claude/settings.json`)

Wenn ein Werkzeug auf einer beliebigen Ebene verweigert wird, kann keine andere Ebene es zulassen. Zum Beispiel kann eine verwaltete Einstellungs-Deny nicht durch `--allowedTools` überschrieben werden, und `--disallowedTools` kann Einschränkungen über das hinaus hinzufügen, was verwaltete Einstellungen definieren.

Wenn eine Berechtigung in Benutzereinstellungen zulässig ist, aber in Projekteinstellungen verweigert wird, hat die Projekteinstellung Vorrang und die Berechtigung wird blockiert.

## Beispielkonfigurationen

Dieses [Repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) enthält Starter-Einstellungskonfigurationen für häufige Bereitstellungsszenarien. Verwenden Sie diese als Ausgangspunkte und passen Sie sie an Ihre Anforderungen an.

## Siehe auch

* [Einstellungen](/de/settings): vollständige Konfigurationsreferenz einschließlich der Berechtigungseinstellungstabelle
* [Sandboxing](/de/sandboxing): OS-Ebenen-Dateisystem- und Netzwerkisolation für Bash-Befehle
* [Authentifizierung](/de/authentication): Richten Sie Benutzerzugriff auf Claude Code ein
* [Sicherheit](/de/security): Sicherheitsvorkehrungen und Best Practices
* [Hooks](/de/hooks-guide): Automatisieren Sie Workflows und erweitern Sie die Berechtigungsevaluierung
