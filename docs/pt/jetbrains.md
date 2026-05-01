> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Use Claude Code with JetBrains IDEs including IntelliJ, PyCharm, WebStorm, and more

Claude Code integra-se com JetBrains IDEs através de um plugin dedicado, fornecendo recursos como visualização de diff interativa, compartilhamento de contexto de seleção e muito mais.

## IDEs Suportadas

O plugin Claude Code funciona com a maioria dos JetBrains IDEs, incluindo:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Recursos

* **Inicialização rápida**: Use `Cmd+Esc` (Mac) ou `Ctrl+Esc` (Windows/Linux) para abrir Claude Code diretamente do seu editor, ou clique no botão Claude Code na interface
* **Visualização de diff**: As alterações de código podem ser exibidas diretamente no visualizador de diff do IDE em vez do terminal
* **Contexto de seleção**: A seleção ou aba atual no IDE é compartilhada automaticamente com Claude Code
* **Atalhos de referência de arquivo**: Use `Cmd+Option+K` (Mac) ou `Alt+Ctrl+K` (Linux/Windows) para inserir referências de arquivo como `@src/auth.ts#L1-99`
* **Compartilhamento de diagnóstico**: Erros de diagnóstico do IDE, como erros de lint e sintaxe, são compartilhados automaticamente com Claude conforme você trabalha

## Instalação

### Instalação do Marketplace

Encontre e instale o [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) do marketplace JetBrains e reinicie seu IDE.

Se você ainda não instalou Claude Code, consulte o [guia de início rápido](/pt/quickstart) para instruções de instalação.

<Note>
  Após instalar o plugin, você pode precisar reiniciar completamente seu IDE para que ele entre em vigor.
</Note>

## Uso

### Do Seu IDE

Execute `claude` do terminal integrado do seu IDE, e todos os recursos de integração estarão ativos.

### De Terminais Externos

Use o comando `/ide` em qualquer terminal externo para conectar Claude Code ao seu JetBrains IDE e ativar todos os recursos:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Se você deseja que Claude tenha acesso aos mesmos arquivos do seu IDE, inicie Claude Code no mesmo diretório que a raiz do projeto do seu IDE.

## Configuração

### Configurações do Claude Code

Configure a integração do IDE através das configurações do Claude Code:

1. Execute `claude`
2. Digite o comando `/config`
3. Defina a ferramenta de diff como `auto` para mostrar diffs no IDE, ou `terminal` para mantê-los no terminal

### Configurações do Plugin

Configure o plugin Claude Code acessando **Settings → Tools → Claude Code \[Beta]**:

#### Configurações Gerais

* **Claude command**: Especifique um comando personalizado para executar Claude, por exemplo `claude`, `/usr/local/bin/claude`, ou `npx @anthropic-ai/claude-code`
* **Suppress notification for Claude command not found**: Pule notificações sobre não encontrar o comando Claude
* **Enable using Option+Enter for multi-line prompts**: apenas no macOS. Quando ativado, Option+Enter insere novas linhas em prompts do Claude Code. Desative se a tecla Option estiver sendo capturada inesperadamente. Requer reinicialização do terminal.
* **Enable automatic updates**: Verifique e instale automaticamente atualizações do plugin, aplicadas na reinicialização

<Tip>
  Para usuários WSL: Defina `wsl -d Ubuntu -- bash -lic "claude"` como seu comando Claude (substitua `Ubuntu` pelo nome da sua distribuição WSL)
</Tip>

#### Configuração da Tecla ESC

Se a tecla ESC não interromper as operações do Claude Code nos terminais JetBrains:

1. Vá para **Settings → Tools → Terminal**
2. Faça um dos seguintes:
   * Desmarque "Move focus to the editor with Escape", ou
   * Clique em "Configure terminal keybindings" e delete o atalho "Switch focus to Editor"
3. Aplique as alterações

Isso permite que a tecla ESC interrompa adequadamente as operações do Claude Code.

## Configurações Especiais

### Desenvolvimento Remoto

<Warning>
  Ao usar JetBrains Remote Development, você deve instalar o plugin no host remoto via **Settings → Plugin (Host)**.
</Warning>

O plugin deve ser instalado no host remoto, não na sua máquina cliente local.

### Configuração WSL

Se você estiver usando Claude Code no WSL2 com um JetBrains IDE e vir "No available IDEs detected", a causa geralmente é a rede NAT do WSL2 ou o Windows Firewall bloqueando a conexão entre WSL2 e o IDE em execução no host Windows. WSL1 usa a rede do host diretamente e não é afetado.

#### Permitir tráfego WSL2 através do Windows Firewall

Esta é a correção recomendada porque mantém seu modo de rede WSL2 existente.

<Steps>
  <Step title="Encontre seu endereço IP do WSL2">
    De dentro do seu shell WSL, execute:

    ```bash theme={null}
    hostname -I
    ```

    Anote a sub-rede, por exemplo `172.21.123.45` está em `172.21.0.0/16`.
  </Step>

  <Step title="Crie uma regra de firewall">
    Abra PowerShell como Administrador e execute o seguinte, ajustando o intervalo de IP para corresponder à sua sub-rede:

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="Reinicie seu IDE e Claude Code">
    Feche e reabra ambos para que a nova regra entre em vigor.
  </Step>
</Steps>

#### Mude WSL2 para rede espelhada

A rede espelhada requer Windows 11 22H2 ou posterior. Se você estiver no Windows 10, use a regra de firewall acima.

Adicione isto ao `.wslconfig` no seu diretório de usuário Windows:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Em seguida, reinicie WSL com `wsl --shutdown` do PowerShell.

## Solução de Problemas

### Plugin não funcionando

Se o plugin estiver instalado mas os recursos do Claude Code não aparecerem no seu IDE:

* Certifique-se de que você está executando Claude Code no diretório raiz do projeto
* Verifique se o plugin JetBrains está ativado nas configurações do IDE
* Reinicie completamente o IDE (você pode precisar fazer isso várias vezes)
* Para Remote Development, certifique-se de que o plugin está instalado no host remoto

### IDE não detectado

Se executar `claude` mostrar "No available IDEs detected":

* Verifique se o plugin está instalado e ativado
* Reinicie o IDE completamente
* Verifique se você está executando Claude Code no terminal integrado
* Para usuários WSL, consulte [Configuração WSL](#wsl-configuration) acima

### Comando não encontrado

Se clicar no ícone Claude mostrar "command not found":

1. Verifique se Claude Code está instalado executando `claude --version` em um terminal
2. Configure o caminho do comando Claude nas configurações do plugin
3. Para usuários WSL, use o formato de comando WSL mencionado na seção de configuração

## Considerações de Segurança

Quando Claude Code é executado em um JetBrains IDE com permissões de auto-edição ativadas, ele pode ser capaz de modificar arquivos de configuração do IDE que podem ser executados automaticamente pelo seu IDE. Isso pode aumentar o risco de executar Claude Code no modo auto-edição e permitir contornar os prompts de permissão do Claude Code para execução de bash.

Ao executar em JetBrains IDEs, considere:

* Usar modo de aprovação manual para edições
* Tomar cuidado extra para garantir que Claude seja usado apenas com prompts confiáveis
* Estar ciente de quais arquivos Claude Code tem acesso para modificar

Para problemas de instalação ou login do Claude Code fora do IDE, consulte [Solucionar problemas de instalação e login](/pt/troubleshoot-install).
