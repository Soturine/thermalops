# ADR-0004: Explainable maintenance and health model

- Status: Accepted for product design
- Date: 2026-09-07

## Context

A preventive-maintenance product needs an understandable summary of device condition, maintenance due state, baseline drift and history without creating misleading magic scores or AI-generated certainty.

Manufacturer maintenance schedules vary by model, media, print mode and application. Device capabilities also vary.

## Decision

ThermalOps will model preventive maintenance with versioned, source-backed tasks and explainable evidence-derived health assessments.

Primary health UX is categorical/component-based. A numeric score is optional and secondary.

Maintenance schedules may be sourced from:

- exact applicable manufacturer documentation;
- organization-approved policy;
- approved site/application procedure;
- validated usage/condition thresholds.

Unknown applicability/data remains `Unknown`, not healthy.

## Health model requirements

If a numeric score is added:

- deterministic/versioned rule set;
- every contribution visible;
- unknown values handled explicitly;
- no LLM-generated weights/scores;
- not compared across incompatible model/policy classes;
- evidence and rule version retained in history;
- no claim of remaining useful life or imminent failure without separate predictive validation.

## Predictive maintenance

Deferred. Requires representative labeled history, a defined prediction target, calibration/validation, applicability matrix, drift monitoring and false-positive/negative cost analysis.

## Consequences

- `MaintenanceTaskCatalog`, `MaintenanceBaseline`, `MaintenanceDue`, `HealthAssessment`, `HealthContribution` and `ConditionTrend` belong to Domain/Application;
- vendor adapters expose capabilities/evidence, not maintenance business policy;
- manufacturer references are versioned inputs rather than copied ad-hoc instructions;
- Fleet stores underlying contributions/evidence rather than only a final score.
