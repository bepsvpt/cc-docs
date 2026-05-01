> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Enterprise-Netzwerkkonfiguration

> Konfigurieren Sie Claude Code für Enterprise-Umgebungen mit Proxy-Servern, benutzerdefinierten Zertifizierungsstellen (CA) und gegenseitiger Transport Layer Security (mTLS)-Authentifizierung.

Claude Code unterstützt verschiedene Enterprise-Netzwerk- und Sicherheitskonfigurationen über Umgebungsvariablen. Dies umfasst das Routing von Datenverkehr über unternehmenseigene Proxy-Server, das Vertrauen in benutzerdefinierte Zertifizierungsstellen (CA) und die Authentifizierung mit gegenseitigen Transport Layer Security (mTLS)-Zertifikaten für erhöhte Sicherheit.

<Note>
  Alle auf dieser Seite gezeigten Umgebungsvariablen können auch in [`settings.json`](/de/settings) konfiguriert werden.
</Note>

## Proxy-Konfiguration

### Umgebungsvariablen

Claude Code respektiert Standard-Proxy-Umgebungsvariablen:

```bash theme={null}
# HTTPS-Proxy (empfohlen)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP-Proxy (falls HTTPS nicht verfügbar)
export HTTP_PROXY=http://proxy.example.com:8080

# Proxy für spezifische Anfragen umgehen – durch Leerzeichen getrennt
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Proxy für spezifische Anfragen umgehen – durch Komma getrennt
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Proxy für alle Anfragen umgehen
export NO_PROXY="*"
```

<Note>
  Claude Code unterstützt keine SOCKS-Proxies.
</Note>

### Basis-Authentifizierung

Wenn Ihr Proxy eine Basis-Authentifizierung erfordert, fügen Sie Anmeldedaten in die Proxy-URL ein:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Vermeiden Sie das Hardcodieren von Passwörtern in Skripten. Verwenden Sie stattdessen Umgebungsvariablen oder sichere Anmeldedatenspeicherung.
</Warning>

<Tip>
  Für Proxies, die erweiterte Authentifizierung erfordern (NTLM, Kerberos usw.), erwägen Sie die Verwendung eines LLM-Gateway-Dienstes, der Ihre Authentifizierungsmethode unterstützt.
</Tip>

## CA-Zertifikatspeicher

Standardmäßig vertraut Claude Code sowohl seinen gebündelten Mozilla-CA-Zertifikaten als auch dem Zertifikatspeicher Ihres Betriebssystems. Enterprise-TLS-Inspektions-Proxies wie CrowdStrike Falcon und Zscaler funktionieren ohne zusätzliche Konfiguration, wenn ihr Root-Zertifikat im Betriebssystem-Vertrauensspeicher installiert ist.

<Note>
  Die Integration des System-CA-Speichers erfordert die native Claude Code-Binärdistribution. Bei Ausführung auf der Node.js-Laufzeit wird der System-CA-Speicher nicht automatisch zusammengeführt. Setzen Sie in diesem Fall `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem`, um einer Enterprise-Root-CA zu vertrauen.
</Note>

`CLAUDE_CODE_CERT_STORE` akzeptiert eine durch Kommas getrennte Liste von Quellen. Erkannte Werte sind `bundled` für den mit Claude Code ausgelieferten Mozilla-CA-Satz und `system` für den Betriebssystem-Vertrauensspeicher. Der Standard ist `bundled,system`.

Um nur dem gebündelten Mozilla-CA-Satz zu vertrauen:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

Um nur dem Betriebssystem-Zertifikatspeicher zu vertrauen:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` hat keinen dedizierten `settings.json`-Schemaschlüssel. Setzen Sie ihn über den `env`-Block in `~/.claude/settings.json` oder direkt in der Prozessumgebung.
</Note>

## Benutzerdefinierte CA-Zertifikate

Wenn Ihre Enterprise-Umgebung eine benutzerdefinierte CA verwendet, konfigurieren Sie Claude Code so, dass dieser direkt vertraut wird:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS-Authentifizierung

Für Enterprise-Umgebungen, die Client-Zertifikat-Authentifizierung erfordern:

```bash theme={null}
# Client-Zertifikat für Authentifizierung
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Privater Schlüssel des Clients
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optional: Passphrase für verschlüsselten privaten Schlüssel
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Netzwerkzugriffanforderungen

