# Documentação do ThermalOps

Este diretório organiza a documentação por responsabilidade para evitar mistura entre product requirements, engineering design, security, research e planning.

A estrutura segue a Engineering Constitution: decisões de Domain ficam separadas de detalhes de Infrastructure/UI; decisões arquiteturais relevantes usam ADR; documentos de research não são tratados como fonte de business truth; e status de implementação deve ser descrito com precisão.

## Navegação

### Produto

- [Visão do Produto](produto/visao-do-produto.md)
- [Portable](produto/portable.md)
- [Preventive Maintenance](produto/manutencao-preventiva.md)
- [Field Service, Triage e Escalation](produto/field-service-e-escalation.md)
- [Fleet e Condition Monitoring](produto/fleet-e-condition-monitoring.md)
- [AI e Knowledge Assistance](produto/ai-e-knowledge-assistance.md)
- [Localização e Terminologia](produto/localizacao-e-terminologia.md)

### Engenharia

- [Arquitetura](engenharia/arquitetura.md)
- [Diagnóstico e Local Remediation](engenharia/diagnostico-e-remediacao-local.md)
- [Deployment e Application Lifecycle](engenharia/deployment-e-lifecycle.md)
- [Support Bundles e Service Cases](engenharia/support-bundles-e-service-cases.md)
- [Testing](engenharia/testing.md)
- [Release Engineering](engenharia/release-engineering.md)

### Segurança

- [Security e Privacy](seguranca/security-e-privacy.md)

### Pesquisa

- [Referências e Padrões Externos](pesquisa/referencias-e-padroes.md)

### Planejamento

- [Roadmap](planejamento/roadmap.md)

### Architecture Decision Records

- [ADR-0001 — C#/.NET 10 e WPF](adr/0001-stack-and-desktop-ui.md)
- [ADR-0002 — Temporary Privileged Helper](adr/0002-privileged-helper.md)
- [ADR-0003 — Field Service e Preventive Scope](adr/0003-field-service-and-preventive-scope.md)
- [ADR-0004 — Maintenance e Health Model](adr/0004-maintenance-and-health-model.md)
- [ADR-0005 — Localization e Technical Language](adr/0005-localization-and-technical-language.md)

## Convenção de idioma

A documentação narrativa é escrita em **pt-BR**, preservando termos técnicos em inglês quando são nomes estabelecidos de arquitetura, APIs, protocolos, Domain concepts, tooling ou práticas de software.

Não traduzimos literalmente termos como `Domain`, `Application`, `Infrastructure`, `Adapter`, `Policy`, `Baseline`, `RepairPlan`, `ServiceCase`, `ServiceDisposition`, `HealthAssessment`, `Spooler`, `WinSpool`, `PnP`, `Event Log`, `Link-OS`, `SGD`, `ZPL`, `CI/CD`, `SBOM` e `RBAC` apenas para deixar a frase “100% portuguesa”.

O objetivo é documentação natural para quem trabalha em português sem perder precisão técnica.

## Fonte de verdade

A ordem de autoridade é:

1. `ENGINEERING_CONSTITUTION.md`;
2. ADRs aceitos para decisões arquiteturais;
3. documentos de produto/engineering/security aplicáveis;
4. roadmap e issues para planejamento;
5. research como referência externa, nunca como business rule automaticamente válida.

Se dois documentos entrarem em conflito, a divergência deve ser resolvida explicitamente; não é permitido escolher silenciosamente a versão mais conveniente.

## Status e completude

Os documentos descrevem a direção aprovada do produto, inclusive capabilities futuras. Isso não significa que todas estejam implementadas.

Use os seguintes termos:

- `fixed` — implementado e validado;
- `partial` — parte dos acceptance criteria ainda falta;
- `experimental` — suporte limitado/condicionado;
- `deferred` — intencionalmente adiado;
- `not validated` — existe implementação, mas a validação necessária ainda não ocorreu.

O status atual global permanece **M0 / foundation** até os exit criteria correspondentes serem concluídos.
