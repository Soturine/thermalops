# Auditoria M0 — Lifecycle, Guided Operations e Self-Service

## Objetivo

Esta auditoria verifica se as novas ideias discutidas para ThermalOps — Lifecycle/Health, usage/counters, component condition, Guided Operations, model-aware Knowledge, native diagnostics, Commissioning, Return-to-Service e Self-Service — ficaram amarradas ao Domain, Architecture, Security, Testing, Roadmap e Engineering Constitution sem criar gaps ou claims não validados.

A auditoria é documental/M0. Ela não transforma capabilities futuras em implementation validada.

## Baseline auditado

Baseline antes desta expansão:

- modular monolith;
- Windows-first;
- Zebra-first Vendor Adapter;
- Portable Lite/Pro/Enterprise;
- read-only-first;
- evidence-driven diagnosis;
- Preventive Maintenance source-backed;
- ServiceCase/escalation;
- Fleet/Condition Monitoring futuro;
- optional AI;
- Engineering Constitution como highest authority.

Novos requisitos auditados:

```text
Lifecycle & Health
Usage / odometer / counters
Component condition
Hours-of-use semantics
Remaining Useful Life boundary
Guided Troubleshooting
Model-aware manuals/runbooks
Knowledge Packs offline
Native printer diagnostics/self-tests
Calibration / print quality diagnostics
Security Assessment
Commissioning
Return-to-Service
Client/End-User Self-Service
Managed corporate deployment
Helpdesk connector direction
```

## Finding A — Health, vida útil e uso estavam parcialmente misturados

### Gap

`HealthAssessment` já existia, mas ainda faltava uma contract explícita separando:

- asset age;
- usage counters;
- component condition;
- maintenance compliance;
- current health;
- condition trend;
- remaining life estimate.

Sem essa separação, uma future UI poderia inferir lifetime a partir de age/usage ou usar `Health Score` como prediction.

### Resolution

Criados:

- `docs/produto/lifecycle-e-health.md`;
- ADR-0008;
- validation matrix específica.

Semantics fixadas:

```text
Age != Health
Usage != Wear proof
Health Score != RUL
Unknown != 0
RUL = unavailable/not validated by default
```

### Status

`fixed` no design/documentation; implementation `not validated` porque ainda não existe M1-M3 code/HIL.

## Finding B — OperatingHours poderia ser assumido indevidamente

### Gap

Official Zebra Link-OS documentation confirma odometer/counter capabilities em printers compatíveis, mas isso não prova um universal `OperatingHours` field para todos os models.

### Resolution

`UsageMetric` é capability-driven. `OperatingHours` e `PowerOnHours` são Domain candidates que só são populated quando source/interface e HIL comprovarem support.

States explícitos:

```text
Unsupported
Unknown
Unavailable
Success(value)
```

Nunca usar zero para ausência de dado.

### Status

`fixed` semanticamente; per-model support `not validated`.

## Finding C — Guided Troubleshooting não tinha architecture própria

### Gap

Diagnosis já produzia evidence/findings/recommendations, mas faltava modelar um workflow passo a passo que:

- pula checks já resolvidos por evidence;
- verifica applicability;
- mostra manual instructions;
- resolve typed actions;
- rechecks outcome;
- preserva timeline.

### Resolution

Criados:

- `docs/produto/guided-operations-e-knowledge.md`;
- `docs/engenharia/guided-operations-architecture.md`;
- ADR-0006;
- `GuidanceSession`, `Runbook`, `RunbookStep`, `CanonicalSymptom`, `ActionSafetyClass`, `SourceReference` como Domain candidates.

### Status

Design `fixed`; implementation `not validated`.

## Finding D — Runbook poderia virar script engine

### Gap

Uma implementação ingênua de guided troubleshooting poderia armazenar PowerShell, commands ou dynamic expressions em JSON/Markdown.

Isso violaria least privilege e o privileged-helper model.

### Resolution