Claude Code benötigt Zugriff auf die folgenden URLs. Setzen Sie diese in Ihrer Proxy-Konfiguration und Firewall-Regeln auf die Allowlist, besonders in containerisierten oder eingeschränkten Netzwerkumgebungen.

| URL                            | Erforderlich für                                                                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------- |
| `api.anthropic.com`            | Claude-API-Anfragen                                                                             |
| `claude.ai`                    | Authentifizierung für claude.ai-Konten                                                          |
| `platform.claude.com`          | Authentifizierung für Anthropic Console-Konten                                                  |
| `downloads.claude.ai`          | Download von Plugin-Ausführungsdateien; nativer Installer und nativer Auto-Updater              |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}Nativer Installer und nativer Auto-Updater in Versionen vor 2.1.116 |
| `bridge.claudeusercontent.com` | [Claude in Chrome](/de/chrome) Erweiterungs-WebSocket-Brücke                                    |

Wenn Sie Claude Code über npm installieren oder Ihre eigene Binärverteilung verwalten, benötigen Endbenutzer möglicherweise keinen Zugriff auf `downloads.claude.ai` oder `storage.googleapis.com`.

Claude Code sendet standardmäßig optionale operative Telemetrie, die Sie mit Umgebungsvariablen deaktivieren können. Siehe [Telemetrie-Dienste](/de/data-usage#telemetry-services), um zu erfahren, wie Sie diese deaktivieren, bevor Sie Ihre Allowlist finalisieren.

Bei Verwendung von [Amazon Bedrock](/de/amazon-bedrock), [Google Vertex AI](/de/google-vertex-ai) oder [Microsoft Foundry](/de/microsoft-foundry) geht der Modell-Datenverkehr und die Authentifizierung zu Ihrem Anbieter statt zu `api.anthropic.com`, `claude.ai` oder `platform.claude.com`. Das WebFetch-Tool ruft weiterhin `api.anthropic.com` für seine [Domain-Sicherheitsprüfung](/de/data-usage#webfetch-domain-safety-check) auf, es sei denn, Sie setzen `skipWebFetchPreflight: true` in [Einstellungen](/de/settings).

[Claude Code im Web](/de/claude-code-on-the-web) und [Code Review](/de/code-review) verbinden sich von der von Anthropic verwalteten Infrastruktur aus mit Ihren Repositories. Wenn Ihre GitHub Enterprise Cloud-Organisation den Zugriff nach IP-Adresse einschränkt, aktivieren Sie [IP-Allowlist-Vererbung für installierte GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). Die Claude GitHub App registriert ihre IP-Bereiche, sodass die Aktivierung dieser Einstellung den Zugriff ohne manuelle Konfiguration ermöglicht. Um [die Bereiche stattdessen manuell zu Ihrer Allowlist hinzuzufügen](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) oder um andere Firewalls zu konfigurieren, siehe [Anthropic API IP-Adressen](https://platform.claude.com/docs/en/api/ip-addresses).

Für selbstgehostete [GitHub Enterprise Server](/de/github-enterprise-server)-Instanzen hinter einer Firewall müssen Sie die gleichen [Anthropic API IP-Adressen](https://platform.claude.com/docs/en/api/ip-addresses) auf die Allowlist setzen, damit die Anthropic-Infrastruktur Ihren GHES-Host erreichen kann, um Repositories zu klonen und Review-Kommentare zu posten.

## Zusätzliche Ressourcen

* [Claude Code-Einstellungen](/de/settings)
* [Referenz für Umgebungsvariablen](/de/env-vars)
* [Leitfaden zur Fehlerbehebung](/de/troubleshooting)
