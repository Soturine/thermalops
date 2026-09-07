# Fleet e Condition Monitoring

A capability de Fleet estende o ThermalOps de um toolkit point-in-time para field support para uma plataforma de lifecycle e Condition Monitoring. Ela é deliberadamente posterior às fundações de read-only diagnosis, local remediation, vendor-native adapters, Preventive Maintenance e ServiceCase.

Fleet não deve contaminar Portable com dependência de backend, account ou persistent agent.

## Objetivos

Enterprise Fleet deve ajudar equipes a responder:

- Quais thermal printers existem e como estão logicamente atribuídas?
- Quais precisam de atenção agora?
- Quais maintenance tasks vencem em breve?
- Quais apresentam configuration drift?
- Quais warnings/errors são recorrentes ou crescentes?
- Quais geram ServiceCases repetidos?
- Quais baselines/policies se aplicam a cada dispositivo?
- O que mudou ao longo do tempo?
- Quais sites/queues/families concentram incidentes?
- Onde a equipe deve atuar primeiro?

## Maintenance by Exception

O primary fleet UX deve priorizar exceções em vez de exigir abertura manual de cada printer.

Exemplo conceitual:

```text
Fleet: 183 printers

Healthy.................... 159
Observation................. 17
Preventive attention......... 5
Critical..................... 2
Maintenance due < 7 days.... 11
Configuration drift.......... 8
Repeated comm errors..........4
Open ServiceCases............ 6
```

Todo aggregate precisa permitir drill-down até:

- affected devices;
- underlying evidence;
- rule/policy version;
- current status;
- last observation;
- acknowledgement/action state.

## Inventory

Inventory precisa modelar identity de forma robusta.

Potential fields:

```text
PrinterIdentity
  internalId
  vendor
  model
  serial?              # policy/privacy controlled
  WindowsQueueIds[]
  PnP identifiers[]
  network endpoints[]
  location/site metadata
  capabilities
  firmware
  firstSeen
  lastSeen
  lifecycleState
```

Friendly name não é identity suficiente.

Device merge/split logic deve evitar associar duas printers físicas diferentes apenas porque nomes coincidem.

## Data Categories

Potential policy-controlled history:

- device identity/capability snapshots;
- firmware/version;
- normalized status observations;
- counters/odometer;
- selected configuration snapshots;
- drift events;
- Preventive Inspections;
- MaintenanceTask results;
- MaintenanceDue history;
- ServiceDisposition;
- ServiceCases;
- Windows print-path errors/events;
- transport failure/timeouts;
- HealthAssessment components;
- rule/policy/baseline/catalog versions;
- acknowledgement/resolution metadata.

Não armazenar label/document contents como fleet telemetry.

## Persistence Boundary

Fleet introduz persistent state e, por isso, exige ADR antes da implementação.

O design precisa definir:

- database technology;
- data model/versioning;
- retention;
- archival/deletion;
- backup/restore;
- migration;
- encryption at rest quando aplicável;
- site/tenant boundaries se existirem;
- offline/degraded operation;
- source-of-truth ownership.

Não adotar database distribuído ou event bus sem problema real que exija isso.

## Condition Trends

Trend deve mostrar observation antes de inference.

Exemplo:

```text
Observed
Transport timeouts in last 4 weekly windows:
1, 2, 5, 11

Derived Trend
Increasing

Recommendation
Inspect network/transport path and compare with peer devices.

Not claimed
Hardware failure confirmed.
```

Potential trend types:

```text
CommunicationFailureTrend
ThermalWarningTrend
StalledJobTrend
ServiceCaseRecurrenceTrend
ConfigurationDriftTrend
UsageCounterTrend
MaintenanceComplianceTrend
FirmwareDivergenceTrend
```

## Peer Comparison

Fleet pode permitir comparação com compatible peer group, desde que applicability seja explícita.

Exemplo de dimensions:

- vendor/model/family;
- DPI;
- firmware range;
- connection type;
- media/application context;
- site/policy profile.

Não comparar tudo contra “fleet average” sem considerar context.

## Alerting

Alerts precisam ser deterministic, explainable, rate-limited e deduplicated.

Lifecycle:

```text
Observed condition
  -> rule evaluation
  -> debounce / persistence window
  -> open alert
  -> acknowledge / assign
  -> resolve / suppress with reason
  -> retain audit/history
```

### AlertRule

Potential fields:

```text
AlertRule
  ruleId
  version
  scope
  evidenceRequirements
  severity
  persistenceWindow
  debounce
  cooldown
  dedupKey
  sourcePolicy
  recommendation
  escalationPolicy
  enabled
```

## Alert Storm Prevention

Transient polling failure não deve gerar centenas de alerts.

Aplicar conforme o caso:

- debounce;
- consecutive-failure threshold;
- hysteresis;
- cooldown;
- deduplication;
- maintenance window suppression;
- aggregate outage detection;
- acknowledgement state.

