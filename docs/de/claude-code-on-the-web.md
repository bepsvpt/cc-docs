> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code im Web verwenden

> Konfigurieren Sie Cloud-Umgebungen, Setup-Skripte, Netzwerkzugriff und Docker in Anthropics Sandbox. Verschieben Sie Sitzungen zwischen Web und Terminal mit `--remote` und `--teleport`.

<Note>
  Claude Code im Web befindet sich in der Forschungsvorschau für Pro-, Max- und Team-Benutzer sowie für Enterprise-Benutzer mit Premium-Sitzen oder Chat + Claude Code-Sitzen.
</Note>

Claude Code im Web führt Aufgaben auf von Anthropic verwalteter Cloud-Infrastruktur unter [claude.ai/code](https://claude.ai/code) aus. Sitzungen bleiben bestehen, auch wenn Sie Ihren Browser schließen, und Sie können sie über die Claude Mobile-App überwachen.

<Tip>
  Neu bei Claude Code im Web? Beginnen Sie mit [Erste Schritte](/de/web-quickstart), um Ihr GitHub-Konto zu verbinden und Ihre erste Aufgabe einzureichen.
</Tip>

Diese Seite behandelt:

* [GitHub-Authentifizierungsoptionen](#github-authentication-options): zwei Möglichkeiten, GitHub zu verbinden
* [Die Cloud-Umgebung](#the-cloud-environment): welche Konfiguration übertragen wird, welche Tools installiert sind und wie Umgebungen konfiguriert werden
* [Setup-Skripte](#setup-scripts) und Abhängigkeitsverwaltung
* [Netzwerkzugriff](#network-access): Ebenen, Proxys und die Standard-Allowlist
* [Aufgaben zwischen Web und Terminal verschieben](#move-tasks-between-web-and-terminal) mit `--remote` und `--teleport`
* [Mit Sitzungen arbeiten](#work-with-sessions): Überprüfung, Freigabe, Archivierung, Löschung
* [Auto-fix Pull Requests](#auto-fix-pull-requests): automatische Reaktion auf CI-Fehler und Review-Kommentare
* [Sicherheit und Isolation](#security-and-isolation): wie Sitzungen isoliert sind
* [Einschränkungen](#limitations): Ratenlimits und Plattformbeschränkungen

## GitHub-Authentifizierungsoptionen

Cloud-Sitzungen benötigen Zugriff auf Ihre GitHub-Repositories, um Code zu klonen und Branches zu pushen. Sie können Zugriff auf zwei Arten gewähren:

| Methode          | Funktionsweise                                                                                                                                                                     | Am besten für                                              |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------- |
| **GitHub App**   | Installieren Sie die Claude GitHub App auf bestimmten Repositories während des [Web-Onboardings](/de/web-quickstart). Der Zugriff ist pro Repository begrenzt.                     | Teams, die explizite Pro-Repository-Autorisierung wünschen |
| **`/web-setup`** | Führen Sie `/web-setup` in Ihrem Terminal aus, um Ihr lokales `gh` CLI-Token mit Ihrem Claude-Konto zu synchronisieren. Der Zugriff entspricht dem, was Ihr `gh`-Token sehen kann. | Einzelne Entwickler, die bereits `gh` verwenden            |

Beide Methoden funktionieren. [`/schedule`](/de/routines) überprüft auf beide Formen des Zugriffs und fordert Sie auf, `/web-setup` auszuführen, wenn keines konfiguriert ist. Siehe [Vom Terminal verbinden](/de/web-quickstart#connect-from-your-terminal) für die `/web-setup`-Anleitung.

Die GitHub App ist erforderlich für [Auto-fix](#auto-fix-pull-requests), das die App verwendet, um PR-Webhooks zu empfangen. Wenn Sie sich mit `/web-setup` verbinden und später Auto-fix möchten, installieren Sie die App auf diesen Repositories.

Team- und Enterprise-Administratoren können `/web-setup` mit dem Quick web setup-Umschalter unter [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) deaktivieren.

<Note>
  Organisationen mit aktivierter [Zero Data Retention](/de/zero-data-retention) können `/web-setup` oder andere Cloud-Sitzungsfunktionen nicht verwenden.
</Note>

## Die Cloud-Umgebung

Jede Sitzung wird in einer frischen, von Anthropic verwalteten VM mit Ihrem geklonten Repository ausgeführt. Dieser Abschnitt behandelt, was verfügbar ist, wenn eine Sitzung startet, und wie Sie sie anpassen können.

### Was in Cloud-Sitzungen verfügbar ist

Cloud-Sitzungen starten von einem frischen Klon Ihres Repositories. Alles, was zum Repo committed ist, ist verfügbar. Alles, was Sie nur auf Ihrem eigenen Computer installiert oder konfiguriert haben, ist nicht verfügbar.

|                                                                      | Verfügbar in Cloud-Sitzungen | Warum                                                                                                                                                                  |
| :------------------------------------------------------------------- | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ihr Repo's `CLAUDE.md`                                               | Ja                           | Teil des Klons                                                                                                                                                         |
| Ihr Repo's `.claude/settings.json` Hooks                             | Ja                           | Teil des Klons                                                                                                                                                         |
| Ihr Repo's `.mcp.json` MCP-Server                                    | Ja                           | Teil des Klons                                                                                                                                                         |
| Ihr Repo's `.claude/rules/`                                          | Ja                           | Teil des Klons                                                                                                                                                         |
| Ihr Repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/` | Ja                           | Teil des Klons                                                                                                                                                         |
| In `.claude/settings.json` deklarierte Plugins                       | Ja                           | Installiert beim Sitzungsstart vom [Marketplace](/de/plugin-marketplaces), den Sie deklariert haben. Erfordert Netzwerkzugriff, um die Marketplace-Quelle zu erreichen |
| Ihr Benutzer `~/.claude/CLAUDE.md`                                   | Nein                         | Lebt auf Ihrem Computer, nicht im Repo                                                                                                                                 |
| Plugins, die nur in Ihren Benutzereinstellungen aktiviert sind       | Nein                         | Benutzer-scoped `enabledPlugins` lebt in `~/.claude/settings.json`. Deklarieren Sie sie stattdessen in der `.claude/settings.json` des Repos                           |
| MCP-Server, die Sie mit `claude mcp add` hinzugefügt haben           | Nein                         | Diese schreiben in Ihre lokale Benutzerkonfiguration, nicht ins Repo. Deklarieren Sie den Server stattdessen in [`.mcp.json`](/de/mcp#project-scope)                   |
| Statische API-Token und Anmeldedaten                                 | Nein                         | Es existiert noch kein dedizierter Secrets-Store. Siehe unten                                                                                                          |
| Interaktive Authentifizierung wie AWS SSO                            | Nein                         | Nicht unterstützt. SSO erfordert browserbasierte Anmeldung, die nicht in einer Cloud-Sitzung ausgeführt werden kann                                                    |

Um Konfiguration in Cloud-Sitzungen verfügbar zu machen, committen Sie sie ins Repo. Ein dedizierter Secrets-Store ist noch nicht verfügbar. Sowohl Umgebungsvariablen als auch Setup-Skripte werden in der Umgebungskonfiguration gespeichert, sichtbar für jeden, der diese Umgebung bearbeiten kann. Wenn Sie Secrets in einer Cloud-Sitzung benötigen, fügen Sie sie als Umgebungsvariablen mit dieser Sichtbarkeit im Hinterkopf hinzu.

### Installierte Tools

Cloud-Sitzungen werden mit gängigen Sprachlaufzeiten, Build-Tools und Datenbanken vorinstalliert geliefert. Die folgende Tabelle fasst zusammen, was nach Kategorie enthalten ist.

| Kategorie       | Enthalten                                                                         |
| :-------------- | :-------------------------------------------------------------------------------- |
| **Python**      | Python 3.x mit pip, poetry, uv, black, mypy, pytest, ruff                         |
| **Node.js**     | 20, 21 und 22 über nvm, mit npm, yarn, pnpm, bun¹, eslint, prettier, chromedriver |
| **Ruby**        | 3.1, 3.2, 3.3 mit gem, bundler, rbenv                                             |
| **PHP**         | 8.4 mit Composer                                                                  |
| **Java**        | OpenJDK 21 mit Maven und Gradle                                                   |
| **Go**          | neueste stabile Version mit Modulunterstützung                                    |
| **Rust**        | rustc und cargo                                                                   |
| **C/C++**       | GCC, Clang, cmake, ninja, conan                                                   |
| **Docker**      | docker, dockerd, docker compose                                                   |
| **Datenbanken** | PostgreSQL 16, Redis 7.0                                                          |
| **Utilities**   | git, jq, yq, ripgrep, tmux, vim, nano                                             |

¹ Bun ist installiert, hat aber bekannte [Proxy-Kompatibilitätsprobleme](#install-dependencies-with-a-sessionstart-hook) beim Paketabruf.

Für genaue Versionen bitten Sie Claude, `check-tools` in einer Cloud-Sitzung auszuführen. Dieser Befehl existiert nur in Cloud-Sitzungen.

### Mit GitHub-Issues und Pull Requests arbeiten

Cloud-Sitzungen enthalten integrierte GitHub-Tools, mit denen Claude Issues lesen, Pull Requests auflisten, Diffs abrufen und Kommentare posten kann, ohne Setup. Diese Tools authentifizieren sich über den [GitHub-Proxy](#github-proxy) mit der Methode, die Sie unter [GitHub-Authentifizierungsoptionen](#github-authentication-options) konfiguriert haben, sodass Ihr Token niemals in den Container gelangt.

Die `gh` CLI ist nicht vorinstalliert. Wenn Sie einen `gh`-Befehl benötigen, den die integrierten Tools nicht abdecken, wie `gh release` oder `gh workflow run`, installieren und authentifizieren Sie ihn selbst:

<Steps>
  <Step title="Installieren Sie gh in Ihrem Setup-Skript">
    Fügen Sie `apt update && apt install -y gh` zu Ihrem [Setup-Skript](#setup-scripts) hinzu.
  </Step>

  <Step title="Stellen Sie ein Token bereit">
    Fügen Sie eine `GH_TOKEN`-Umgebungsvariable zu Ihren [Umgebungseinstellungen](#configure-your-environment) mit einem GitHub Personal Access Token hinzu. `gh` liest `GH_TOKEN` automatisch, daher ist kein `gh auth login`-Schritt erforderlich.
  </Step>
</Steps>

### Verknüpfen Sie Artifacts zurück zur Sitzung

Jede Cloud-Sitzung hat eine Transkript-URL auf claude.ai, und die Sitzung kann ihre eigene ID aus der Umgebungsvariablen `CLAUDE_CODE_REMOTE_SESSION_ID` lesen. Verwenden Sie dies, um einen nachverfolgbaren Link in PR-Bodies, Commit-Nachrichten, Slack-Posts oder generierten Berichten zu platzieren, damit ein Reviewer den Lauf öffnen kann, der sie produziert hat.

Bitten Sie Claude, den Link aus der Umgebungsvariablen zu konstruieren. Der folgende Befehl gibt die URL aus:

```bash theme={null}
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

### Tests ausführen, Services starten und Pakete hinzufügen

Claude führt Tests als Teil der Arbeit an einer Aufgabe aus. Bitten Sie darum in Ihrem Prompt, wie „fix the failing tests in `tests/`" oder „run pytest after each change." Test-Runner wie pytest, jest und cargo test funktionieren sofort, da sie vorinstalliert sind.

PostgreSQL und Redis sind vorinstalliert, aber nicht standardmäßig ausgeführt. Bitten Sie Claude, jeden während der Sitzung zu starten:

```bash theme={null}
service postgresql start
```

```bash theme={null}
service redis-server start
```

Docker ist für die Ausführung containerisierter Services verfügbar. Bitten Sie Claude, `docker compose up` auszuführen, um die Services Ihres Projekts zu starten. Der Netzwerkzugriff zum Abrufen von Images folgt der [Zugriffsstufe](#access-levels) Ihrer Umgebung, und die [Vertrauenswürdigen Standards](#default-allowed-domains) enthalten Docker Hub und andere gängige Registries.

Wenn Ihre Images groß oder langsam zum Abrufen sind, fügen Sie `docker compose pull` oder `docker compose build` zu Ihrem [Setup-Skript](#setup-scripts) hinzu. Die abgerufenen Images werden in der [gecachten Umgebung](#environment-caching) gespeichert, daher hat jede neue Sitzung sie auf der Festplatte. Der Cache speichert nur Dateien, keine laufenden Prozesse, daher startet Claude die Container immer noch jede Sitzung.

Um Pakete hinzuzufügen, die nicht vorinstalliert sind, verwenden Sie ein [Setup-Skript](#setup-scripts). Die Ausgabe des Skripts wird [gecacht](#environment-caching), daher sind Pakete, die Sie dort installieren, am Anfang jeder Sitzung verfügbar, ohne jedes Mal neu installiert zu werden. Sie können Claude auch bitten, Pakete während der Sitzung zu installieren, aber diese Installationen bleiben nicht über Sitzungen hinweg bestehen.

### Ressourcenlimits

Cloud-Sitzungen werden mit ungefähren Ressourcengrenzen ausgeführt, die sich im Laufe der Zeit ändern können:

* 4 vCPUs
* 16 GB RAM
* 30 GB Festplatte

Aufgaben, die erheblich mehr Speicher erfordern, wie große Build-Jobs oder speicherintensive Tests, können fehlschlagen oder beendet werden. Für Workloads jenseits dieser Limits verwenden Sie [Remote Control](/de/remote-control), um Claude Code auf Ihrer eigenen Hardware auszuführen.

### Konfigurieren Sie Ihre Umgebung

Umgebungen steuern [Netzwerkzugriff](#network-access), Umgebungsvariablen und das [Setup-Skript](#setup-scripts), das vor einer Sitzung ausgeführt wird. Siehe [Installierte Tools](#installed-tools) für das, was ohne Konfiguration verfügbar ist. Sie können Umgebungen über die Web-Oberfläche oder das Terminal verwalten:

| Aktion                            | Wie                                                                                                                                                                                                                                                                   |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Umgebung hinzufügen               | Wählen Sie die aktuelle Umgebung, um die Auswahl zu öffnen, dann wählen Sie **Umgebung hinzufügen**. Der Dialog enthält Name, Netzwerkzugriffsstufe, Umgebungsvariablen und Setup-Skript.                                                                             |
| Umgebung bearbeiten               | Wählen Sie das Einstellungssymbol rechts neben dem Umgebungsnamen.                                                                                                                                                                                                    |
| Umgebung archivieren              | Öffnen Sie die Umgebung zum Bearbeiten und wählen Sie **Archivieren**. Archivierte Umgebungen sind in der Auswahl ausgeblendet, aber vorhandene Sitzungen werden weiterhin ausgeführt.                                                                                |
| Standard für `--remote` festlegen | Führen Sie `/remote-env` in Ihrem Terminal aus. Wenn Sie eine einzelne Umgebung haben, zeigt dieser Befehl Ihre aktuelle Konfiguration. `/remote-env` wählt nur den Standard; fügen Sie Umgebungen über die Web-Oberfläche hinzu, bearbeiten und archivieren Sie sie. |

Umgebungsvariablen verwenden das `.env`-Format mit einem `KEY=value`-Paar pro Zeile. Wickeln Sie Werte nicht in Anführungszeichen ein, da Anführungszeichen als Teil des Werts gespeichert werden.

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

## Setup-Skripte

Ein Setup-Skript ist ein Bash-Skript, das ausgeführt wird, wenn eine neue Cloud-Sitzung startet, bevor Claude Code startet. Verwenden Sie Setup-Skripte, um Abhängigkeiten zu installieren, Tools zu konfigurieren oder alles zu holen, das die Sitzung benötigt und nicht vorinstalliert ist.

Skripte werden als Root auf Ubuntu 24.04 ausgeführt, daher funktionieren `apt install` und die meisten Sprachpaketmanager.

Um ein Setup-Skript hinzuzufügen, öffnen Sie den Dialog Umgebungseinstellungen und geben Sie Ihr Skript in das Feld **Setup-Skript** ein.

Dieses Beispiel installiert die `gh` CLI, die nicht vorinstalliert ist:

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Wenn das Skript mit einem Nicht-Null-Wert beendet wird, schlägt die Sitzung fehl zu starten. Fügen Sie `|| true` an nicht kritische Befehle an, um zu vermeiden, dass die Sitzung bei einem fehlerhaften Install blockiert wird.

<Note>
  Setup-Skripte, die Pakete installieren, benötigen Netzwerkzugriff, um Registries zu erreichen. Der Standard-**Trusted**-Netzwerkzugriff ermöglicht Verbindungen zu [gängigen Paketregistries](#default-allowed-domains), einschließlich npm, PyPI, RubyGems und crates.io. Skripte schlagen fehl, Pakete zu installieren, wenn Ihre Umgebung **None**-Netzwerkzugriff verwendet.
</Note>

### Umgebungs-Caching

Das Setup-Skript wird beim ersten Starten einer Sitzung in einer Umgebung ausgeführt. Nach Abschluss erstellt Anthropic einen Snapshot des Dateisystems und verwendet diesen Snapshot als Ausgangspunkt für spätere Sitzungen. Neue Sitzungen starten mit Ihren Abhängigkeiten, Tools und Docker-Images bereits auf der Festplatte, und der Setup-Skript-Schritt wird übersprungen. Dies hält den Start schnell, auch wenn das Skript große Toolchains installiert oder Container-Images abruft.

Der Cache erfasst Dateien, keine laufenden Prozesse. Alles, das das Setup-Skript auf die Festplatte schreibt, wird übertragen. Services oder Container, die es startet, nicht, daher starten Sie diese pro Sitzung, indem Sie Claude bitten oder einen [SessionStart-Hook](#setup-scripts-vs-sessionstart-hooks) verwenden.

Das Setup-Skript wird erneut ausgeführt, um den Cache neu zu erstellen, wenn Sie das Setup-Skript der Umgebung oder die zulässigen Netzwerk-Hosts ändern, und wenn der Cache nach ungefähr sieben Tagen abläuft. Das Fortsetzen einer vorhandenen Sitzung führt das Setup-Skript niemals erneut aus.

Sie müssen Caching nicht aktivieren oder Snapshots selbst verwalten.

### Setup-Skripte vs. SessionStart-Hooks

Verwenden Sie ein Setup-Skript, um Dinge zu installieren, die die Cloud benötigt, aber Ihr Laptop bereits hat, wie eine Sprachlaufzeit oder ein CLI-Tool. Verwenden Sie einen [SessionStart-Hook](/de/hooks#sessionstart) für Projekt-Setup, das überall ausgeführt werden sollte, Cloud und lokal, wie `npm install`.

Beide werden am Anfang einer Sitzung ausgeführt, aber sie gehören an verschiedene Orte:

|                 | Setup-Skripte                                                                                 | SessionStart-Hooks                                                       |
| --------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Angehängt an    | Die Cloud-Umgebung                                                                            | Ihr Repository                                                           |
| Konfiguriert in | Cloud-Umgebungs-UI                                                                            | `.claude/settings.json` in Ihrem Repo                                    |
| Wird ausgeführt | Bevor Claude Code startet, wenn keine [gecachte Umgebung](#environment-caching) verfügbar ist | Nach Claude Code startet, bei jeder Sitzung einschließlich fortgesetzter |
| Umfang          | Nur Cloud-Umgebungen                                                                          | Sowohl lokal als auch Cloud                                              |

SessionStart-Hooks können auch in Ihrer Benutzer-Level-Datei `~/.claude/settings.json` lokal definiert werden, aber Benutzer-Level-Einstellungen werden nicht zu Cloud-Sitzungen übertragen. In der Cloud werden nur Hooks ausgeführt, die zum Repo committed sind.

### Abhängigkeiten mit einem SessionStart-Hook installieren

Um Abhängigkeiten nur in Cloud-Sitzungen zu installieren, fügen Sie einen SessionStart-Hook zu Ihrer Repo's `.claude/settings.json` hinzu:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Erstellen Sie das Skript unter `scripts/install_pkgs.sh` und machen Sie es ausführbar mit `chmod +x`. Die Umgebungsvariable `CLAUDE_CODE_REMOTE` ist in Cloud-Sitzungen auf `true` gesetzt, daher können Sie sie verwenden, um die lokale Ausführung zu überspringen:

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

SessionStart-Hooks haben einige Einschränkungen in Cloud-Sitzungen:

* **Keine Cloud-Only-Scoping**: Hooks werden in lokalen und Cloud-Sitzungen ausgeführt. Um die lokale Ausführung zu überspringen, überprüfen Sie die Umgebungsvariable `CLAUDE_CODE_REMOTE` wie oben gezeigt.
* **Erfordert Netzwerkzugriff**: Installationsbefehle benötigen Zugriff auf Paketregistries. Wenn Ihre Umgebung **None**-Netzwerkzugriff verwendet, schlagen diese Hooks fehl. Die [Standard-Allowlist](#default-allowed-domains) unter **Trusted** deckt npm, PyPI, RubyGems und crates.io ab.
* **Proxy-Kompatibilität**: Der gesamte ausgehende Datenverkehr läuft durch einen [Sicherheits-Proxy](#security-proxy). Einige Paketmanager funktionieren mit diesem Proxy nicht korrekt. Bun ist ein bekanntes Beispiel.
* **Fügt Startup-Latenz hinzu**: Hooks werden jedes Mal ausgeführt, wenn eine Sitzung startet oder fortgesetzt wird, im Gegensatz zu Setup-Skripten, die von [Umgebungs-Caching](#environment-caching) profitieren. Halten Sie Installationsskripte schnell, indem Sie überprüfen, ob Abhängigkeiten bereits vorhanden sind, bevor Sie sie neu installieren.

Um Umgebungsvariablen für nachfolgende Bash-Befehle beizubehalten, schreiben Sie in die Datei unter `$CLAUDE_ENV_FILE`. Siehe [SessionStart-Hooks](/de/hooks#sessionstart) für Details.

Das Ersetzen des Basis-Images durch Ihr eigenes Docker-Image wird noch nicht unterstützt. Verwenden Sie ein Setup-Skript, um zu installieren, was Sie auf dem [bereitgestellten Image](#installed-tools) benötigen, oder führen Sie Ihr Image als Container neben Claude mit `docker compose` aus.

## Netzwerkzugriff

Der Netzwerkzugriff steuert ausgehende Verbindungen aus der Cloud-Umgebung. Jede Umgebung gibt eine Zugriffsstufe an, und Sie können sie mit benutzerdefinierten zulässigen Domains erweitern. Der Standard ist **Trusted**, das Paketregistries und andere [Allowlist-Domains](#default-allowed-domains) ermöglicht.

### Zugriffsstufen

Wählen Sie eine Zugriffsstufe, wenn Sie eine Umgebung erstellen oder bearbeiten:

| Stufe       | Ausgehende Verbindungen                                                                |
| :---------- | :------------------------------------------------------------------------------------- |
| **None**    | Kein ausgehender Netzwerkzugriff                                                       |
| **Trusted** | [Allowlist-Domains](#default-allowed-domains) nur: Paketregistries, GitHub, Cloud-SDKs |
| **Full**    | Jede Domain                                                                            |
| **Custom**  | Ihre eigene Allowlist, optional einschließlich der Standards                           |

GitHub-Operationen verwenden einen [separaten Proxy](#github-proxy), der unabhängig von dieser Einstellung ist.

### Spezifische Domains zulassen

Um Domains zuzulassen, die nicht in der Trusted-Liste enthalten sind, wählen Sie **Custom** in den Netzwerkzugriffseinstellungen der Umgebung. Ein Feld **Zulässige Domains** wird angezeigt. Geben Sie eine Domain pro Zeile ein:

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

Verwenden Sie `*.` für Wildcard-Subdomain-Matching. Aktivieren Sie **Auch Standard-Liste der gängigen Paketmanager einschließen**, um die [Trusted-Domains](#default-allowed-domains) neben Ihren benutzerdefinierten Einträgen zu behalten, oder lassen Sie es deaktiviert, um nur das zuzulassen, was Sie auflisten.

### GitHub-Proxy

Aus Sicherheitsgründen gehen alle GitHub-Operationen durch einen dedizierten Proxy-Service, der alle Git-Interaktionen transparent verwaltet. Innerhalb der Sandbox authentifiziert sich der Git-Client mit einem benutzerdefinierten Scoped-Credential. Dieser Proxy:

* Verwaltet GitHub-Authentifizierung sicher: Der Git-Client verwendet ein Scoped-Credential innerhalb der Sandbox, das der Proxy überprüft und in Ihr tatsächliches GitHub-Authentifizierungstoken übersetzt
* Beschränkt Git-Push-Operationen auf den aktuellen Arbeitsbranch aus Sicherheitsgründen
* Ermöglicht Klonen, Abrufen und PR-Operationen bei Beibehaltung von Sicherheitsgrenzen

### Sicherheits-Proxy

Umgebungen werden aus Sicherheits- und Missbrauchspräventionsgründen hinter einem HTTP/HTTPS-Netzwerk-Proxy ausgeführt. Der gesamte ausgehende Internetdatenverkehr läuft durch diesen Proxy, der Folgendes bietet:

* Schutz vor böswilligen Anfragen
* Ratenbegrenzung und Missbrauchsprävention
* Inhaltsfilterung für erhöhte Sicherheit

### Standard-Allowlist-Domains

Bei Verwendung von **Trusted**-Netzwerkzugriff sind die folgenden Domains standardmäßig zulässig. Domains, die mit `*` gekennzeichnet sind, zeigen Wildcard-Subdomain-Matching an, daher erlaubt `*.gcr.io` jede Subdomain von `gcr.io`.

<AccordionGroup>
  <Accordion title="Anthropic-Services">
    * api.anthropic.com
    * statsig.anthropic.com
    * docs.claude.com
    * platform.claude.com
    * code.claude.com
    * claude.ai
  </Accordion>

  <Accordion title="Versionskontrolle">
    * github.com
    * [www.github.com](http://www.github.com)
    * api.github.com
    * npm.pkg.github.com
    * raw\.githubusercontent.com
    * pkg-npm.githubusercontent.com
    * objects.githubusercontent.com
    * release-assets.githubusercontent.com
    * codeload.github.com
    * avatars.githubusercontent.com
    * camo.githubusercontent.com
    * gist.github.com
    * gitlab.com
    * [www.gitlab.com](http://www.gitlab.com)
    * registry.gitlab.com
    * bitbucket.org
    * [www.bitbucket.org](http://www.bitbucket.org)
    * api.bitbucket.org
  </Accordion>

  <Accordion title="Container-Registries">
    * registry-1.docker.io
    * auth.docker.io
    * index.docker.io
    * hub.docker.com
    * [www.docker.com](http://www.docker.com)
    * production.cloudflare.docker.com
    * download.docker.com
    * gcr.io
    * \*.gcr.io
    * ghcr.io
    * mcr.microsoft.com
    * \*.data.mcr.microsoft.com
    * public.ecr.aws
  </Accordion>

  <Accordion title="Cloud-Plattformen">
    * cloud.google.com
    * accounts.google.com
    * gcloud.google.com
    * \*.googleapis.com
    * storage.googleapis.com
    * compute.googleapis.com
    * container.googleapis.com
    * azure.com
    * portal.azure.com
    * microsoft.com
    * [www.microsoft.com](http://www.microsoft.com)
    * \*.microsoftonline.com
    * packages.microsoft.com
    * dotnet.microsoft.com
    * dot.net
    * visualstudio.com
    * dev.azure.com
    * \*.amazonaws.com
    * \*.api.aws
    * oracle.com
    * [www.oracle.com](http://www.oracle.com)
    * java.com
    * [www.java.com](http://www.java.com)
    * java.net
    * [www.java.net](http://www.java.net)
    * download.oracle.com
    * yum.oracle.com
  </Accordion>

  <Accordion title="JavaScript und Node-Paketmanager">
    * registry.npmjs.org
    * [www.npmjs.com](http://www.npmjs.com)
    * [www.npmjs.org](http://www.npmjs.org)
    * npmjs.com
    * npmjs.org
    * yarnpkg.com
    * registry.yarnpkg.com
  </Accordion>

  <Accordion title="Python-Paketmanager">
    * pypi.org
    * [www.pypi.org](http://www.pypi.org)
    * files.pythonhosted.org
    * pythonhosted.org
    * test.pypi.org
    * pypi.python.org
    * pypa.io
    * [www.pypa.io](http://www.pypa.io)
  </Accordion>

  <Accordion title="Ruby-Paketmanager">
    * rubygems.org
    * [www.rubygems.org](http://www.rubygems.org)
    * api.rubygems.org
    * index.rubygems.org
    * ruby-lang.org
    * [www.ruby-lang.org](http://www.ruby-lang.org)
    * rubyforge.org
    * [www.rubyforge.org](http://www.rubyforge.org)
    * rubyonrails.org
    * [www.rubyonrails.org](http://www.rubyonrails.org)
    * rvm.io
    * get.rvm.io
  </Accordion>

  <Accordion title="Rust-Paketmanager">
    * crates.io
    * [www.crates.io](http://www.crates.io)
    * index.crates.io
    * static.crates.io
    * rustup.rs
    * static.rust-lang.org
    * [www.rust-lang.org](http://www.rust-lang.org)
  </Accordion>

  <Accordion title="Go-Paketmanager">
    * proxy.golang.org
    * sum.golang.org
    * index.golang.org
    * golang.org
    * [www.golang.org](http://www.golang.org)
    * goproxy.io
    * pkg.go.dev
  </Accordion>

  <Accordion title="JVM-Paketmanager">
    * maven.org
    * repo.maven.org
    * central.maven.org
    * repo1.maven.org
    * repo.maven.apache.org
    * jcenter.bintray.com
    * gradle.org
    * [www.gradle.org](http://www.gradle.org)
    * services.gradle.org
    * plugins.gradle.org
    * kotlinlang.org
    * [www.kotlinlang.org](http://www.kotlinlang.org)
    * spring.io
    * repo.spring.io
  </Accordion>

  <Accordion title="Andere Paketmanager">
    * packagist.org (PHP Composer)
    * [www.packagist.org](http://www.packagist.org)
    * repo.packagist.org
    * nuget.org (.NET NuGet)
    * [www.nuget.org](http://www.nuget.org)
    * api.nuget.org
    * pub.dev (Dart/Flutter)
    * api.pub.dev
    * hex.pm (Elixir/Erlang)
    * [www.hex.pm](http://www.hex.pm)
    * cpan.org (Perl CPAN)
    * [www.cpan.org](http://www.cpan.org)
    * metacpan.org
    * [www.metacpan.org](http://www.metacpan.org)
    * api.metacpan.org
    * cocoapods.org (iOS/macOS)
    * [www.cocoapods.org](http://www.cocoapods.org)
    * cdn.cocoapods.org
    * haskell.org
    * [www.haskell.org](http://www.haskell.org)
    * hackage.haskell.org
    * swift.org
    * [www.swift.org](http://www.swift.org)
  </Accordion>

  <Accordion title="Linux-Distributionen">
    * archive.ubuntu.com
    * security.ubuntu.com
    * ubuntu.com
    * [www.ubuntu.com](http://www.ubuntu.com)
    * \*.ubuntu.com
    * ppa.launchpad.net
    * launchpad.net
    * [www.launchpad.net](http://www.launchpad.net)
    * \*.nixos.org
  </Accordion>

  <Accordion title="Entwicklungstools und Plattformen">
    * dl.k8s.io (Kubernetes)
    * pkgs.k8s.io
    * k8s.io
    * [www.k8s.io](http://www.k8s.io)
    * releases.hashicorp.com (HashiCorp)
    * apt.releases.hashicorp.com
    * rpm.releases.hashicorp.com
    * archive.releases.hashicorp.com
    * hashicorp.com
    * [www.hashicorp.com](http://www.hashicorp.com)
    * repo.anaconda.com (Anaconda/Conda)
    * conda.anaconda.org
    * anaconda.org
    * [www.anaconda.com](http://www.anaconda.com)
    * anaconda.com
    * continuum.io
    * apache.org (Apache)
    * [www.apache.org](http://www.apache.org)
    * archive.apache.org
    * downloads.apache.org
    * eclipse.org (Eclipse)
    * [www.eclipse.org](http://www.eclipse.org)
    * download.eclipse.org
    * nodejs.org (Node.js)
    * [www.nodejs.org](http://www.nodejs.org)
    * developer.apple.com
    * developer.android.com
    * pkg.stainless.com
    * binaries.prisma.sh
  </Accordion>

  <Accordion title="Cloud-Services und Überwachung">
    * statsig.com
    * [www.statsig.com](http://www.statsig.com)
    * api.statsig.com
    * sentry.io
    * \*.sentry.io
    * downloads.sentry-cdn.com
    * http-intake.logs.datadoghq.com
    * \*.datadoghq.com
    * \*.datadoghq.eu
    * api.honeycomb.io
  </Accordion>

  <Accordion title="Content Delivery und Mirrors">
    * sourceforge.net
    * \*.sourceforge.net
    * packagecloud.io
    * \*.packagecloud.io
    * fonts.googleapis.com
    * fonts.gstatic.com
  </Accordion>

  <Accordion title="Schema und Konfiguration">
    * json-schema.org
    * [www.json-schema.org](http://www.json-schema.org)
    * json.schemastore.org
    * [www.schemastore.org](http://www.schemastore.org)
  </Accordion>

  <Accordion title="Model Context Protocol">
    * \*.modelcontextprotocol.io
  </Accordion>
</AccordionGroup>

## Aufgaben zwischen Web und Terminal verschieben

Diese Workflows erfordern die [Claude Code CLI](/de/quickstart), die bei demselben claude.ai-Konto angemeldet ist. Sie können neue Cloud-Sitzungen von Ihrem Terminal aus starten oder Cloud-Sitzungen in Ihr Terminal ziehen, um lokal fortzufahren. Cloud-Sitzungen bleiben bestehen, auch wenn Sie Ihren Laptop schließen, und Sie können sie von überall aus überwachen, einschließlich der Claude Mobile-App.

<Note>
  Von der CLI ist die Sitzungsübergabe unidirektional: Sie können Cloud-Sitzungen mit `--teleport` in Ihr Terminal ziehen, aber Sie können keine vorhandene Terminal-Sitzung ins Web verschieben. Das Flag `--remote` erstellt eine neue Cloud-Sitzung für Ihr aktuelles Repository. Die [Desktop-App](/de/desktop#continue-in-another-surface) bietet ein Continue in-Menü, das eine lokale Sitzung ins Web senden kann.
</Note>

### Vom Terminal zum Web

Starten Sie eine Cloud-Sitzung von der Befehlszeile mit dem Flag `--remote`:

```bash theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Dies erstellt eine neue Cloud-Sitzung auf claude.ai. Die Sitzung klont Ihr aktuelles Verzeichnis's GitHub-Remote bei Ihrem aktuellen Branch, daher pushen Sie zuerst, wenn Sie lokale Commits haben, da die VM von GitHub klont, nicht von Ihrem Computer. `--remote` funktioniert mit einem Repository auf einmal. Die Aufgabe wird in der Cloud ausgeführt, während Sie lokal weiterarbeiten.

<Note>
  `--remote` erstellt Cloud-Sitzungen. `--remote-control` ist nicht verwandt: Es stellt eine lokale CLI-Sitzung zur Überwachung vom Web aus bereit. Siehe [Remote Control](/de/remote-control).
</Note>

Verwenden Sie `/tasks` in der Claude Code CLI, um den Fortschritt zu überprüfen, oder öffnen Sie die Sitzung auf claude.ai oder der Claude Mobile-App, um direkt zu interagieren. Von dort aus können Sie Claude steuern, Feedback geben oder Fragen beantworten, genau wie in jedem anderen Gespräch.

#### Tipps für Cloud-Aufgaben

**Planen Sie lokal, führen Sie remote aus**: Für komplexe Aufgaben starten Sie Claude im Plan Mode, um den Ansatz zu besprechen, und senden Sie dann die Arbeit ins Web:

```bash theme={null}
claude --permission-mode plan
```

Im Plan Mode liest Claude Dateien, führt Befehle aus, um zu erkunden, und schlägt einen Plan vor, ohne Quellcode zu bearbeiten. Sobald Sie mit dem Plan zufrieden sind, speichern Sie den Plan im Repo, committen und pushen Sie, damit die Cloud-VM ihn klonen kann. Dann starten Sie eine Cloud-Sitzung für autonome Ausführung:

```bash theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Dieses Muster gibt Ihnen Kontrolle über die Strategie, während Claude autonom in der Cloud ausgeführt wird.

**Planen Sie in der Cloud mit ultraplan**: Um den Plan selbst in einer Web-Sitzung zu entwerfen und zu überprüfen, verwenden Sie [ultraplan](/de/ultraplan). Claude generiert den Plan auf Claude Code im Web, während Sie weiterarbeiten, dann kommentieren Sie Abschnitte in Ihrem Browser und wählen, ob Sie remote ausführen oder den Plan zurück zu Ihrem Terminal senden.

**Führen Sie Aufgaben parallel aus**: Jeder `--remote`-Befehl erstellt seine eigene Cloud-Sitzung, die unabhängig ausgeführt wird. Sie können mehrere Aufgaben starten und sie werden alle gleichzeitig in separaten Sitzungen ausgeführt:

```bash theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Überwachen Sie alle Sitzungen mit `/tasks` in der Claude Code CLI. Wenn eine Sitzung abgeschlossen ist, können Sie einen PR aus der Web-Oberfläche erstellen oder [die Sitzung teleportieren](#from-web-to-terminal), um lokal fortzufahren.

#### Senden Sie lokale Repositories ohne GitHub

Wenn Sie `claude --remote` aus einem Repository ausführen, das nicht mit GitHub verbunden ist, bündelt Claude Code Ihr lokales Repository und lädt es direkt in die Cloud-Sitzung hoch. Das Bündel enthält Ihre vollständige Repository-Historie über alle Branches hinweg, plus alle nicht committeten Änderungen an verfolgten Dateien.

Dieses Fallback wird automatisch aktiviert, wenn GitHub-Zugriff nicht verfügbar ist. Um es zu erzwingen, auch wenn GitHub verbunden ist, setzen Sie `CCR_FORCE_BUNDLE=1`:

```bash theme={null}
CCR_FORCE_BUNDLE=1 claude --remote "Run the test suite and fix any failures"
```

Gebündelte Repositories müssen diese Limits erfüllen:

* Das Verzeichnis muss ein Git-Repository mit mindestens einem Commit sein
* Das gebündelte Repository muss unter 100 MB liegen. Größere Repositories fallen auf das Bündeln nur des aktuellen Branches zurück, dann auf einen einzelnen gequetschten Snapshot des Arbeitsbaums, und schlagen nur fehl, wenn der Snapshot immer noch zu groß ist
* Nicht verfolgte Dateien sind nicht enthalten; führen Sie `git add` auf Dateien aus, die die Cloud-Sitzung sehen soll
* Sitzungen, die aus einem Bündel erstellt wurden, können nicht zurück zu einem Remote pushen, es sei denn, Sie haben auch [GitHub-Authentifizierung](#github-authentication-options) konfiguriert

### Vom Web zum Terminal

Ziehen Sie eine Cloud-Sitzung in Ihr Terminal mit einer dieser Methoden:

* **Mit `--teleport`**: Führen Sie von der Befehlszeile `claude --teleport` für eine interaktive Sitzungsauswahl aus, oder `claude --teleport <session-id>`, um eine bestimmte Sitzung direkt fortzusetzen. Wenn Sie nicht committete Änderungen haben, werden Sie aufgefordert, diese zuerst zu stashen.
* **Mit `/teleport`**: Führen Sie innerhalb einer vorhandenen CLI-Sitzung `/teleport` (oder `/tp`) aus, um die gleiche Sitzungsauswahl zu öffnen, ohne Claude Code neu zu starten.
* **Von `/tasks`**: Führen Sie `/tasks` aus, um Ihre Hintergrund-Sitzungen zu sehen, drücken Sie dann `t`, um in eine zu teleportieren
* **Von der Web-Oberfläche**: Wählen Sie **Open in CLI**, um einen Befehl zu kopieren, den Sie in Ihr Terminal einfügen können

Wenn Sie eine Sitzung teleportieren, überprüft Claude, dass Sie sich im richtigen Repository befinden, ruft den Branch aus der Cloud-Sitzung ab und checkt ihn aus, und lädt die vollständige Gesprächshistorie in Ihr Terminal.

`--teleport` unterscheidet sich von `--resume`. `--resume` öffnet ein Gespräch aus der lokalen Historie dieser Maschine und listet keine Cloud-Sitzungen auf; `--teleport` zieht eine Cloud-Sitzung und ihren Branch.

#### Teleport-Anforderungen

Teleport überprüft diese Anforderungen, bevor eine Sitzung fortgesetzt wird. Wenn eine Anforderung nicht erfüllt ist, sehen Sie einen Fehler oder werden aufgefordert, das Problem zu beheben.

| Anforderung          | Details                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Sauberer Git-Status  | Ihr Arbeitsverzeichnis darf keine nicht committeten Änderungen haben. Teleport fordert Sie auf, Änderungen zu stashen, falls erforderlich. |
| Korrektes Repository | Sie müssen `--teleport` aus einem Checkout desselben Repositories ausführen, nicht aus einem Fork.                                         |
| Branch verfügbar     | Der Branch aus der Cloud-Sitzung muss in das Remote gepusht worden sein. Teleport ruft ihn automatisch ab und checkt ihn aus.              |
| Gleiches Konto       | Sie müssen sich bei demselben claude.ai-Konto authentifizieren, das in der Cloud-Sitzung verwendet wurde.                                  |

#### `--teleport` ist nicht verfügbar

Teleport erfordert claude.ai-Abonnement-Authentifizierung. Wenn Sie sich über API-Schlüssel, Bedrock, Vertex AI oder Microsoft Foundry authentifizieren, führen Sie `/login` aus, um sich stattdessen mit Ihrem claude.ai-Konto anzumelden. Wenn Sie bereits über claude.ai angemeldet sind und `--teleport` immer noch nicht verfügbar ist, hat Ihre Organisation möglicherweise Cloud-Sitzungen deaktiviert.

## Mit Sitzungen arbeiten

Sitzungen werden in der Seitenleiste unter claude.ai/code angezeigt. Von dort aus können Sie Änderungen überprüfen, mit Teamkollegen teilen, abgeschlossene Arbeiten archivieren oder Sitzungen dauerhaft löschen.

### Kontext verwalten

Cloud-Sitzungen unterstützen [integrierte Befehle](/de/commands), die Textausgabe erzeugen. Befehle, die eine interaktive Terminal-Auswahl öffnen, wie `/model` oder `/config`, sind nicht verfügbar.

Für Kontextverwaltung speziell:

| Befehl     | Funktioniert in Cloud-Sitzungen | Notizen                                                                                                                         |
| :--------- | :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| `/compact` | Ja                              | Fasst das Gespräch zusammen, um Kontext freizugeben. Akzeptiert optionale Fokus-Anweisungen wie `/compact keep the test output` |
| `/context` | Ja                              | Zeigt, was sich derzeit im Kontextfenster befindet                                                                              |
| `/clear`   | Nein                            | Starten Sie stattdessen eine neue Sitzung aus der Seitenleiste                                                                  |

Auto-Kompaktierung wird automatisch ausgeführt, wenn sich das Kontextfenster der Kapazität nähert, genau wie in der CLI. Um es früher auszulösen, setzen Sie [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/de/env-vars) in Ihren [Umgebungsvariablen](#configure-your-environment). Zum Beispiel kompaktiert `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` bei 70% Kapazität statt des Standards \~95%. Um die effektive Fenstergröße für Kompaktierungsberechnungen zu ändern, verwenden Sie [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/de/env-vars).

[Subagents](/de/sub-agents) funktionieren genauso wie lokal. Claude kann sie mit dem Task-Tool spawnen, um Forschung oder parallele Arbeit in ein separates Kontextfenster auszulagern, um das Hauptgespräch leichter zu halten. Subagents, die in Ihrem Repo's `.claude/agents/` definiert sind, werden automatisch aufgegriffen. [Agent-Teams](/de/agent-teams) sind standardmäßig deaktiviert, können aber aktiviert werden, indem Sie `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` zu Ihren [Umgebungsvariablen](#configure-your-environment) hinzufügen.

### Änderungen überprüfen

Jede Sitzung zeigt einen Diff-Indikator mit hinzugefügten und entfernten Zeilen, wie `+42 -18`. Wählen Sie ihn, um die Diff-Ansicht zu öffnen, hinterlassen Sie Inline-Kommentare zu bestimmten Zeilen und senden Sie sie mit Ihrer nächsten Nachricht an Claude. Siehe [Überprüfung und Iteration](/de/web-quickstart#review-and-iterate) für die vollständige Anleitung, einschließlich PR-Erstellung. Um Claude den PR auf CI-Fehler und Review-Kommentare automatisch überwachen zu lassen, siehe [Auto-fix Pull Requests](#auto-fix-pull-requests).

### Sitzungen teilen

Um eine Sitzung zu teilen, schalten Sie ihre Sichtbarkeit gemäß den folgenden Kontotypen um. Danach teilen Sie den Sitzungslink wie gewohnt. Empfänger sehen den neuesten Status, wenn sie den Link öffnen, aber ihre Ansicht wird nicht in Echtzeit aktualisiert.

#### Teilen von einem Enterprise- oder Team-Konto

Für Enterprise- und Team-Konten sind die beiden Sichtbarkeitsoptionen **Private** und **Team**. Team-Sichtbarkeit macht die Sitzung für andere Mitglieder Ihrer claude.ai-Organisation sichtbar. Die Überprüfung des Repository-Zugriffs ist standardmäßig aktiviert, basierend auf dem GitHub-Konto, das mit dem Konto des Empfängers verbunden ist. Der Anzeigename Ihres Kontos ist für alle Empfänger mit Zugriff sichtbar. [Claude in Slack](/de/slack)-Sitzungen werden automatisch mit Team-Sichtbarkeit geteilt.

#### Teilen von einem Max- oder Pro-Konto

Für Max- und Pro-Konten sind die beiden Sichtbarkeitsoptionen **Private** und **Public**. Public-Sichtbarkeit macht die Sitzung für jeden Benutzer sichtbar, der bei claude.ai angemeldet ist.

Überprüfen Sie Ihre Sitzung auf sensible Inhalte, bevor Sie sie teilen. Sitzungen können Code und Anmeldedaten aus privaten GitHub-Repositories enthalten. Die Überprüfung des Repository-Zugriffs ist standardmäßig nicht aktiviert.

Um zu verlangen, dass Empfänger Repository-Zugriff haben, oder um Ihren Namen aus gemeinsamen Sitzungen auszublenden, gehen Sie zu Einstellungen > Claude Code > Freigabeeinstellungen.

### Sitzungen archivieren

Sie können Sitzungen archivieren, um Ihre Sitzungsliste organisiert zu halten. Archivierte Sitzungen sind in der Standard-Sitzungsliste ausgeblendet, können aber durch Filtern nach archivierten Sitzungen angezeigt werden.

Um eine Sitzung zu archivieren, bewegen Sie den Mauszeiger über die Sitzung in der Seitenleiste und wählen Sie das Archiv-Symbol.

### Sitzungen löschen

Das Löschen einer Sitzung entfernt die Sitzung und ihre Daten dauerhaft. Diese Aktion kann nicht rückgängig gemacht werden. Sie können eine Sitzung auf zwei Arten löschen:

* **Von der Seitenleiste**: Filtern Sie nach archivierten Sitzungen, bewegen Sie dann den Mauszeiger über die Sitzung, die Sie löschen möchten, und wählen Sie das Lösch-Symbol
* **Vom Sitzungsmenü**: Öffnen Sie eine Sitzung, wählen Sie das Dropdown-Menü neben dem Sitzungstitel und wählen Sie **Löschen**

Sie werden aufgefordert, vor dem Löschen einer Sitzung zu bestätigen.

## Auto-fix Pull Requests

Claude kann einen Pull Request überwachen und automatisch auf CI-Fehler und Review-Kommentare reagieren. Claude abonniert GitHub-Aktivitäten auf dem PR, und wenn eine Überprüfung fehlschlägt oder ein Reviewer einen Kommentar hinterlässt, untersucht Claude das Problem und pusht eine Lösung, wenn eine klar ist.

<Note>
  Auto-fix erfordert, dass die Claude GitHub App auf Ihrem Repository installiert ist. Falls noch nicht geschehen, installieren Sie sie von der [GitHub App-Seite](https://github.com/apps/claude) oder wenn Sie dazu während des [Setups](/de/web-quickstart#connect-github-and-create-an-environment) aufgefordert werden.
</Note>

Es gibt mehrere Möglichkeiten, Auto-fix zu aktivieren, je nachdem, woher der PR stammt und welches Gerät Sie verwenden:

* **PRs, die in Claude Code im Web erstellt wurden**: Öffnen Sie die CI-Statusleiste und wählen Sie **Auto-fix**
* **Von Ihrem Terminal**: Führen Sie [`/autofix-pr`](/de/commands) aus, während Sie auf dem PR's Branch sind. Claude Code erkennt den offenen PR mit `gh`, spawnt eine Web-Sitzung und aktiviert Auto-fix in einem Schritt
* **Von der Mobile-App**: Sagen Sie Claude, den PR zu auto-fixen, zum Beispiel „watch this PR and fix any CI failures or review comments"
* **Jeder vorhandene PR**: Fügen Sie die PR-URL in eine Sitzung ein und sagen Sie Claude, den PR zu auto-fixen

### Wie Claude auf PR-Aktivität reagiert

Wenn Auto-fix aktiv ist, empfängt Claude GitHub-Events für den PR, einschließlich neuer Review-Kommentare und CI-Check-Fehler. Für jedes Event untersucht Claude das Problem und entscheidet, wie vorgegangen wird:

* **Klare Fixes**: Wenn Claude sich einer Lösung sicher ist und sie nicht mit früheren Anweisungen in Konflikt steht, nimmt Claude die Änderung vor, pusht sie und erklärt, was getan wurde, in der Sitzung
* **Mehrdeutige Anfragen**: Wenn ein Reviewer-Kommentar auf mehrere Arten interpretiert werden könnte oder etwas architektonisch Bedeutsames betrifft, fragt Claude Sie, bevor er handelt
* **Doppelte oder keine Aktion erforderlich Events**: Wenn ein Event ein Duplikat ist oder keine Änderung erfordert, notiert Claude es in der Sitzung und fährt fort

Claude kann als Teil der Auflösung auf Review-Kommentar-Threads auf GitHub antworten. Diese Antworten werden mit Ihrem GitHub-Konto gepostet, sodass sie unter Ihrem Benutzernamen erscheinen, aber jede Antwort ist als von Claude Code stammend gekennzeichnet, damit Reviewer wissen, dass sie vom Agent geschrieben wurde und nicht direkt von Ihnen.

<Warning>
  Wenn Ihr Repository Kommentar-ausgelöste Automatisierung wie Atlantis, Terraform Cloud oder benutzerdefinierte GitHub Actions verwendet, die auf `issue_comment`-Events ausgeführt werden, beachten Sie, dass Claude auf Ihrem Behalf antworten kann, was diese Workflows auslösen kann. Überprüfen Sie die Automatisierung Ihres Repositories, bevor Sie Auto-fix aktivieren, und erwägen Sie, Auto-fix für Repositories zu deaktivieren, in denen ein PR-Kommentar Infrastruktur bereitstellen oder privilegierte Operationen ausführen kann.
</Warning>

## Sicherheit und Isolation

Jede Cloud-Sitzung ist von Ihrem Computer und von anderen Sitzungen durch mehrere Schichten getrennt:

* **Isolierte virtuelle Maschinen**: Jede Sitzung wird in einer isolierten, von Anthropic verwalteten VM ausgeführt
* **Netzwerkzugriffskontrolle**: Der Netzwerkzugriff ist standardmäßig begrenzt und kann deaktiviert werden. Wenn Claude Code mit deaktiviertem Netzwerkzugriff ausgeführt wird, kann Claude Code immer noch mit der Anthropic API kommunizieren, was möglicherweise ermöglicht, dass Daten die VM verlassen.
* **Schutz von Anmeldedaten**: Sensible Anmeldedaten wie Git-Anmeldedaten oder Signaturschlüssel befinden sich niemals in der Sandbox mit Claude Code. Die Authentifizierung wird über einen sicheren Proxy mit Scoped-Credentials verwaltet.
* **Sichere Analyse**: Code wird in isolierten VMs analysiert und geändert, bevor PRs erstellt werden

## Einschränkungen

Bevor Sie Cloud-Sitzungen für einen Workflow verwenden, berücksichtigen Sie diese Einschränkungen:

* **Ratenlimits**: Claude Code im Web teilt Ratenlimits mit allen anderen Claude- und Claude Code-Nutzungen in Ihrem Konto. Das Ausführen mehrerer Aufgaben parallel verbraucht proportional mehr Ratenlimits. Es gibt keine separate Compute-Gebühr für die Cloud-VM.
* **Repository-Authentifizierung**: Sie können Sitzungen nur vom Web zum lokalen Computer verschieben, wenn Sie sich bei demselben Konto authentifizieren
* **Plattformbeschränkungen**: Repository-Klonen und Pull Request-Erstellung erfordern GitHub. Selbstgehostete [GitHub Enterprise Server](/de/github-enterprise-server)-Instanzen werden für Team- und Enterprise-Pläne unterstützt. GitLab, Bitbucket und andere Nicht-GitHub-Repositories können als lokales [Bündel](#send-local-repositories-without-github) zu Cloud-Sitzungen gesendet werden, aber die Sitzung kann nicht zurück zum Remote pushen

## Verwandte Ressourcen

* [Ultraplan](/de/ultraplan): Entwerfen Sie einen Plan in einer Cloud-Sitzung und überprüfen Sie ihn in Ihrem Browser
* [Ultrareview](/de/ultrareview): Führen Sie eine tiefe Multi-Agent-Code-Review in einer Cloud-Sandbox aus
* [Routines](/de/routines): Automatisieren Sie Arbeiten nach einem Zeitplan, über API-Aufruf oder als Reaktion auf GitHub-Events
* [Hooks-Konfiguration](/de/hooks): Führen Sie Skripte bei Sitzungs-Lifecycle-Events aus
* [Einstellungsreferenz](/de/settings): Alle Konfigurationsoptionen
* [Sicherheit](/de/security): Isolationsgarantien und Datenverarbeitung
* [Datennutzung](/de/data-usage): Was Anthropic aus Cloud-Sitzungen behält
