# Testing Strategy

ThermalOps combina Domain rules, Windows integration, vendor protocols, Preventive Maintenance, TechnicianObservation, privileged execution, support exports, lifecycle/packaging e futura Fleet. A estratégia de testes deve acompanhar o risco real de cada boundary, não apenas maximizar quantidade de testes.

## Princípios

- testar business rules no nível mais baixo possível;
- testar integrações reais onde mocks esconderiam problemas;
- manter poucos E2E, mas representativos;
- negative paths são obrigatórios para privileged/write behavior;
- hardware claims exigem hardware-in-the-loop;
- Portable claims exigem no-persistence verification;
- Enterprise lifecycle claims exigem install/upgrade/uninstall tests;
- maintenance claims exigem source/applicability validation;
- AI não pode ser requisito para passar workflow determinístico.

## Test Pyramid

```text
                 E2E / HIL
                /         \
        Windows / lifecycle integration
             /               \
      Adapter contract / Application
           /                     \
              Domain unit tests
```

O volume maior fica no Domain; os testes mais caros ficam concentrados em boundaries que realmente precisam deles.

## Domain Tests

Devem cobrir, entre outros:

### Evidence e Status

- Windows status flag normalization;
- múltiplas flags simultâneas;
- unknown/unavailable state;
- evidence source preservation;
- certainty semantics;
- `Unknown` nunca virando `Healthy` por default;
- EvidenceCompleteness independente de health.

### Printer Identity

- friendly names iguais não fundem devices distintos;
- partial identity evidence;
- PnP + queue + vendor identity correlation;
- identity conflict;
- stale endpoint evidence;
- serial absent/hidden by policy.

### Diagnostic Rules

- expected Finding para evidence suficiente;
- insufficient evidence;
- conflicting sources;
- vendor-native condition precedendo Windows remediation quando aplicável;
- stale job rule;
- transport failure rule;
- rule version preserved.

### Maintenance

- `MaintenanceTaskDefinition` applies / does not apply / applicability unknown;
- vendor/model/family mismatch;
- firmware range boundary;
- media/application context mismatch;
- source missing/invalid;
- calendar interval boundaries;
- usage counter threshold boundaries;
- `DueSoon`/`Due`/`Overdue` transitions;
- missing counter -> `Unknown`, não `NotDue`;
- blocked task;
- MaintenancePolicy version behavior;
- approved exception/acknowledgement.

### Baseline

- compatible baseline;
- incompatible DPI/model/context;
- version mismatch;
- configuration drift;
- acknowledged drift;
- approved exception;
- missing baseline;
- stale baseline;
- baseline never authorizes write automatically.

### HealthAssessment

Se implementado:

- every HealthContribution visible;
- deterministic result;
- rule versioning;
- unknown handling;
- score normalization boundaries;
- incompatible comparison classes;
- no AI-generated authoritative score.

### ServiceDisposition

- policy allows/denies disposition;
- `RemoveFromService` requires explicit authority;
- escalation with insufficient field authority;
- operator-selected vs rule-recommended attribution;
- disposition does not overwrite raw device state.

### RepairPlan

- preconditions;
- impact calculation;
- target scope;
- capability reduction by policy;
- confirmation requirement;
- expected post-condition;
- recovery path requirement;
- no arbitrary command action type.

### Privacy/Redaction

- usernames;
- hostnames;
- IPs;
- UNC paths;
- document/job names;
- serials;
- stable per-bundle pseudonyms;
- unrelated printer exclusion;
- nested structures;
- localization does not alter canonical schema values.

## Application Tests

Cobrir orchestration com controlled adapters:

- evidence collection order/parallelism;
- cancellation;
- per-adapter timeout;
- partial collection;
- finding aggregation;
- Quick Diagnosis workflow;
- Preventive Inspection workflow;
- TechnicianObservation attribution;
- baseline import/validation;
- ServiceCase generation;
- Support Bundle generation;
- RepairPlan lifecycle;
- no write path em Lite/`--readonly`;
- Customer Safe restrictions;
- AI unavailable -> deterministic flow continues;
- localization resource failure -> safe fallback sem alterar decision.

## Windows Integration Tests

Executar em controlled Windows runners/VMs.

### WinSpool

- printer enumeration;
- selected queue info;
- job enumeration;
- multiple status flags;
- no-printer scenario;
- inaccessible print server/queue;
- selected-job cancellation em dedicated test environment.

### Service Control Manager

