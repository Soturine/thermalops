# ADR-0003: Field Service, Preventive Maintenance e Escalation Scope

- **Status:** Accepted for product design
- **Date:** 2026-09-07

## Context

ThermalOps pretende apoiar workflows reais em que o operador pode diagnosticar, realizar preventive checks, coletar evidence, executar uma remediation local estreita e autorizada ou escalar o equipamento para support level/authorized repair process.

O papel real do técnico varia por organização, contrato e dispositivo. É incorreto assumir tanto que todo field technician apenas observa quanto que todo field technician está autorizado a desmontar e reparar internamente a impressora.

## Problem

Um produto centrado em um botão genérico de “Repair” cria ambiguidades:

- mistura software-side remediation com hardware repair;
- pode sugerir ação fora da authority do operador;
- prejudica Preventive Inspection;
- enfraquece evidence-first triage;
- dificulta handoff para N2/N3/vendor;
- tende a hard-code workflow de uma organização.

## Decision

ThermalOps é primariamente uma plataforma de:

- Diagnosis;
- Preventive Maintenance;
- Field Triage;
- Support Evidence;
- Local Authorized Remediation;
- ServiceDisposition;
- Escalation Assistance.

`Repair` dentro do ThermalOps significa **local, policy-authorized remediation**, salvo se future capability específica for desenhada e aprovada.

Não implica bench repair ou internal hardware service.

## Domain Additions

O Domain model deve distinguir:

```text
TechnicianObservation
MaintenanceInspection
MaintenanceFinding
MaintenanceRecommendation
ServiceDisposition
ServiceCase
FieldServicePolicy
EscalationPolicy
RepairPlan
```

## Field Outcome Model

Suggested `ServiceDisposition`:

```text
ContinueInService
ContinueWithObservation
LocalRemediationAllowed
EscalateToAuthorizedService
RemoveFromService
InsufficientEvidence
```

`RemoveFromService` exige explicit policy authority.

## UI Consequence

Primary workflows devem enfatizar:

```text
Quick Diagnosis
Preventive Inspection
Analyze Failure
Collect Evidence
Prepare Escalation
Technical Report
```

Local remediation aparece no context adequado, não como giant central action.

## Hardware Service Boundary

Generic product não fornece internal-disassembly instruction por default.

Isso não impede future support para authorized wear-part procedure, mas exige:

- verified real workflow;
- policy/authority model;
- source-backed procedure;
- safety analysis;
- device applicability;
- tests/docs;
- separate decision quando architecture impact for significativo.

## Company / Customer / Vendor Process Boundary

Não codificar no public core:

- internal ticket workflow;
- specific escalation contacts;
- who physically removes device;
- mandatory RMA sequence;
- contract-specific SLA;
- customer-specific part authorization;
- private configuration profile;
- employer-specific support levels.

Representar como policy/configuration privada:

```text
FieldServicePolicy
EscalationPolicy
ServiceDispositionRule
MaintenancePolicy
ReportTemplate
```

## Support Bundle Consequence

Support Bundle evolui para também suportar `ServiceCase`, contendo:

- target;
- evidence;
- Findings;
- TechnicianObservation;
- actions/results;
- preventive reference;
- disposition;
- privacy metadata;
- manifest.

## Preventive Consequence

Portable Lite ganha valor mesmo sem write capability:

- inspection;
- checklist;
- baseline comparison;
- MaintenanceDue;
- report;
- escalation preparation.

Isso reforça que Portable não é apenas “repair tool sem admin”.

## Evidence Attribution

Automatic evidence e TechnicianObservation permanecem separadas.

Reason:

- software não observa tudo;
- human observation pode estar errada/incompleta;
- recipient precisa saber provenance;
- future analytics/AI não deve misturar sensor value com manual input.

## Escalation Sem Repair

O workflow deve permitir:

```text
Diagnosis -> Finding -> ServiceDisposition -> ServiceCase -> Export
```

sem exigir qualquer write/local remediation.

Esse é um invariant importante para customer environments restritivos.

## Vendor Integration Boundary

Direct vendor/RMA submission é out of scope inicial.

Future integration exige:

- official interface;
- authentication;
- privacy/data classification;
- idempotency/error model;
- contract/licensing review;
- audit;
- dedicated ADR se architecture impact for relevante.

## Alternatives Considered

### “Repair Utility” First

Rejected porque prioriza state changes antes de evidence/authority e reduz utilidade preventiva/escalation.

### “Read-only Diagnostics Only” Forever

Rejected como product ceiling porque algumas low-risk local actions têm valor real, desde que tightly controlled.

### Hard-code One Support Process

Rejected porque processos variam e isso misturaria product core com proprietary workflow.

## Consequences

### Positive

- scope mais realista;
- safer field behavior;
- Portable Lite mais útil;
- clearer Domain;
- better N1/N2/N3 handoff;
- easier adaptation por policy;
- menos vendor/company coupling.

### Costs

- mais Domain concepts;
- policy/disposition model precisa de design/testes;
- UI precisa diferenciar recommendation/action/escalation;
- report schemas ficam mais ricos.

## Non-goals

Este ADR não define:

- employer-specific workflow;
- customer contract;
- RMA path;
- parts list;
- repair center integration;
- firmware procedure;
- exact technician job description.

## Revisit Triggers

Revisitar se:

- verified service process exigir hardware-service capability;
- direct vendor case integration for necessária;
- entitlement/warranty lookup virar product requirement;
- remote remediation alterar trust boundary;
- legal/compliance requirement mudar disposition semantics.
