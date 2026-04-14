> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuração avançada

> Requisitos do sistema, instalação específica da plataforma, gerenciamento de versão e desinstalação do Claude Code.

Esta página cobre requisitos do sistema, detalhes de instalação específicos da plataforma, atualizações e desinstalação. Para um guia passo a passo de sua primeira sessão, consulte o [guia de início rápido](/pt/quickstart). Se você nunca usou um terminal antes, consulte o [guia de terminal](/pt/terminal-guide).

## Requisitos do sistema

Claude Code é executado nas seguintes plataformas e configurações:

* **Sistema operacional**:
  * macOS 13.0+
  * Windows 10 1809+ ou Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Hardware**: 4 GB+ de RAM
* **Rede**: conexão com a internet obrigatória. Consulte [configuração de rede](/pt/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell ou CMD. No Windows, [Git for Windows](https://git-scm.com/downloads/win) é obrigatório.
* **Localização**: [países suportados pela Anthropic](https://www.anthropic.com/supported-countries)

### Dependências adicionais

* **ripgrep**: geralmente incluído com Claude Code. Se a busca falhar, consulte [solução de problemas de busca](/pt/troubleshooting#search-and-discovery-issues).

## Instalar Claude Code

<Tip>
  Prefere uma interface gráfica? O [aplicativo de desktop](/pt/desktop-quickstart) permite que você use Claude Code sem o terminal. Baixe-o para [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) ou [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs).

  Novo no terminal? Consulte o [guia de terminal](/pt/terminal-guide) para instruções passo a passo.
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

    **Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it. WSL setups do not need it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

Após a conclusão da instalação, abra um terminal no projeto em que deseja trabalhar e inicie Claude Code:

```bash  theme={null}
claude
```

Se você encontrar algum problema durante a instalação, consulte o [guia de solução de problemas](/pt/troubleshooting).

### Configurar no Windows

Claude Code no Windows requer [Git for Windows](https://git-scm.com/downloads/win) ou WSL. Você pode iniciar `claude` a partir do PowerShell, CMD ou Git Bash. Claude Code usa Git Bash internamente para executar comandos. Você não precisa executar o PowerShell como Administrador.

**Opção 1: Windows nativo com Git Bash**

Instale [Git for Windows](https://git-scm.com/downloads/win) e execute o comando de instalação a partir do PowerShell ou CMD.

Se Claude Code não conseguir encontrar sua instalação do Git Bash, defina o caminho em seu [arquivo settings.json](/pt/settings):

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code também pode executar PowerShell nativamente no Windows como uma visualização de aceitação. Consulte [ferramenta PowerShell](/pt/tools-reference#powershell-tool) para configuração e limitações.

**Opção 2: WSL**

Tanto WSL 1 quanto WSL 2 são suportados. WSL 2 suporta [sandboxing](/pt/sandboxing) para segurança aprimorada. WSL 1 não suporta sandboxing.

### Alpine Linux e distribuições baseadas em musl

O instalador nativo no Alpine e outras distribuições baseadas em musl/uClibc requer `libgcc`, `libstdc++` e `ripgrep`. Instale-os usando o gerenciador de pacotes da sua distribuição e defina `USE_BUILTIN_RIPGREP=0`.

Este exemplo instala os pacotes necessários no Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

Em seguida, defina `USE_BUILTIN_RIPGREP` como `0` em seu arquivo [`settings.json`](/pt/settings#available-settings):

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Verificar sua instalação

Após a instalação, confirme que Claude Code está funcionando:

```bash  theme={null}
claude --version
```

Para uma verificação mais detalhada de sua instalação e configuração, execute [`claude doctor`](/pt/troubleshooting#get-more-help):

```bash  theme={null}
claude doctor
```

## Autenticar

Claude Code requer uma conta Pro, Max, Team, Enterprise ou Console. O plano gratuito do Claude.ai não inclui acesso ao Claude Code. Você também pode usar Claude Code com um provedor de API de terceiros como [Amazon Bedrock](/pt/amazon-bedrock), [Google Vertex AI](/pt/google-vertex-ai) ou [Microsoft Foundry](/pt/microsoft-foundry).

Após a instalação, faça login executando `claude` e seguindo os prompts do navegador. Consulte [Autenticação](/pt/authentication) para todos os tipos de conta e opções de configuração de equipe.

## Atualizar Claude Code

As instalações nativas são atualizadas automaticamente em segundo plano. Você pode [configurar o canal de lançamento](#configure-release-channel) para controlar se recebe atualizações imediatamente ou em um cronograma estável com atraso, ou [desabilitar atualizações automáticas](#disable-auto-updates) completamente. As instalações do Homebrew e WinGet requerem atualizações manuais.

### Atualizações automáticas

Claude Code verifica atualizações na inicialização e periodicamente durante a execução. As atualizações são baixadas e instaladas em segundo plano, depois entram em vigor na próxima vez que você inicia Claude Code.

<Note>
  As instalações do Homebrew e WinGet não são atualizadas automaticamente. Use `brew upgrade claude-code` ou `winget upgrade Anthropic.ClaudeCode` para atualizar manualmente.

  **Problema conhecido:** Claude Code pode notificá-lo sobre atualizações antes que a nova versão esteja disponível nesses gerenciadores de pacotes. Se uma atualização falhar, aguarde e tente novamente mais tarde.

  O Homebrew mantém versões antigas no disco após atualizações. Execute `brew cleanup claude-code` periodicamente para recuperar espaço em disco.
</Note>

### Configurar canal de lançamento

Controle qual canal de lançamento Claude Code segue para atualizações automáticas e `claude update` com a configuração `autoUpdatesChannel`:

* `"latest"`, o padrão: receba novos recursos assim que forem lançados
* `"stable"`: use uma versão que normalmente tem cerca de uma semana de idade, pulando lançamentos com regressões importantes

Configure isso via `/config` → **Canal de atualização automática**, ou adicione-o ao seu [arquivo settings.json](/pt/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Para implantações empresariais, você pode impor um canal de lançamento consistente em toda a sua organização usando [configurações gerenciadas](/pt/permissions#managed-settings).

### Desabilitar atualizações automáticas

Defina `DISABLE_AUTOUPDATER` como `"1"` na chave `env` do seu arquivo [`settings.json`](/pt/settings#available-settings):

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Atualizar manualmente

Para aplicar uma atualização imediatamente sem aguardar a próxima verificação em segundo plano, execute:

```bash  theme={null}
claude update
```

## Opções avançadas de instalação

Essas opções são para fixação de versão, migração do npm e verificação da integridade do binário.

### Instalar uma versão específica

O instalador nativo aceita um número de versão específico ou um canal de lançamento (`latest` ou `stable`). O canal que você escolhe no momento da instalação se torna seu padrão para atualizações automáticas. Consulte [configurar canal de lançamento](#configure-release-channel) para mais informações.

Para instalar a versão mais recente (padrão):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Para instalar a versão estável:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Para instalar um número de versão específico:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Instalação npm descontinuada

A instalação npm está descontinuada. O instalador nativo é mais rápido, não requer dependências e é atualizado automaticamente em segundo plano. Use o método de [instalação nativa](#install-claude-code) quando possível.

#### Migrar do npm para nativo

Se você instalou anteriormente Claude Code com npm, mude para o instalador nativo:

```bash  theme={null}
# Instalar o binário nativo
curl -fsSL https://claude.ai/install.sh | bash

# Remover a instalação antiga do npm
npm uninstall -g @anthropic-ai/claude-code
```

Você também pode executar `claude install` a partir de uma instalação npm existente para instalar o binário nativo junto com ela e depois remover a versão npm.

#### Instalar com npm

Se você precisar da instalação npm por motivos de compatibilidade, você deve ter [Node.js 18+](https://nodejs.org/en/download) instalado. Instale o pacote globalmente:

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NÃO use `sudo npm install -g` pois isso pode levar a problemas de permissão e riscos de segurança. Se você encontrar erros de permissão, consulte [solução de problemas de erros de permissão](/pt/troubleshooting#permission-errors-during-installation).
</Warning>

### Integridade binária e assinatura de código

Cada lançamento publica um `manifest.json` contendo checksums SHA256 para cada binário de plataforma. O manifesto é assinado com uma chave GPG da Anthropic, portanto verificar a assinatura no manifesto verifica transitivamente cada binário que ele lista.

#### Verificar a assinatura do manifesto

As etapas 1-3 requerem um shell POSIX com `gpg` e `curl`. No Windows, execute-as no Git Bash ou WSL. A etapa 4 inclui uma opção PowerShell.

<Steps>
  <Step title="Baixar e importar a chave pública">
    A chave de assinatura de lançamento é publicada em uma URL fixa.

    ```bash  theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Exiba a impressão digital da chave importada.

    ```bash  theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Confirme que a saída inclui esta impressão digital:

    ```text  theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Baixar o manifesto e a assinatura">
    Defina `VERSION` para o lançamento que você deseja verificar.

    ```bash  theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Verificar a assinatura">
    Verifique a assinatura destacada contra o manifesto.

    ```bash  theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    Um resultado válido relata `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` também imprime `WARNING: This key is not certified with a trusted signature!` para qualquer chave recém-importada. Isso é esperado. A linha `Good signature` confirma que a verificação criptográfica passou. A comparação de impressão digital na Etapa 1 confirma que a chave em si é autêntica.
  </Step>

  <Step title="Verificar o binário contra o manifesto">
    Compare o checksum SHA256 do seu binário baixado com o valor listado em `platforms.<platform>.checksum` em `manifest.json`.

    <Tabs>
      <Tab title="Linux">
        ```bash  theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash  theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell  theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  As assinaturas de manifesto estão disponíveis para lançamentos de `2.1.89` em diante. Lançamentos anteriores publicam checksums em `manifest.json` sem uma assinatura destacada.
</Note>

#### Assinaturas de código de plataforma

Além do manifesto assinado, os binários individuais carregam assinaturas de código nativas da plataforma onde suportado.

* **macOS**: assinado por "Anthropic PBC" e autenticado pela Apple. Verifique com `codesign --verify --verbose ./claude`.
* **Windows**: assinado por "Anthropic, PBC". Verifique com `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: use a assinatura de manifesto acima para verificar a integridade. Os binários Linux não são individualmente assinados com código.

## Desinstalar Claude Code

Para remover Claude Code, siga as instruções para seu método de instalação.

### Instalação nativa

Remova o binário Claude Code e os arquivos de versão:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Instalação do Homebrew

Remova o cask do Homebrew:

```bash  theme={null}
brew uninstall --cask claude-code
```

### Instalação do WinGet

Remova o pacote WinGet:

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Remova o pacote npm global:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Remover arquivos de configuração

<Warning>
  Remover arquivos de configuração excluirá todas as suas configurações, ferramentas permitidas, configurações do MCP server e histórico de sessão.
</Warning>

Para remover as configurações e dados em cache do Claude Code:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # Remover configurações de usuário e estado
    rm -rf ~/.claude
    rm ~/.claude.json

    # Remover configurações específicas do projeto (execute a partir do diretório do seu projeto)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # Remover configurações de usuário e estado
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Remover configurações específicas do projeto (execute a partir do diretório do seu projeto)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
