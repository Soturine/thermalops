# ADR-0008: Lifecycle, Health e Remaining Useful Life semantics

- Status: Accepted for product/architecture direction
- Date: 2026-09-07

## Context

ThermalOps precisa representar uso acumulado, idade do asset, condition de componentes, maintenance compliance, current health, history/trends e, futuramente, possíveis estimativas de vida útil restante.

Misturar esses conceitos em um único `Health Score` cria risco de falso rigor. Vendor counters podem existir para alguns models e não para outros. Alguns componentes possuem warnings eletrônicos; outros dependem de TechnicianObservation e manutenção periódica. Além disso, um equipamento antigo pode estar saudável e um novo pode apresentar falha crítica.

## Decision

Separar explicitamente:

```text
AssetAge
UsageMetrics
ComponentCondition
MaintenanceCompliance
CurrentHealth
ConditionTrend
RemainingLifeEstimate
```

`HealthAssessment` representa **condição atual explicável**. `RemainingLifeEstimate` representa uma prediction/estimate de futuro e permanece unavailable/not validated até existir modelo validado para uma applicability class explícita.

## Health semantics

Primary UI é component-based, não score-first.

Suggested states:

```text
Good
GoodWithObservations
AttentionRecommended
Critical
InsufficientEvidence
NotApplicable
```

Numeric Health Score, se existir:

- secondary;
- deterministic;
- versioned;
- contributions inspectable;
- missing evidence explicit;
- applicability class definida;
- não é RUL.

## Usage semantics

Usage metrics preservam:

- source;
- raw value;
- raw unit;
- normalized value/unit quando conversão for válida;
- conversion context;
- counter lifetime/resettable semantics;
- collection outcome;
- timestamp.

`Unsupported`/`Unknown` não viram zero.

## Vendor capability rule

A existência de uma metric em um SDK/manual de um vendor não significa disponibilidade universal.

Zebra Link-OS odometer/counter capabilities justificam suporte capability-driven para metrics como total print length e outros counters documentados, mas não autorizam afirmar `OperatingHours` para toda Zebra.

## Component condition

`ComponentCondition` pode combinar:

```text
Automatic evidence
+ Manufacturer warnings
+ Usage metrics
+ Maintenance due
+ TechnicianObservation
```

A provenance de cada input permanece visível.

## RUL boundary

`RemainingLifeEstimate` aceita status:

```text
Unavailable
NotSupported
NotValidated
Experimental
ValidatedForApplicabilityClass
```

Nenhuma early release deve calcular porcentagem/dias restantes por fórmula arbitrária, idade simples ou LLM.

Antes de qualquer validated RUL, exigir M9 validation program com target/ground truth/dataset/calibration/cost/applicability/drift/human review.

## Consequences

Positive:

- evita confundir age, usage e health;
- permite adicionar vendor metrics incrementalmente;
- mantém uncertainty honesta;
- suporta Enterprise history sem prometer prediction;
- abre caminho para preventive/condition-based maintenance real.

Costs:

- more Domain concepts;
- units/conversion/versioning tests;
- applicability matrices;
- reports precisam lidar com unsupported/unknown;
- Health UI exige drill-down.

## Alternatives rejected

### One global health percentage

Rejeitado como primary truth porque esconde source, uncertainty e incompatibilidade entre devices.

### Remaining life derived from age/usage ratio

Rejeitado por não possuir base técnica universal.

### AI-generated lifecycle prediction

Rejeitado como authority/predictive mechanism.

## Related docs

- `docs/produto/lifecycle-e-health.md`
- `docs/produto/manutencao-preventiva.md`
- `docs/produto/fleet-e-condition-monitoring.md`
- `docs/engenharia/validation-matrix-lifecycle-guidance-self-service.md`
