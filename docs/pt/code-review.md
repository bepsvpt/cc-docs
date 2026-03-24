> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Configure análises automatizadas de PR que detectam erros de lógica, vulnerabilidades de segurança e regressões usando análise multi-agente de sua base de código completa

<Note>
  Code Review está em visualização de pesquisa, disponível para assinaturas [Teams e Enterprise](https://claude.ai/admin-settings/claude-code). Não está disponível para organizações com [Zero Data Retention](/pt/zero-data-retention) ativado.
</Note>

Code Review analisa seus pull requests do GitHub e publica descobertas como comentários inline nas linhas de código onde encontrou problemas. Uma frota de agentes especializados examina as alterações de código no contexto de sua base de código completa, procurando por erros de lógica, vulnerabilidades de segurança, casos extremos quebrados e regressões sutis.

As descobertas são marcadas por severidade e não aprovam ou bloqueiam seu PR, portanto os fluxos de trabalho de revisão existentes permanecem intactos. Você pode ajustar o que Claude sinaliza adicionando um arquivo `CLAUDE.md` ou `REVIEW.md` ao seu repositório.

Para executar Claude em sua própria infraestrutura de CI em vez deste serviço gerenciado, consulte [GitHub Actions](/pt/github-actions) ou [GitLab CI/CD](/pt/gitlab-ci-cd).

Esta página cobre:

* [Como as revisões funcionam](#how-reviews-work)
* [Configuração](#set-up-code-review)
* [Personalizando revisões](#customize-reviews) com `CLAUDE.md` e `REVIEW.md`
* [Preços](#pricing)

## Como as revisões funcionam

Depois que um administrador [ativa Code Review](#set-up-code-review) para sua organização, as revisões são acionadas quando um PR é aberto, em cada push ou quando solicitado manualmente, dependendo do comportamento configurado do repositório. Comentar `@claude review` [inicia revisões em um PR](#manually-trigger-reviews) em qualquer modo.

Quando uma revisão é executada, vários agentes analisam o diff e o código circundante em paralelo na infraestrutura da Anthropic. Cada agente procura por uma classe diferente de problema, então uma etapa de verificação verifica os candidatos contra o comportamento real do código para filtrar falsos positivos. Os resultados são desduplicados, classificados por severidade e publicados como comentários inline nas linhas específicas onde os problemas foram encontrados. Se nenhum problema for encontrado, Claude publica um breve comentário de confirmação no PR.

As revisões escalam em custo com o tamanho e complexidade do PR, completando em média em 20 minutos. Os administradores podem monitorar a atividade de revisão e gastos através do [painel de análise](#view-usage).

### Níveis de severidade

Cada descoberta é marcada com um nível de severidade:

| Marcador | Severidade    | Significado                                                             |
| :------- | :------------ | :---------------------------------------------------------------------- |
| 🔴       | Normal        | Um bug que deve ser corrigido antes de fazer merge                      |
| 🟡       | Nit           | Um problema menor, vale a pena corrigir mas não é bloqueante            |
| 🟣       | Pré-existente | Um bug que existe na base de código mas não foi introduzido por este PR |

As descobertas incluem uma seção de raciocínio estendido recolhível que você pode expandir para entender por que Claude sinalizou o problema e como verificou o problema.

### O que Code Review verifica

Por padrão, Code Review se concentra em correção: bugs que quebrariam a produção, não preferências de formatação ou cobertura de testes ausente. Você pode expandir o que verifica [adicionando arquivos de orientação](#customize-reviews) ao seu repositório.

## Configurar Code Review

Um administrador ativa Code Review uma vez para a organização e seleciona quais repositórios incluir.

<Steps>
  <Step title="Abrir configurações de administrador do Claude Code">
    Vá para [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) e encontre a seção Code Review. Você precisa de acesso de administrador à sua organização Claude e permissão para instalar GitHub Apps em sua organização GitHub.
  </Step>

  <Step title="Iniciar configuração">
    Clique em **Setup**. Isso inicia o fluxo de instalação do GitHub App.
  </Step>

  <Step title="Instalar o Claude GitHub App">
    Siga os prompts para instalar o Claude GitHub App em sua organização GitHub. O app solicita estas permissões de repositório:

    * **Contents**: leitura e escrita
    * **Issues**: leitura e escrita
    * **Pull requests**: leitura e escrita

    Code Review usa acesso de leitura a conteúdos e acesso de escrita a pull requests. O conjunto de permissões mais amplo também suporta [GitHub Actions](/pt/github-actions) se você ativar isso mais tarde.
  </Step>

  <Step title="Selecionar repositórios">
    Escolha quais repositórios ativar para Code Review. Se você não vir um repositório, certifique-se de que deu ao Claude GitHub App acesso a ele durante a instalação. Você pode adicionar mais repositórios mais tarde.
  </Step>

  <Step title="Definir gatilhos de revisão por repo">
    Após a conclusão da configuração, a seção Code Review mostra seus repositórios em uma tabela. Para cada repositório, use o dropdown **Review Behavior** para escolher quando as revisões são executadas:

    * **Once after PR creation**: a revisão é executada uma vez quando um PR é aberto ou marcado como pronto para revisão
    * **After every push**: a revisão é executada em cada push para o branch do PR, detectando novos problemas conforme o PR evolui e resolvendo automaticamente threads quando você corrige problemas sinalizados
    * **Manual**: as revisões começam apenas quando alguém [comenta `@claude review` em um PR](#manually-trigger-reviews); pushes subsequentes para esse PR são então revisados automaticamente

    Revisar em cada push executa a maioria das revisões e custa mais. O modo Manual é útil para repositórios de alto tráfego onde você deseja optar PRs específicos para revisão, ou para começar a revisar seus PRs apenas quando estiverem prontos.
  </Step>
</Steps>

A tabela de repositórios também mostra o custo médio por revisão para cada repo com base na atividade recente. Use o menu de ações de linha para ativar ou desativar Code Review por repositório, ou para remover um repositório completamente.

Para verificar a configuração, abra um PR de teste. Se você escolheu um gatilho automático, uma execução de verificação chamada **Claude Code Review** aparece em alguns minutos. Se você escolheu Manual, comente `@claude review` no PR para iniciar a primeira revisão. Se nenhuma execução de verificação aparecer, confirme que o repositório está listado em suas configurações de administrador e que o Claude GitHub App tem acesso a ele.

## Acionador manual de revisões

Comente `@claude review` em um pull request para iniciar uma revisão e optar esse PR em revisões acionadas por push a partir de então. Isso funciona independentemente do gatilho configurado do repositório: use-o para optar PRs específicos para revisão no modo Manual, ou para obter uma re-revisão imediata em outros modos. De qualquer forma, pushes para esse PR acionam revisões a partir de então.

Para o comentário acionar uma revisão:

* Poste-o como um comentário de PR de nível superior, não um comentário inline em uma linha de diff
* Coloque `@claude review` no início do comentário
* Você deve ter acesso de proprietário, membro ou colaborador ao repositório
* O PR deve estar aberto e não ser um rascunho

Se uma revisão já estiver em execução nesse PR, a solicitação é enfileirada até que a revisão em andamento seja concluída. Você pode monitorar o progresso através da execução de verificação no PR.

## Personalizar revisões

Code Review lê dois arquivos do seu repositório para orientar o que sinaliza. Ambos são aditivos além das verificações de correção padrão:

* **`CLAUDE.md`**: instruções de projeto compartilhadas que Claude Code usa para todas as tarefas, não apenas revisões. Use-o quando a orientação também se aplica a sessões interativas do Claude Code.
* **`REVIEW.md`**: orientação exclusiva de revisão, lida exclusivamente durante revisões de código. Use-o para regras que são estritamente sobre o que sinalizar ou pular durante a revisão e que confundiriam seu `CLAUDE.md` geral.

### CLAUDE.md

Code Review lê seus arquivos `CLAUDE.md` do repositório e trata violações recém-introduzidas como descobertas de nível nit. Isso funciona bidirecionalmente: se seu PR altera o código de uma forma que torna uma declaração `CLAUDE.md` desatualizada, Claude sinaliza que os docs precisam ser atualizados também.

Claude lê arquivos `CLAUDE.md` em cada nível de sua hierarquia de diretórios, portanto as regras no `CLAUDE.md` de um subdiretório se aplicam apenas aos arquivos sob esse caminho. Consulte a [documentação de memória](/pt/memory) para mais informações sobre como `CLAUDE.md` funciona.

Para orientação específica de revisão que você não deseja aplicada a sessões gerais do Claude Code, use [`REVIEW.md`](#review-md) em vez disso.

### REVIEW\.md

Adicione um arquivo `REVIEW.md` à raiz do seu repositório para regras específicas de revisão. Use-o para codificar:

* Diretrizes de estilo da empresa ou equipe: "prefira retornos antecipados sobre condicionais aninhados"
* Convenções específicas de linguagem ou framework não cobertas por linters
* Coisas que Claude deve sempre sinalizar: "qualquer nova rota de API deve ter um teste de integração"
* Coisas que Claude deve pular: "não comente sobre formatação em código gerado sob `/gen/`"

Exemplo `REVIEW.md`:

```markdown  theme={null}
# Diretrizes de Code Review

## Sempre verificar
- Novos endpoints de API têm testes de integração correspondentes
- Migrações de banco de dados são compatíveis com versões anteriores
- Mensagens de erro não vazam detalhes internos para usuários

## Estilo
- Prefira declarações `match` sobre verificações `isinstance` encadeadas
- Use logging estruturado, não interpolação de f-string em chamadas de log

## Pular
- Arquivos gerados sob `src/gen/`
- Alterações apenas de formatação em arquivos `*.lock`
```

Claude descobre automaticamente `REVIEW.md` na raiz do repositório. Nenhuma configuração necessária.

## Ver uso

Vá para [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) para ver a atividade de Code Review em toda sua organização. O painel mostra:

| Seção                | O que mostra                                                                                                       |
| :------------------- | :----------------------------------------------------------------------------------------------------------------- |
| PRs reviewed         | Contagem diária de pull requests revisados durante o intervalo de tempo selecionado                                |
| Cost weekly          | Gasto semanal em Code Review                                                                                       |
| Feedback             | Contagem de comentários de revisão que foram resolvidos automaticamente porque um desenvolvedor abordou o problema |
| Repository breakdown | Contagens por repo de PRs revisados e comentários resolvidos                                                       |

A tabela de repositórios nas configurações de administrador também mostra custo médio por revisão para cada repo.

## Preços

Code Review é faturado com base no uso de tokens. As revisões custam em média \$15-25, escalando com o tamanho do PR, complexidade da base de código e quantos problemas requerem verificação. O uso de Code Review é faturado separadamente através de [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) e não conta contra o uso incluído do seu plano.

O gatilho de revisão que você escolhe afeta o custo total:

* **Once after PR creation**: é executado uma vez por PR
* **After every push**: é executado em cada push, multiplicando o custo pelo número de pushes
* **Manual**: sem revisões até que alguém comente `@claude review` em um PR

Em qualquer modo, comentar `@claude review` [opta o PR em revisões acionadas por push](#manually-trigger-reviews), portanto custo adicional acumula por push após esse comentário.

Os custos aparecem em sua fatura da Anthropic independentemente de sua organização usar AWS Bedrock ou Google Vertex AI para outros recursos do Claude Code. Para definir um limite de gasto mensal para Code Review, vá para [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) e configure o limite para o serviço Claude Code Review.

Monitore gastos através do gráfico de custo semanal em [analytics](#view-usage) ou da coluna de custo médio por repo nas configurações de administrador.

## Recursos relacionados

Code Review é projetado para funcionar junto com o resto do Claude Code. Se você deseja executar revisões localmente antes de abrir um PR, precisa de uma configuração auto-hospedada ou deseja aprofundar como `CLAUDE.md` molda o comportamento do Claude em todas as ferramentas, estas páginas são bons próximos passos:

* [Plugins](/pt/discover-plugins): navegue no marketplace de plugins, incluindo um plugin `code-review` para executar revisões sob demanda localmente antes de fazer push
* [GitHub Actions](/pt/github-actions): execute Claude em seus próprios fluxos de trabalho do GitHub Actions para automação personalizada além de code review
* [GitLab CI/CD](/pt/gitlab-ci-cd): integração Claude auto-hospedada para pipelines GitLab
* [Memory](/pt/memory): como arquivos `CLAUDE.md` funcionam em Claude Code
* [Analytics](/pt/analytics): rastreie o uso de Claude Code além de code review
