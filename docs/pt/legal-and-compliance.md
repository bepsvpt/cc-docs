> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Legal e conformidade

> Acordos legais, certificações de conformidade e informações de segurança para Claude Code.

## Acordos legais

### Licença

Seu uso do Claude Code está sujeito a:

* [Termos Comerciais](https://www.anthropic.com/legal/commercial-terms) - para usuários de Team, Enterprise e Claude API
* [Termos de Serviço do Consumidor](https://www.anthropic.com/legal/consumer-terms) - para usuários de Free, Pro e Max

### Acordos comerciais

Se você está usando a Claude API diretamente (1P) ou acessando-a através do AWS Bedrock ou Google Vertex (3P), seu acordo comercial existente será aplicado ao uso do Claude Code, a menos que tenhamos acordado mutuamente de outra forma.

## Conformidade

### Conformidade em saúde (BAA)

Se um cliente tem um Business Associate Agreement (BAA) conosco e deseja usar Claude Code, o BAA será automaticamente estendido para cobrir Claude Code se o cliente tiver executado um BAA e tiver [Zero Data Retention (ZDR)](/pt/zero-data-retention) ativado. O BAA será aplicável ao tráfego de API desse cliente fluindo através do Claude Code. ZDR é habilitado por organização, portanto cada organização deve ter ZDR habilitado separadamente para ser coberta sob o BAA.

## Política de uso

### Uso aceitável

O uso do Claude Code está sujeito à [Política de Uso da Anthropic](https://www.anthropic.com/legal/aup). Os limites de uso anunciados para os planos Pro e Max assumem uso ordinário e individual do Claude Code e do Agent SDK.

### Autenticação e uso de credenciais

Claude Code autentica com os servidores da Anthropic usando tokens OAuth ou chaves de API. Esses métodos de autenticação servem a propósitos diferentes:

* **Autenticação OAuth** (usada com planos Free, Pro e Max) é destinada exclusivamente para Claude Code e Claude.ai. Usar tokens OAuth obtidos através de contas Claude Free, Pro ou Max em qualquer outro produto, ferramenta ou serviço — incluindo o [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) — não é permitido e constitui uma violação dos [Termos de Serviço do Consumidor](https://www.anthropic.com/legal/consumer-terms).
* **Desenvolvedores** que constroem produtos ou serviços que interagem com as capacidades do Claude, incluindo aqueles que usam o [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview), devem usar autenticação por chave de API através do [Claude Console](https://platform.claude.com/) ou um provedor de nuvem suportado. A Anthropic não permite que desenvolvedores terceirizados ofereçam login Claude.ai ou roteiem solicitações através de credenciais de plano Free, Pro ou Max em nome de seus usuários.

A Anthropic se reserva o direito de tomar medidas para fazer cumprir essas restrições e pode fazê-lo sem aviso prévio.

Para perguntas sobre métodos de autenticação permitidos para seu caso de uso, por favor [entre em contato com vendas](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=legal_compliance_contact_sales).

## Segurança e confiança

### Confiança e segurança

Você pode encontrar mais informações no [Centro de Confiança da Anthropic](https://trust.anthropic.com) e [Hub de Transparência](https://www.anthropic.com/transparency).

### Relatório de vulnerabilidades de segurança

A Anthropic gerencia nosso programa de segurança através do HackerOne. [Use este formulário para relatar vulnerabilidades](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability).

***

© Anthropic PBC. Todos os direitos reservados. O uso está sujeito aos Termos de Serviço aplicáveis da Anthropic.
