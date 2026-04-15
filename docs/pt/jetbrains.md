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
* **Contexto de seleção**: A seleção/aba atual no IDE é compartilhada automaticamente com Claude Code
* **Atalhos de referência de arquivo**: Use `Cmd+Option+K` (Mac) ou `Alt+Ctrl+K` (Linux/Windows) para inserir referências de arquivo (por exemplo, @File#L1-99)
* **Compartilhamento de diagnóstico**: Erros de diagnóstico (lint, sintaxe, etc.) do IDE são compartilhados automaticamente com Claude conforme você trabalha

## Instalação

### Instalação do Marketplace

Encontre e instale o [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) do marketplace JetBrains e reinicie seu IDE.

Se você ainda não instalou Claude Code, consulte [nosso guia de início rápido](/pt/quickstart) para instruções de instalação.

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
3. Defina a ferramenta de diff como `auto` para detecção automática do IDE

### Configurações do Plugin

Configure o plugin Claude Code acessando **Settings → Tools → Claude Code \[Beta]**:

#### Configurações Gerais

* **Claude command**: Especifique um comando personalizado para executar Claude (por exemplo, `claude`, `/usr/local/bin/claude`, ou `npx @anthropic/claude`)
* **Suppress notification for Claude command not found**: Pule notificações sobre não encontrar o comando Claude
* **Enable using Option+Enter for multi-line prompts** (apenas macOS): Quando ativado, Option+Enter insere novas linhas em prompts do Claude Code. Desative se estiver tendo problemas com a tecla Option sendo capturada inesperadamente (requer reinicialização do terminal)
* **Enable automatic updates**: Verifique e instale automaticamente atualizações do plugin (aplicadas na reinicialização)

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

<Warning>
  Usuários WSL podem precisar de configuração adicional para que a detecção do IDE funcione corretamente. Consulte nosso [guia de solução de problemas WSL](/pt/troubleshooting#jetbrains-ide-not-detected-on-wsl2) para instruções de configuração detalhadas.
</Warning>

A configuração WSL pode exigir:

* Configuração adequada do terminal
* Ajustes do modo de rede
* Atualizações de configurações de firewall

## Solução de Problemas

### Plugin Não Funcionando

* Certifique-se de que você está executando Claude Code no diretório raiz do projeto
* Verifique se o plugin JetBrains está ativado nas configurações do IDE
* Reinicie completamente o IDE (você pode precisar fazer isso várias vezes)
* Para Remote Development, certifique-se de que o plugin está instalado no host remoto

### IDE Não Detectado

* Verifique se o plugin está instalado e ativado
* Reinicie o IDE completamente
* Verifique se você está executando Claude Code no terminal integrado
* Para usuários WSL, consulte o [guia de solução de problemas WSL](/pt/troubleshooting#jetbrains-ide-not-detected-on-wsl2)

### Comando Não Encontrado

Se clicar no ícone Claude mostrar "command not found":

1. Verifique se Claude Code está instalado: `npm list -g @anthropic-ai/claude-code`
2. Configure o caminho do comando Claude nas configurações do plugin
3. Para usuários WSL, use o formato de comando WSL mencionado na seção de configuração

## Considerações de Segurança

Quando Claude Code é executado em um JetBrains IDE com permissões de auto-edição ativadas, ele pode ser capaz de modificar arquivos de configuração do IDE que podem ser executados automaticamente pelo seu IDE. Isso pode aumentar o risco de executar Claude Code no modo auto-edição e permitir contornar os prompts de permissão do Claude Code para execução de bash.

Ao executar em JetBrains IDEs, considere:

* Usar modo de aprovação manual para edições
* Tomar cuidado extra para garantir que Claude seja usado apenas com prompts confiáveis
* Estar ciente de quais arquivos Claude Code tem acesso para modificar

Para obter ajuda adicional, consulte nosso [guia de solução de problemas](/pt/troubleshooting).
