# Contributing

ThermalOps is safety-sensitive support software. Contributions are welcome when they preserve the project constitution and authorization model.

## Before coding

Read `AGENTS.md` and `ENGINEERING_CONSTITUTION.md`.

For behavior changes, identify the roadmap milestone and acceptance criterion being advanced.

## Change expectations

- keep scope narrow;
- add/update tests;
- update docs in the same change;
- add an ADR for meaningful architecture/security decisions;
- avoid unrelated refactoring in a safety-critical fix;
- preserve read-only guarantees;
- explain risk for write/privileged changes;
- include failure-path tests, not only the happy path.

## Commit style

Use clear logical commits, e.g.:

```text
feat(domain): model printer status flags
fix(spooler): preserve original service state
security(helper): reject unknown capabilities
test(portable): verify no-persistence cleanup
docs(adr): define Zebra adapter boundary
```

## Pull requests

A PR should state:

- problem;
- scope;
- milestone;
- design/ADR if relevant;
- tests run;
- security/privacy impact;
- known limitations;
- validation status (`fixed`, `partial`, `experimental`, `deferred`, `not validated`).

## Third-party code

Do not copy code from a repository merely because it is public. Confirm license compatibility, attribution requirements, maintenance, and security before adding a dependency or implementation.

Until ThermalOps selects its own project license, do not assume inbound/outbound licensing terms beyond the repository owner's explicit decisions.

## Customer data

Never submit real customer logs, hostnames, usernames, IP addresses, printer serials/configurations, tickets, credentials, or screenshots. Create synthetic fixtures.
