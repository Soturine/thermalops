# Contributing

ThermalOps is safety-sensitive printer lifecycle/support software. Contributions must preserve authorization, evidence integrity, preventive-maintenance sourcing, privacy and least privilege.

## Before coding

Read `AGENTS.md` and `ENGINEERING_CONSTITUTION.md`, then the product/architecture docs relevant to the milestone.

For preventive changes read `docs/PREVENTIVE_MAINTENANCE.md`. For field/escalation changes read `docs/FIELD_SERVICE_AND_ESCALATION.md`. For enterprise packaging read `docs/DEPLOYMENT_AND_LIFECYCLE.md`.

## Change expectations

- narrow scope and logical commits;
- tests with failure/unknown cases;
- docs in the same change;
- ADR for architecture/security/lifecycle decisions;
- preserve read-only guarantees;
- keep auto evidence distinct from technician input;
- identify source/applicability for maintenance rules;
- explain security/privacy impact for writes, exports and fleet changes;
- avoid unrelated refactors in safety fixes.

## Commit examples

```text
feat(domain): model maintenance due states
feat(service): add service disposition policy
fix(spooler): preserve original service state
security(helper): reject unknown capabilities
test(portable): verify no-persistence cleanup
docs(adr): define enterprise package lifecycle
```

## Pull requests

State problem, scope, milestone, design/ADR, tests, security/privacy impact, maintenance source if relevant, known limitations and validation status (`fixed`, `partial`, `experimental`, `deferred`, `not validated`).

## Third-party code/dependencies

Public code is not automatically reusable. Confirm license compatibility, attribution, maintenance and security. Prefer official API/vendor docs and independent implementation.

Until ThermalOps selects its license, do not assume inbound/outbound terms beyond explicit repository-owner decisions.

## External maintenance data

If adding a maintenance task/rule:

- cite official/approved source;
- record source version/date/model applicability;
- include safety notes;
- test applicability and unknown-data behavior;
- do not generalize one model's interval to all printers.

## Customer/employer data

Never commit real customer/employer hostnames, usernames, IPs, serials, tickets, configs, internal procedures, credentials, logs, photos or screenshots. Use synthetic fixtures and generic policy abstractions.
