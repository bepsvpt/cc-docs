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

```bash  theme={null}
# HTTPS-Proxy (empfohlen)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP-Proxy (falls HTTPS nicht verfügbar)
export HTTP_PROXY=http://proxy.example.com:8080

# Proxy für spezifische Anfragen umgehen - durch Leerzeichen getrennt
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Proxy für spezifische Anfragen umgehen - durch Komma getrennt
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Proxy für alle Anfragen umgehen
export NO_PROXY="*"
```

<Note>
  Claude Code unterstützt keine SOCKS-Proxies.
</Note>

### Basis-Authentifizierung

Wenn Ihr Proxy eine Basis-Authentifizierung erfordert, fügen Sie Anmeldedaten in die Proxy-URL ein:

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Vermeiden Sie das Hartcodieren von Passwörtern in Skripten. Verwenden Sie stattdessen Umgebungsvariablen oder sichere Anmeldedatenspeicherung.
</Warning>

<Tip>
  Für Proxies, die erweiterte Authentifizierung erfordern (NTLM, Kerberos usw.), erwägen Sie die Verwendung eines LLM-Gateway-Dienstes, der Ihre Authentifizierungsmethode unterstützt.
</Tip>

## Benutzerdefinierte CA-Zertifikate

Wenn Ihre Enterprise-Umgebung benutzerdefinierte CAs für HTTPS-Verbindungen verwendet (ob über einen Proxy oder direkten API-Zugriff), konfigurieren Sie Claude Code so, dass diese vertraut werden:

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS-Authentifizierung

Für Enterprise-Umgebungen, die Client-Zertifikat-Authentifizierung erfordern:

```bash  theme={null}
# Client-Zertifikat für Authentifizierung
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Privater Schlüssel des Clients
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optional: Passphrase für verschlüsselten privaten Schlüssel
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Netzwerkzugriffanforderungen

Claude Code benötigt Zugriff auf die folgenden URLs:

* `api.anthropic.com`: Claude-API-Endpunkte
* `claude.ai`: Authentifizierung für claude.ai-Konten
* `platform.claude.com`: Authentifizierung für Anthropic Console-Konten

Stellen Sie sicher, dass diese URLs in Ihrer Proxy-Konfiguration und Firewall-Regeln auf die Whitelist gesetzt sind. Dies ist besonders wichtig, wenn Sie Claude Code in containerisierten oder eingeschränkten Netzwerkumgebungen verwenden.

## Zusätzliche Ressourcen

* [Claude Code-Einstellungen](/de/settings)
* [Referenz für Umgebungsvariablen](/de/settings#environment-variables)
* [Leitfaden zur Fehlerbehebung](/de/troubleshooting)
