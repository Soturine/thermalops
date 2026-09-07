# Documentação do ThermalOps

Este diretório organiza a documentação por responsabilidade para evitar mistura entre product requirements, engineering design, security, research e planning.

A estrutura segue a Engineering Constitution: decisões de Domain ficam separadas de Infrastructure/UI; architecture decisions relevantes usam ADR; research não vira business truth automaticamente; e capabilities futuras carregam validation status explícito.

## Navegação

### Produto

- [Visão do Produto](produto/visao-do-produto.md)
- [Portable](produto/portable.md)
- [Preventive Maintenance](produto/manutencao-preventiva.md)
- [Lifecycle e Health](produto/lifecycle-e-health.md)
- [Guided Operations e Knowledge](produto/guided-operations-e-knowledge.md)
- [Self-Service / End-User Experience](produto/self-service.md)
- [Field Service, Triage e Escalation](produto/field-service-e-escalation.md)
- [Fleet e Condition Monitoring](produto/fleet-e-condition-monitoring.md)
- [AI e Knowledge Assistance](produto/ai-e-knowledge-assistance.md)
- [Localização e Terminologia](produto/localizacao-e-terminologia.md)

### Engenharia

- [Arquitetura](engenharia/arquitetura.md)
- [Guided Operations Architecture](engenharia/guided-operations-architecture.md)
- [Validation Matrix — Lifecycle, Guidance e Self-Service](engenharia/validation-matrix-lifecycle-guidance-self-service.md)
- [Diagnóstico e Local Remediation](engenharia/diagnostico-e-remediacao-local.md)
- [Deployment e Application Lifecycle](engenharia/deployment-e-lifecycle.md)
- [Support Bundles e Service Cases](engenharia/support-bundles-e-service-cases.md)
- [Testing](engenharia/testing.md)
- [Release Engineering](engenharia/release-engineering.md)

### Segurança

- [Security e Privacy](seguranca/security-e-privacy.md)
- [Threat Model — Self-Service, Guided Operations e Knowledge](seguranca/self-service-e-guided-operations-threat-model.md)

### Pesquisa

- [Referências e Padrões Externos](pesquisa/referencias-e-padroes.md)
- [Pesquisa 2026 — Zebra Guided Operations, Lifecycle e Self-Service Corporativo](pesquisa/zebra-guidance-self-service-2026.md)

### Planejamento

- [Roadmap](planejamento/roadmap.md)
- [Auditoria M0 — Lifecycle, Guidance e Self-Service](planejamento/auditoria-m0-lifecycle-guidance-self-service.md)

### Architecture Decision Records

- [ADR-0001 — C#/.NET 10 e WPF](adr/0001-stack-and-desktop-ui.md)
- [ADR-0002 — Temporary Privileged Helper](adr/0002-privileged-helper.md)
- [ADR-0003 — Field Service e Preventive Scope](adr/0003-field-service-and-preventive-scope.md)
- [ADR-0004 — Maintenance e Health Model](adr/0004-maintenance-and-health-model.md)
- [ADR-0005 — Localization e Technical Language](adr/0005-localization-and-technical-language.md)
- [ADR-0006 — Guided Operations e Knowledge](adr/0006-guided-operations-and-knowledge.md)
- [ADR-0007 — Self-Service Experience e Policy](adr/0007-self-service-experience-and-policy.md)
- [ADR-0008 — Lifecycle, Health e RUL Semantics](adr/0008-lifecycle-health-and-rul-semantics.md)

## Novas boundaries formalizadas

A documentação agora diferencia explicitamente:

```text
CurrentHealth != RemainingLifeEstimate
Usage != Wear proof
ExperienceProfile != Authorization
Runbook != Script
Knowledge != Executable control plane
GuidedManual != AssistedWrite
Vendor capability != Policy permission
Self-Service != IT bypass
```

Essas diferenças são importantes porque a UI pode parecer simples enquanto o Domain precisa preservar semântica, source, applicability, authorization e uncertainty.

## Convenção de idioma

A documentação narrativa é escrita em **pt-BR**, preservando termos técnicos em inglês quando são nomes estabelecidos de arquitetura, APIs, protocolos, Domain concepts, tooling ou práticas de software.

Exemplos preservados:

`Domain`, `Application`, `Infrastructure`, `Adapter`, `Policy`, `Baseline`, `RepairPlan`, `ServiceCase`, `ServiceDisposition`, `HealthAssessment`, `GuidanceSession`, `Runbook`, `ExperienceProfile`, `RemainingLifeEstimate`, `Spooler`, `WinSpool`, `PnP`, `Event Log`, `Link-OS`, `SGD`, `ZPL`, `CI/CD`, `SBOM` e `RBAC`.

O objetivo é documentação natural para quem trabalha em português sem perder precisão técnica.

## Fonte de verdade

A ordem de autoridade é:

1. `ENGINEERING_CONSTITUTION.md`;
2. ADRs aceitos para decisões arquiteturais;
3. documentos de produto/engineering/security aplicáveis;
4. roadmap e issues para planejamento;
5. research como referência externa, nunca como business rule automaticamente válida.

Se dois documentos entrarem em conflito, a divergência deve ser resolvida explicitamente. Não escolher silenciosamente a versão mais conveniente.

## Regras de source e validation

Vendor documentation pode justificar capability candidates e source-backed procedures, mas não prova que a feature foi implementada ou validada no ThermalOps.

Uma capability só deve ser anunciada como suportada quando, conforme o risco, existirem:

- official interface/source review;
- applicability model;
- parser/Domain tests;
- integration tests;
- HIL para vendor-native claims;
- failure-path/security tests para writes;
- known limitations;
- documentation matching implementation.

Uma operation existir no painel/manual de uma printer não significa que exista API programática equivalente para todos os models.

## Self-Service governance

Self-Service é `ExperienceProfile`, não edição e não authorization boundary isolada. Effective capabilities sempre dependem da interseção de build, device, organization policy, user/asset scope, profile e runtime constraints.

Em corporate environments, o objetivo é pre-approval/distribution controlada. ThermalOps não tenta contornar WDAC/App Control, AppLocker, EDR, firewall, proxy ou privilege controls.

## Knowledge governance

Runbooks e Knowledge Packs são data-only. Não aceitam arbitrary scripts, DLLs ou general-purpose expression engines.

Official/vendor docs podem ser linked/retrieved; redistribution offline exige review de licença. AI pode explicar/retrieval, mas não converte document text em executable authority.

## Lifecycle governance

`Lifecycle e Health` preserva idade, usage, component condition, maintenance, current health e RUL como concepts separados.

`RemainingLifeEstimate` permanece `Unavailable`/`NotValidated` até cumprir M9 validation; não é derivado de fórmula arbitrária ou LLM.

## Status e completude

Os documentos descrevem direção aprovada e capabilities futuras; isso não significa implementation pronta.

Status permitidos:

- `fixed` — implementado e required validation concluída;
- `partial` — acceptance criteria ainda faltam;
- `experimental` — funciona em subset/controlled conditions;
- `deferred` — adiado intencionalmente;
- `not validated` — implementação existe sem required validation.

O status global permanece **M0 / foundation** até os exit criteria correspondentes serem concluídos. A licença do projeto permanece uma decisão M0 pendente.