Runbooks são data-only, sem general-purpose scripting. Steps podem apenas usar deterministic small rule model e `ActionReference` para registered compiled actions.

Unknown action never executes.

Threat model cobre Knowledge Pack abuse e runbook execution.

### Status

`fixed` no architecture contract.

## Finding E — Manuals/Knowledge offline tinham licensing gap

### Gap

“Colocar os manuais dentro do app” poderia implicar redistribution de copyrighted vendor content sem autorização.

### Resolution

Três source modes definidos:

- official link;
- local Knowledge Pack apenas com conteúdo redistributable/authorized ou ThermalOps-authored metadata/summaries;
- future approved online retrieval.

`KnowledgeSource` preserva publisher, URL, version/date, license/redistribution status, trust class e applicability.

### Status

`fixed` como governance. Licença por source/package continua review-required.

## Finding F — Native diagnostics poderiam ser confundidos com read-only

### Gap

Calibration, diagnostic label e alguns self-tests consomem mídia ou alteram printer state, embora pareçam “diagnóstico”.

### Resolution

Introduzido `ActionSafetyClass` e explicit `stateChange` semantics.

Examples:

```text
Configuration view/report -> classify by actual implementation
Print quality report/test -> may consume media; not readonly by assumption
Calibration -> AssistedWrite
Factory/network reset -> HighImpact
```

`--readonly` e Self-Service reject state-changing actions.

### Status

`fixed` no design; each action implementation requires source/HIL.

## Finding G — Feature existir no manual não prova API programática

### Gap

Um onboard printer tool pode ser acionável pelo front panel/manual sem existir uma SDK method estável para todas as printers.

### Resolution

Roadmap/validation requirement: each native action requires official interface mapping + applicability + HIL before support claim.

### Status

`fixed` como validation rule.

## Finding H — Zebra SettingsProvider podia virar arbitrary config writer

### Gap

Settings APIs podem expor muitos settings, inclusive writable. Um generic “write any setting name/value” seria equivalente a ampliar risky command surface.

### Resolution

Separadas:

```text
CanReadSetting(X)
CanWriteSetting(X)
AllowedRange(X)
PolicyAllowsWrite(X)
```

Future writes são allowlisted/typed e não um generic privileged string interface.

### Status

`fixed` architecture/security; implementation `not validated`.

## Finding I — Self-Service poderia virar nova edição desnecessária

### Gap

Uma `Client Edition` separada criaria duplicate packaging, duplicate diagnosis logic e long-term drift.

### Resolution

ADR-0007 define `SelfService` como `ExperienceProfile`.

Edition e experience são orthogonal:

```text
Portable Lite / Portable Pro / Enterprise
        x
SelfService / Technician / AdvancedSupport
```

### Status

`fixed` no product architecture.

## Finding J — ExperienceProfile poderia ser confundido com authorization

### Gap

Esconder buttons não impede direct invocation de Application methods.

### Resolution

Effective capability definida por intersection:

```text
ExecutableCapabilities
∩ DeviceCapabilities
∩ OrganizationPolicy
∩ UserAssetScope
∩ ExperienceProfile
∩ RuntimeConstraints
```

Application/execution boundary revalidates policy. Portable Lite remains structurally read-only.

### Status

`fixed` design; tests required in implementation.

## Finding K — “Sem permissão da TI” precisava de boundary correta

### Gap

Frase poderia ser interpretada como bypass de AppLocker/WDAC/firewall/EDR.

### Resolution

Product requirement corrigido para:

> IT/organization may approve/distribute once; the end user can use repeatedly without per-session elevation/installation, while all endpoint controls remain authoritative.

Managed software catalogs são deployment patterns, não bypass.

### Status

`fixed`.

## Finding L — Self-Service não tinha standard-user/no-UAC contract

### Gap

Um diagnostic app para end user que pede admin credential perde o principal valor e cria security risk.

### Resolution

