> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Rastreie e reverta automaticamente as edições do Claude para recuperar-se rapidamente de alterações indesejadas.

Claude Code rastreia automaticamente as edições de arquivo do Claude conforme você trabalha, permitindo que você desfaça rapidamente as alterações e reverta para estados anteriores se algo sair do caminho.

## Como o checkpointing funciona

Conforme você trabalha com Claude, o checkpointing captura automaticamente o estado do seu código antes de cada edição. Esta rede de segurança permite que você realize tarefas ambiciosas e em larga escala sabendo que sempre pode retornar a um estado de código anterior.

### Rastreamento automático

Claude Code rastreia todas as alterações feitas por suas ferramentas de edição de arquivo:

* Cada prompt do usuário cria um novo checkpoint
* Os checkpoints persistem entre sessões, para que você possa acessá-los em conversas retomadas
* Limpeza automática junto com as sessões após 30 dias (configurável)

### Revertendo alterações

Pressione `Esc` duas vezes (`Esc` + `Esc`) ou use o comando `/rewind` para abrir o menu de rewind. Você pode escolher restaurar:

* **Apenas conversa**: Reverta para uma mensagem do usuário mantendo as alterações de código
* **Apenas código**: Reverta as alterações de arquivo mantendo a conversa
* **Código e conversa**: Restaure ambos para um ponto anterior na sessão

## Casos de uso comuns

Os checkpoints são particularmente úteis quando:

* **Explorando alternativas**: Experimente diferentes abordagens de implementação sem perder seu ponto de partida
* **Recuperando de erros**: Desfaça rapidamente as alterações que introduziram bugs ou quebraram a funcionalidade
* **Iterando em recursos**: Experimente variações sabendo que você pode reverter para estados funcionais

## Limitações

### Alterações de comando Bash não rastreadas

O checkpointing não rastreia arquivos modificados por comandos bash. Por exemplo, se Claude Code executar:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Essas modificações de arquivo não podem ser desfeitas através de rewind. Apenas edições diretas de arquivo feitas através das ferramentas de edição de arquivo do Claude são rastreadas.

### Alterações externas não rastreadas

O checkpointing rastreia apenas arquivos que foram editados na sessão atual. Alterações manuais que você faz em arquivos fora do Claude Code e edições de outras sessões simultâneas normalmente não são capturadas, a menos que modifiquem os mesmos arquivos da sessão atual.

### Não é um substituto para controle de versão

Os checkpoints são projetados para recuperação rápida no nível da sessão. Para histórico de versão permanente e colaboração:

* Continue usando controle de versão (ex. Git) para commits, branches e histórico de longo prazo
* Os checkpoints complementam mas não substituem o controle de versão adequado
* Pense em checkpoints como "desfazer local" e Git como "histórico permanente"

## Veja também

* [Modo interativo](/pt/interactive-mode) - Atalhos de teclado e controles de sessão
* [Comandos integrados](/pt/interactive-mode#built-in-commands) - Acessando checkpoints usando `/rewind`
* [Referência CLI](/pt/cli-reference) - Opções de linha de comando