Uma outage geral de network/service pode exigir um parent event em vez de um alert por printer.

## Health History

Persistir os components que produziram `HealthAssessment`, não somente a cor/final score.

Isso permite responder:

> Por que esta printer mudou de Good para Attention na terça-feira?

Historical record deve guardar rule version para evitar reinterpretar silently um score antigo com regras novas.

## Maintenance Scheduling

Enterprise pode manter:

- last completed task;
- next due;
- due reason;
- calendar/usage trigger;
- source/applicability;
- assigned technician/team;
- blocked status;
- completion evidence;
- overdue duration;
- follow-up from ServiceCase.

Scheduler não inventa due date quando input obrigatório não existe.

## Configuration Baselines

Fleet pode distribuir/gerenciar approved baselines, mas write-back automático não é consequência obrigatória.

Capabilities:

- baseline assignment;
- compatibility validation;
- current vs baseline diff;
- acknowledgement;
- approved exception;
- drift history;
- severity;
- optional remediation plan futuramente, sob policy própria.

## ServiceCase Recurrence

Fleet deve permitir análise de recurrence sem reduzir correlation a causation.

Examples:

```text
Same device: 4 cases / 30 days
Same model/firmware: elevated case rate
Same site: transport incidents elevated
Same config drift: recurring across subset
```

Esses são signals para investigation, não proof automática de root cause.

## Multi-vendor Architecture

Market patterns reforçam a abordagem:

```text
Common Domain
+ Vendor Capability Adapters
+ Policy-driven monitoring
+ Explainable alerts
+ Baselines
+ Audit/history
```

Cada vendor pode exigir protocol diferente: SDK, SNMP, MQTT, HTTP, proprietary commands etc. O Domain não deve fingir que todos os equipamentos expõem capabilities idênticas.

## Potential Components

Somente após ADR:

```text
Managed Agent or Collector
Central API
Database
Policy/Baseline Service
Web Dashboard
Alert Engine
Authentication/RBAC
Audit Log
```

Esses nomes não significam microservices obrigatórios. O primeiro design deve buscar a menor deployment topology que atenda os requisitos.

## Agent / Collector

Se necessário, um managed collector deve:

- usar least privilege;
- ter explicit service identity;
- possuir narrow capabilities;
- usar outbound-only communication quando possível;
- suportar proxy/offline que o target environment exija;
- ter update lifecycle gerenciado;
- não herdar unrestricted Portable helper privilege;
- expor health/readiness;
- tratar device responses como untrusted.

## Authentication e RBAC

Se central services existirem, definir:

- identity provider/integration;
- user/service authentication;
- role model;
- site/device scope;
- permission boundaries;
- audit log;
- break-glass admin;
- session expiration;
- secrets/token handling.

Potential roles devem surgir de use cases reais, não de uma lista genérica arbitrária.

## TLS e Certificates

Distributed components exigem design para:

- TLS versions;
- certificate issuance;
- trust roots;
- rotation;
- expiration;
- revocation/compromise;
- hostname/device identity;
- offline enrollment quando necessário.

Não usar certificate validation bypass em production.

## Privacy e Retention

Fleet precisa de policy explícita para:

- identifiers;
- event retention;
- ServiceCase retention;
- attachment retention;
- deletion/archival;
- access/audit;
- data export;
- backup lifecycle.

Document/job content permanece fora de telemetry por default.

## Observability do próprio ThermalOps Enterprise

Distributed components devem expor:

- health;
- readiness;
- structured logs;
- metrics;
- queue/backlog quando houver;
- collection success/failure rate;
- database migration status;
- alert-engine status;
- version/build identity.

Tracing distribuído só é exigido quando existir distributed request flow que realmente se beneficie dele.

## Performance

Measure:

- device polling latency;
- concurrency limits;
- network traffic;
- CPU/memory do collector;
- database growth;
- alert-evaluation latency;
- dashboard query performance;
- offline backlog/recovery.

Não aumentar polling frequency para parecer “realtime” sem avaliar impacto no device/network.

## Predictive Maintenance Boundary

Fleet history habilita research, mas não automaticamente predictive maintenance.

Antes de predictions, cumprir M9:

- labeled representative data;
- defined target;
- train/validation/test separation;
- calibration;
- cost analysis;
- applicability matrix;
- drift monitoring;
- human review.

## Portable Independence

Mesmo com Enterprise disponível:

```text
Portable + offline endpoint
```

continua capaz de diagnosis, preventive inspection, reporting e policy-permitted local work sem Central API.

Essa independência é um product invariant.

## Exit Criteria para Fleet inicial

Antes de chamar Fleet de validated:

- architecture ADR accepted;
- identity model tested;
- security/RBAC reviewed;
- retention policy definida;
- backup/restore tested;
- alert rules explainable;
- alert-storm controls validated;
- Portable independence tested;
- trend UI não apresenta causation indevida;
- upgrade/migration tested;
- operational observability existe.
