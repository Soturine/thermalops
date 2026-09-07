# Threat Model — Self-Service, Guided Operations e Knowledge

## Escopo

Este documento complementa `security-e-privacy.md` para as novas boundaries introduzidas por:

- `SelfService` ExperienceProfile;
- Guided Troubleshooting e runbooks;
- Knowledge Packs offline;
- online documentation retrieval;
- Helpdesk / ServiceDesk connectors;
- native printer diagnostic actions;
- Lifecycle/Health e future RUL;
- managed asset assignment e user identity.

O objetivo é evitar que features de conveniência ampliem a superfície de ataque ou enfraqueçam least privilege, evidence integrity e customer controls.

## Assets a proteger

```text
Customer endpoint
Printer/device state
Windows print subsystem
Customer network
Customer identifiers
ServiceCase data
Maintenance/history data
Organization policies
Knowledge/runbook trust
ThermalOps executable capabilities
User/asset authorization
Health/lifecycle decision integrity
```

## Trust boundaries

```text
End User / Technician
        |
        v
Localized UI / ExperienceProfile
        |
        v
Application / Domain
   |        |          |          |
   |        |          |          +--> Helpdesk Connector
   |        |          +-------------> Knowledge Pack / Online Source
   |        +------------------------> Windows / Vendor Adapters
   +---------------------------------> Policy / Identity / Asset Scope

Writes:
Application -> typed action -> policy -> privileged/vendor write boundary
```

## Threat: Self-Service privilege expansion

### Risk

UI simplification ou ExperienceProfile pode ser tratado incorretamente como authorization, permitindo que um end user alcance capabilities de Technician/AdvancedSupport.

### Controls

- `ExperienceProfile` é somente uma entrada restritiva, nunca grant de capability;
- effective capability = executable capability ∩ device capability ∩ organization policy ∩ user/asset scope ∩ experience profile ∩ runtime constraints;
- no hidden-button security;
- write methods inacessíveis em Portable Lite;
- all privileged/write actions revalidate policy no execution boundary;
- tests cobrem direct invocation bypass attempts.

## Threat: Fake “no-IT” bypass

### Risk

Product messaging ou implementation incentiva desabilitar WDAC/AppLocker/EDR/firewall para executar.

### Controls

- explicit product rule: approval once is acceptable; bypass is not;
- blocked controls retornam `BlockedByPolicy`;
- documentation never recommends disabling corporate controls;
- signed publisher/package support;
- documented network behavior;
- managed deployment pattern preferred for restrictive enterprises.

## Threat: Runbook as code execution

### Risk

Runbook importado contém scripts, command strings, expression language ou references que podem ser convertidas em arbitrary execution.

### Controls

- runbooks are data-only;
- no embedded scripting;
- small enumerated condition model;
- `ActionReference` resolves only to compiled/registered typed action;
- unknown action IDs rejected/unsupported;
- documents and AI cannot create new ActionType;
- pack cannot load DLL/plugin automatically.

## Threat: Malicious Knowledge Pack

### Risk

Pack adulterado tenta path traversal, zip bomb, parser abuse, oversized content, fake source metadata ou action references perigosas.

### Controls

- archive size/file-count/decompression ratio limits;
- reject absolute/traversal paths;
- schema/version validation;
- SHA-256 manifest;
- signature/trust verification when organization-trusted pack support exists;
- source inventory and licensing metadata;
- allowlisted file types;
- no executable content;
- unknown actions do not execute;
- untrusted packs cannot expand executable capability.

## Threat: Stale or wrong-model guidance

### Risk

Um procedimento correto para outro model/firmware/media context é apresentado como aplicável ao target atual.

### Controls

- explicit `RunbookApplicability`;
- vendor/model/family/firmware/capability/context checks;
- source/version surfaced;
- `BlockedByMissingCapability` / `InsufficientEvidence` instead of guessing;
- HIL/fixture tests for supported combinations;
- source freshness review at knowledge-pack release.

## Threat: Unsafe manual instruction

### Risk

