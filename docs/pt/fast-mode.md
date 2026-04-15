> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Acelere respostas com modo rápido

> Obtenha respostas mais rápidas do Opus 4.6 no Claude Code alternando o modo rápido.

<Note>
  O modo rápido está em [visualização de pesquisa](#research-preview). O recurso, preços e disponibilidade podem mudar com base no feedback.
</Note>

O modo rápido é uma configuração de alta velocidade para Claude Opus 4.6, tornando o modelo 2,5x mais rápido a um custo maior por token. Ative-o com `/fast` quando você precisar de velocidade para trabalho interativo como iteração rápida ou depuração ao vivo, e desative-o quando o custo importa mais do que a latência.

O modo rápido não é um modelo diferente. Ele usa o mesmo Opus 4.6 com uma configuração de API diferente que prioriza a velocidade sobre a eficiência de custo. Você obtém qualidade e capacidades idênticas, apenas respostas mais rápidas.

<Note>
  O modo rápido requer Claude Code v2.1.36 ou posterior. Verifique sua versão com `claude --version`.
</Note>

O que você precisa saber:

* Use `/fast` para alternar o modo rápido no CLI do Claude Code. Também disponível via `/fast` na Extensão Claude Code VS Code.
* O preço do modo rápido para Opus 4.6 começa em \$30/150 MTok. O modo rápido está disponível com desconto de 50% para todos os planos até 23:59 PT em 16 de fevereiro.
* Disponível para todos os usuários do Claude Code em planos de assinatura (Pro/Max/Team/Enterprise) e Claude Console.
* Para usuários do Claude Code em planos de assinatura (Pro/Max/Team/Enterprise), o modo rápido está disponível apenas via uso extra e não está incluído nos limites de taxa de assinatura.

Esta página cobre como [alternar o modo rápido](#toggle-fast-mode), seu [tradeoff de custo](#understand-the-cost-tradeoff), [quando usá-lo](#decide-when-to-use-fast-mode), [requisitos](#requirements), [opt-in por sessão](#require-per-session-opt-in) e [comportamento de limite de taxa](#handle-rate-limits).

## Alternar modo rápido

Alterne o modo rápido de uma destas formas:

* Digite `/fast` e pressione Tab para alternar ativado ou desativado
* Defina `"fastMode": true` no seu [arquivo de configurações do usuário](/pt/settings)

Por padrão, o modo rápido persiste entre sessões. Os administradores podem configurar o modo rápido para ser redefinido a cada sessão. Consulte [require per-session opt-in](#require-per-session-opt-in) para obter detalhes.

Para melhor eficiência de custo, ative o modo rápido no início de uma sessão em vez de alternar no meio da conversa. Consulte [understand the cost tradeoff](#understand-the-cost-tradeoff) para obter detalhes.

Quando você ativa o modo rápido:

* Se você estiver em um modelo diferente, o Claude Code alterna automaticamente para Opus 4.6
* Você verá uma mensagem de confirmação: "Fast mode ON"
* Um pequeno ícone `↯` aparece ao lado do prompt enquanto o modo rápido está ativo
* Execute `/fast` novamente a qualquer momento para verificar se o modo rápido está ativado ou desativado

Quando você desativa o modo rápido com `/fast` novamente, você permanece no Opus 4.6. O modelo não reverte para seu modelo anterior. Para alternar para um modelo diferente, use `/model`.

## Entender o tradeoff de custo

O modo rápido tem preços por token mais altos do que o Opus 4.6 padrão:

| Modo                             | Entrada (MTok) | Saída (MTok) |
| -------------------------------- | -------------- | ------------ |
| Modo rápido no Opus 4.6 (\<200K) | \$30           | \$150        |
| Modo rápido no Opus 4.6 (>200K)  | \$60           | \$225        |

O modo rápido é compatível com a janela de contexto estendida de 1M token.

Quando você alterna para o modo rápido no meio de uma conversa, você paga o preço total do token de entrada não armazenado em cache do modo rápido para todo o contexto da conversa. Isso custa mais do que se você tivesse ativado o modo rápido desde o início.

## Decidir quando usar o modo rápido

O modo rápido é melhor para trabalho interativo onde a latência de resposta importa mais do que o custo:

* Iteração rápida em mudanças de código
* Sessões de depuração ao vivo
* Trabalho sensível ao tempo com prazos apertados

O modo padrão é melhor para:

* Tarefas autônomas longas onde a velocidade importa menos
* Processamento em lote ou pipelines CI/CD
* Cargas de trabalho sensíveis ao custo

### Modo rápido vs nível de esforço

O modo rápido e o nível de esforço afetam a velocidade de resposta, mas de formas diferentes:

| Configuração                    | Efeito                                                                                                      |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Modo rápido**                 | Mesma qualidade de modelo, latência mais baixa, custo mais alto                                             |
| **Nível de esforço mais baixo** | Menos tempo de pensamento, respostas mais rápidas, qualidade potencialmente mais baixa em tarefas complexas |

Você pode combinar ambos: use o modo rápido com um [nível de esforço](/pt/model-config#adjust-effort-level) mais baixo para máxima velocidade em tarefas diretas.

## Requisitos

O modo rápido requer todos os seguintes:

* **Não disponível em provedores de nuvem de terceiros**: o modo rápido não está disponível no Amazon Bedrock, Google Vertex AI ou Microsoft Azure Foundry. O modo rápido está disponível através da API do Anthropic Console e para planos de assinatura Claude usando uso extra.
* **Uso extra ativado**: sua conta deve ter o uso extra ativado, o que permite cobrança além do uso incluído no seu plano. Para contas individuais, ative isso nas suas [configurações de cobrança do Console](https://platform.claude.com/settings/organization/billing). Para Teams e Enterprise, um administrador deve ativar o uso extra para a organização.

<Note>
  O uso do modo rápido é cobrado diretamente no uso extra, mesmo que você tenha uso restante no seu plano. Isso significa que os tokens do modo rápido não contam contra o uso incluído do seu plano e são cobrados à taxa do modo rápido desde o primeiro token.
</Note>

* **Habilitação de administrador para Teams e Enterprise**: o modo rápido está desativado por padrão para organizações Teams e Enterprise. Um administrador deve explicitamente [ativar o modo rápido](#enable-fast-mode-for-your-organization) antes que os usuários possam acessá-lo.

<Note>
  Se seu administrador não tiver ativado o modo rápido para sua organização, o comando `/fast` mostrará "Fast mode has been disabled by your organization."
</Note>

### Ativar modo rápido para sua organização

Os administradores podem ativar o modo rápido em:

* **Console** (clientes de API): [Preferências do Claude Code](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Teams e Enterprise): [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

Outra opção para desativar completamente o modo rápido é definir `CLAUDE_CODE_DISABLE_FAST_MODE=1`. Consulte [Variáveis de ambiente](/pt/env-vars).

### Require per-session opt-in

Por padrão, o modo rápido persiste entre sessões: se um usuário ativa o modo rápido, ele permanece ativado em futuras sessões. Os administradores em planos [Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) ou [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) podem evitar isso definindo `fastModePerSessionOptIn` como `true` em [managed settings](/pt/settings#settings-files) ou [server-managed settings](/pt/server-managed-settings). Isso faz com que cada sessão comece com o modo rápido desativado, exigindo que os usuários o ativem explicitamente com `/fast`.

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

Isso é útil para controlar custos em organizações onde os usuários executam várias sessões simultâneas. Os usuários ainda podem ativar o modo rápido com `/fast` quando precisam de velocidade, mas ele é redefinido no início de cada nova sessão. A preferência de modo rápido do usuário ainda é salva, portanto remover essa configuração restaura o comportamento padrão persistente.

## Lidar com limites de taxa

O modo rápido tem limites de taxa separados do Opus 4.6 padrão. Quando você atinge o limite de taxa do modo rápido ou fica sem créditos de uso extra:

1. O modo rápido automaticamente volta para Opus 4.6 padrão
2. O ícone `↯` fica cinza para indicar cooldown
3. Você continua trabalhando com velocidade e preços padrão
4. Quando o cooldown expira, o modo rápido é automaticamente reativado

Para desativar o modo rápido manualmente em vez de esperar pelo cooldown, execute `/fast` novamente.

## Research preview

O modo rápido é um recurso de visualização de pesquisa. Isso significa:

* O recurso pode mudar com base no feedback
* A disponibilidade e preços estão sujeitos a alterações
* A configuração de API subjacente pode evoluir

Relate problemas ou feedback através de seus canais de suporte Anthropic usuais.

## Veja também

* [Configuração de modelo](/pt/model-config): alterne modelos e ajuste níveis de esforço
* [Gerenciar custos efetivamente](/pt/costs): rastreie o uso de tokens e reduza custos
* [Configuração da linha de status](/pt/statusline): exiba informações de modelo e contexto