Self-Service default é standard-user/read-only, sem UAC no normal flow. Se operation exigir privilege, UI normalmente oferece support/escalation em vez de pedir administrator credential.

### Status

`fixed` design; E2E pending.

## Finding M — Self-Service poderia expor toda a Fleet

### Gap

Managed user não deve automaticamente ver/diagnosticar todos os assets.

### Resolution

`AssignedAssetScope`/RBAC future design. Friendly name não é authorization identity. Portable Lite remains local/explicit-target only.

### Status

Design `fixed`; Enterprise identity/RBAC deferred to M5/M6 ADR.

## Finding N — Helpdesk integration poderia hard-code employer flow

### Gap

URLs, ticket queues, SLA, credentials e proprietary fields não pertencem ao public core.

### Resolution

Future `IServiceDeskConnector` Adapter/Application port. Handoff format continua `ServiceCase`.

Connector receives redacted/approved payload only after privacy preview.

### Status

`fixed` architecture direction; connector implementation deferred.

## Finding O — Helpdesk connector poderia virar remote command channel

### Gap

Bidirectional ticket integrations podem evoluir para executing instructions coming from ticket text.

### Resolution

Initial connector is outbound support submission only. Inbound remote automation requires separate ADR/threat model.

### Status

`fixed`.

## Finding P — Ticket deflection poderia incentivar comportamento inseguro

### Gap

Se KPI principal for “reduzir chamados”, product could continue guidance mesmo com uncertainty/critical condition.

### Resolution

`InsufficientEvidence` e `EscalationRecommended` são valid outcomes. Metrics cannot disable escalation. Safety/authority outrank ticket volume.

### Status

`fixed` product/security rule.

## Finding Q — AI poderia tomar o controle do Assistente Técnico

### Gap

Natural-language symptom input cria tentação de deixar AI escolher/executar repair.

### Resolution

AI pode mapear text -> candidate canonical symptom e explicar source/evidence. Deterministic engine resolves runbook/action. Model output cannot authorize ActionType.

### Status

`fixed`.

## Finding R — Online docs/RAG introduzem prompt injection

### Gap

Vendor/community web content é untrusted e pode conter instructions contra o system/application policy.

### Resolution

Retrieved text is content only, never authority. Source allowlist, size bounds, citations e AI prompt-injection defenses required. No action direct from retrieved text.

### Status

`fixed` threat model; M8 implementation pending.

## Finding S — Commissioning podia virar um “configure everything” privilegiado

### Gap

Setup de nova printer envolve driver, queue, port, device config, calibration e test print com diferentes privileges/rollback semantics.

### Resolution

`CommissioningPlan` é phased. Cada state-changing phase remains typed, scoped, policy-gated and verified.

### Status

`fixed` design direction; implementation deferred.

## Finding T — Return-to-Service precisava re-identificar equipamento

### Gap

Printer returning from service may be replacement device behind same queue/friendly name.

### Resolution

Return-to-Service re-resolves `PrinterIdentity` before applying baseline or comparison. Firmware/capability changes are reviewed before write-back.

### Status

`fixed`.

## Finding U — Security Assessment poderia auto-hardening

### Gap

Security baseline drift could lead to automatic disabling/enabling of network protocols without approval.

### Resolution

Security Assessment is read-only-first and produces `SecurityFinding`. Automatic hardening is separate high-impact capability.

### Status

`fixed`.

## Finding V — Knowledge Pack trust could incorrectly grant capabilities

### Gap

Signed/trusted pack might be treated like executable authorization.

### Resolution

Signature changes provenance/trust of data only. Pack cannot add compiled ActionType or override executable/policy capability envelope.

### Status

`fixed`.

## Finding W — Privacy de usage/lifecycle

### Gap

Counters/history may reveal production intensity even without document content.

### Resolution

Usage becomes operational metadata subject to classification, retention and export policy. Self-Service can hide exact counters. No document contents required for usage.

### Status