- read Spooler state;
- startup/config evidence;
- access denied;
- controlled stop/start somente em dedicated environment;
- service already stopped;
- stop timeout;
- start failure;
- external state change durante operation.

### PnP / SetupAPI

- local printer/PnP enumeration quando environment permitir;
- disconnected device;
- multiple similar devices;
- mapping unavailable;
- access restriction.

### Event Log

- relevant provider/channel access;
- no matching events;
- malformed/unexpected event data;
- access denied;
- bounded query window.

### Filesystem/Temp

- session directory creation;
- restrictive permissions quando suportado;
- cleanup;
- locked file;
- disk full/quota simulation onde viável;
- reparse-point/path safety nos privileged paths.

## Vendor Adapter Contract Tests

Cada adapter precisa de contract suite comum.

Testar:

- capability discovery;
- valid response;
- multiple simultaneous flags;
- unknown firmware field;
- unsupported command/capability;
- truncated response;
- malformed response;
- oversized response;
- timeout;
- disconnect;
- reconnect/stale data behavior;
- encoding issues;
- counter numeric boundaries;
- config values/units;
- invalid/untrusted strings;
- cancellation.

Adapter não deve lançar vendor-specific behavior para dentro do Domain sem normalization.

## Zebra Hardware-in-the-Loop

Antes de declarar support para model/capability, registrar:

```text
Model
DPI
Firmware
Connection type
Windows driver/version
Adapter version
Test date
Capabilities tested
Expected/observed result
Known limitations
```

Initial matrix deve priorizar hardware fisicamente disponível.

Claims ficam `experimental` ou `not validated` até HIL necessário existir.

### HIL Scenarios

Quando seguro e reproduzível:

- ready state;
- head open/closed;
- media out/present;
- ribbon state em model aplicável;
- paused;
- transport disconnect/reconnect;
- supported counter read;
- supported config read;
- malformed/timeout simulation quando possível;
- diagnostic print sob test policy.

Não criar unsafe hardware condition apenas para satisfazer teste.

## Preventive Maintenance Tests

Além dos Domain tests:

- source-backed task rendering;
- source/version visible;
- technician checklist persistence apenas na session esperada;
- incomplete checklist;
- task blocked by policy;
- maintenance report automatic/manual separation;
- imported baseline corruption;
- incompatible baseline warning;
- previous inspection import;
- no hidden history em Portable;
- localized task labels sem alterar task ID;
- safety note present when required;
- predictive claim path unavailable antes de M9.

## ServiceCase e Support Bundle Tests

- sanitized vs FullTechnical vs VendorServiceCase;
- privacy preview matches actual fields;
- manifest includes missing/blocked/unsupported sections;
- file hash consistency;
- schema version included;
- timeline ordering;
- action history separates request/execution/verification;
- attachments opt-in;
- unsafe filename normalization;
- archive traversal rejection;
- absolute path rejection;
- zip-bomb/file-count/size limits;
- metadata stripping policy;
- corrupt archive input;
- localized human report com invariant machine JSON.

## Privileged Helper Security Tests

Obrigatórios em M2+:

- unauthorized caller;
- wrong user/session;
- wrong nonce/token;
- replayed request;
- unsupported protocol version;
- unknown action type;
- oversized payload;
- malformed payload;
- canonical target tampering;
- UI-provided display name spoofing;
- policy mismatch;
- helper binary mismatch/signature failure quando implementado;
- UAC denied;
- timeout;
- helper crash;
- UI exits mid-operation;
- IPC client disconnect;
- orphan helper cleanup;
- attempt to request arbitrary shell capability;
- reparse-point/path tampering;
- request for unrelated queue/resource.

## Failure Injection

Mandatory cases para local remediation e export/lifecycle:

- Spooler already stopped;
- Spooler cannot stop;
- Spooler stops but cannot start;
- service state changes externally;
- job disappears between plan and execution;
- access denied;
- selected printer disconnects;
- device returns stale/malformed data;
- network timeout;
- support-bundle write fails;
- destination removed;
- disk full;
- cleanup file locked;
- helper exits unexpectedly;
- policy changes mid-session;
- baseline corrupted;
- report localization resource missing;
- Enterprise migration failure;
- installer rollback failure path quando testável.

## Portable E2E

### Before/After Persistence Diff

Em clean VM/snapshot, comparar antes e depois:

- services;
- scheduled tasks;
- Run/Startup entries;
- ThermalOps processes;
- expected IPC endpoints;
- app-owned registry state;
- temp/session directories;
- executable-directory/USB logs;
- installed packages/components.

