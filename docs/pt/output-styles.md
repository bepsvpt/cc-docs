> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Estilos de saída

> Adapte Claude Code para usos além da engenharia de software

Os estilos de saída alteram como Claude responde, não o que Claude sabe. Eles modificam o prompt do sistema para definir papel, tom e formato de saída, mantendo capacidades principais como executar scripts, ler e escrever arquivos e rastrear TODOs. Use um quando você continua re-solicitando a mesma voz ou formato a cada turno, ou quando você quer que Claude atue como algo diferente de um engenheiro de software.

Para instruções sobre seu projeto, convenções ou base de código, use [CLAUDE.md](/pt/memory) em vez disso.

## Estilos de saída integrados

O estilo de saída **Default** do Claude Code é o prompt do sistema existente, projetado para ajudá-lo a completar tarefas de engenharia de software com eficiência.

Existem três estilos de saída integrados adicionais:

* **Proactive**: Claude executa imediatamente, faz suposições razoáveis em vez de pausar para decisões rotineiras e prefere ação ao planejamento. Isso aplica a mesma orientação que [modo automático](/pt/permission-modes#eliminate-prompts-with-auto-mode) sem alterar seu modo de permissão, portanto você ainda vê prompts de permissão antes das ferramentas serem executadas.

* **Explanatory**: Fornece "Insights" educacionais entre ajudá-lo a completar tarefas de engenharia de software. Ajuda você a entender as escolhas de implementação e padrões da base de código.

* **Learning**: Modo colaborativo de aprender fazendo, onde Claude não apenas compartilhará "Insights" enquanto codifica, mas também pedirá que você contribua com pequenos e estratégicos pedaços de código. Claude Code adicionará marcadores `TODO(human)` no seu código para você implementar.

## Como os estilos de saída funcionam

Os estilos de saída modificam diretamente o prompt do sistema do Claude Code.

* Os estilos de saída personalizados excluem instruções para codificação (como verificar código com testes), a menos que `keep-coding-instructions` seja verdadeiro.
* Todos os estilos de saída têm suas próprias instruções personalizadas adicionadas ao final do prompt do sistema.
* Todos os estilos de saída acionam lembretes para Claude aderir às instruções do estilo de saída durante a conversa.

O uso de tokens depende do estilo. Adicionar instruções ao prompt do sistema aumenta os tokens de entrada, embora o prompt caching reduza esse custo após a primeira solicitação em uma sessão. Os estilos integrados Explanatory e Learning produzem respostas mais longas que Default por design, o que aumenta os tokens de saída. Para estilos personalizados, o uso de tokens de saída depende do que suas instruções dizem ao Claude para produzir.

## Altere seu estilo de saída

Execute `/config` e selecione **Output style** para escolher um estilo de um menu. Sua seleção é salva em `.claude/settings.local.json` no [nível do projeto local](/pt/settings).

Para definir um estilo sem o menu, edite o campo `outputStyle` diretamente em um arquivo de configurações:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Como o estilo de saída é definido no prompt do sistema no início da sessão, as alterações entram em vigor na próxima vez que você iniciar uma nova sessão. Isso mantém o prompt do sistema estável durante uma conversa para que o prompt caching possa reduzir a latência e o custo.

## Crie um estilo de saída personalizado

Os estilos de saída personalizados são arquivos Markdown com frontmatter e o texto que será adicionado ao prompt do sistema:

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

Você pode salvar esses arquivos em três níveis:

* Usuário: `~/.claude/output-styles`
* Projeto: `.claude/output-styles`
* Política gerenciada: `.claude/output-styles` dentro do [diretório de configurações gerenciadas](/pt/settings#settings-files)

[Plugins](/pt/plugins-reference) também podem enviar estilos de saída em um diretório `output-styles/`.

### Frontmatter

Os arquivos de estilo de saída suportam frontmatter para especificar metadados:

| Frontmatter                | Propósito                                                                                                                                                                                                                                                                            | Padrão                   |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------- |
| `name`                     | Nome do estilo de saída, se não for o nome do arquivo                                                                                                                                                                                                                                | Herda do nome do arquivo |
| `description`              | Descrição do estilo de saída, mostrada no seletor `/config`                                                                                                                                                                                                                          | Nenhum                   |
| `keep-coding-instructions` | Se deve manter as partes do prompt do sistema do Claude Code relacionadas à codificação.                                                                                                                                                                                             | false                    |
| `force-for-plugin`         | Apenas estilos de saída de plugin: aplique este estilo automaticamente sempre que o plugin estiver habilitado, sem exigir que os usuários o selecionem. Substitui a configuração `outputStyle` do usuário. Se vários plugins habilitados definirem isso, o primeiro carregado vence. | false                    |

## Comparações com recursos relacionados

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Escolha com base em se Claude deve parar de agir como um assistente de codificação ou manter seu papel padrão e aprender mais. Os estilos de saída substituem as partes de engenharia de software do prompt do sistema do Claude Code pela sua própria função e voz, então use um quando Claude deve adotar uma identidade diferente, como um editor de redação ou um assistente de análise de dados. CLAUDE.md e `--append-system-prompt` mantêm a identidade padrão do Claude Code e adicionam a ela, então use-os quando Claude deve permanecer um assistente de codificação que também segue suas convenções de projeto ou instruções extras.

Os mecanismos também diferem. Os estilos de saída editam o prompt do sistema diretamente. CLAUDE.md adiciona seu conteúdo como uma mensagem do usuário após o prompt do sistema. `--append-system-prompt` anexa conteúdo ao final do prompt do sistema sem remover nada.

### Output Styles vs. [Agents](/pt/sub-agents)

Use um estilo de saída para alterar como a conversa principal responde em cada sessão. Use um [subagente](/pt/sub-agents) quando você quiser um auxiliar com escopo separado para o qual a conversa principal delega. Os estilos de saída afetam apenas o prompt do sistema do loop do agente principal. Os agentes lidam com tarefas específicas e podem ter seu próprio modelo, ferramentas e contexto sobre quando invocá-los.

### Output Styles vs. [Skills](/pt/skills)

Os estilos de saída modificam como Claude responde (formatação, tom, estrutura) e estão sempre ativos uma vez selecionados. Skills são prompts específicos de tarefas que você invoca com `/skill-name` ou que Claude carrega automaticamente quando relevante. Use estilos de saída para preferências de formatação consistentes; use skills para fluxos de trabalho e tarefas reutilizáveis.