Self-Service orienta disassembly, cleaning ou physical intervention não autorizada.

### Controls

- `ActionSafetyClass`;
- Self-Service allowlist of `Informational` and approved `GuidedManual` only;
- service-only steps excluded from Self-Service packs/profile;
- safety notes/source preserved;
- no generic “open and replace part” guidance;
- field authority policy can further restrict Technician mode.

## Threat: Native diagnostic action misclassified as read-only

### Risk

Calibration, test print ou device diagnostic altera state/consome media, mas é apresentado como read-only.

### Controls

- every diagnostic action declares `stateChange`, media/ribbon consumption, expected duration and requirements;
- read-only profiles reject any action with write/state-change semantics;
- `--readonly` hard guardrail remains authoritative;
- test label/calibration are explicitly write-class operations;
- preflight + verification for assisted writes.

## Threat: Factory/network reset through guidance

### Risk

High-impact reset fica acessível como “próximo passo” trivial.

### Controls

- `HighImpact` safety class;
- disabled in Self-Service by default;
- explicit policy key;
- stronger confirmation;
- snapshot/impact preview;
- dedicated implementation review/ADR if introduced;
- no auto-execution from runbook.

## Threat: Helpdesk connector data exfiltration

### Risk

Connector envia mais dados que o usuário/policy espera, ou usa endpoint/credentials mal configurados.

### Controls

- ServiceCase created and redacted before connector;
- privacy preview matches actual payload;
- connector receives scoped serialized payload, not unrestricted filesystem access;
- endpoint allowlist/configuration;
- TLS validation;
- credentials stored through approved secret mechanism;
- no arbitrary webhook URL from untrusted runbook;
- submission audit with external case ID, without leaking secret.

## Threat: Helpdesk connector becomes control plane

### Risk

External ticket system sends commands back to ThermalOps to execute remediation.

### Controls

- initial connector direction is outbound support submission only;
- inbound automation requires separate ADR/threat model;
- ServiceDesk adapter never owns device remediation capability;
- ticket content is untrusted text.

## Threat: Online documentation prompt injection

### Risk

Retrieved page contains instructions aimed at an AI agent or content that conflicts with policy.

### Controls

- retrieval content treated as untrusted source text;
- source trust class maintained;
- AI tool instructions never taken from retrieved content;
- no direct action execution from generated/retrieved text;
- output grounded in approved sources/evidence;
- source allowlist;
- size/content sanitation.

## Threat: Source substitution / link rot

### Risk

Official URL changes, redirects to unrelated content, or source revision invalidates guidance.

### Controls

- canonical source metadata;
- retrieved date/version/hash where feasible;
- approved domains;
- local pack release freezes reviewed source mapping;
- source unavailable leads to explicit status, not fabricated replacement.

## Threat: User/asset authorization mismatch

### Risk

End user sees/diagnoses printers outside assigned site/department.

### Controls

- canonical `PrinterIdentity` and `AssignedAssetScope`;
- friendly name not used for authorization;
- scope checks in Application before evidence collection where policy requires;
- Enterprise identity/RBAC ADR before managed fleet access;
- Portable Lite operates only on local/explicit targets within its envelope.

## Threat: Identity spoofing

### Risk

Printer is replaced but keeps same queue/friendly name, causing baseline/history/action to target wrong physical device.

### Controls

- multi-source identity resolution;
- re-identify after service/replacement;
- compare serial/vendor identity/PnP/network evidence when available;
- baseline applicability checked again;
- high-impact writes require stronger target confidence.

## Threat: Health score hides uncertainty

### Risk

User sees “82/100” and assumes device is safe despite missing evidence.

### Controls

- component-first UI;
- numeric score secondary;
- EvidenceCompleteness shown separately;
- unknown components explicit;
- every contribution inspectable;
- no green score from missing data;
- rule version included.

## Threat: Unsupported lifetime / RUL claim

### Risk

ThermalOps outputs “62% life remaining” based on arbitrary formula, AI text or non-representative data.

### Controls

