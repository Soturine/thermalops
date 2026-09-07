# ADR-0004: Maintenance e Health Model Explicável

- **Status:** Accepted for product design
- **Date:** 2026-09-07

## Context

ThermalOps precisa apoiar Preventive Maintenance sem inventar service intervals, misturar device status com maintenance state ou transformar um score opaco em autoridade.

O mesmo printer model pode ter diferenças de DPI, firmware, media, ribbon, operating mode, environment e policy. Além disso, parte da condição física só pode ser registrada pelo técnico.

## Problem

Modelos simplificados como:

```text
printer online => healthy
```

ou:

```text
AI score = 87 => healthy
```

não preservam source, uncertainty, applicability ou maintenance reasoning.

Da mesma forma, comparar toda printer contra um baseline universal gera false positives.

## Decision

Adotar um maintenance/health model composto por concepts distintos:

```text
MaintenanceTaskDefinition
MaintenanceInspection
MaintenanceTaskResult
MaintenancePolicy
MaintenanceBaseline
MaintenanceDue
MaintenanceFinding
MaintenanceRecommendation
TechnicianObservation
HealthAssessment
HealthContribution
ConditionTrend
ServiceDisposition
```

## Source-backed Tasks

Toda maintenance task/schedule precisa de:

- source/reference;
- version/date quando conhecida;
- vendor/model/family applicability;
- capability/context applicability;
- trigger/interval;
- safety notes;
- result semantics.

Se source/applicability necessária estiver ausente, o outcome é `Unknown`/`NotApplicable` conforme regra, nunca uma recommendation inventada.

## Baseline Decision

`MaintenanceBaseline` é approved/reference state, não universal truth.

Applicability deve poder considerar:

- vendor/model/family;
- DPI;
- media/application context;
- firmware range;
- connection context;
- policy/site profile;
- schema version.

`ConfigurationDrift` é Finding, não fault proof.

## Automatic vs Human Evidence

`TechnicianObservation` é first-class evidence com provenance própria.

Automatic device/Windows evidence e manual observation não podem compartilhar origem fictícia.

Exemplo:

```text
Automatic: HeadState=Closed
TechnicianObservation: Print quality has missing vertical lines
```

## MaintenanceDue

Suggested normalized states:

```text
Unknown
NotApplicable
NotDue
DueSoon
Due
Overdue
Blocked
```

O calculation registra rule/source/version que produziu o resultado.

## HealthAssessment

Primary health UX é component-based.

Exemplo:

```text
Overall: AttentionRecommended
Device: OK
Windows: OK
Transport: Observation
Configuration: Drift
Maintenance: DueSoon
EvidenceCompleteness: 91%
```

### Numeric Score

Um numeric Health Score pode existir apenas como secondary representation.

Requirements:

- deterministic;
- rule/weight versioned;
- every HealthContribution inspectable;
- missing evidence treated explicitly;
- applicability/comparison class known;
- not generated authoritatively by AI;
- not interpreted as warranty/failure prediction.

Se esses requirements não trouxerem valor suficiente, o produto pode permanecer sem numeric score.

## ConditionTrend

Historical trend representa mudança de observações ao longo do tempo.

Não equivale a causal diagnosis.

UI/report precisa ser capaz de mostrar:

```text
Observed series
Derived trend
Recommendation
What is not claimed
```

## Predictive Boundary

Predictive Maintenance não é consequência automática de HealthAssessment/Fleet history.

Antes de qualquer prediction claim, M9 exige:

- defined target;
- labeled representative data;
- validation separation;
- calibration;
- false-positive/negative analysis;
- applicability matrix;
- drift monitoring;
- human/policy review.

## ServiceDisposition Relationship

Health/Maintenance state não define sozinho ServiceDisposition.

Disposition combina:

- Findings;
- evidence;
- field authority;
- policy;
- operator decision quando aplicável.

Exemplo:

```text
Maintenance: Overdue
Device: Ready
Disposition: ContinueWithObservation
```

ou outro resultado conforme policy. Não hard-code universal mapping.

## Localization

Canonical Domain values permanecem em inglês. Human labels são resources localizáveis.

Exemplo:

```text
DueSoon -> “Vence em breve” (pt-BR)
DueSoon -> “Due soon” (en-US)
```

## Alternatives Considered

### Single Green/Yellow/Red Status

Rejected como primary model porque perde provenance/uncertainty.

Pode existir como summary visual desde que drill-down preserve components/evidence.

### AI-generated Health Score

Rejected como authority por falta de determinism/auditability.

### Universal Vendor Maintenance Schedule

Rejected porque schedules variam por device/context e precisam de source.

### Baseline From “Majority of Fleet” Automatically

Rejected como default. Majority não significa approved/correct, e mixed contexts podem distorcer comparação.

## Consequences

### Positive

- explainable preventive decisions;
- safer unknown handling;
- model/context-specific maintenance;
- stronger reports/audit;
- future Fleet analytics with preserved rule versions;
- AI remains explanatory only.

### Costs

- more Domain types;
- maintenance catalogs require governance;
- baseline compatibility logic;
- score versioning if score is added;
- richer test matrix.

## Testing Requirements

- task applicability boundaries;
- missing source/input;
- due transitions;
- baseline compatibility/mismatch;
- drift acknowledgement;
- TechnicianObservation attribution;
- HealthContribution explainability;
- unknown handling;
- score versioning if present;
- locale invariance;
- condition trend semantics.

## Revisit Triggers

Revisitar se:

- sufficient real data supports predictive program;
- vendor exposes standardized health metric worth mapping;
- Enterprise needs new comparison/normalization model;
- maintenance policy model proves insufficient for real contracts;
- regulatory/service requirements mandate different semantics.
