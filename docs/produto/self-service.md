# Self-Service / End-User Experience

## Objetivo

Self-Service é um `ExperienceProfile` para end users que precisam verificar impressoras, entender condições simples, executar guided checks, consultar status e preparar support evidence sem receber privilégios técnicos desnecessários.

O objetivo correto não é “rodar sem a TI permitir”. O objetivo é ser seguro, previsível e governável o suficiente para que a organização possa **aprovar uma vez** e permitir uso recorrente por standard users dentro de seus controles de endpoint.

## Positioning

Self-Service não é uma quarta edição do ThermalOps.

```text
ThermalOps
|
+-- Portable Lite
+-- Portable Pro
+-- Enterprise
     |
     +-- ExperienceProfile
          +-- SelfService
          +-- Technician
          +-- AdvancedSupport
```

Edition define deployment/lifecycle/capability envelope. `ExperienceProfile` define presentation, progressive disclosure e subset de capabilities permitidas pela active policy.

## Main goals

Um usuário não técnico deve conseguir, quando a organização permitir:

- ver se a printer está disponível;
- executar Quick Diagnosis;
- entender health/current status em linguagem simples;
- seguir Guided Troubleshooting seguro;
- consultar approved model-aware guides;
- visualizar preventive/maintenance status permitido;
- recheck após uma ação manual simples;
- coletar sanitized evidence;
- preparar ServiceCase/support request;
- receber uma resposta clara quando uma capability for restrita pela policy.

Self-Service não transforma end user em N2/N3 nem em administrator.

## Security premise

```text
Organization approval
  -> signed/approved application
  -> standard-user execution
  -> restrictive PolicyProfile
  -> local/known-endpoint evidence
  -> optional helpdesk integration
```

Não:

```text
Blocked by WDAC/AppLocker/firewall
  -> bypass
```

ThermalOps respeita endpoint controls e mostra `BlockedByPolicy` quando necessário.

## Experience design

A Home do Self-Service deve ser muito mais simples que AdvancedSupport.

Example:

```text
THERMALOPS

Minha impressora
Zebra ZT411 - Expedição 02

Estado geral
Bom, com uma observação

[ Verificar impressora ]
[ Resolver um problema ]
[ Ver manutenção ]
[ Preciso de ajuda ]
```

Não expor por default:

```text
WinSpool handles
SCM internals
PnP instance IDs
raw SGD/ZPL
RepairPlan internals
raw Event Log XML
```

O mesmo Domain/Diagnostic engine é usado; muda presentation e authorization surface.

## Progressive disclosure

### Self-Service

Mostrar:

- friendly status;
- top-level Health components;
- approved warnings;
- guided next steps;
- support request.

### Technician

Adicionar:

- more detailed evidence;
- Preventive Inspection;
- TechnicianObservation;
- baseline comparison;
- counters;
- diagnostic label;
- limited remediation.

### AdvancedSupport

Adicionar:

- raw/normalized evidence;
- rule/source versions;
- deeper Windows/vendor details;
- RepairPlan;
- privileged actions;
- ServiceCase diagnostics.

Não duplicar engines por profile.

## Capability policy

Conceptual `ExperiencePolicy`:

```text
allowQuickDiagnosis = true
allowGuidedTroubleshooting = true
allowPreventiveStatus = true
allowKnowledgeCenter = true
allowEvidenceCollection = true
allowSanitizedServiceCase = true
allowTechnicalDetails = false
allowNetworkDiscovery = false
allowDiagnosticPrint = false
allowSpoolerRestart = false
allowDriverInstall = false
allowFirmwareUpdate = false
allowFactoryReset = false
allowNetworkReset = false
allowPrinterConfigWrite = false
```

Algumas low-risk actions podem ser habilitadas por organization policy depois de validation específica, por exemplo:

```text
allowCancelOwnStaleJob
allowUnpauseAssignedQueue
```

Essas actions continuam typed, scoped, audited e verified.

## Default permission posture

Self-Service é **read-only by default**.

Recommended initial M4/M5 scope:

```text
Status
Quick Diagnosis
GuidedManual steps
Knowledge Center
Health summary
Maintenance status
Evidence collection
Sanitized report
ServiceCase draft
```

Nenhuma UAC prompt deve aparecer no normal Self-Service diagnosis flow.

Se uma operation exigir elevation, o profile deve preferir:

