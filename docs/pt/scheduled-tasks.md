> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Executar prompts em um cronograma

> Use /loop e as ferramentas de agendamento cron para executar prompts repetidamente, pesquisar status ou definir lembretes únicos em uma sessão do Claude Code.

<Note>
  Tarefas agendadas requerem Claude Code v2.1.72 ou posterior. Verifique sua versão com `claude --version`.
</Note>

Tarefas agendadas permitem que Claude execute novamente um prompt automaticamente em um intervalo. Use-as para pesquisar uma implantação, cuidar de um PR, verificar uma compilação de longa duração ou lembrar-se de fazer algo mais tarde na sessão.

As tarefas têm escopo de sessão: elas vivem no processo atual do Claude Code e desaparecem quando você sai. Para agendamento durável que sobreviva a reinicializações e seja executado sem uma sessão de terminal ativa, consulte [tarefas agendadas do Desktop](/pt/desktop#schedule-recurring-tasks) ou [GitHub Actions](/pt/github-actions).

## Agendar um prompt recorrente com /loop

A [skill agrupada](/pt/skills#bundled-skills) `/loop` é a maneira mais rápida de agendar um prompt recorrente. Passe um intervalo opcional e um prompt, e Claude configura um trabalho cron que é acionado em segundo plano enquanto a sessão permanece aberta.

```text  theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude analisa o intervalo, o converte em uma expressão cron, agenda o trabalho e confirma a cadência e o ID do trabalho.

### Sintaxe de intervalo

Os intervalos são opcionais. Você pode colocá-los no início, no final ou omiti-los completamente.

| Forma                  | Exemplo                               | Intervalo analisado         |
| :--------------------- | :------------------------------------ | :-------------------------- |
| Token inicial          | `/loop 30m check the build`           | a cada 30 minutos           |
| Cláusula `every` final | `/loop check the build every 2 hours` | a cada 2 horas              |
| Sem intervalo          | `/loop check the build`               | padrão de a cada 10 minutos |

As unidades suportadas são `s` para segundos, `m` para minutos, `h` para horas e `d` para dias. Os segundos são arredondados para o minuto mais próximo, pois o cron tem granularidade de um minuto. Os intervalos que não se dividem uniformemente em sua unidade, como `7m` ou `90m`, são arredondados para o intervalo mais próximo e Claude informa qual foi escolhido.

### Fazer loop sobre outro comando

O prompt agendado pode ser um comando ou invocação de skill. Isso é útil para re-executar um fluxo de trabalho que você já empacotou.

```text  theme={null}
/loop 20m /review-pr 1234
```

Cada vez que o trabalho é acionado, Claude executa `/review-pr 1234` como se você tivesse digitado.

## Definir um lembrete único

Para lembretes únicos, descreva o que você deseja em linguagem natural em vez de usar `/loop`. Claude agenda uma tarefa de disparo único que se deleta após ser executada.

```text  theme={null}
remind me at 3pm to push the release branch
```

```text  theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude fixa o tempo de disparo em um minuto e hora específicos usando uma expressão cron e confirma quando será acionado.

## Gerenciar tarefas agendadas

Peça a Claude em linguagem natural para listar ou cancelar tarefas, ou referencie as ferramentas subjacentes diretamente.

```text  theme={null}
what scheduled tasks do I have?
```

```text  theme={null}
cancel the deploy check job
```

Nos bastidores, Claude usa estas ferramentas:

| Ferramenta   | Propósito                                                                                                                 |
| :----------- | :------------------------------------------------------------------------------------------------------------------------ |
| `CronCreate` | Agendar uma nova tarefa. Aceita uma expressão cron de 5 campos, o prompt a ser executado e se recorre ou dispara uma vez. |
| `CronList`   | Listar todas as tarefas agendadas com seus IDs, cronogramas e prompts.                                                    |
| `CronDelete` | Cancelar uma tarefa por ID.                                                                                               |

Cada tarefa agendada tem um ID de 8 caracteres que você pode passar para `CronDelete`. Uma sessão pode conter até 50 tarefas agendadas por vez.

## Como as tarefas agendadas são executadas

O agendador verifica a cada segundo se há tarefas vencidas e as enfileira com baixa prioridade. Um prompt agendado é acionado entre seus turnos, não enquanto Claude está no meio de uma resposta. Se Claude estiver ocupado quando uma tarefa vencer, o prompt aguarda até que o turno atual termine.

Todos os horários são interpretados em seu fuso horário local. Uma expressão cron como `0 9 * * *` significa 9h onde você está executando Claude Code, não UTC.

### Jitter

Para evitar que cada sessão acesse a API no mesmo momento do relógio de parede, o agendador adiciona um pequeno deslocamento determinístico aos tempos de disparo:

* Tarefas recorrentes disparam até 10% de seu período atrasadas, limitadas a 15 minutos. Um trabalho por hora pode disparar em qualquer lugar de `:00` a `:06`.
* Tarefas únicas agendadas para o topo ou fundo da hora disparam até 90 segundos mais cedo.

O deslocamento é derivado do ID da tarefa, portanto a mesma tarefa sempre obtém o mesmo deslocamento. Se o tempo exato for importante, escolha um minuto que não seja `:00` ou `:30`, por exemplo `3 9 * * *` em vez de `0 9 * * *`, e o jitter único não será aplicado.

### Expiração de três dias

Tarefas recorrentes expiram automaticamente 3 dias após a criação. A tarefa é acionada uma última vez e depois se deleta. Isso limita quanto tempo um loop esquecido pode ser executado. Se você precisar que uma tarefa recorrente dure mais tempo, cancele e recrie-a antes de expirar, ou use [tarefas agendadas do Desktop](/pt/desktop#schedule-recurring-tasks) para agendamento durável.

## Referência de expressão cron

`CronCreate` aceita expressões cron padrão de 5 campos: `minute hour day-of-month month day-of-week`. Todos os campos suportam curingas (`*`), valores únicos (`5`), passos (`*/15`), intervalos (`1-5`) e listas separadas por vírgula (`1,15,30`).

| Exemplo        | Significado                        |
| :------------- | :--------------------------------- |
| `*/5 * * * *`  | A cada 5 minutos                   |
| `0 * * * *`    | A cada hora na hora                |
| `7 * * * *`    | A cada hora aos 7 minutos passados |
| `0 9 * * *`    | Todos os dias às 9h local          |
| `0 9 * * 1-5`  | Dias da semana às 9h local         |
| `30 14 15 3 *` | 15 de março às 14h30 local         |

O dia da semana usa `0` ou `7` para domingo até `6` para sábado. A sintaxe estendida como `L`, `W`, `?` e aliases de nome como `MON` ou `JAN` não é suportada.

Quando tanto o dia do mês quanto o dia da semana são restritos, uma data corresponde se qualquer campo corresponder. Isso segue a semântica padrão do vixie-cron.

## Desabilitar tarefas agendadas

Defina `CLAUDE_CODE_DISABLE_CRON=1` em seu ambiente para desabilitar o agendador completamente. As ferramentas cron e `/loop` ficam indisponíveis e qualquer tarefa já agendada para de ser acionada. Consulte [Variáveis de ambiente](/pt/settings#environment-variables) para a lista completa de sinalizadores de desabilitação.

## Limitações

O agendamento com escopo de sessão tem limitações inerentes:

* As tarefas só são acionadas enquanto Claude Code está em execução e ocioso. Fechar o terminal ou deixar a sessão sair cancela tudo.
* Sem recuperação para disparos perdidos. Se o tempo agendado de uma tarefa passar enquanto Claude está ocupado em uma solicitação de longa duração, ela dispara uma vez quando Claude fica ocioso, não uma vez por intervalo perdido.
* Sem persistência entre reinicializações. Reiniciar Claude Code limpa todas as tarefas com escopo de sessão.

Para automação orientada por cron que precisa ser executada sem supervisão, use um [fluxo de trabalho do GitHub Actions](/pt/github-actions) com um gatilho `schedule`, ou [tarefas agendadas do Desktop](/pt/desktop#schedule-recurring-tasks) se você quiser um fluxo de configuração gráfico.
