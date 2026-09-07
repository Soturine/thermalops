# AGENTS.md

Este arquivo é o operating contract para coding agents e automações que trabalham no ThermalOps.

O objetivo não é apenas padronizar estilo de código. ThermalOps é safety-sensitive support software: alterações podem afetar filas de impressão, serviços do Windows, dados de cliente, ações privilegiadas, maintenance recommendations e decisões de escalation. Agentes devem preservar o Domain model, os guardrails e a evidência que justificou cada decisão.

## Leitura obrigatória

Antes de qualquer mudança de arquitetura, comportamento ou segurança, leia nesta ordem:

1. `ENGINEERING_CONSTITUTION.md`;
2. `docs/README.md`;
3. `docs/produto/visao-do-produto.md`;
4. `docs/engenharia/arquitetura.md`;
5. `docs/seguranca/security-e-privacy.md`;
6. o documento funcional relacionado à mudança;
7. ADRs relevantes;
8. `docs/planejamento/roadmap.md` e a issue/milestone correspondente.

Leituras adicionais obrigatórias por área:

- preventive: `docs/produto/manutencao-preventiva.md`;
- field service/escalation: `docs/produto/field-service-e-escalation.md`;
- local remediation: `docs/engenharia/diagnostico-e-remediacao-local.md`;
- packaging/lifecycle: `docs/engenharia/deployment-e-lifecycle.md`;
- fleet: `docs/produto/fleet-e-condition-monitoring.md`;
- AI: `docs/produto/ai-e-knowledge-assistance.md`;
- localization/UI wording: `docs/produto/localizacao-e-terminologia.md`.

Se uma solicitação entrar em conflito com a Constitution, ADR ou safety model, **pare e exponha o conflito**. Não enfraqueça um guardrail silenciosamente para “fazer funcionar”.

## Idioma e naming

A documentação e textos do repositório são pt-BR por padrão, mas termos técnicos consolidados permanecem em inglês.

O código permanece em inglês:

- namespaces;
- classes;
- interfaces;
- methods;
- properties;
- enums;
- schema field names;
- internal contracts;
- telemetry/event type names;
- test names quando isso melhorar a correspondência com a API/código.

Não crie identificadores como `InspecaoDeManutencaoPreventiva` quando o Domain concept aprovado é `MaintenanceInspection`.

A UI é localization-ready. Não espalhe strings hard-coded no code-behind/ViewModel. Use resources/localization boundary conforme a implementação evoluir.

## Non-negotiable constraints

- Domain rules são authoritative.
- Default behavior é read-only.
- Portable Lite é estruturalmente read-only.
- A main UI não permanece elevated.
- Privileged actions são typed, allowlisted, narrow, auditable e policy-gated.
- Nunca crie `ExecuteCommand(string)`, arbitrary PowerShell/cmd/shell, generic process launcher ou equivalente privilegiado.
- Nunca use broad spool-directory deletion como caminho normal para corrigir um selected job/queue.
- Nunca declare physical printer health por um único Windows status value.
- Windows evidence, vendor-native evidence e TechnicianObservation permanecem distinguíveis.
- `Unknown` não vira `Healthy`, `NotDue`, `Pass` ou sucesso por conveniência.
- AI nunca autoriza/executa repair, maintenance due, ServiceDisposition, firmware/configuration changes ou policy override.
- Core field functionality não depende de cloud, login, internet ou telemetry.
- Não há automatic broad network scan.
- Não há automatic customer-data upload ou logging no USB.
- Portable não deixa intentional persistence após clean exit.
- Maintenance interval, threshold e component lifetime exigem source + applicability.
- Não assuma que field technician pode desmontar/reparar hardware.
- Company/customer/vendor-specific support workflow é policy/configuration, não hard-coded public core.
- Imported policy/baseline é untrusted data e nunca cria executable capability.
- Firmware update e driver install exigem ADR, threat analysis, rollback design e milestone approval próprios.
- Não introduza microservices para resolver um problema de modularidade in-process.

## Architecture expectations

Comece e permaneça com modular monolith enquanto ele resolver o problema de forma clara.

Boundaries esperados:

```text
ThermalOps.Desktop
        |
        v
ThermalOps.Application
        |
        v
ThermalOps.Domain
   ^              ^
   |              |
Windows Infra   Vendor Adapters

Approved write only:
Application -> strict IPC -> Temporary Privileged Helper
```

Responsabilidades:

- `ThermalOps.Domain` — entities, value objects, evidence semantics, findings, maintenance, ServiceDisposition, ServiceCase, RepairPlan, policy invariants;
- `ThermalOps.Application` — use cases e orchestration;
- `ThermalOps.Infrastructure.Windows` — WinSpool, SCM, PnP, Event Log e outras boundaries de Windows;
- `ThermalOps.Adapters.Zebra` — capability detection e vendor-native evidence;
- `ThermalOps.Desktop` — WPF delivery/composition;
- `ThermalOps.PrivilegedHelper` — processo elevado mínimo, sem generic command surface.

Domain não depende de WPF, P/Invoke implementation, filesystem/network implementation, vendor SDK, database, installer technology ou AI SDK.

## Evidence discipline

Cada observação importante deve preservar, quando aplicável:

- source;
- timestamp;
- target/canonical resource ID;
- collection outcome;
- normalized value;
- safe raw representation;
- schema/rule version.

Mantenha distintos:

```text
Observed fact
TechnicianObservation
Derived Finding
MaintenanceRecommendation
ServiceDisposition
Operator request
Executed action
Verified result
```

Não compacte tudo em uma string do tipo `Printer OK`.

## Preventive Maintenance discipline

Uma `MaintenanceTaskDefinition` deve preservar:

- task ID;
- version;
- source/reference;
- source version/date quando conhecida;
- applicability por vendor/model/family/capability/context;
- trigger/interval;
- safety notes;
- required policy/capability;
- expected result semantics.

Baseline drift é finding, não fault proof. `HealthAssessment` deve ser component-based e explicável. Numeric Health Score, se implementado, é secundário, deterministic, versioned e com contributions visíveis.

## Local Remediation lifecycle

Toda ação com write segue:

```text
Preflight
 -> Snapshot
 -> Present plan/impact
 -> Explicit confirmation
 -> Execute
 -> Verify
 -> Recovery/Rollback if required
 -> Post-condition
 -> Audit event
```

Exit code `0`, API return success ou ausência de exception **não são suficientes** para marcar repair como validated. É necessário observar o post-condition.

## Field Service e escalation

Não hard-code suposições sobre:

- quem abre RMA;
- quem remove equipamento;
- support level autorizado;
- fabricante que será contatado;
- SLA/entitlement;
- contrato específico;
- internal ticket fields.

Modele com `FieldServicePolicy`, `EscalationPolicy`, `ServiceDispositionRule` e `ServiceCase`, mantendo policy proprietária fora do public core.

## Privacy

- session-local temp storage;
- sanitized export como default;
- full technical/service-case export explícito;
- data minimization;
- redaction/pseudonymization testada;
- attachments são untrusted content;
- nunca commit real customer/employer data.

Não commit:

- hostnames;
- usernames;
- IPs;
- serials;
- tickets;
- screenshots/fotos reais de cliente;
- printer configs reais;
- proprietary service procedures;
- credentials/tokens;
- customer logs.

Use synthetic fixtures.

## Testing rules

Mudanças não estão completas sem testes proporcionais ao risco.

Considere obrigatoriamente:

- Domain unit tests;
- Application orchestration tests;
- adapter contract tests;
- Windows integration tests;
- failure injection;
- helper security tests;
- preventive schedule/baseline tests;
- redaction/ServiceCase tests;
- Portable no-persistence E2E;
- Enterprise lifecycle tests quando existir;
- hardware-in-the-loop para vendor-native claims.

Mocks servem para external boundaries verdadeiras, não para esconder integração quebrada.

## Git e CI

Fluxo esperado:

```text
logical change -> commit -> push -> CI -> next logical change
```

Regras:

- commits logicamente escopados;
- preserve last-known-green;
- não tag/release com CI vermelho;
- não auto-merge safety-sensitive change;
- release tag aponta para source SHA validado;
- não marque check quebrado como opcional apenas para “ficar verde”;
- status report usa `fixed`, `partial`, `experimental`, `deferred`, `not validated` corretamente.

## Documentation e ADRs

Behavior change e docs mudam juntos.

Use ADR para decisões que alterem:

- architecture boundary;
- security/trust boundary;
- persistent lifecycle;
- packaging strategy;
- privilege model;
- localization architecture;
- fleet architecture;
- vendor integration strategy relevante.

Não esconda uma decisão arquitetural importante em comentário de código.

## External code, dependencies e research

Public source não significa reusable source.

Antes de adicionar dependency ou copiar implementação:

- verificar licença;
- attribution;
- maintenance health;
- security history;
- necessity;
- alternatives;
- supply-chain impact.

Research docs informam patterns e riscos, mas não se tornam automaticamente business rules. Prefira official platform/vendor documentation e implementação independente.