`fixed` design; data-classification refinement remains when schemas exist.

## Finding X — Observability dos guided workflows

### Gap

Sem structured events seria difícil saber qual runbook/step/action led to a result.

### Resolution

Architecture defines events such as `GuidanceSessionStarted`, `RunbookResolved`, `RunbookStepVerified`, `GuidanceActionBlocked`, `HealthAssessmentProduced` e `ServiceRequestSubmitted`.

### Status

`fixed` design; implementation pending.

## Finding Y — Documentation governance

### Gap

Novas features poderiam ficar em um único giant product doc ou docs flat.

### Resolution

Created responsibility-specific files in:

```text
docs/produto/
docs/engenharia/
docs/seguranca/
docs/adr/
docs/planejamento/
```

Index and validation script are updated to require them.

### Status

`fixed`.

## Finding Z — Roadmap placement

### Gap

Guidance/Self-Service could be implemented prematurely as AI/Enterprise work.

### Resolution

Recommended sequencing:

```text
M0 semantics/ADRs/threat model
M1 read-only evidence + guidance primitives
M2 safe remediation foundation
M3 Zebra capability/status/counters
M4 guided preventive/support workflows + local Knowledge Pack foundation
M5 managed Self-Service/deployment/helpdesk integration direction
M6 Fleet health/history/condition trends
M8 AI/RAG explanation/retrieval
M9 RUL/predictive research
```

Guidance does not depend on AI.

### Status

`fixed` planning direction; roadmap document/issue backlog must remain aligned as implementation evolves.

## Engineering Constitution compliance

### Business/Domain correctness

Pass: new concepts are explicit and separated. UI/profile cannot redefine Domain truth.

### Safety/security

Pass at design level: ActionSafetyClass, no runbook scripts, no IT bypass, no automatic high-impact action, dedicated threat model.

### Authorization/privacy

Pass at design level: ExperienceProfile not authorization, asset scope, policy intersection, privacy preview, usage metadata classification.

### Reliability/recoverability

Pass at design level: state-changing guidance reuses RepairPlan/preflight/verification/recovery discipline.

### Maintainability/testability

Pass at design level: data-only runbooks, typed actions, explicit ports, dedicated validation matrix, no duplicate Client Edition.

### UX/accessibility

Pass in requirements: Self-Service progressive disclosure, plain language, no color-only state, keyboard/screen-reader/scaling requirements.

### Performance/efficiency

No new performance claim. Knowledge/Guidance metrics are measurable; no forced realtime/network scan.

### Architecture

Pass: modular monolith preserved; no new microservice/project required without boundary proof.

### Offline-first

Pass: deterministic guidance can use local Knowledge Pack; cloud/AI optional.

### Honest status

Pass: all capabilities remain M0 design / planned / not validated until implementation and HIL where required.

## Remaining open items

Esses itens são intentionally open, não documentation gaps escondidos:

```text
Project license decision (M0)
Exact Zebra model/firmware capability matrix (M3/HIL)
Exact API path for each native diagnostic action (M3/M4 research/HIL)
Knowledge Pack redistribution rights per source
Enterprise authentication/RBAC topology
Packaging technology (MSI/MSIX/etc.)
Specific ServiceDesk connectors and credentials model
Production signing identity
RUL/predictive model/data (M9)
```

Cada item possui milestone/ADR requirement; nenhum deve ser “preenchido” com assumption.

## Audit conclusion

A expansão não exige microservices, new cloud dependency, new edition ou AI control plane. As capabilities novas se encaixam no modular monolith e reutilizam evidence, policy, RepairPlan, ServiceCase, Vendor Adapter e localization boundaries existentes.

O principal design improvement foi separar claramente:

```text
knowledge from authority
experience from authorization
health from lifetime prediction
capability from permission
manual guidance from state-changing action
vendor feature documentation from validated programmatic support
```

A documentação pode avançar para implementation incremental sem deixar esses conceitos implícitos.