- `RemainingLifeEstimate` unavailable by default;
- explicit statuses `NotSupported`, `NotValidated`, `Experimental`, `ValidatedForApplicabilityClass`;
- no RUL from LLM;
- dedicated M9 validation program;
- applicability/model version attached to any future estimate;
- UI separates CurrentHealth from RUL.

## Threat: Usage metric semantic error

### Risk

Dots/meters/labels/hours are misinterpreted, converted using wrong DPI, or resettable counters treated as lifetime totals.

### Controls

- preserve raw unit/value/source;
- normalized unit includes conversion context;
- distinguish lifetime vs resettable counter semantics;
- no conversion without required context;
- parser/unit contract tests;
- firmware/model capability matrix.

## Threat: Sensitive operational telemetry

### Risk

Usage counters and maintenance history reveal production intensity or operational patterns.

### Controls

- data classification includes operational metadata;
- retention/purpose limitation;
- sanitized export can omit exact counters;
- Self-Service display subject to policy;
- no unnecessary centralized telemetry;
- no document contents required for usage metrics.

## Threat: Service worker/agent privilege creep

### Risk

Managed Self-Service client introduces persistent privileged service only to make actions easier.

### Controls

- standard-user UI remains default;
- Enterprise agent/service only after ADR and necessity proof;
- least-privilege service identity;
- no reuse of Temporary Privileged Helper as permanent unrestricted service;
- read-only Self-Service must not require privileged agent.

## Threat: Automatic remediation from guidance

### Risk

Guidance decides to “fix” based on incomplete evidence.

### Controls

- default guidance = explain/verify/recommend;
- `AutomatedLowRisk` disabled unless explicit policy and validation;
- deterministic preconditions;
- narrow target;
- post-condition verification;
- no auto factory reset/firmware/network reconfiguration.

## Threat: Localization changes safety meaning

### Risk

Translated instruction loses a warning or changes action semantics.

### Controls

- canonical runbook/action IDs locale-neutral;
- safety-critical translations reviewed;
- source reference accessible;
- machine schema unaffected by locale;
- localization tests for warnings/long labels.

## Threat: Metrics incentivize unsafe ticket deflection

### Risk

Product optimizes for fewer tickets and pressures users to keep troubleshooting instead of escalating.

### Controls

- `InsufficientEvidence` and `EscalationRecommended` are valid successful workflow outcomes;
- no KPI may disable escalation path;
- ticket deflection metrics are secondary and policy/privacy controlled;
- safety/authority outrank support cost.

## Required security tests

```text
Self-Service direct write invocation rejected
Self-Service UAC-free normal flow
ExperienceProfile cannot grant capability
Runbook unknown action rejected
Runbook traversal/script fields rejected
Knowledge pack zip-bomb/path traversal rejected
Invalid signature/trust rejected when trusted pack required
Wrong-model runbook not selected
High-impact action hidden and policy-rejected in Self-Service
Helpdesk payload equals privacy preview
Helpdesk endpoint/TLS failure handled safely
Retrieved prompt injection cannot authorize action
Asset-scope bypass rejected
Printer identity replacement detected/flagged
Health unknown evidence not scored healthy
RUL unavailable without validated estimator
Usage unit conversion boundaries tested
```

## Residual risk

Mesmo com esses controls, guidance pode ficar stale, manufacturer behavior pode variar por firmware, end users podem interpretar manual instructions incorretamente e corporate controls podem bloquear capabilities necessárias. Por isso:

- capability/status honesty é mandatory;
- source/version/applicability permanecem visíveis;
- escalation continua fácil;
- real hardware validation é obrigatória para vendor-native claims;
- high-impact operations permanecem fora do early Self-Service scope.

## Threat model update triggers

Revisar este documento ao adicionar:

- inbound ticket automation;
- remote remediation;
- signed organization Knowledge Packs;
- direct Zebra/vendor portal integration;
- firmware updater;
- network/factory reset;
- security auto-hardening;
- persistent Self-Service agent;
- RUL estimator;
- cloud AI using customer evidence;
- multi-tenant Enterprise.
