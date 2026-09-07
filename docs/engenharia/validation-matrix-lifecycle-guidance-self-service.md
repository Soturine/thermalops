# Validation Matrix — Lifecycle, Guided Operations e Self-Service

## Objetivo

Esta matriz transforma requisitos recentes de Lifecycle/Health, Guided Operations, Knowledge e Self-Service em acceptance criteria verificáveis. Ela complementa `testing.md` e evita que uma feature seja considerada pronta apenas por existir na UI.

## 1. Lifecycle / Usage Metrics

### Domain

Validar:

- `Unknown` diferente de zero;
- `Unsupported` diferente de `Unknown`;
- lifetime counter diferente de user-resettable counter;
- raw value/unit preservados;
- normalized conversion exige contexto suficiente;
- DPI incorreto não é usado silenciosamente;
- AssetAge não influencia CurrentHealth por shortcut;
- Usage acima da média não vira fault;
- manufacturer warning mantém source/applicability.

### Adapter

Para cada metric anunciada:

- official interface/documentation reviewed;
- model/firmware/transport applicability documentada;
- valid response fixture;
- missing field;
- malformed value;
- numeric overflow/boundaries;
- resettable/lifetime semantics;
- units;
- timeout/disconnect;
- unsupported model.

### HIL

Registrar model, DPI, firmware, connection, SDK/adapter version e observed output.

Support claim somente após real hardware validation para a combination relevante.

## 2. HealthAssessment

Validar:

- every component references evidence;
- every derived contribution references rule version;
- missing evidence não produz positive contribution artificial;
- EvidenceCompleteness é separado de Health;
- component result estável para same evidence/policy;
- SelfService/Technician/AdvancedSupport recebem o mesmo Domain result;
- numeric score, se existir, mostra todas as contributions;
- incompatible applicability classes não são comparadas;
- AI disabled não altera HealthAssessment.

Required scenarios:

```text
Old asset + healthy evidence -> can be Good
New asset + critical evidence -> can be Critical
High usage + no fault evidence -> not automatically Critical
Missing device-native evidence -> Insufficient/Unknown component
Maintenance overdue + printer ready -> Ready and MaintenanceAttention coexist
```

## 3. RemainingLifeEstimate / RUL

Early releases:

- no estimator registered;
- UI/report returns `NotValidated`/`Unavailable` rather than fabricated percentage;
- AI cannot populate RUL;
- no age+usage arbitrary formula;
- report schema supports explicit limitation.

Future experimental estimator requires:

- model version;
- target definition;
- training/evaluation metadata;
- applicability class;
- calibration results;
- holdout/prospective validation;
- drift handling;
- disable/rollback path.

## 4. Runbook Resolution

Test dimensions:

- vendor;
- model/family;
- firmware range;
- capability presence;
- printer language;
- connection type;
- locale;
- policy;
- symptom;
- source version.

Required cases:

- exact applicable runbook selected;
- wrong-model runbook rejected;
- missing capability returns blocked/unsupported;
- multiple candidates ranked/resolved deterministically;
- no source -> `BlockedByMissingSource`;
- stale/unsupported runbook version handled;
- localized label does not alter runbook ID.

## 5. Runbook Safety

Reject:

- embedded shell/PowerShell/cmd;
- arbitrary executable path;
- script/expression body outside approved rule model;
- unknown ActionType presented as executable;
- absolute/traversal paths in pack;
- dynamic DLL/plugin loading;
- action that mismatches declared SafetyClass.

Verify:

- `Informational` cannot mutate state;
- `GuidedManual` only records user action/observation;
- `AssistedWrite` requires policy/preflight/confirmation/verification;
- `HighImpact` is unavailable in Self-Service by default;
- `--readonly` blocks all state-changing actions regardless of runbook.

## 6. Guidance Session

Required E2E:

```text
DoesNotPrint -> Windows OK -> Transport OK -> HeadOpen
-> guided manual check
-> recheck HeadClosed/Ready
-> outcome Resolved
-> no Windows remediation recorded
```

Additional cases:

- user cancels mid-session;
- target disconnects;
- target identity changes;
- evidence conflicts;
- policy changes mid-session;
- step verification fails;
- escalation recommended;
- guidance summary included in ServiceCase;
- offline source unavailable;
- AI unavailable.

## 7. Knowledge Pack

Validate:

- manifest/schema;
- file hashes;
- max archive/file count/decompressed size;
- traversal rejection;
- executable/binary content rejection where not allowed;
- duplicate runbook IDs/version conflict;
- unsupported schema version;
- missing source metadata;
- license/notices inventory;
- localization resources;
- invalid signature when trusted mode applies;
- untrusted pack cannot add executable capability.

## 8. Online Knowledge Retrieval

Validate:

- source allowlist;
- redirects/domain handling;
- timeout/offline;
- oversized content;
- stale source metadata;
- no automatic customer-data disclosure in query;
- retrieved prompt injection remains untrusted;
- source citation visible;
- missing source leads to uncertainty, not invented instruction.

## 9. Zebra Native Diagnostics

For each action claimed, classify and test independently:

