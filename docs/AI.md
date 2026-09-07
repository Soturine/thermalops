# AI and Knowledge Assistance

AI is optional and downstream of deterministic diagnosis.

## Authority model

```text
Windows APIs + Vendor APIs + Rules
              |
              v
          Evidence/Findings
              |
              +--> Repair policy/plan (deterministic)
              |
              +--> AI explanation (optional)
```

AI must never be a privileged-control plane.

## Allowed uses

- explain a normalized finding in technician-friendly language;
- summarize a support bundle;
- retrieve relevant approved manuals/runbooks;
- suggest which deterministic diagnostic view to inspect next;
- translate/simplify technical evidence;
- generate a draft support note based on verified session facts.

## Forbidden uses

- autonomous repair execution;
- arbitrary PowerShell/cmd generation passed to the helper;
- overriding customer policy;
- inventing hardware state;
- turning uncertain evidence into a confident diagnosis;
- uploading customer data by default;
- changing firmware/drivers/configuration without a deterministic approved workflow.

## Offline-first knowledge

A future local knowledge pack can index vendor manuals/runbooks where redistribution/licensing permits it. Answers should cite the exact local source/version used.

## Cloud AI

If ever enabled:

- organization/user opt-in;
- explicit provider configuration;
- redaction before transmission;
- data-classification and retention review;
- no secrets/credentials;
- evidence citations shown with the response;
- feature remains nonessential to diagnosis/repair.

If cloud AI is unavailable, ThermalOps must continue to provide the deterministic finding and recommended action.

## Guardrail example

Input evidence:

```text
HEAD_OPEN=true
MEDIA_OUT=false
SPOOLER=RUNNING
QUEUE=0
```

Deterministic finding:

```text
Device reports print head open. Windows spooler is running and no queue backlog is observed.
```

AI may explain:

```text
Check/close the print head before changing Windows state; current evidence does not justify a spooler restart.
```

The actual set of enabled buttons comes from policy and deterministic repair-plan rules, not the model output.
