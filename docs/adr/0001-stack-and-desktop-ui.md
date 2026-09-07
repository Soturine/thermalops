# ADR-0001: C#/.NET 10 and WPF for the first Windows client

- Status: Accepted for initial implementation
- Date: 2026-09-07

## Context

ThermalOps integrates deeply with Windows printing, services, PnP, eventing, local IPC, enterprise security controls, portable packaging, and vendor printer SDKs. The first supported operating-system family is Windows.

## Decision

Use:

- C#;
- .NET 10 LTS as the initial runtime/framework baseline;
- WPF for the first desktop UI;
- self-contained publishing for Portable;
- Windows-native interop/adapters behind application/domain interfaces.

## Rationale

- strong Windows API interoperability;
- mature desktop/runtime ecosystem;
- good fit for service/IPC/security primitives;
- self-contained deployment supports portable use;
- WPF is stable and sufficient for the technician UI;
- avoids a browser/runtime bridge in the privileged control path.

## Consequences

- Windows-first product;
- UI project is platform-specific;
- Domain/Application remain platform-independent where practical;
- vendor SDK compatibility must be validated with .NET 10;
- if a vendor SDK requires a different target/runtime, isolate that constraint in the adapter and create a follow-up ADR.

## Alternatives considered

### Electron/React

Attractive for web UI skills, but adds a larger runtime and should not own privileged execution. It remains a possible future UI option if a concrete cross-platform/web-shell need appears.

### Python/Tkinter

Good for prototypes/scripts but less aligned with the intended Windows security, packaging, helper, signing, and enterprise deployment model.

### WinUI 3

Viable, but WPF is chosen initially for maturity and lower delivery risk. Revisit only for a concrete product requirement.
