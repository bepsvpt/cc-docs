> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Uso de dados

> Saiba mais sobre as políticas de uso de dados da Anthropic para Claude

## Políticas de dados

### Política de treinamento de dados

**Usuários consumidores (planos Free, Pro e Max)**:
Oferecemos a você a opção de permitir que seus dados sejam usados para melhorar futuros modelos Claude. Treinaremos novos modelos usando dados de contas Free, Pro e Max quando essa configuração estiver ativada (inclusive quando você usa Claude Code dessas contas).

**Usuários comerciais**: (planos Team e Enterprise, API, plataformas de terceiros e Claude Gov) mantêm as políticas existentes: a Anthropic não treina modelos generativos usando código ou prompts enviados para Claude Code sob termos comerciais, a menos que o cliente tenha optado por fornecer seus dados para melhorias de modelo (por exemplo, o [Development Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)).

### Development Partner Program

Se você optar explicitamente por métodos para nos fornecer materiais para treinar, como através do [Development Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program), podemos usar esses materiais fornecidos para treinar nossos modelos. Um administrador da organização pode optar explicitamente pelo Development Partner Program para sua organização. Observe que este programa está disponível apenas para API de primeira parte da Anthropic, e não para usuários de Bedrock ou Vertex.

### Feedback usando o comando `/feedback`

Se você optar por nos enviar feedback sobre Claude Code usando o comando `/feedback`, podemos usar seu feedback para melhorar nossos produtos e serviços. As transcrições compartilhadas via `/feedback` são retidas por 5 anos.

### Pesquisas de qualidade de sessão

Quando você vê o prompt "How is Claude doing this session?" (Como Claude está se saindo nesta sessão?) em Claude Code, responder a esta pesquisa (inclusive selecionando "Dismiss"), apenas sua classificação numérica (1, 2, 3 ou dismiss) é registrada. Não coletamos ou armazenamos nenhuma transcrição de conversa, entradas, saídas ou outros dados de sessão como parte desta pesquisa. Diferentemente do feedback com polegar para cima/para baixo ou relatórios `/feedback`, esta pesquisa de qualidade de sessão é uma métrica simples de satisfação do produto. Suas respostas a esta pesquisa não afetam suas preferências de treinamento de dados e não podem ser usadas para treinar nossos modelos de IA.

