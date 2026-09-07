# AI and Knowledge Assistance

AI is optional and downstream of deterministic evidence, maintenance policy, and authorization rules.

## Authority model

```text
Windows APIs + Vendor APIs + Technician evidence + Approved rules/policy
                              |
                              v
                       Evidence / Findings
                    +---------+----------+
                    |                    |
                    v                    v
          Deterministic plan/       AI explanation
          maintenance/disposition   (optional)
```

AI is never a privileged, maintenance, or service-disposition control plane.

## Allowed uses

- explain a normalized finding;
- summarize a diagnostic/preventive/service-case bundle;
- retrieve relevant approved manuals/runbooks;
- suggest which deterministic evidence view to inspect next;
- translate/simplify technical evidence;
- draft a support note from verified session facts;
- explain why a maintenance task is due using the source-backed rule;
- summarize a configuration/baseline diff;
- highlight uncertainty or missing evidence.

## Forbidden uses

- autonomous repair execution;
- arbitrary PowerShell/cmd passed to helper;
- enabling a disabled capability;
- overriding organization/customer policy;
- inventing device/technician state;
- defining maintenance intervals or component lifetime from intuition;
- declaring `RemoveFromService` without policy authority;
- turning a trend into a confirmed failure cause;
- automatic firmware/driver/configuration change;
- uploading customer evidence by default.

## Maintenance guardrail

AI may say:

```text
This cleaning task is due because policy X, sourced from the applicable model guide, requires it after the recorded usage interval.
```

AI may **not** invent:

```text
Replace the printhead after 2,000,000 labels.
```

unless that exact threshold is an approved source-backed rule for the applicable device/context.

## Predictive maintenance

LLM output is not predictive maintenance.

M9 research requires real labeled historical data, a defined prediction target, representative train/validation/test splits, calibration, applicability matrix, drift monitoring and cost analysis for false positives/negatives.

Until then AI may summarize trends but must not claim remaining useful life or “failure in N days”.

## Offline-first knowledge

A future local knowledge pack may index manuals/runbooks where redistribution/licensing permits. Answers should cite exact source/version/section where possible.

Do not silently ingest proprietary customer or employer procedures into the public repository.

## Cloud AI

If ever enabled:

- explicit organization/user opt-in;
- provider configuration;
- data classification;
- redaction before transmission;
- retention/contract review;
- no secrets;
- evidence/source citations;
- nonessential to core operation.

If unavailable, deterministic diagnosis/preventive/reporting continues.

## Example

Evidence:

```text
HEAD_OPEN=true
MEDIA_OUT=false
SPOOLER=RUNNING
QUEUE=0
```

Deterministic finding:

```text
Device reports printhead open. Windows Spooler is running and no queue backlog is observed.
```

AI may explain:

```text
Current evidence points to a device-side condition rather than a blocked Windows queue. Follow the approved device check before changing Windows state.
```

Enabled buttons/disposition come from policy and deterministic rules, not model output.
