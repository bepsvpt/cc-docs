> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurar Claude Code

> Instale, autentique e comece a usar Claude Code em sua máquina de desenvolvimento.

## Requisitos do sistema

* **Sistema Operacional**:
  * macOS 13.0+
  * Windows 10 1809+ ou Windows Server 2019+ ([consulte as notas de configuração](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([dependências adicionais necessárias](#platform-specific-setup))
* **Hardware**: 4 GB+ de RAM
* **Rede**: Conexão com a Internet necessária (consulte [configuração de rede](/pt/network-config#network-access-requirements))
* **Shell**: Funciona melhor em Bash ou Zsh
* **Localização**: [Países suportados pela Anthropic](https://www.anthropic.com/supported-countries)

### Dependências adicionais

* **ripgrep**: Geralmente incluído com Claude Code. Se a busca falhar, consulte [solução de problemas de busca](/pt/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)**: Necessário apenas para [instalação npm descontinuada](#npm-installation-deprecated)

## Instalação

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

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
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

Após a conclusão do processo de instalação, navegue até seu projeto e inicie Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Se você encontrar algum problema durante a instalação, consulte o [guia de solução de problemas](/pt/troubleshooting).

<Tip>
  Execute `claude doctor` após a instalação para verificar seu tipo de instalação e versão.
</Tip>

### Configuração específica da plataforma

**Windows**: Execute Claude Code nativamente (requer [Git Bash](https://git-scm.com/downloads/win)) ou dentro do WSL. Tanto WSL 1 quanto WSL 2 são suportados, mas WSL 1 tem suporte limitado e não suporta recursos como sandboxing de ferramentas Bash.

**Alpine Linux e outras distribuições baseadas em musl/uClibc**:

O instalador nativo no Alpine e outras distribuições baseadas em musl/uClibc requer `libgcc`, `libstdc++` e `ripgrep`. Instale-os usando o gerenciador de pacotes de sua distribuição e, em seguida, defina `USE_BUILTIN_RIPGREP=0`.

No Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Autenticação

#### Para indivíduos

1. **Plano Claude Pro ou Max** (recomendado): Inscreva-se no [plano Pro ou Max](https://claude.ai/pricing) do Claude para uma assinatura unificada que inclui Claude Code e Claude na web. Gerencie sua conta em um único lugar e faça login com sua conta Claude.ai.
2. **Claude Console**: Conecte-se através do [Claude Console](https://console.anthropic.com) e conclua o processo OAuth. Requer faturamento ativo no Console Anthropic. Um espaço de trabalho "Claude Code" é criado automaticamente para rastreamento de uso e gerenciamento de custos. Você não pode criar chaves de API para o espaço de trabalho Claude Code; é dedicado exclusivamente para uso do Claude Code.

#### Para equipes e organizações

1. **Claude for Teams ou Enterprise** (recomendado): Inscreva-se em [Claude for Teams](https://claude.com/pricing#team-&-enterprise) ou [Claude for Enterprise](https://anthropic.com/contact-sales) para faturamento centralizado, gerenciamento de equipe e acesso a Claude Code e Claude na web. Os membros da equipe fazem login com suas contas Claude.ai.
2. **Claude Console com faturamento de equipe**: Configure uma organização compartilhada do [Claude Console](https://console.anthropic.com) com faturamento de equipe. Convide membros da equipe e atribua funções para rastreamento de uso.
3. **Provedores de nuvem**: Configure Claude Code para usar [Amazon Bedrock, Google Vertex AI ou Microsoft Foundry](/pt/third-party-integrations) para implantações com sua infraestrutura de nuvem existente.

### Instalar uma versão específica

O instalador nativo aceita um número de versão específico ou um canal de lançamento (`latest` ou `stable`). O canal que você escolhe no momento da instalação se torna seu padrão para atualizações automáticas. Consulte [Configurar canal de lançamento](#configure-release-channel) para obter mais informações.

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
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Integridade binária e assinatura de código

* Somas de verificação SHA256 para todas as plataformas são publicadas nos manifestos de lançamento, atualmente localizados em `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (exemplo: substitua `{VERSION}` por `2.0.30`)
* Binários assinados são distribuídos para as seguintes plataformas:
  * macOS: Assinado por "Anthropic PBC" e notarizado pela Apple
  * Windows: Assinado por "Anthropic, PBC"

## Instalação NPM (descontinuada)

A instalação NPM está descontinuada. Use o método de [instalação nativa](#installation) quando possível. Para migrar uma instalação npm existente para nativa, execute `claude install`.

**Instalação global npm**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NÃO use `sudo npm install -g` pois isso pode levar a problemas de permissão e riscos de segurança.
  Se você encontrar erros de permissão, consulte [solução de problemas de permissão](/pt/troubleshooting#command-not-found-claude-or-permission-errors) para soluções recomendadas.
</Warning>

## Configuração do Windows

**Opção 1: Claude Code dentro do WSL**

* Tanto WSL 1 quanto WSL 2 são suportados
* WSL 2 suporta [sandboxing](/pt/sandboxing) para segurança aprimorada. WSL 1 não suporta sandboxing.

**Opção 2: Claude Code no Windows nativo com Git Bash**

* Requer [Git for Windows](https://git-scm.com/downloads/win)
* Para instalações portáteis do Git, especifique o caminho para seu `bash.exe`:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Atualizar Claude Code

### Atualizações automáticas

Claude Code se atualiza automaticamente para garantir que você tenha os recursos mais recentes e correções de segurança.

* **Verificações de atualização**: Realizadas na inicialização e periodicamente durante a execução
* **Processo de atualização**: Baixa e instala automaticamente em segundo plano
* **Notificações**: Você verá uma notificação quando as atualizações forem instaladas
* **Aplicando atualizações**: As atualizações entram em vigor na próxima vez que você iniciar Claude Code

<Note>
  As instalações do Homebrew e WinGet não se atualizam automaticamente. Use `brew upgrade claude-code` ou `winget upgrade Anthropic.ClaudeCode` para atualizar manualmente.

  **Problema conhecido:** Claude Code pode notificá-lo sobre atualizações antes que a nova versão esteja disponível nesses gerenciadores de pacotes. Se uma atualização falhar, aguarde e tente novamente mais tarde.
</Note>

### Configurar canal de lançamento

Configure qual canal de lançamento Claude Code segue para atualizações automáticas e `claude update` com a configuração `autoUpdatesChannel`:

* `"latest"` (padrão): Receba novos recursos assim que forem lançados
* `"stable"`: Use uma versão que normalmente tem cerca de uma semana de idade, pulando lançamentos com regressões importantes

Configure isso via `/config` → **Auto-update channel**, ou adicione-o ao seu [arquivo settings.json](/pt/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Para implantações empresariais, você pode impor um canal de lançamento consistente em toda a sua organização usando [configurações gerenciadas](/pt/settings#settings-files).

### Desabilitar atualizações automáticas

Defina a variável de ambiente `DISABLE_AUTOUPDATER` em seu shell ou [arquivo settings.json](/pt/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Atualizar manualmente

```bash  theme={null}
claude update
```

## Desinstalar Claude Code

Se você precisar desinstalar Claude Code, siga as instruções para seu método de instalação.

### Instalação nativa

Remova o binário Claude Code e os arquivos de versão:

**macOS, Linux, WSL:**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell:**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD:**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Instalação Homebrew

```bash  theme={null}
brew uninstall --cask claude-code
```

### Instalação WinGet

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Instalação NPM

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Limpar arquivos de configuração (opcional)

<Warning>
  Remover arquivos de configuração excluirá todas as suas configurações, ferramentas permitidas, configurações de servidor MCP e histórico de sessão.
</Warning>

Para remover as configurações e dados em cache do Claude Code:

**macOS, Linux, WSL:**

```bash  theme={null}
# Remove user settings and state
rm -rf ~/.claude
rm ~/.claude.json

# Remove project-specific settings (run from your project directory)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# Remove user settings and state
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Remove project-specific settings (run from your project directory)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM Remove user settings and state
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Remove project-specific settings (run from your project directory)
rmdir /s /q ".claude"
del ".mcp.json"
```
