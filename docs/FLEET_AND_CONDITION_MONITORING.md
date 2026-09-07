# Fleet and Condition Monitoring

Fleet capability extends ThermalOps from a point-in-time field toolkit into a lifecycle and condition-monitoring platform. It is intentionally deferred until the read-only, repair, vendor-adapter, support, and preventive foundations are trustworthy.

## Goals

Enterprise fleet mode should help teams answer:

- What thermal printers exist and where are they logically assigned?
- Which devices need attention now?
- Which maintenance tasks are due soon?
- Which printers show configuration drift?
- Which warnings/errors are recurring or increasing?
- Which devices repeatedly generate service cases?
- Which baselines/policies apply to each device?
- What changed over time?

## Maintenance by exception

The primary fleet UX should prioritize exceptions, not require opening every device.

Example:

```text
Fleet: 183 printers

Healthy................... 159
Observation................ 17
Preventive attention........ 5
Critical.................... 2
Maintenance due < 7 days... 11
Configuration drift......... 8
Repeated comms errors........4
```

Every aggregate must drill down to the underlying devices and evidence.

## Data categories

Potential policy-controlled historical data:

- device identity and capability snapshot;
- firmware/version;
- normalized status observations;
- selected counters/odometer values;
- configuration snapshots and drift events;
- maintenance inspections and tasks;
- service dispositions;
- service cases;
- print-path errors/events;
- transport failures/timeouts;
- health assessments and their rule versions;
- policy/baseline versions.

Do not store document/label contents as fleet telemetry.

## Trends

Condition trends must report observation before inference.

Example:

```text
Observed
Transport timeouts in last 4 weekly windows:
1, 2, 5, 11

Derived trend
Increasing

Recommendation
Inspect network/transport path and compare with peers.

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
```

## Alerting

Alerts should be rule-based, rate-limited, deduplicated, and explainable.

Alert lifecycle:

```text
Observed condition
  -> rule evaluation
  -> debounce/persistence window
  -> open alert
  -> acknowledge/assign
  -> resolve or suppress with reason
```

Avoid an alert storm for transient polling failures.

Alert rules carry:

- rule ID/version;
- scope;
- evidence requirements;
- severity;
- persistence/debounce requirement;
- cooldown/dedup key;
- source policy;
- recommended action;
- escalation policy.

## Health history

Store the components that produced a health assessment, not only the final color/score.

This allows later questions such as:

> Why did this device change from Good to Attention on Tuesday?

## Fleet architecture boundary

Fleet requires a dedicated ADR before implementation because it introduces persistence, identity, authentication, authorization, network services, retention, upgrades, and operational ownership.

Portable must not depend on Fleet to perform core diagnosis or preventive inspection.

Potential future components:

```text
Managed Agent or Collector
Central API
Database
Policy/Baseline service
Web dashboard
Alert service
Authentication/RBAC
Audit log
```

These are not permission to create microservices by default. Start with the smallest maintainable deployment that meets the real need.

## Multi-vendor learning

The market validates several useful design patterns:

- SOTI Connect manages lifecycle/health for multiple industrial/mobile printer OEMs, including Zebra, Honeywell, TSC, SATO, Toshiba and others;
- SOTI Connect uses OEM/protocol adapters rather than forcing one protocol on every printer;
- TSC Console Web emphasizes centralized monitoring, proactive rule-based alerts, activity logs, remote management and preventive maintenance;
- Zebra Printer Profile Manager Enterprise demonstrates centralized configuration/profile management for Zebra fleets.

ThermalOps should borrow **patterns**, not copy implementations:

```text
common domain
+ vendor capability adapters
+ policy-driven monitoring
+ explainable alerts
+ configuration baselines
+ audit/history
```

## Security and privacy

Fleet mode requires explicit design for:

- device/service authentication;
- RBAC;
- least-privilege agent identity;
- TLS/certificate lifecycle;
- secrets management;
- retention/deletion policy;
- tenant/site boundaries if applicable;
- audit log integrity;
- API rate limits;
- health/readiness;
- backup/restore;
- offline/degraded behavior;
- update strategy.

No central monitoring should silently inherit Portable's local privileges.

## Predictive maintenance boundary

Fleet history enables future research but does not automatically justify predictive claims. See `PREVENTIVE_MAINTENANCE.md` and `AI.md`.
