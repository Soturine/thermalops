# ADR-0003: Field-service, preventive-maintenance, and escalation scope

- Status: Accepted for product design
- Date: 2026-09-07

## Context

ThermalOps is intended for real support workflows where the person operating the tool may diagnose, perform preventive checks, collect evidence, execute a narrow authorized software-side remediation, or escalate the printer to a higher support level/authorized repair process.

It is unsafe to assume every operator is authorized to disassemble or repair printer hardware.

## Decision

ThermalOps is primarily a **diagnostic, preventive-maintenance, field-triage, support-evidence, and escalation-assistance** platform.

`Repair` inside ThermalOps means **local, policy-authorized remediation** unless another feature is explicitly designed and approved. It does not imply bench repair or internal hardware service.

The domain adds distinct concepts for:

- preventive inspection;
- technician observation;
- maintenance finding/recommendation;
- service disposition;
- service case;
- escalation policy.

## Consequences

- UI emphasizes `Diagnose`, `Preventive Inspection`, `Analyze Failure`, `Collect Evidence`, `Prepare Escalation`, and `Report` rather than a generic repair button;
- hardware-disassembly instructions are not part of the generic product scope;
- organization/vendor-specific service processes remain policy/configuration, not hard-coded core rules;
- support bundles evolve into service-case packages when escalation is needed;
- automatic evidence and technician-entered inspection results remain separately attributable;
- Portable Lite gains strong value for preventive/triage work while staying read-only.

## Non-goals

This ADR does not define any specific employer/customer workflow, RMA path, service contract, parts replacement procedure, or proprietary escalation rule.

## Revisit when

A verified service process requires additional hardware-service capabilities, direct vendor case integration, entitlement lookup, or RMA submission. Those require separate security/privacy/licensing/API analysis.
