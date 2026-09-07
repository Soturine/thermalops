# ADR-0001: C#/.NET 10 e WPF para o primeiro Windows Client

- **Status:** Accepted for initial implementation
- **Date:** 2026-09-07
- **Decision owners:** ThermalOps maintainers

## Context

ThermalOps integra profundamente com Windows printing, Print Spooler, WinSpool, Service Control Manager, PnP, Event Log, local IPC, enterprise security controls, Portable packaging e vendor printer SDKs.

O primeiro operating-system family suportado é Windows e os early milestones são centrados em field support/diagnosis nesse ambiente.

A stack precisa favorecer:

- Windows API interop;
- secure local privilege boundary;
- self-contained Portable deployment;
- signing/enterprise distribution;
- testability;
- long-term maintainability;
- vendor SDK integration;
- offline-first behavior.

## Decision

Adotar inicialmente:

- **C#** como implementation language;
- **.NET 10 LTS** como runtime/framework baseline;
- **WPF** para o primeiro Desktop UI;
- self-contained publishing para Portable;
- Windows-native interop behind Application/Domain interfaces;
- code identifiers/internal contracts em inglês;
- UI localization-ready com `pt-BR` como locale inicial de referência.

## Rationale

### C# / .NET

- strong Windows interoperability;
- mature runtime/tooling;
- good async/cancellation primitives;
- strong typing para evidence/policy/RepairPlan contracts;
- suitable IPC/security APIs;
- self-contained publishing;
- good test ecosystem;
- familiar enterprise packaging/signing ecosystem.

### .NET 10 LTS

A linha LTS reduz churn de runtime para uma ferramenta que pretende ser usada em customer/enterprise environments.

A escolha não significa que qualquer vendor SDK é automaticamente compatível. Cada dependency precisa de validation.

### WPF

WPF foi escolhido para primeira UI por:

- maturity;
- Windows-first fit;
- low architecture risk;
- support para desktop patterns/MVVM;
- accessibility/localization capabilities suficientes;
- ausência de necessidade de browser runtime no privileged path.

## Consequences

### Positive

- strong fit para Windows diagnosis;
- simpler native API access;
- self-contained Portable viável;
- consistent language entre Desktop/Application/Helper;
- mature corporate tooling;
- lower initial risk que introducing web shell + local privileged bridge.

### Costs

- UI é Windows-specific;
- WPF modernization/visual polish precisa de design discipline;
- vendor SDK compatibility com .NET 10 precisa ser tested;
- cross-platform UI não é goal inicial.

## Dependency Boundary

Mesmo usando Windows/.NET:

```text
Domain/Application
```

não devem depender diretamente de WPF ou P/Invoke implementation.

Windows-specific details ficam em:

```text
ThermalOps.Infrastructure.Windows
ThermalOps.Desktop
ThermalOps.PrivilegedHelper
```

## Vendor SDK Compatibility

Se um vendor SDK exigir target/runtime diferente:

1. documentar incompatibilidade;
2. avaliar supported newer package/interface;
3. isolar constraint no adapter;
4. não contaminar Domain;
5. criar follow-up ADR se architecture impact for significativo.

Não downgrade global runtime silenciosamente por causa de uma única dependency.

## Portable Implications

Self-contained publish é default para evitar preinstalled runtime requirement.

Target order:

- win-x64 primary;
- win-arm64 após real testing;
- win-x86 somente com demonstrated requirement.

Single-file é desejável, não obrigatório.

## Localization Implications

WPF UI não deve hard-code user-facing strings no business logic.

Resource/localization mechanism será definida no implementation, obedecendo ADR-0005.

Canonical Domain/schema values permanecem em inglês.

## Alternatives Considered

### Electron / React

Advantages:

- familiar web UI ecosystem;
- flexible design;
- potential future cross-platform/web reuse.

Rejected for initial client because:

- larger runtime/deployment surface;
- additional browser/local bridge complexity;
- not needed for current Windows-first scope;
- should not own privileged execution anyway.

Pode ser revisitado se concrete requirement justificar.

### Python / Tkinter / PyQt

Advantages:

- fast prototyping;
- rich ecosystem.

Not selected because target production model enfatiza:

- Windows security boundaries;
- signing;
- self-contained corporate deployment;
- typed privileged contracts;
- long-term enterprise maintenance.

Python continua útil para repository tooling/tests scripts quando apropriado, mas não como main application runtime.

### WinUI 3

Viável e mais moderno em alguns aspectos, porém WPF possui maturity/lower delivery risk para este scope.

Revisit only for concrete product requirement.

### Native C++

Strong Windows access, mas aumenta memory-safety/complexity cost sem necessidade demonstrada para o Domain/UI inteiro.

Pode existir native interop pontual via supported library/API, não como default stack.

## Revisit Triggers

Reavaliar este ADR se:

- .NET 10 deixar de ser suportado antes de production release;
- vendor-critical SDK tornar a stack inviável;
- cross-platform requirement virar business priority;
- WPF não atender requirement essencial de accessibility/deployment;
- Microsoft platform direction exigir migration clara.

Mudança exige novo ADR/migration plan; não alterar stack silenciosamente.