```text
Esta ação requer suporte autorizado.
[ Preparar chamado ]
```

em vez de pedir credential administrativa ao end user.

## Printer selection and scope

Self-Service não deve listar toda a fleet indiscriminadamente.

Potential targeting mechanisms:

- printers installed for current user/device;
- assigned queues;
- current site/department scope;
- explicit allowed asset IDs;
- managed Enterprise assignment;
- manually selected local target when policy permits.

`friendly name` não é authorization identity.

## Local-first operation

Self-Service deve funcionar sem internet para basic workflows:

```text
Windows queue
+ PnP/local printer
+ known configured endpoint
+ vendor-local status
+ local Knowledge Pack
```

No automatic broad network scan.

Se uma installed queue aponta para um known IP/port e a policy permite reachability check, o ThermalOps pode testar aquele endpoint específico.

## Status presentation

Example:

```text
SAÚDE DO EQUIPAMENTO

Estado geral........... Bom
Impressora............. OK
Comunicação............ OK
Windows/Fila........... OK
Mídia.................. OK
Ribbon................. OK
Manutenção............. Atenção

Nenhum erro crítico detectado.
```

Se a evidence não for suficiente:

```text
Não foi possível verificar o estado físico da impressora.
O Windows reconhece a fila, mas isso não confirma que o equipamento está pronto.
```

Nunca simplificar uncertainty para “Tudo certo”.

## Guided Troubleshooting

Self-Service deve usar uma subset de runbooks adequada a end users.

Example:

```text
Problema: Não imprime

1. Windows queue........ OK
2. Comunicação.......... OK
3. Printer status....... Media Out

A impressora informa que está sem mídia.

[ Ver instrução do modelo ]
[ Verificar novamente ]
```

Uma guidance action manual precisa deixar claro:

- o que verificar;
- se é seguro para end user;
- source/model applicability;
- como voltar e recheck.

Não mostrar disassembly/service instructions em Self-Service.

## Health and lifecycle visibility

Self-Service pode mostrar um subset de `Lifecycle & Health`:

```text
Uso acumulado............. disponível quando suportado
Última preventiva......... quando organization history existir
Próxima inspeção.......... apenas se source/policy-backed
Maintenance status........ Current / DueSoon / Due / Unknown
```

Raw odometer/counters podem ficar escondidos se não forem úteis ou se a policy classificar como sensitive operational data.

## “Preciso de ajuda” workflow

Quando o issue não for resolvido:

```text
Quick Diagnosis
  -> Guided Troubleshooting
  -> NotResolved / EscalationRecommended
  -> Generate sanitized ServiceCase draft
  -> Privacy preview
  -> handoff/export/integration
```

Suggested summary:

```text
Printer: Zebra ZT411
Observed problem: Printer not ready
Windows: OK
Transport: OK
Device: MediaOut persists after guided check
Actions performed: manual media verification
Result: NotResolved
Evidence: attached according to policy
```

## Service desk integration

Future connectors may support systems such as ServiceNow, Jira Service Management, Movidesk, Freshservice, Zendesk or a private organization API.

Architecture:

```text
Application
  -> IServiceDeskConnector
       -> Vendor-specific adapter
```

The public core must not hard-code:

- employer URL;
- internal ticket schema;
- credentials;
- queue/project IDs;
- SLA;
- proprietary routing rules.

Direct ticket creation is optional. Exportable `ServiceCase` remains the portable interoperability format.

## Identity and SSO

Enterprise may integrate with Windows/Entra ID or another organization identity provider after an auth/RBAC ADR.

Potential uses:

- resolve current user;
- site/department assignment;
- allowed printers;
- ServiceCase requester metadata;
- authorization policy.

SSO must not become a requirement for Portable/offline diagnosis.

Self-Service should not create a second ThermalOps password if existing enterprise identity can be used safely.

## Deployment models

### Portable Self-Service

Possible for less-restricted environments using Portable Lite.

Requirements:

- organization permits execution;
- standard user;
- no installer;
- no persistence;
- restrictive profile;
- no UAC/write path.

### Managed Self-Service Client

Preferred for tightly controlled enterprises.

```text
IT approves/signs/allowlists package
  -> deploys via Intune / Configuration Manager / approved software catalog
  -> user launches on demand
  -> no repeated IT approval per diagnosis
```

