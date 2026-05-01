> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting

> Corrija o alto uso de CPU ou memória, travamentos, thrashing de auto-compact e problemas de pesquisa no Claude Code, e encontre a página correta para outros problemas.

Esta página cobre problemas de desempenho, estabilidade e pesquisa uma vez que Claude Code está em execução. Para outros problemas, comece com a página que corresponde ao local onde você está preso:

| Sintoma                                                                                                   | Ir para                                                                                  |
| :-------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `command not found`, falha na instalação, problemas de PATH, `EACCES`, erros de TLS                       | [Troubleshoot installation and login](/pt/troubleshoot-install)                          |
| Loops de login, erros OAuth, `403 Forbidden`, "organization disabled", credenciais Bedrock/Vertex/Foundry | [Troubleshoot installation and login](/pt/troubleshoot-install#login-and-authentication) |
| Configurações não aplicadas, hooks não disparando, servidores MCP não carregando                          | [Debug your configuration](/pt/debug-your-config)                                        |
| `API Error: 5xx`, `529 Overloaded`, `429`, erros de validação de solicitação                              | [Error reference](/pt/errors)                                                            |
| `model not found` ou `you may not have access to it`                                                      | [Error reference](/pt/errors#theres-an-issue-with-the-selected-model)                    |
| Extensão VS Code não conectando ou detectando Claude                                                      | [VS Code integration](/pt/vs-code#fix-common-issues)                                     |
| Plugin JetBrains ou IDE não detectado                                                                     | [JetBrains integration](/pt/jetbrains#troubleshooting)                                   |
| Alto uso de CPU ou memória, respostas lentas, travamentos, pesquisa não encontrando arquivos              | [Performance and stability](#performance-and-stability) abaixo                           |

Se você não tem certeza qual se aplica, execute `/doctor` dentro do Claude Code para uma verificação automatizada de sua instalação, configurações, servidores MCP e uso de contexto. Se `claude` não iniciar completamente, execute `claude doctor` do seu shell em vez disso.

## Performance and stability

Essas seções cobrem problemas relacionados ao uso de recursos, responsividade e comportamento de pesquisa.

### Alto uso de CPU ou memória

Claude Code é projetado para funcionar com a maioria dos ambientes de desenvolvimento, mas pode consumir recursos significativos ao processar grandes bases de código. Se você está experimentando problemas de desempenho:

1. Use `/compact` regularmente para reduzir o tamanho do contexto
2. Feche e reinicie Claude Code entre tarefas principais
3. Considere adicionar grandes diretórios de compilação ao seu arquivo `.gitignore`

Se o uso de memória permanecer alto após essas etapas, execute `/heapdump` para escrever um snapshot de heap JavaScript e um detalhamento de memória para `~/Desktop`. No Linux sem uma pasta Desktop, os arquivos são escritos em seu diretório home.

O detalhamento mostra resident set size, JS heap, array buffers e memória nativa não contabilizada, o que ajuda a identificar se o crescimento está em objetos JavaScript ou em código nativo. Para inspecionar retentores, abra o arquivo `.heapsnapshot` no Chrome DevTools em Memory → Load. Anexe ambos os arquivos ao relatar um problema de memória no [GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compactação para com erro de thrashing

Se você vir `Autocompact is thrashing: the context refilled to the limit...`, a compactação automática foi bem-sucedida mas um arquivo ou saída de ferramenta imediatamente refilled a janela de contexto várias vezes seguidas. Claude Code para de tentar novamente para evitar desperdiçar chamadas de API em um loop que não está fazendo progresso.

Para recuperar:

1. Peça ao Claude para ler o arquivo oversized em pedaços menores, como um intervalo de linha específico ou função, em vez do arquivo inteiro
2. Execute `/compact` com um foco que descarta a saída grande, por exemplo `/compact keep only the plan and the diff`
3. Mova o trabalho de arquivo grande para um [subagent](/pt/sub-agents) para que ele execute em uma janela de contexto separada
4. Execute `/clear` se a conversa anterior não for mais necessária

### Comando trava ou congela

Se Claude Code parece não responsivo:

1. Pressione Ctrl+C para tentar cancelar a operação atual
2. Se não responsivo, você pode precisar fechar o terminal e reiniciar

Reiniciar não perde sua conversa. Execute `claude --resume` no mesmo diretório para retomar a sessão.

### Problemas de pesquisa e descoberta

Se a ferramenta Search, menções `@file`, agentes personalizados ou skills personalizados não estão encontrando arquivos, o binário `ripgrep` incluído pode não ser executado em seu sistema. Instale o pacote `ripgrep` da sua plataforma e diga ao Claude Code para usá-lo em vez disso:

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

Depois defina `USE_BUILTIN_RIPGREP=0` em seu [environment](/pt/env-vars).

### Resultados de pesquisa lentos ou incompletos em WSL

Penalidades de desempenho de leitura de disco ao [trabalhar entre sistemas de arquivos em WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) podem resultar em menos correspondências do que o esperado ao usar Claude Code em WSL. A pesquisa ainda funciona, mas retorna menos resultados do que em um sistema de arquivos nativo.

<Note>
  `/doctor` mostrará Search como OK neste caso.
</Note>

**Soluções:**

1. **Envie pesquisas mais específicas**: reduza o número de arquivos pesquisados especificando diretórios ou tipos de arquivo: "Search for JWT validation logic in the auth-service package" ou "Find use of md5 hash in JS files".

2. **Mova o projeto para o sistema de arquivos Linux**: se possível, certifique-se de que seu projeto está localizado no sistema de arquivos Linux (`/home/`) em vez do sistema de arquivos do Windows (`/mnt/c/`).

3. **Use Windows nativo em vez disso**: considere executar Claude Code nativamente no Windows em vez de através de WSL, para melhor desempenho do sistema de arquivos.

## Get more help

Se você está experimentando problemas não cobertos aqui:

1. Execute `/doctor` para verificar a saúde da instalação, validade das configurações, configuração de MCP e uso de contexto em uma única passagem
2. Use o comando `/feedback` dentro do Claude Code para relatar problemas diretamente à Anthropic
3. Verifique o [repositório GitHub](https://github.com/anthropics/claude-code) para problemas conhecidos
4. Pergunte ao Claude diretamente sobre suas capacidades e recursos. Claude tem acesso integrado à sua documentação.