```text
ConfigurationReport
NetworkConfigurationReport
PrintQualityReport
CommunicationDiagnosticsTest
SensorProfileReport
MediaCalibration
```

Need:

- official interface/manual mapping;
- applicability matrix;
- state-change classification;
- media consumption;
- prerequisites;
- timeout;
- expected result;
- HIL;
- read-only enforcement;
- failure path.

Do not claim programmatic support merely because a printer front panel/manual exposes the operation.

## 10. SettingsProvider

For supported Zebra settings:

- available settings enumeration;
- read value;
- range;
- read-only semantics;
- validity check;
- unsupported setting;
- malformed setting value;
- policy denial for write despite vendor write capability;
- no arbitrary setting-name write path in privileged UI.

Invariant:

```text
VendorCanWrite(X) != ThermalOpsPolicyAllowsWrite(X)
```

## 11. Self-Service Capability Matrix

Default Self-Service expected:

```text
Quick Diagnosis............... Allowed
Health summary................ Allowed
Guided Troubleshooting........ Allowed
Knowledge Center.............. Allowed
Preventive status............. Allowed
Sanitized evidence/report..... Allowed
ServiceCase draft............. Allowed
Technical raw details......... Restricted by profile/policy
Diagnostic print.............. Denied by default
Spooler restart............... Denied
Driver install................ Denied
Firmware update............... Denied
Factory/network reset......... Denied
Arbitrary config write........ Denied
```

Test UI and direct Application invocation. Hiding a button is not enough.

## 12. Self-Service Standard User

E2E on clean/supported Windows:

- standard user launch;
- no UAC during normal flow;
- no admin-only dependency;
- local queue diagnosis;
- known endpoint check when allowed;
- blocked network check when policy denies;
- offline Knowledge Pack;
- ServiceCase draft;
- clean exit;
- no hidden persistence for Portable profile.

## 13. Corporate Endpoint Controls

Test where environments are available:

- AppLocker/App Control block application;
- firewall blocks printer endpoint;
- firewall blocks helpdesk connector;
- Controlled Folder Access blocks export destination;
- EDR/allowlisting compatible signed artifact path when signing exists;
- removable media restrictions;
- proxy required;
- no suggestion to disable controls.

Expected product behavior is explicit `BlockedByPolicy`/`AccessDenied`, not generic crash.

## 14. Asset Scope

Managed Self-Service:

- assigned printer visible;
- unassigned printer not exposed/collection rejected;
- friendly-name spoof does not bypass scope;
- replaced physical printer triggers identity review;
- user/site change updates scope;
- central identity unavailable has defined degraded behavior.

Portable Lite:

- no central identity dependency;
- only local/explicit target within compiled read-only envelope.

## 15. Helpdesk Connector

Test:

- ServiceCase redacted before connector;
- privacy preview exactly matches categories/fields transmitted;
- TLS validation;
- auth failure;
- timeout/retry behavior;
- duplicate submission/idempotency where supported;
- external ticket ID recorded;
- no credentials in logs;
- connector cannot request remediation;
- arbitrary URL from runbook rejected;
- offline export remains available if connector fails.

## 16. Privacy

Self-Service and lifecycle data tests:

- exact usage counters removable by policy;
- serial/IP/hostname redaction;
- document content absent;
- other printers excluded;
- Technician/user identity minimized;
- ServiceCase sanitized default;
- retention disabled for Portable;
- Enterprise retention policy honored.

## 17. Accessibility / UX

Test:

- keyboard-only completion of Quick Diagnosis and support request;
- screen-reader names;
- high contrast;
- 125/150/200% scaling;
- status not conveyed by color alone;
- plain-language Self-Service text;
- expandable technical details;
- long pt-BR/en-US strings;
- safety-critical warning translations reviewed.

## 18. Ticket Deflection Safety

Validate that product metrics cannot block escalation:

- `InsufficientEvidence` always exposes support path;
- repeated guidance failure escalates according to rule/policy;
- unresolved issue cannot be marked resolved merely to improve metric;
- user can request help even when guidance is available;
- critical Finding bypasses optional low-value steps when policy requires.

## 19. Documentation / Source Completeness

CI/docs review should verify:

- all new product docs indexed;
- ADR links valid;
- threat-model supplement linked from security docs;
- roadmap maps each capability to milestone;
- AGENTS has required reading entries;
- research records external sources separately from business rules;
- no claim of supported feature without validation status;
- no prose says all printers expose hours/RUL;
- no public doc hard-codes confidential employer/customer workflow.

## 20. Definition of Done by capability

### Lifecycle indicators

Done only when Domain semantics, adapter capability, unit tests, HIL where applicable, UI uncertainty and reports agree.

### Guided Troubleshooting

Done only when applicable runbooks are deterministic, source-backed, policy-safe, testable offline and cannot execute arbitrary content.

### Self-Service

Done only when standard-user, no-UAC normal flow, capability matrix, privacy, endpoint-control behavior, accessibility and support handoff are validated.

### Native diagnostic write

Done only when action classification, policy, preview, typed execution, HIL, verification and failure handling are validated.

### RUL

Not done until M9 validation criteria are satisfied for an explicit applicability class.