The goal is similar to enterprise self-service tooling: pre-approval and controlled availability, not security bypass.

Microsoft Intune Company Portal is one example of an enterprise pattern where administrators publish apps and users install/use apps made available to them. ThermalOps should be compatible with such managed deployment patterns without depending on one platform.

## Endpoint control compatibility

Self-Service design must explicitly handle:

- App Control for Business / WDAC;
- AppLocker;
- Defender/EDR;
- firewall/proxy restrictions;
- Controlled Folder Access;
- removable-media controls;
- standard-user file/registry ACLs;
- privilege management.

Expected result when blocked:

```text
Capability: Vendor network status
Outcome: BlockedByPolicy
Reason: outbound connection not permitted
Next step: use local checks or contact support
```

Do not recommend disabling security controls.

## Firewall behavior

Document expected network behavior per feature.

Self-Service basic diagnosis should prefer no external internet connection.

Potential connection classes:

```text
Local Windows API
Local USB
Known printer endpoint
Organization helpdesk endpoint
Approved vendor documentation URL
Optional ThermalOps Enterprise API
Optional AI provider
```

Each external class must be independently policy-disableable.

## Privacy

Self-Service is operated by end users, so privacy preview must be understandable.

Before support handoff:

```text
Este pacote incluirá:
- modelo/status da impressora
- driver e fila selecionada
- eventos relevantes
- diagnóstico realizado

Não incluirá por padrão:
- conteúdo de documentos
- credenciais
- outras impressoras
```

Identity-bearing fields such as hostname, IP, serial and username depend on the export policy.

## Ticket deflection

Self-Service can reduce unnecessary support contacts through safe first-level resolution.

Potential future metrics, only with policy/privacy approval:

```text
SelfServiceSessions
ResolvedByGuidance
EscalatedAfterGuidance
AverageResolutionSteps
TopCanonicalSymptoms
BlockedByPolicyCount
```

Do not measure by collecting document content or personal behavior unnecessarily.

A “deflected ticket” is a business metric, not a reason to hide escalation when evidence remains insufficient.

## Failure behavior

Self-Service must handle:

- no printer found;
- printer disconnected;
- vendor status unsupported;
- access denied;
- network blocked;
- knowledge source unavailable offline;
- helpdesk connector unavailable;
- policy changed mid-session;
- endpoint unsupported;
- evidence partial/conflicting.

The UI must always distinguish `Unsupported`, `Blocked`, `Unavailable` and `Fault`.

## Accessibility

Self-Service is likely used by a broader population than Technician mode.

Require:

- keyboard navigation;
- high contrast compatibility;
- clear focus order;
- screen-reader semantics;
- no color-only status meaning;
- plain-language primary text;
- expandable technical detail;
- scalable UI/high DPI;
- localized instructions.

## Non-goals

- bypassing IT policy;
- asking end user for admin credentials;
- exposing AdvancedSupport controls by obscurity;
- making end user responsible for hardware repair;
- broad network discovery;
- unrestricted remediation;
- automatic firmware/factory reset;
- mandatory cloud/helpdesk integration;
- separate duplicated diagnostic engine.

## Domain/Application candidates

```text
ExperienceProfile
SelfServicePolicy
UserCapabilityView
AssignedAssetScope
SupportRequest
ServiceCaseDraft
GuidanceSession
CapabilityPresentation
BlockedCapabilityReason
```

`ExperienceProfile` influences presentation and available use cases; it does not redefine `DiagnosticFinding`, `HealthAssessment` or raw evidence.

## Validation requirements

Before calling Self-Service validated:

- standard-user E2E;
- no-UAC normal flow;
- capability/policy matrix tests;
- no hidden write path;
- endpoint-control blocked behavior;
- offline diagnosis;
- local Knowledge Pack fallback;
- sanitized ServiceCase privacy preview;
- accessibility review;
- localization review;
- same Domain result across SelfService/Technician profiles;
- no automatic broad scan/upload.

## Relação com outros documentos

- [Guided Operations](guided-operations-e-knowledge.md)
- [Lifecycle e Health](lifecycle-e-health.md)
- [Portable](portable.md)
- [Deployment e Lifecycle](../engenharia/deployment-e-lifecycle.md)
- [Security Threat Model complementar](../seguranca/self-service-e-guided-operations-threat-model.md)
- [ADR-0007](../adr/0007-self-service-experience-and-policy.md)
