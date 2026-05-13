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

<Note>
  Berechtigungsregeln werden von Claude Code durchgesetzt, nicht vom Modell. Anweisungen in Ihrem Prompt oder `CLAUDE.md` bestimmen, was Claude versucht zu tun, aber sie ändern nicht, was Claude Code erlaubt. Um Zugriff zu gewähren oder zu widerrufen, verwenden Sie `/permissions`, die hier beschriebenen Regeln, einen [Berechtigungsmodus](/de/permission-modes) oder einen [PreToolUse-Hook](#extend-permissions-with-hooks).
</Note>

## Berechtigungsmodi

Claude Code unterstützt mehrere Berechtigungsmodi, die steuern, wie Werkzeuge genehmigt werden. Siehe [Berechtigungsmodi](/de/permission-modes) für den Zeitpunkt der Verwendung jedes Modus. Legen Sie den `defaultMode` in Ihren [Einstellungsdateien](/de/settings#settings-files) fest:

| Modus               | Beschreibung                                                                                                                                                                                    |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Standardverhalten: fordert Genehmigung bei der ersten Verwendung jedes Werkzeugs auf                                                                                                            |
| `acceptEdits`       | Akzeptiert automatisch Dateiberechtigungen und häufige Dateisystem-Befehle (`mkdir`, `touch`, `mv`, `cp` usw.) für Pfade im Arbeitsverzeichnis oder `additionalDirectories`                     |
| `plan`              | Plan Mode: Claude liest Dateien und führt schreibgeschützte Shell-Befehle aus, um zu erkunden, bearbeitet aber nicht Ihre Quelldateien                                                          |
| `auto`              | Genehmigt Werkzeugaufrufe automatisch mit Hintergrund-Sicherheitsprüfungen, die überprüfen, ob Aktionen mit Ihrer Anfrage übereinstimmen. Derzeit eine Forschungsvorschau                       |
| `dontAsk`           | Verweigert Werkzeuge automatisch, es sei denn, sie sind vorab über `/permissions` oder `permissions.allow`-Regeln genehmigt                                                                     |
| `bypassPermissions` | Überspringt alle Berechtigungsaufforderungen. Entfernungen von Dateisystem-Root oder Home-Verzeichnis wie `rm -rf /` und `rm -rf ~` fordern weiterhin auf als Schutzschalter gegen Modellfehler |

<Warning>
  Der Modus `bypassPermissions` überspringt alle Berechtigungsaufforderungen, einschließlich Schreibvorgänge in `.git`, `.claude`, `.vscode`, `.idea` und `.husky`. Entfernungen, die auf das Dateisystem-Root oder Home-Verzeichnis abzielen, wie `rm -rf /` und `rm -rf ~`, fordern weiterhin auf als Schutzschalter gegen Modellfehler. Verwenden Sie diesen Modus nur in isolierten Umgebungen wie Containern oder VMs, in denen Claude Code keinen Schaden anrichten kann. Administratoren können diesen Modus verhindern, indem sie `permissions.disableBypassPermissionsMode` in [verwalteten Einstellungen](#managed-settings) auf `"disable"` setzen.
</Warning>

Um zu verhindern, dass der Modus `bypassPermissions` oder `auto` verwendet wird, setzen Sie `permissions.disableBypassPermissionsMode` oder `permissions.disableAutoMode` in einer beliebigen [Einstellungsdatei](/de/settings#settings-files) auf `"disable"`. Diese sind am nützlichsten in [verwalteten Einstellungen](#managed-settings), wo sie nicht überschrieben werden können.

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

```json theme={null}
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

Das Leerzeichen vor `*` ist wichtig: `Bash(ls *)` gleicht `ls -la` ab, aber nicht `lsof`, während `Bash(ls*)` beide abgleicht. Das Suffix `:*` ist eine gleichwertige Möglichkeit, einen nachgestellten Platzhalter zu schreiben, daher gleicht `Bash(ls:*)` die gleichen Befehle ab wie `Bash(ls *)`.

Der Berechtigungsdialog schreibt die durch Leerzeichen getrennte Form, wenn Sie „Ja, nicht mehr fragen" für ein Befehlspräfix auswählen. Die Form `:*` wird nur am Ende eines Musters erkannt. In einem Muster wie `Bash(git:* push)` wird der Doppelpunkt als Literalzeichen behandelt und passt nicht zu git-Befehlen.

## Werkzeugspezifische Berechtigungsregeln

### Bash

Bash-Berechtigungsregeln unterstützen Wildcard-Abgleich mit `*`. Platzhalter können an jeder Position im Befehl erscheinen, einschließlich am Anfang, in der Mitte oder am Ende:

* `Bash(npm run build)` gleicht den genauen Bash-Befehl `npm run build` ab
* `Bash(npm run test *)` gleicht Bash-Befehle ab, die mit `npm run test` beginnen
* `Bash(npm *)` gleicht jeden Befehl ab, der mit `npm ` beginnt
* `Bash(* install)` gleicht jeden Befehl ab, der mit ` install` endet
* `Bash(git * main)` gleicht Befehle wie `git checkout main` und `git log --oneline main` ab

Ein einzelnes `*` gleicht jede Zeichenfolge ab, einschließlich Leerzeichen, daher kann ein Platzhalter mehrere Argumente umfassen. `Bash(git *)` gleicht `git log --oneline --all` ab, und `Bash(git * main)` gleicht sowohl `git push origin main` als auch `git merge main` ab.

Wenn `*` am Ende mit einem Leerzeichen davor erscheint (wie `Bash(ls *)`), wird eine Wortgrenze erzwungen, die erfordert, dass dem Präfix ein Leerzeichen oder das Ende der Zeichenkette folgt. Zum Beispiel gleicht `Bash(ls *)` `ls -la` ab, aber nicht `lsof`. Im Gegensatz dazu gleicht `Bash(ls*)` ohne Leerzeichen sowohl `ls -la` als auch `lsof` ab, da es keine Wortgrenzbeschränkung gibt.

#### Zusammengesetzte Befehle

<Tip>
  Claude Code ist sich Shell-Operatoren bewusst, daher gibt eine Regel wie `Bash(safe-cmd *)` ihm nicht die Berechtigung, den Befehl `safe-cmd && other-cmd` auszuführen. Die erkannten Befehlstrennzeichen sind `&&`, `||`, `;`, `|`, `|&`, `&` und Zeilenumbrüche. Eine Regel muss jeden Unterbefehl unabhängig abgleichen.
</Tip>

Wenn Sie einen zusammengesetzten Befehl mit „Ja, nicht mehr fragen" genehmigen, speichert Claude Code eine separate Regel für jeden Unterbefehl, der Genehmigung erfordert, anstelle einer einzelnen Regel für die vollständige zusammengesetzte Zeichenkette. Zum Beispiel speichert das Genehmigen von `git status && npm test` eine Regel für `npm test`, sodass zukünftige `npm test`-Aufrufe erkannt werden, unabhängig davon, was dem `&&` vorausgeht. Unterbefehle wie `cd` in ein Unterverzeichnis generieren ihre eigene Read-Regel für diesen Pfad. Für einen einzelnen zusammengesetzten Befehl können bis zu 5 Regeln gespeichert werden.

#### Prozess-Wrapper

Vor dem Abgleich von Bash-Regeln entfernt Claude Code einen festen Satz von Prozess-Wrappern, daher gleicht eine Regel wie `Bash(npm test *)` auch `timeout 30 npm test` ab. Die erkannten Wrapper sind `timeout`, `time`, `nice`, `nohup` und `stdbuf`.

Auch bloßes `xargs` wird entfernt, daher gleicht `Bash(grep *)` `xargs grep pattern` ab. Das Entfernen gilt nur, wenn `xargs` keine Flags hat: Ein Aufruf wie `xargs -n1 grep pattern` wird als `xargs`-Befehl abgeglichen, daher decken Regeln, die für den inneren Befehl geschrieben wurden, ihn nicht ab.

Diese Wrapper-Liste ist integriert und nicht konfigurierbar. Entwicklungsumgebungs-Runner wie `direnv exec`, `devbox run`, `mise exec`, `npx` und `docker exec` sind nicht in der Liste. Da diese Tools ihre Argumente als Befehl ausführen, gleicht eine Regel wie `Bash(devbox run *)` alles ab, was nach `run` kommt, einschließlich `devbox run rm -rf .`. Um Arbeit innerhalb eines Umgebungs-Runners zu genehmigen, schreiben Sie eine spezifische Regel, die sowohl den Runner als auch den inneren Befehl enthält, wie `Bash(devbox run npm test)`. Fügen Sie eine Regel pro innerem Befehl hinzu, den Sie zulassen möchten.

Exec-Wrapper wie `watch`, `setsid`, `ionice` und `flock` fordern immer auf und können nicht durch eine Präfixregel wie `Bash(watch *)` automatisch genehmigt werden. Das gleiche gilt für `find` mit `-exec` oder `-delete`: Eine `Bash(find *)` Regel deckt diese Formen nicht ab. Um einen spezifischen Aufruf zu genehmigen, schreiben Sie eine exakte Übereinstimmungsregel für die vollständige Befehlszeichenkette.

#### Schreibgeschützte Befehle

Claude Code erkennt einen integrierten Satz von Bash-Befehlen als schreibgeschützt und führt sie ohne Berechtigungsaufforderung in jedem Modus aus. Diese umfassen `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd` und schreibgeschützte Formen von `git`. Der Satz ist nicht konfigurierbar; um eine Aufforderung für einen dieser Befehle zu erfordern, fügen Sie eine `ask`- oder `deny`-Regel dafür hinzu.

Unquotierte Glob-Muster sind für Befehle zulässig, deren jedes Flag schreibgeschützt ist, daher laufen `ls *.ts` und `wc -l src/*.py` ohne Aufforderung. Befehle mit schreibfähigen oder ausführungsfähigen Flags, wie `find`, `sort`, `sed` und `git`, fordern immer noch auf, wenn ein unquotiertes Glob vorhanden ist, da das Glob zu einem Flag wie `-delete` expandieren könnte.

Ein `cd` in einen Pfad innerhalb Ihres Arbeitsverzeichnisses oder eines [zusätzlichen Verzeichnisses](#working-directories) ist auch schreibgeschützt. Ein zusammengesetzter Befehl wie `cd packages/api && ls` läuft ohne Aufforderung, wenn jeder Teil auf eigene Faust qualifiziert. Das Kombinieren von `cd` mit `git` in einem zusammengesetzten Befehl fordert immer auf, unabhängig vom Zielverzeichnis.

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
  * **CLAUDE.md-Anleitung hinzufügen**: Beschreiben Sie Ihre zulässigen curl-Muster in `CLAUDE.md`. Dies beeinflusst, was Claude versucht, erzwingt aber keine Grenze, daher kombinieren Sie es mit einer der obigen Optionen

  Beachten Sie, dass die alleinige Verwendung von WebFetch keinen Netzwerkzugriff verhindert. Wenn Bash zulässig ist, kann Claude immer noch `curl`, `wget` oder andere Werkzeuge verwenden, um auf jede URL zuzugreifen.
</Warning>

### PowerShell

PowerShell-Berechtigungsregeln verwenden die gleiche Form wie Bash-Regeln. Platzhalter mit `*` gleichen an jeder Position ab, das Suffix `:*` ist gleichwertig mit einem nachgestellten ` *`, und ein bloßes `PowerShell` oder `PowerShell(*)` gleicht jeden Befehl ab. Diese Konfiguration ermöglicht `Get-ChildItem`- und `git commit`-Befehle, blockiert aber `Remove-Item`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Häufige Aliase werden vor dem Abgleich kanonisiert. Eine Regel, die für den Cmdlet-Namen geschrieben wurde, gleicht auch seine Aliase ab, daher gleicht `PowerShell(Get-ChildItem *)` auch `gci`, `ls` und `dir` ab. Der Abgleich ist nicht case-sensitiv.

Claude Code analysiert die PowerShell-AST und überprüft jeden Befehl in einem zusammengesetzten Befehl unabhängig. Pipeline-Operatoren `|`, Anweisungstrennzeichen `;` und auf PowerShell 7+ die Kettenoperatoren `&&` und `||` teilen einen zusammengesetzten Befehl in Unterbefehle auf. Eine Regel muss jeden Unterbefehl abgleichen, damit der zusammengesetzte Befehl zulässig ist.

### Read und Edit

`Edit`-Regeln gelten für alle integrierten Werkzeuge, die Dateien bearbeiten. Claude versucht nach besten Kräften, `Read`-Regeln auf alle integrierten Werkzeuge anzuwenden, die Dateien lesen, wie Grep und Glob.

<Warning>
  Read- und Edit-Deny-Regeln gelten für Claude's integrierte Dateiwerkzeuge und für Dateibefehle, die Claude Code in Bash erkennt, wie `cat`, `head`, `tail` und `sed`. Sie gelten nicht für beliebige Unterprozesse, die Dateien indirekt lesen oder schreiben, wie ein Python- oder Node-Skript, das Dateien selbst öffnet. Für OS-Ebenen-Durchsetzung, die alle Prozesse daran hindert, auf einen Pfad zuzugreifen, [aktivieren Sie die Sandbox](/de/sandboxing).
</Warning>

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

Unter Windows werden Pfade vor dem Abgleich in POSIX-Form normalisiert. `C:\Users\alice` wird zu `/c/Users/alice`, verwenden Sie also `//c/**/.env`, um `.env`-Dateien überall auf diesem Laufwerk abzugleichen. Um über alle Laufwerke hinweg abzugleichen, verwenden Sie `//**/.env`.

Beispiele:

* `Edit(/docs/**)`: Bearbeitungen in `<project>/docs/` (NICHT `/docs/` und NICHT `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: liest die `.zshrc` Ihres Home-Verzeichnisses
* `Edit(//tmp/scratch.txt)`: bearbeitet den absoluten Pfad `/tmp/scratch.txt`
* `Read(src/**)`: liest aus `<current-directory>/src/`

Eine Regel gleicht nur Dateien unter ihrem Anker ab, daher bestimmt der Anker, wie weit eine Deny-Regel reicht. Bare Dateinamen folgen gitignore-Semantik und gleichen in jeder Tiefe ab, daher sind `Read(.env)` und `Read(**/.env)` gleichwertig:

| Deny-Regel                        | Blockiert                                           | Blockiert nicht                                                       |
| --------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------- |
| `Read(.env)` oder `Read(**/.env)` | jede `.env` im oder unter dem aktuellen Verzeichnis | `.env` in einem übergeordneten Verzeichnis oder einem anderen Projekt |
| `Read(//**/.env)`                 | jede `.env` überall im Dateisystem                  | nichts; die Regel ist am Dateisystem-Root verankert                   |

<Note>
  In gitignore-Mustern gleicht `*` Dateien in einem einzelnen Verzeichnis ab, während `**` rekursiv über Verzeichnisse hinweg abgleicht. Um allen Dateizugriff zu ermöglichen, verwenden Sie einfach den Werkzeugnamen ohne Klammern: `Read`, `Edit` oder `Write`.
</Note>

Wenn Claude auf einen Symlink zugreift, überprüfen Berechtigungsregeln zwei Pfade: den Symlink selbst und die Datei, auf die er verweist. Allow- und Deny-Regeln behandeln dieses Paar unterschiedlich: Allow-Regeln fallen auf Aufforderungen zurück, während Deny-Regeln direkt blockieren.

* **Allow-Regeln**: gelten nur, wenn sowohl der Symlink-Pfad als auch sein Ziel übereinstimmen. Ein Symlink in einem zulässigen Verzeichnis, der außerhalb davon verweist, fordert Sie immer noch auf.
* **Deny-Regeln**: gelten, wenn entweder der Symlink-Pfad oder sein Ziel übereinstimmt. Ein Symlink, der auf eine verweigerte Datei verweist, ist selbst verweigert.

Zum Beispiel mit `Read(./project/**)` zulässig und `Read(~/.ssh/**)` verweigert, wird ein Symlink bei `./project/key`, der auf `~/.ssh/id_rsa` verweist, blockiert: Das Ziel schlägt die Allow-Regel fehl und passt zur Deny-Regel.

### WebFetch

* `WebFetch(domain:example.com)` gleicht Fetch-Anfragen an example.com ab

### MCP

* `mcp__puppeteer` gleicht jedes Werkzeug ab, das vom `puppeteer`-Server bereitgestellt wird (Name in Claude Code konfiguriert)
* `mcp__puppeteer__*` Wildcard-Syntax, die auch alle Werkzeuge vom `puppeteer`-Server abgleicht
* `mcp__puppeteer__puppeteer_navigate` gleicht das `puppeteer_navigate`-Werkzeug ab, das vom `puppeteer`-Server bereitgestellt wird

### Agent (Subagents)

Verwenden Sie `Agent(AgentName)`-Regeln, um zu steuern, welche [Subagents](/de/sub-agents) Claude verwenden kann:

* `Agent(Explore)` gleicht den Explore-Subagent ab
* `Agent(Plan)` gleicht den Plan-Subagent ab
* `Agent(my-custom-agent)` gleicht einen benutzerdefinierten Subagent namens `my-custom-agent` ab

Fügen Sie diese Regeln zum `deny`-Array in Ihren Einstellungen hinzu oder verwenden Sie das `--disallowedTools`-CLI-Flag, um bestimmte Agenten zu deaktivieren. Um den Explore-Agenten zu deaktivieren:

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Berechtigungen mit Hooks erweitern

[Claude Code Hooks](/de/hooks-guide) bieten eine Möglichkeit, benutzerdefinierte Shell-Befehle zu registrieren, um die Berechtigungsevaluierung zur Laufzeit durchzuführen. Wenn Claude Code einen Werkzeugaufruf tätigt, werden PreToolUse-Hooks vor dem Berechtigungssystem ausgeführt. Die Hook-Ausgabe kann den Werkzeugaufruf verweigern, eine Aufforderung erzwingen oder die Aufforderung überspringen, um den Aufruf fortzufahren.

Hook-Entscheidungen umgehen keine Berechtigungsregeln. Deny- und Ask-Regeln werden unabhängig davon ausgewertet, was ein PreToolUse-Hook zurückgibt, daher blockiert eine übereinstimmende Deny-Regel den Aufruf und eine übereinstimmende Ask-Regel fordert immer noch auf, selbst wenn der Hook `"allow"` oder `"ask"` zurückgegeben hat. Dies bewahrt die Deny-First-Priorität, die in [Berechtigungen verwalten](#manage-permissions) beschrieben ist, einschließlich Deny-Regeln, die in verwalteten Einstellungen festgelegt sind.

Ein blockierender Hook hat auch Vorrang vor Allow-Regeln. Ein Hook, der mit Code 2 beendet wird, stoppt den Werkzeugaufruf, bevor Berechtigungsregeln ausgewertet werden, daher gilt die Blockierung auch dann, wenn eine Allow-Regel den Aufruf sonst zulassen würde. Um alle Bash-Befehle ohne Aufforderungen auszuführen, außer für einige, die Sie blockieren möchten, fügen Sie `"Bash"` zu Ihrer Allow-Liste hinzu und registrieren Sie einen PreToolUse-Hook, der diese spezifischen Befehle ablehnt. Siehe [Bearbeitungen geschützter Dateien blockieren](/de/hooks-guide#block-edits-to-protected-files) für ein Hook-Skript, das Sie anpassen können.

## Arbeitsverzeichnisse

Standardmäßig hat Claude Zugriff auf Dateien in dem Verzeichnis, in dem es gestartet wurde. Sie können diesen Zugriff erweitern:

* **Beim Start**: Verwenden Sie das CLI-Argument `--add-dir <path>`
* **Während der Sitzung**: Verwenden Sie den Befehl `/add-dir`
* **Persistente Konfiguration**: Fügen Sie zu `additionalDirectories` in [Einstellungsdateien](/de/settings#settings-files) hinzu

Dateien in zusätzlichen Verzeichnissen folgen den gleichen Berechtigungsregeln wie das ursprüngliche Arbeitsverzeichnis: Sie werden lesbar ohne Aufforderungen, und Dateiberechtigungen folgen dem aktuellen Berechtigungsmodus.

### Zusätzliche Verzeichnisse gewähren Dateizugriff, keine Konfiguration

Das Hinzufügen eines Verzeichnisses erweitert, wo Claude Dateien lesen und bearbeiten kann. Es macht dieses Verzeichnis nicht zu einem vollständigen Konfigurationsroot: Die meisten `.claude/`-Konfigurationen werden nicht aus zusätzlichen Verzeichnissen erkannt, obwohl einige Typen als Ausnahmen geladen werden.

Die folgenden Konfigurationstypen werden aus `--add-dir`-Verzeichnissen geladen:

| Konfiguration                                                           | Geladen aus `--add-dir`                                                                                                                                                       |
| :---------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Skills](/de/skills) in `.claude/skills/`                               | Ja, mit Live-Reload                                                                                                                                                           |
| Plugin-Einstellungen in `.claude/settings.json`                         | Nur `enabledPlugins` und `extraKnownMarketplaces`                                                                                                                             |
| [CLAUDE.md](/de/memory)-Dateien, `.claude/rules/` und `CLAUDE.local.md` | Nur wenn `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` gesetzt ist. `CLAUDE.local.md` erfordert zusätzlich die `local`-Einstellungsquelle, die standardmäßig aktiviert ist |

Subagents, Befehle und Ausgabestile werden aus dem aktuellen Arbeitsverzeichnis und seinen übergeordneten Verzeichnissen, Ihrem Benutzerverzeichnis unter `~/.claude/` und verwalteten Einstellungen erkannt. Hooks und andere `settings.json`-Schlüssel werden aus dem `.claude/`-Ordner des aktuellen Arbeitsverzeichnisses ohne Fallback für übergeordnete Verzeichnisse geladen, zusammen mit Ihren Benutzer-`~/.claude/settings.json` und verwalteten Einstellungen. Um diese Konfiguration über Projekte hinweg zu teilen, verwenden Sie einen dieser Ansätze:

* **Benutzergesteuerte Konfiguration**: Platzieren Sie Dateien in `~/.claude/agents/`, `~/.claude/output-styles/` oder `~/.claude/settings.json`, um sie in jedem Projekt verfügbar zu machen
* **Plugins**: Verpacken und verteilen Sie Konfiguration als [Plugin](/de/plugins), das Teams installieren können
* **Starten Sie aus dem Konfigurationsverzeichnis**: Führen Sie Claude Code aus dem Verzeichnis aus, das die `.claude/`-Konfiguration enthält, die Sie verwenden möchten

## Wie Berechtigungen mit Sandboxing interagieren

Berechtigungen und [Sandboxing](/de/sandboxing) sind komplementäre Sicherheitsebenen:

* **Berechtigungen** steuern, welche Werkzeuge Claude Code verwenden kann und auf welche Dateien oder Domänen es zugreifen kann. Sie gelten für alle Werkzeuge (Bash, Read, Edit, WebFetch, MCP und andere).
* **Sandboxing** bietet OS-Ebenen-Durchsetzung, die den Zugriff des Bash-Werkzeugs auf das Dateisystem und das Netzwerk einschränkt. Es gilt nur für Bash-Befehle und ihre untergeordneten Prozesse.

Verwenden Sie beide für Defense-in-Depth:

* Berechtigungs-Deny-Regeln blockieren Claude daran, überhaupt zu versuchen, auf eingeschränkte Ressourcen zuzugreifen
* Sandbox-Einschränkungen verhindern, dass Bash-Befehle Ressourcen außerhalb definierter Grenzen erreichen, selbst wenn eine Prompt-Injection Claude's Entscheidungsfindung umgeht
* Dateisystem-Einschränkungen in der Sandbox kombinieren die [`sandbox.filesystem`](/de/sandboxing)-Einstellungen mit Read- und Edit-Deny-Regeln; beide werden in die endgültige Sandbox-Grenze zusammengeführt
* Netzwerk-Einschränkungen kombinieren WebFetch-Berechtigungsregeln mit den `allowedDomains`- und `deniedDomains`-Listen der Sandbox

Wenn Sandboxing mit `autoAllowBashIfSandboxed: true` aktiviert ist, was die Standardeinstellung ist, laufen sandboxed Bash-Befehle ohne Aufforderung, selbst wenn Ihre Berechtigungen `ask: Bash(*)` enthalten. Die Sandbox-Grenze ersetzt die Pro-Befehl-Aufforderung. Explizite Deny-Regeln gelten weiterhin, und `rm`- oder `rmdir`-Befehle, die auf `/`, Ihr Home-Verzeichnis oder andere kritische Systempfade abzielen, lösen weiterhin eine Aufforderung aus. Siehe [Sandbox-Modi](/de/sandboxing#sandbox-modes), um dieses Verhalten zu ändern.

## Verwaltete Einstellungen

Für Organisationen, die eine zentralisierte Kontrolle über die Claude Code-Konfiguration benötigen, können Administratoren verwaltete Einstellungen bereitstellen, die nicht von Benutzer- oder Projekteinstellungen überschrieben werden können. Diese Richtlinieneinstellungen folgen dem gleichen Format wie reguläre Einstellungsdateien und können über MDM/OS-Ebenen-Richtlinien, verwaltete Einstellungsdateien oder [servergesteuerte Einstellungen](/de/server-managed-settings) bereitgestellt werden. Siehe [Einstellungsdateien](/de/settings#settings-files) für Bereitstellungsmechanismen und Dateispeicherorte.

### Nur verwaltete Einstellungen

Die folgenden Einstellungen sind nur in verwalteten Einstellungen wirksam. Das Platzieren in Benutzer- oder Projekteinstellungsdateien hat keine Auswirkung.

| Einstellung                                    | Beschreibung                                                                                                                                                                                                                                                                                        |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Zulassungsliste von Channel-Plugins, die Nachrichten pushen dürfen. Ersetzt die Standard-Anthropic-Zulassungsliste, wenn gesetzt. Erfordert `channelsEnabled: true`. Siehe [Einschränken Sie, welche Channel-Plugins ausgeführt werden können](/de/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Wenn `true`, werden nur verwaltete Hooks, SDK-Hooks und Hooks aus Plugins, die in verwalteten Einstellungen `enabledPlugins` erzwungen sind, geladen. Benutzer-, Projekt- und alle anderen Plugin-Hooks werden blockiert                                                                            |
| `allowManagedMcpServersOnly`                   | Wenn `true`, werden nur `allowedMcpServers` aus verwalteten Einstellungen berücksichtigt. `deniedMcpServers` wird immer noch aus allen Quellen zusammengeführt. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                             |
| `allowManagedPermissionRulesOnly`              | Wenn `true`, verhindert, dass Benutzer- und Projekteinstellungen `allow`-, `ask`- oder `deny`-Berechtigungsregeln definieren. Nur Regeln in verwalteten Einstellungen gelten                                                                                                                        |
| `blockedMarketplaces`                          | Blocklist von Marketplace-Quellen. Blockierte Quellen werden vor dem Download überprüft, sodass sie das Dateisystem nie berühren. Siehe [verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                          |
| `channelsEnabled`                              | Ermöglichen Sie [Channels](/de/channels) für die Organisation. Siehe [Enterprise-Kontrollen](/de/channels#enterprise-controls) für die Standardeinstellung bei jedem Plan                                                                                                                           |
| `forceRemoteSettingsRefresh`                   | Wenn `true`, blockiert CLI-Start, bis remote verwaltete Einstellungen aktuell abgerufen werden, und beendet sich, wenn der Abruf fehlschlägt. Siehe [Fail-Closed-Durchsetzung](/de/server-managed-settings#enforce-fail-closed-startup)                                                             |
| `pluginTrustMessage`                           | Benutzerdefinierte Nachricht, die der vor der Installation angezeigten Plugin-Vertrauenswarnung hinzugefügt wird                                                                                                                                                                                    |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Wenn `true`, werden nur `filesystem.allowRead`-Pfade aus verwalteten Einstellungen berücksichtigt. `denyRead` wird immer noch aus allen Quellen zusammengeführt                                                                                                                                     |
| `sandbox.network.allowManagedDomainsOnly`      | Wenn `true`, werden nur `allowedDomains` und `WebFetch(domain:...)`-Allow-Regeln aus verwalteten Einstellungen berücksichtigt. Nicht zulässige Domänen werden automatisch blockiert, ohne den Benutzer zu fragen. Verweigerte Domänen werden immer noch aus allen Quellen zusammengeführt           |
| `strictKnownMarketplaces`                      | Steuert, welche Plugin-Marketplace-Quellen Benutzer hinzufügen und Plugins installieren können. Siehe [verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                                            |
| `wslInheritsWindowsSettings`                   | Wenn `true` im Windows HKLM-Registrierungsschlüssel oder in `C:\Program Files\ClaudeCode\managed-settings.json`, liest WSL verwaltete Einstellungen aus der Windows-Richtlinienkette zusätzlich zu `/etc/claude-code`. Siehe [Einstellungsdateien](/de/settings#settings-files)                     |

`disableBypassPermissionsMode` wird normalerweise in verwalteten Einstellungen platziert, um Organisationsrichtlinien durchzusetzen, funktioniert aber aus jedem Bereich. Ein Benutzer kann es in seinen eigenen Einstellungen festlegen, um sich selbst aus dem Bypass-Modus auszusperren.

<Note>
  Bei Team- und Enterprise-Plänen aktiviert oder deaktiviert ein Administrator [Remote Control](/de/remote-control) und [Web-Sitzungen](/de/claude-code-on-the-web) organisationsweit in [Claude Code-Administratoreinstellungen](https://claude.ai/admin-settings/claude-code). Remote Control kann zusätzlich pro Gerät mit der verwalteten Einstellung [`disableRemoteControl`](/de/settings#available-settings) deaktiviert werden. Web-Sitzungen haben keinen verwalteten Einstellungsschlüssel pro Gerät.
</Note>

## Einstellungspriorität

Berechtigungsregeln folgen der gleichen [Einstellungspriorität](/de/settings#settings-precedence) wie alle anderen Claude Code-Einstellungen:

1. **Verwaltete Einstellungen**: können von keiner anderen Ebene überschrieben werden, einschließlich Befehlszeilenargumenten
2. **Befehlszeilenargumente**: temporäre Sitzungsüberschreibungen
3. **Lokale Projekteinstellungen** (`.claude/settings.local.json`)
4. **Gemeinsame Projekteinstellungen** (`.claude/settings.json`)
5. **Benutzereinstellungen** (`~/.claude/settings.json`)

Wenn ein Werkzeug auf einer beliebigen Ebene verweigert wird, kann keine andere Ebene es zulassen. Zum Beispiel kann eine verwaltete Einstellungs-Deny nicht durch `--allowedTools` überschrieben werden, und `--disallowedTools` kann Einschränkungen über das hinaus hinzufügen, was verwaltete Einstellungen definieren.

Embedding-Hosts können zusätzliche verwaltete Richtlinien über die SDK-Option `managedSettings` bereitstellen, wenn [`parentSettingsBehavior`](/de/settings#settings-precedence) auf `"merge"` gesetzt ist; Embedder-Werte können die Richtlinie verschärfen, aber nicht lockern.

Wenn eine Berechtigung in Benutzereinstellungen zulässig ist, aber in Projekteinstellungen verweigert wird, hat die Projekteinstellung Vorrang und die Berechtigung wird blockiert.

## Beispielkonfigurationen

Dieses [Repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) enthält Starter-Einstellungskonfigurationen für häufige Bereitstellungsszenarien. Verwenden Sie diese als Ausgangspunkte und passen Sie sie an Ihre Anforderungen an.

## Siehe auch

* [Einstellungen](/de/settings): vollständige Konfigurationsreferenz einschließlich der Berechtigungseinstellungstabelle
* [Konfigurieren Sie den Auto-Mode](/de/auto-mode-config): Teilen Sie dem Auto-Mode-Klassifizierer mit, welche Infrastruktur Ihre Organisation vertraut
* [Sandboxing](/de/sandboxing): OS-Ebenen-Dateisystem- und Netzwerkisolation für Bash-Befehle
* [Authentifizierung](/de/authentication): Richten Sie Benutzerzugriff auf Claude Code ein
* [Sicherheit](/de/security): Sicherheitsvorkehrungen und Best Practices
* [Hooks](/de/hooks-guide): Automatisieren Sie Workflows und erweitern Sie die Berechtigungsevaluierung