Explicit exports são exceção esperada.

### Minimum Portable Scenarios

1. no printers installed;
2. one controlled Windows queue;
3. `--readonly` under standard user;
4. `--readonly` launched by Administrator;
5. Customer Safe;
6. Preventive Inspection com synthetic catalog/baseline;
7. ServiceCase sanitized export;
8. corrupted baseline import;
9. offline execution;
10. endpoint policy blocks an optional operation;
11. clean exit/no persistence.

## Enterprise Lifecycle Tests

Quando M5 existir:

- clean install;
- silent install;
- silent uninstall;
- offline install;
- invalid signature/package;
- N-1 -> N upgrade;
- schema migration;
- migration failure;
- rollback/recovery;
- policy/baseline/history preservation;
- clean uninstall;
- retention option behavior;
- service startup/recovery;
- no-reboot normal path;
- blocked-by-policy behavior;
- update deferral/channel quando updater existir.

Use clean VM snapshots para evitar false positives de state residual.

## Fleet Tests

Quando M6 existir:

- device identity lifecycle;
- duplicate/collision handling;
- polling timeout/backoff;
- alert debounce;
- deduplication;
- cooldown;
- maintenance-window suppression;
- parent outage aggregation;
- RBAC scope;
- audit log;
- retention/deletion;
- backup/restore;
- migration;
- offline collector backlog/recovery;
- certificate rotation/expiry scenarios;
- dashboard aggregate -> evidence drill-down consistency;
- trend calculation/versioning;
- no document-content telemetry.

## Localization Tests

- all required resource keys present;
- pt-BR fallback behavior;
- en-US sample locale quando existir;
- no Domain decision changes across locale;
- report machine schema unchanged;
- long labels/layout;
- DPI/scaling;
- date/time/number formatting;
- screen-reader accessible names;
- safety-critical warning reviewed, not solely machine translated.

## AI Evaluation

AI is optional, mas quando existir:

- groundedness;
- evidence/source citation accuracy;
- unsupported-claim rate;
- uncertainty behavior;
- prompt injection from retrieved docs/device text;
- privacy/redaction;
- multilingual consistency;
- deterministic fallback;
- no action authorization from model output.

AI tests nunca substituem Domain tests.

## Performance Budgets

Medir, não adivinhar.

Potential metrics:

- app startup;
- time to first diagnosis;
- Quick Diagnosis duration;
- per-device timeout;
- UI responsiveness;
- Preventive Inspection duration;
- bundle generation time/size;
- memory usage;
- fleet polling throughput;
- alert evaluation latency;
- DB growth.

Não sacrificar safety por benchmark superficial.

## Test Data

Use synthetic fixtures por default.

Nunca colocar em repo:

- customer logs;
- real hostnames/IPs;
- real serials ligados a cliente;
- proprietary procedures;
- credentials;
- customer screenshots;
- document contents.

Real HIL metadata deve ser minimizada e sanitizada quando registrada.

## Flakiness

Flaky test não deve ser simplesmente retried até ficar verde.

Investigar:

- timing race;
- environment dependency;
- device state leak;
- shared queue/service interference;
- network instability;
- insufficient isolation.

Retry pode existir para known transient external setup, mas resultado final precisa continuar significativo.

## CI Strategy

Stages crescem com implementação:

1. docs validation;
2. formatting/lint;
3. build;
4. Domain unit tests;
5. Application/component tests;
6. adapter contract tests;
7. Windows integration tests;
8. security/static analysis;
9. dependency/license checks;
10. packaging/lifecycle tests;
11. HIL release gate quando claim exigir.

## Definition of Validated

Uma feature não é `validated` só porque unit tests passam.

Examples:

- Windows integration feature -> Windows integration test;
- privileged remediation -> security + failure-path test;
- Zebra native capability -> compatible real hardware;
- Preventive task/due claim -> source/applicability tests;
- Portable no-persistence -> E2E before/after;
- Enterprise lifecycle -> install/upgrade/uninstall matrix;
- Fleet alert -> persistence/dedup/evidence drill-down tests;
- predictive claim -> M9 validation program.

## Test Status Reporting

Use:

- `fixed` — implementação e required validation completas;
- `partial` — criteria faltando;
- `experimental` — funciona em controlled subset;
- `deferred` — intentionally postponed;
- `not validated` — implementação existe sem required validation.

Um green happy path não transforma capability física em production-ready.
