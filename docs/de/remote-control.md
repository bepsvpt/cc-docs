> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Lokale Sitzungen von jedem Gerät aus mit Remote Control fortsetzen

> Setzen Sie eine lokale Claude Code-Sitzung von Ihrem Telefon, Tablet oder einem beliebigen Browser aus mit Remote Control fort. Funktioniert mit claude.ai/code und der Claude-Mobile-App.

<Note>
  Remote Control ist in allen Plänen verfügbar. Team- und Enterprise-Administratoren müssen Claude Code zunächst in den [Admin-Einstellungen](https://claude.ai/admin-settings/claude-code) aktivieren.
</Note>

Remote Control verbindet [claude.ai/code](https://claude.ai/code) oder die Claude-App für [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) und [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) mit einer Claude Code-Sitzung, die auf Ihrem Computer ausgeführt wird. Starten Sie eine Aufgabe an Ihrem Schreibtisch und setzen Sie sie dann von Ihrem Telefon auf der Couch oder einem Browser auf einem anderen Computer fort.

Wenn Sie eine Remote Control-Sitzung auf Ihrem Computer starten, wird Claude die ganze Zeit lokal ausgeführt, sodass nichts in die Cloud verschoben wird. Mit Remote Control können Sie:

* **Ihre vollständige lokale Umgebung remote nutzen**: Ihr Dateisystem, [MCP servers](/de/mcp), Tools und Projektkonfiguration bleiben verfügbar
* **Von beiden Oberflächen gleichzeitig arbeiten**: Das Gespräch bleibt auf allen verbundenen Geräten synchronisiert, sodass Sie Nachrichten von Ihrem Terminal, Browser und Telefon austauschbar senden können
* **Unterbrechungen überstehen**: Wenn Ihr Laptop in den Ruhezustand wechselt oder Ihr Netzwerk ausfällt, wird die Sitzung automatisch wiederhergestellt, wenn Ihr Computer wieder online ist

Im Gegensatz zu [Claude Code im Web](/de/claude-code-on-the-web), das auf Cloud-Infrastruktur ausgeführt wird, werden Remote Control-Sitzungen direkt auf Ihrem Computer ausgeführt und interagieren mit Ihrem lokalen Dateisystem. Die Web- und Mobile-Schnittstellen sind nur ein Fenster in diese lokale Sitzung.

<Note>
  Remote Control erfordert Claude Code v2.1.51 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

Diese Seite behandelt die Einrichtung, das Starten und Verbinden mit Sitzungen sowie den Vergleich von Remote Control mit Claude Code im Web.

## Anforderungen

Bevor Sie Remote Control verwenden, bestätigen Sie, dass Ihre Umgebung diese Bedingungen erfüllt:

* **Abonnement**: verfügbar in Pro-, Max-, Team- und Enterprise-Plänen. Team- und Enterprise-Administratoren müssen Claude Code zunächst in den [Admin-Einstellungen](https://claude.ai/admin-settings/claude-code) aktivieren. API-Schlüssel werden nicht unterstützt.
* **Authentifizierung**: Führen Sie `claude` aus und verwenden Sie `/login`, um sich über claude.ai anzumelden, falls Sie dies noch nicht getan haben.
* **Workspace-Vertrauen**: Führen Sie `claude` mindestens einmal in Ihrem Projektverzeichnis aus, um den Workspace-Vertrauensdialog zu akzeptieren.

## Starten Sie eine Remote Control-Sitzung

Sie können einen dedizierten Remote Control-Server starten, eine interaktive Sitzung mit aktiviertem Remote Control starten oder eine bereits laufende Sitzung verbinden.

<Tabs>
  <Tab title="Server-Modus">
    Navigieren Sie zu Ihrem Projektverzeichnis und führen Sie aus:

    ```bash  theme={null}
    claude remote-control
    ```

    Der Prozess läuft weiterhin in Ihrem Terminal im Server-Modus und wartet auf Remote-Verbindungen. Er zeigt eine Sitzungs-URL an, die Sie zum [Verbinden von einem anderen Gerät](#connect-from-another-device) verwenden können, und Sie können die Leertaste drücken, um einen QR-Code für schnellen Zugriff von Ihrem Telefon anzuzeigen. Während eine Remote-Sitzung aktiv ist, zeigt das Terminal den Verbindungsstatus und die Tool-Aktivität an.

    Verfügbare Flags:

    | Flag                         | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
    | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | `--name "My Project"`        | Legen Sie einen benutzerdefinierten Sitzungstitel fest, der in der Sitzungsliste unter claude.ai/code sichtbar ist.                                                                                                                                                                                                                                                                                                                                          |
    | `--spawn <mode>`             | Wie gleichzeitige Sitzungen erstellt werden. Drücken Sie `w` zur Laufzeit zum Umschalten.<br />• `same-dir` (Standard): Alle Sitzungen teilen sich das aktuelle Arbeitsverzeichnis, sodass sie in Konflikt geraten können, wenn dieselben Dateien bearbeitet werden.<br />• `worktree`: Jede On-Demand-Sitzung erhält ihren eigenen [git worktree](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Erfordert ein Git-Repository. |
    | `--capacity <N>`             | Maximale Anzahl gleichzeitiger Sitzungen. Standard ist 32.                                                                                                                                                                                                                                                                                                                                                                                                   |
    | `--verbose`                  | Zeigen Sie detaillierte Verbindungs- und Sitzungsprotokolle an.                                                                                                                                                                                                                                                                                                                                                                                              |
    | `--sandbox` / `--no-sandbox` | Aktivieren oder deaktivieren Sie [sandboxing](/de/sandboxing) für Dateisystem- und Netzwerkisolation. Standardmäßig deaktiviert.                                                                                                                                                                                                                                                                                                                             |
  </Tab>

  <Tab title="Interaktive Sitzung">
    Um eine normale interaktive Claude Code-Sitzung mit aktiviertem Remote Control zu starten, verwenden Sie das Flag `--remote-control` (oder `--rc`):

    ```bash  theme={null}
    claude --remote-control
    ```

    Geben Sie optional einen Namen für die Sitzung an:

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    Dies gibt Ihnen eine vollständige interaktive Sitzung in Ihrem Terminal, die Sie auch von claude.ai oder der Claude-App aus steuern können. Im Gegensatz zu `claude remote-control` (Server-Modus) können Sie lokal Nachrichten eingeben, während die Sitzung auch remote verfügbar ist.
  </Tab>

  <Tab title="Aus einer bestehenden Sitzung">
    Wenn Sie sich bereits in einer Claude Code-Sitzung befinden und diese remote fortsetzen möchten, verwenden Sie den Befehl `/remote-control` (oder `/rc`):

    ```text  theme={null}
    /remote-control
    ```

    Übergeben Sie einen Namen als Argument, um einen benutzerdefinierten Sitzungstitel festzulegen:

    ```text  theme={null}
    /remote-control My Project
    ```

    Dies startet eine Remote Control-Sitzung, die Ihren aktuellen Gesprächsverlauf überträgt und eine Sitzungs-URL und einen QR-Code anzeigt, die Sie zum [Verbinden von einem anderen Gerät](#connect-from-another-device) verwenden können. Die Flags `--verbose`, `--sandbox` und `--no-sandbox` sind mit diesem Befehl nicht verfügbar.
  </Tab>
</Tabs>

### Verbinden Sie sich von einem anderen Gerät

Sobald eine Remote Control-Sitzung aktiv ist, haben Sie mehrere Möglichkeiten, sich von einem anderen Gerät aus zu verbinden:

* **Öffnen Sie die Sitzungs-URL** in einem beliebigen Browser, um direkt zur Sitzung auf [claude.ai/code](https://claude.ai/code) zu gehen. Sowohl `claude remote-control` als auch `/remote-control` zeigen diese URL im Terminal an.
* **Scannen Sie den QR-Code**, der neben der Sitzungs-URL angezeigt wird, um ihn direkt in der Claude-App zu öffnen. Mit `claude remote-control` drücken Sie die Leertaste, um die QR-Code-Anzeige umzuschalten.
* **Öffnen Sie [claude.ai/code](https://claude.ai/code) oder die Claude-App** und finden Sie die Sitzung nach Name in der Sitzungsliste. Remote Control-Sitzungen zeigen ein Computersymbol mit einem grünen Statusindikator an, wenn sie online sind.

Die Remote-Sitzung erhält ihren Namen vom Argument `--name` (oder dem Namen, der an `/remote-control` übergeben wird), Ihrer letzten Nachricht, Ihrem Wert `/rename` oder 'Remote Control-Sitzung", wenn es keinen Gesprächsverlauf gibt. Wenn die Umgebung bereits eine aktive Sitzung hat, werden Sie gefragt, ob Sie diese fortsetzen oder eine neue starten möchten.

Wenn Sie die Claude-App noch nicht haben, verwenden Sie den Befehl `/mobile` in Claude Code, um einen Download-QR-Code für [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) oder [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) anzuzeigen.

### Aktivieren Sie Remote Control für alle Sitzungen

Standardmäßig wird Remote Control nur aktiviert, wenn Sie explizit `claude remote-control`, `claude --remote-control` oder `/remote-control` ausführen. Um es automatisch für jede interaktive Sitzung zu aktivieren, führen Sie `/config` in Claude Code aus und setzen Sie **Enable Remote Control for all sessions** auf `true`. Setzen Sie es auf `false` zurück, um es zu deaktivieren.

Mit dieser Einstellung registriert jeder interaktive Claude Code-Prozess eine Remote-Sitzung. Wenn Sie mehrere Instanzen ausführen, erhält jede ihre eigene Umgebung und Sitzung. Um mehrere gleichzeitige Sitzungen aus einem einzelnen Prozess auszuführen, verwenden Sie stattdessen den Server-Modus mit `--spawn`.

## Verbindung und Sicherheit

Ihre lokale Claude Code-Sitzung stellt nur ausgehende HTTPS-Anfragen und öffnet niemals eingehende Ports auf Ihrem Computer. Wenn Sie Remote Control starten, registriert es sich bei der Anthropic-API und fragt nach Arbeit ab. Wenn Sie sich von einem anderen Gerät aus verbinden, leitet der Server Nachrichten zwischen dem Web- oder Mobile-Client und Ihrer lokalen Sitzung über eine Streaming-Verbindung weiter.

Der gesamte Datenverkehr verläuft über die Anthropic-API über TLS, die gleiche Transportsicherheit wie jede Claude Code-Sitzung. Die Verbindung verwendet mehrere kurzlebige Anmeldeinformationen, die jeweils auf einen einzelnen Zweck beschränkt sind und unabhängig ablaufen.

## Remote Control vs. Claude Code im Web

Remote Control und [Claude Code im Web](/de/claude-code-on-the-web) verwenden beide die Schnittstelle claude.ai/code. Der Hauptunterschied liegt darin, wo die Sitzung ausgeführt wird: Remote Control wird auf Ihrem Computer ausgeführt, sodass Ihre lokalen MCP servers, Tools und Projektkonfiguration verfügbar bleiben. Claude Code im Web wird in von Anthropic verwalteter Cloud-Infrastruktur ausgeführt.

Verwenden Sie Remote Control, wenn Sie sich mitten in lokaler Arbeit befinden und von einem anderen Gerät aus weitermachen möchten. Verwenden Sie Claude Code im Web, wenn Sie eine Aufgabe ohne lokale Einrichtung starten möchten, an einem Repository arbeiten, das Sie nicht geklont haben, oder mehrere Aufgaben parallel ausführen möchten.

## Einschränkungen

* **Eine Remote-Sitzung pro interaktivem Prozess**: Außerhalb des Server-Modus unterstützt jede Claude Code-Instanz jeweils eine Remote-Sitzung. Verwenden Sie den Server-Modus mit `--spawn`, um mehrere gleichzeitige Sitzungen aus einem einzelnen Prozess auszuführen.
* **Terminal muss offen bleiben**: Remote Control wird als lokaler Prozess ausgeführt. Wenn Sie das Terminal schließen oder den `claude`-Prozess beenden, endet die Sitzung. Führen Sie `claude remote-control` erneut aus, um eine neue zu starten.
* **Längerer Netzwerkausfall**: Wenn Ihr Computer aktiv ist, aber länger als etwa 10 Minuten das Netzwerk nicht erreichen kann, läuft die Sitzung ab und der Prozess wird beendet. Führen Sie `claude remote-control` erneut aus, um eine neue Sitzung zu starten.

## Verwandte Ressourcen

* [Claude Code im Web](/de/claude-code-on-the-web): Führen Sie Sitzungen in von Anthropic verwalteten Cloud-Umgebungen aus, anstatt auf Ihrem Computer
* [Authentifizierung](/de/authentication): Richten Sie `/login` ein und verwalten Sie Anmeldeinformationen für claude.ai
* [CLI-Referenz](/de/cli-reference): Vollständige Liste von Flags und Befehlen einschließlich `claude remote-control`
* [Sicherheit](/de/security): Wie Remote Control-Sitzungen in das Claude Code-Sicherheitsmodell passen
* [Datennutzung](/de/data-usage): Welche Daten während lokaler und Remote-Sitzungen durch die Anthropic-API fließen
