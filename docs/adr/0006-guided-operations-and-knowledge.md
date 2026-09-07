# ADR-0006: Guided Operations e Knowledge como camada determinística e source-backed

- Status: Accepted for product/architecture direction
- Date: 2026-09-07

## Context

ThermalOps precisa ir além de coletar evidence e apresentar Findings. Técnicos e end users também precisam de troubleshooting orientado, model-aware instructions, maintenance procedures, setup/commissioning guidance, native self-tests e acesso contextual à documentação.

Vendor tools como Zebra Printer Setup/Nucleus, onboard printer diagnostics e security-assessment patterns demonstram que setup, guided troubleshooting e diagnostic actions são necessidades reais. Entretanto, copiar um manual para dentro do app ou deixar AI decidir passos/ações criaria problemas de licenciamento, stale guidance, capability mismatch e privilege escalation.

## Decision

Adicionar **Guided Operations** como uma camada transversal do produto, com:

- structured `Runbook`/`RunbookStep` data;
- explicit source/version/applicability;
- deterministic evidence-driven branching;
- model/capability/policy-aware step resolution;
- `ActionSafetyClass` para cada operation;
- local Knowledge Packs data-only quando redistribution/licensing permitir;
- official-link/online retrieval como source modes opcionais;
- AI limitada a interpretation/explanation/retrieval assistance;
- typed compiled actions resolvidas pelo Application, nunca arbitrary command text vindo de runbook/document/AI.

## Canonical flow

```text
Evidence + Capabilities + Policy + Approved Source
                |
                v
          Applicable Runbook
                |
                v
        Deterministic Guidance
                |
      +---------+----------+
      |                    |
      v                    v
Manual/Read step      Typed ActionReference
                           |
                           v
                    revalidate policy
                           |
                           v
                   RepairPlan/action flow
```

## ActionSafetyClass

Adotar categorias conceituais:

```text
Informational
GuidedManual
AssistedWrite
AutomatedLowRisk
HighImpact
ForbiddenInProfile
```

A classificação é parte da definição da action/runbook e não pode ser reduzida pela UI para tornar a experiência mais simples.

## Runbook safety

Runbooks:

- não contêm PowerShell/cmd/shell;
- não carregam DLL/plugin;
- não possuem general-purpose scripting/expression language;
- só podem referenciar registered `ActionType`;
- não criam executable capability;
- são tratados como untrusted input até schema/trust validation.

## Knowledge sources

A source hierarchy e trust metadata são explicitadas. Official vendor/platform docs são preferidas para technical procedures. Organization-approved private procedures podem existir fora do public core.

O repository não redistribui vendor manuals automaticamente. Local packs só incluem conteúdo permitido ou ThermalOps-authored metadata/summaries/runbooks com attribution/licensing apropriados.

## AI boundary

AI pode:

- mapear natural-language symptom para candidate canonical symptom;
- explicar step/evidence;
- recuperar approved source;
- resumir GuidanceSession.

AI não pode:

- autorizar ActionType;
- inventar capability;
- executar write;
- transformar retrieved text em system instruction;
- criar authoritative runbook step sem approved source/rule.

## Consequences

Positive:

- troubleshooting mais rápido e consistente;
- reuso do mesmo evidence engine em Technician e Self-Service;
- offline guidance possível;
- vendor/model differences explícitas;
- AI permanece fora do control plane;
- runbook history pode entrar em ServiceCase.

Costs:

- precisa de schema/version lifecycle;
- source curation;
- knowledge-pack validation;
- localization/safety review;
- HIL para native diagnostic actions;
- more test surface.

## Alternatives rejected

### PDF/manual viewer only

Útil como referência, mas não oferece evidence-driven branching, verification, runbook state ou safe action resolution.

### LLM-driven troubleshooting agent

Rejeitado como authority/control plane por nondeterminism, prompt injection, unverifiable procedures e privilege risk.

### Hard-coded model-specific UI flows

Rejeitado por duplicação, poor versioning e vendor leakage na presentation layer.

### General scripting engine for runbooks

Rejeitado por criar uma programming/privilege boundary desnecessária.

## Implementation timing

- read-only guidance pode começar sobre M1 evidence;
- Zebra capabilities crescem em M3;
- Preventive/ServiceCase guidance amadurece em M4;
- managed packs/helpdesk integrations em M5+;
- AI/RAG em M8;
- no dependency on AI for core guidance.

## Related docs

- `docs/produto/guided-operations-e-knowledge.md`
- `docs/engenharia/guided-operations-architecture.md`
- `docs/seguranca/self-service-e-guided-operations-threat-model.md`
- `docs/engenharia/validation-matrix-lifecycle-guidance-self-service.md`