Para desabilitar essas pesquisas, defina `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. A pesquisa também é desabilitada quando `DISABLE_TELEMETRY` ou `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` está definido. Para controlar a frequência em vez de desabilitar, defina [`feedbackSurveyRate`](/pt/settings#available-settings) em seu arquivo de configurações para uma probabilidade entre `0` e `1`.

### Retenção de dados

A Anthropic retém dados de Claude Code com base no tipo de conta e preferências.

**Usuários consumidores (planos Free, Pro e Max)**:

* Usuários que permitem o uso de dados para melhorias de modelo: período de retenção de 5 anos para suportar desenvolvimento de modelo e melhorias de segurança
* Usuários que não permitem o uso de dados para melhorias de modelo: período de retenção de 30 dias
* As configurações de privacidade podem ser alteradas a qualquer momento em [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Usuários comerciais (Team, Enterprise e API)**:

* Padrão: período de retenção de 30 dias
* [Zero data retention](/pt/zero-data-retention): disponível para Claude Code no Claude for Enterprise. ZDR é habilitado por organização; cada nova organização deve ter ZDR habilitado separadamente pela sua equipe de conta
* Cache local: os clientes de Claude Code armazenam transcrições de sessão localmente em texto simples em `~/.claude/projects/` por 30 dias por padrão para permitir retomada de sessão. Ajuste o período com `cleanupPeriodDays`. Consulte [dados da aplicação](/pt/claude-directory#application-data) para saber o que é armazenado e como limpá-lo.

Você pode excluir sessões individuais de Claude Code na web a qualquer momento. Excluir uma sessão remove permanentemente os dados de evento da sessão. Para instruções sobre como excluir sessões, consulte [Excluir sessões](/pt/claude-code-on-the-web#delete-sessions).

Saiba mais sobre práticas de retenção de dados em nosso [Privacy Center](https://privacy.anthropic.com/).

Para detalhes completos, consulte nossos [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (para usuários de Team, Enterprise e API) ou [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (para usuários de Free, Pro e Max) e [Privacy Policy](https://www.anthropic.com/legal/privacy).

## Acesso a dados

Para todos os usuários de primeira parte, você pode aprender mais sobre quais dados são registrados para [Claude Code local](#local-claude-code-data-flow-and-dependencies) e [Claude Code remoto](#cloud-execution-data-flow-and-dependencies). As sessões de [Remote Control](/pt/remote-control) seguem o fluxo de dados local, pois toda a execução acontece em sua máquina. Observe que para Claude Code remoto, Claude acessa o repositório onde você inicia sua sessão de Claude Code. Claude não acessa repositórios que você conectou mas não iniciou uma sessão.

## Local Claude Code: Fluxo de dados e dependências

O diagrama abaixo mostra como Claude Code se conecta a serviços externos durante a instalação e operação normal. Linhas sólidas indicam conexões obrigatórias, enquanto linhas tracejadas representam fluxos de dados opcionais ou iniciados pelo usuário.

<img src="https://mintcdn.com/claude-code/YcBW2H7CArGcduPb/images/claude-code-data-flow.svg?fit=max&auto=format&n=YcBW2H7CArGcduPb&q=85&s=b600a89f84fc86f9ff7be00a466c0635" alt="Diagram showing Claude Code's external connections: install/update connects to the distribution server, and user requests connect to Anthropic services including Console auth, public-api, and optionally Statsig, Sentry, and bug reporting" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code é executado localmente. Para interagir com o LLM, Claude Code envia dados pela rede. Esses dados incluem todos os prompts do usuário e saídas do modelo, criptografados em trânsito via TLS 1.2+. Claude Code é compatível com a maioria dos VPNs e proxies LLM populares.

A criptografia em repouso depende do seu provedor de modelo:

| Provedor               | Criptografia em repouso                                                                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anthropic API          | Criptografia de disco em nível de infraestrutura (AES-256). Ative [Zero Data Retention](/pt/zero-data-retention) para nenhuma persistência no servidor. |
| Amazon Bedrock         | AES-256 com chaves gerenciadas pela AWS. Chaves gerenciadas pelo cliente disponíveis via AWS KMS.                                                       |
| Google Cloud Vertex AI | Chaves de criptografia gerenciadas pelo Google. CMEK disponível.                                                                                        |
| Microsoft Foundry      | Solicitações são roteadas para infraestrutura Anthropic com criptografia de disco AES-256.                                                              |

Claude Code é construído nas APIs da Anthropic. Para detalhes sobre controles de segurança da API, incluindo procedimentos de logging de API, consulte os artefatos de conformidade no [Anthropic Trust Center](https://trust.anthropic.com).

### Cloud execution: Fluxo de dados e dependências

Ao usar [Claude Code on the web](/pt/claude-code-on-the-web), as sessões são executadas em máquinas virtuais gerenciadas pela Anthropic em vez de localmente. Em ambientes de nuvem:

* **Armazenamento de código e dados:** Seu repositório é clonado para uma VM isolada. Código e dados de sessão estão sujeitos às políticas de retenção e uso para seu tipo de conta (consulte a seção Retenção de dados acima)
* **Credenciais:** A autenticação do GitHub é tratada através de um proxy seguro; suas credenciais do GitHub nunca entram na sandbox
* **Tráfego de rede:** Todo o tráfego de saída passa por um proxy de segurança para logging de auditoria e prevenção de abuso
* **Dados de sessão:** Prompts, alterações de código e saídas seguem as mesmas políticas de dados que o uso local de Claude Code

Para detalhes de segurança sobre execução em nuvem, consulte [Security](/pt/security#cloud-execution-security).

## Serviços de telemetria

Claude Code se conecta de máquinas dos usuários ao serviço Statsig para registrar métricas operacionais como latência, confiabilidade e padrões de uso. Este logging não inclui nenhum código ou caminho de arquivo. Os dados são criptografados em trânsito usando TLS e em repouso usando criptografia AES de 256 bits. Leia mais na [documentação de segurança do Statsig](https://www.statsig.com/trust/security). Para desabilitar a telemetria do Statsig, defina a variável de ambiente `DISABLE_TELEMETRY`.

Claude Code se conecta de máquinas dos usuários ao Sentry para logging de erros operacionais. Os dados são criptografados em trânsito usando TLS e em repouso usando criptografia AES de 256 bits. Leia mais na [documentação de segurança do Sentry](https://sentry.io/security/). Para desabilitar o logging de erros, defina a variável de ambiente `DISABLE_ERROR_REPORTING`.

Quando os usuários executam o comando `/feedback`, uma cópia do histórico completo de conversa incluindo código é enviada para a Anthropic. Os dados são criptografados em trânsito usando TLS. Opcionalmente, um problema do GitHub é criado no repositório público. Para desabilitar, defina a variável de ambiente `DISABLE_FEEDBACK_COMMAND` como `1`.

## Comportamentos padrão por provedor de API

Por padrão, relatório de erros, telemetria e relatório de bugs são desabilitados ao usar Bedrock, Vertex ou Foundry. Pesquisas de qualidade de sessão e a verificação de segurança de domínio WebFetch são exceções e são executadas independentemente do provedor. Você pode desabilitar todo o tráfego não essencial, incluindo pesquisas, de uma vez definindo `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Esta variável não afeta a verificação WebFetch, que tem seu próprio opt-out. Aqui estão os comportamentos padrão completos:

