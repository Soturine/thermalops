# ADR-0007: Self-Service como ExperienceProfile policy-driven

- Status: Accepted for product/architecture direction
- Date: 2026-09-07

## Context

Alguns ambientes podem permitir que o próprio end user execute diagnosis básico, consulte status/health, siga troubleshooting guiado e prepare evidence para suporte. Em ambientes corporativos, a aplicação pode ser previamente aprovada/distribuída pela TI e usada depois sem nova intervenção por sessão.

Criar uma edição separada para esse caso duplicaria produto, Domain logic e deployment complexity. Também seria perigoso tratar uma UI simplificada como authorization boundary.

## Decision

Modelar `SelfService` como um `ExperienceProfile`, não como uma nova edição.

```text
Edition
  Portable Lite / Portable Pro / Enterprise

ExperienceProfile
  SelfService / Technician / AdvancedSupport
```

Effective capability é a interseção de:

```text
Executable capability
∩ Device capability
∩ Organization policy
∩ User/asset scope
∩ ExperienceProfile
∩ Runtime constraints
```

`ExperienceProfile` só restringe/apresenta; nunca concede uma capability ausente ou negada.

## Self-Service defaults

Self-Service é read-only-first e standard-user-first.

Default allowed surface:

- status/Health summary;
- Quick Diagnosis;
- Guided Troubleshooting aprovado;
- Knowledge Center;
- Preventive/Maintenance status;
- sanitized evidence/report;
- ServiceCase/support request.

Default denied surface:

- Spooler restart;
- driver install/remove;
- firmware update;
- factory/network reset;
- arbitrary printer config write;
- AdvancedSupport raw controls;
- UAC-dependent repair in normal flow.

Low-risk write capabilities podem ser avaliadas futuramente por explicit policy e validation, sem alterar esse default.

## Corporate deployment semantics

O objetivo é **pre-approval**, não bypass.

Em managed environments, uma organization pode publicar/aprovar ThermalOps via enterprise software distribution. Depois, end users podem executar o app dentro da policy autorizada sem precisar abrir chamado para instalar/elevar a cada diagnosis.

ThermalOps deve cooperar com WDAC/App Control, AppLocker, EDR, firewall, proxy e removable-media controls. Quando uma feature for bloqueada, retorna status explícito e oferece fallback/escalation; não sugere desabilitar controles.

## Domain consistency

SelfService, Technician e AdvancedSupport usam o mesmo:

- `DiagnosticEvidence`;
- `DiagnosticFinding`;
- `HealthAssessment`;
- `MaintenanceDue`;
- `ServiceDisposition`;
- `GuidanceSession`.

Somente presentation/progressive disclosure e available use cases mudam.

Isso evita dois motores que possam discordar sobre o estado da mesma printer.

## Asset scope

Managed Self-Service pode limitar devices por `AssignedAssetScope`, site, department ou explicit assignment.

Friendly name não é authorization identity. `PrinterIdentity` continua canônica e multi-source.

Portable Lite não depende de central identity; opera somente dentro de seu compiled read-only envelope e local/explicit targets permitidos.

## Support handoff

Quando guidance não resolve:

```text
Diagnosis
 -> Guidance
 -> NotResolved / EscalationRecommended
 -> sanitized ServiceCase draft
 -> privacy preview
 -> export or configured helpdesk connector
```

Helpdesk integration é optional Adapter/Application boundary e não entra como hard-coded employer workflow.

## Consequences

Positive:

- lower support friction;
- ticket deflection para problemas simples;
- no duplicate product edition;
- same Domain truth across personas;
- clear standard-user security posture;
- compatible with managed enterprise deployment.

Costs:

- policy/capability matrix tests;
- user/asset scope design for Enterprise;
- accessibility burden maior;
- plain-language UX/localization review;
- helpdesk/privacy integration complexity.

## Alternatives rejected

### Separate Client Edition

Rejeitada por duplicar packaging, roadmap e feature matrix sem necessidade de Domain diferente.

### Technician UI with hidden advanced buttons

Rejeitada porque obscurity não é authorization e gera poor UX.

### Require administrator credentials for Self-Service repair

Rejeitada como normal flow. Self-Service deve escalar quando a action sair do envelope autorizado.

### Bypass corporate controls

Explicitamente proibido.

## Related docs

- `docs/produto/self-service.md`
- `docs/produto/guided-operations-e-knowledge.md`
- `docs/seguranca/self-service-e-guided-operations-threat-model.md`
- `docs/engenharia/validation-matrix-lifecycle-guidance-self-service.md`