| Serviço                                          | Claude API                                                                                       | Vertex API                                                                                       | Bedrock API                                                                                      | Foundry API                                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **Statsig (Métricas)**                           | Padrão ativado.<br />`DISABLE_TELEMETRY=1` para desabilitar.                                     | Padrão desativado.<br />`CLAUDE_CODE_USE_VERTEX` deve ser 1.                                     | Padrão desativado.<br />`CLAUDE_CODE_USE_BEDROCK` deve ser 1.                                    | Padrão desativado.<br />`CLAUDE_CODE_USE_FOUNDRY` deve ser 1.                                    |
| **Sentry (Erros)**                               | Padrão ativado.<br />`DISABLE_ERROR_REPORTING=1` para desabilitar.                               | Padrão desativado.<br />`CLAUDE_CODE_USE_VERTEX` deve ser 1.                                     | Padrão desativado.<br />`CLAUDE_CODE_USE_BEDROCK` deve ser 1.                                    | Padrão desativado.<br />`CLAUDE_CODE_USE_FOUNDRY` deve ser 1.                                    |
| **Claude API (relatórios `/feedback`)**          | Padrão ativado.<br />`DISABLE_FEEDBACK_COMMAND=1` para desabilitar.                              | Padrão desativado.<br />`CLAUDE_CODE_USE_VERTEX` deve ser 1.                                     | Padrão desativado.<br />`CLAUDE_CODE_USE_BEDROCK` deve ser 1.                                    | Padrão desativado.<br />`CLAUDE_CODE_USE_FOUNDRY` deve ser 1.                                    |
| **Pesquisas de qualidade de sessão**             | Padrão ativado.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` para desabilitar.                   | Padrão ativado.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` para desabilitar.                   | Padrão ativado.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` para desabilitar.                   | Padrão ativado.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` para desabilitar.                   |
| **Verificação de segurança de domínio WebFetch** | Padrão ativado.<br />`skipWebFetchPreflight: true` em [settings](/pt/settings) para desabilitar. | Padrão ativado.<br />`skipWebFetchPreflight: true` em [settings](/pt/settings) para desabilitar. | Padrão ativado.<br />`skipWebFetchPreflight: true` em [settings](/pt/settings) para desabilitar. | Padrão ativado.<br />`skipWebFetchPreflight: true` em [settings](/pt/settings) para desabilitar. |

Todas as variáveis de ambiente podem ser verificadas em `settings.json` (consulte [referência de configurações](/pt/settings)).

### Verificação de segurança de domínio WebFetch

Antes de buscar uma URL, a ferramenta WebFetch envia o nome do host solicitado para `api.anthropic.com` para verificá-lo em relação a uma lista de bloqueio de segurança mantida pela Anthropic. Apenas o nome do host é enviado, não a URL completa, caminho ou conteúdo da página. Os resultados são armazenados em cache por nome do host por cinco minutos.

Esta verificação é executada independentemente de qual provedor de modelo você usa e não é afetada por `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Se sua rede bloqueia `api.anthropic.com`, as solicitações WebFetch falham até que você permita o domínio ou defina `skipWebFetchPreflight: true` em [settings](/pt/settings). Desabilitar a verificação significa que WebFetch tenta recuperar qualquer URL sem consultar a lista de bloqueio, portanto combine com [regras de permissão `WebFetch`](/pt/permissions#webfetch) se precisar restringir quais domínios Claude pode acessar.
