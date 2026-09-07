# Referências Públicas e Padrões Externos

Este documento registra public research que influencia decisões do ThermalOps. Ele **não é dependency list, não é licença para copiar implementation code e não transforma um produto externo ou página pública em business rule**.

O objetivo é preservar contexto: por que determinadas abstrações existem, quais capabilities já aparecem no mercado e quais riscos precisamos considerar antes de implementar.

## Regras de Research

- preferir official platform/vendor documentation;
- registrar pattern/capability, não copiar implementation;
- verificar license antes de reutilizar source/dependency;
- revalidar docs antes da implementação porque APIs/products mudam;
- public service/job pages podem informar generic requirements, mas não internal process;
- não registrar customer/employer confidential data;
- não implicar partnership, certification, endorsement ou validated compatibility;
- separar fact pública de design inference do ThermalOps.

## Microsoft Windows Printing

ThermalOps depende de uma leitura correta do Windows print subsystem.

Public platform concepts relevantes incluem:

- WinSpool APIs para printer/job enumeration/control;
- `PRINTER_INFO_2` e status flags;
- Service Control Manager para Print Spooler;
- PnP/SetupAPI para device evidence;
- Windows Event Log;
- Windows application-control/security guidance.

### Design implications

- não parsear PowerShell/CLI quando supported API existir;
- Windows queue status não é physical readiness;
- status flags podem coexistir;
- selected-job control é preferível a broad spool cleanup;
- Spooler state deve ser preservado/validado durante remediation;
- PrintNightmare/Point-and-Print history reforça que driver/policy behavior merece conservative design.

## Zebra Routine Maintenance

A documentação pública Zebra ZT411/ZT421 possui seção específica de routine maintenance e cleaning schedule.

Ela cobre, conforme configuração/modelo:

- printhead;
- platen roller;
- media/ribbon sensors;
- media/ribbon paths;
- tear-off/peel areas;
- take-label sensor;
- cutter-related parts;
- outros componentes da família.

Os intervals variam conforme componente e operating context. A documentação também indica que published intervals são guidance e podem precisar de adaptação ao application/media.

### Design implications

- maintenance schedule é model/family/context-specific;
- não existe universal “Zebra schedule”;
- task precisa preservar source/version/applicability;
- media/application pode alterar frequência;
- technique/safety note faz parte da task;
- ThermalOps deve apontar para approved instruction em vez de condensar procedimento detalhado em receita genérica potencialmente insegura.

### ThermalOps response

Usar:

```text
MaintenanceTaskCatalog
MaintenanceTaskDefinition
MaintenancePolicy
MaintenanceDue
```

em vez de hard-coded global intervals.

## Zebra Native Status e Configuration

Zebra Link-OS SDK e printer command interfaces fornecem vendor-native status/configuration capabilities em devices compatíveis.

Potential concepts públicos úteis:

- ready-to-print;
- head open;
- media/ribbon state;
- paused;
- temperature warnings;
- device errors/warnings;
- firmware;
- configuration variables via supported mechanisms;
- counters/odometer em devices que expõem os dados.

### Design implications

- capability detection é obrigatória;
- model/firmware/connection podem alterar capabilities;
- device-native evidence fica separada de Windows evidence;
- malformed/timeout response precisa de defensive parser;
- configuration read não concede configuration write.

## Zebra Link-OS / SGD / ZPL

Direction de implementation:

- prefer supported Link-OS APIs/SDK onde fizer sentido;
- usar SGD para allowlisted status/config queries quando suportado;
- usar ZPL status query quando apropriado;
- não criar generic arbitrary ZPL/SGD privileged console;
- validar physical behavior em real hardware antes de support claim.

## Zebra Support e Repair

Public Zebra support resources distinguem technical support de repair request/repair status/warranty/service workflows.

Alguns workflows públicos podem usar:

- model;
- serial number;
- firmware;
- problem category;
- warranty/service entitlement;
- repair/RMA information.

### Design implications

- diagnosis e physical repair/RMA são etapas distintas;
- ServiceCase precisa conseguir incluir model/serial/firmware quando autorizado;
- warranty/entitlement não deve ser guessed localmente;
- direct submission não é early requirement;
- future vendor connector precisa de official interface, authentication, privacy e error model.

## Zebra Printer Profile Manager Enterprise (PPME)

PPME demonstra que centralized Zebra configuration/profile management é uma category real.

### Design implications

- baselines/profiles têm valor operacional;
- configuration drift é útil em support/preventive context;
- central remote management pertence ao Enterprise surface;
- ThermalOps não precisa recriar toda vendor suite;
- complementary positioning é mais racional que breadth prematura.

## Zebra OneCare / Visibility Services

Public Zebra service offerings reforçam que lifecycle, service entitlement e managed visibility são problemas reais em enterprise printing.

### ThermalOps boundary

ThermalOps não declara substituição desses serviços nem compatibility/partnership sem validation/agreements. A utilidade inicial permanece field diagnosis, preventive inspection, evidence e safe handoff.

## Public Field-Service Market Evidence: Proxion Solutions

Material publicamente disponível da Proxion Solutions serve como **market/context evidence**, não como fonte de processo proprietário.

Páginas públicas de manutenção descrevem cenários envolvendo:

- preventive/corrective maintenance;
- equipamentos sob contrato;
- lifecycle/inventory management;
- relação com fabricante/assistência;
- manutenção de equipment availability/configuration.

Uma página pública de vaga para suporte descreve atividades como:

- startup de equipment/software;
- customer visits para analysis/problem solving;
- preventive, corrective e diagnostic visits;
- limited repairs, incluindo exemplos de wear-part replacement em thermal printers;
- remote support tickets/service orders;
- service reports e knowledge-base material;
- inventory visits;
- acompanhamento de manufacturer maintenance e SLA;
- diagnosis de equipamento encaminhado para manutenção;
- reconfiguration de equipment retornado de maintenance conforme configuração estabelecida.

### Design implications

Isso valida genericamente a combinação:

```text
Field Diagnosis
+ Preventive Inspection
+ Limited Authorized Local Remediation
+ Inventory
+ Reports
+ Configuration Baseline/Evidence
+ Manufacturer Maintenance Tracking
+ Escalation / ServiceCase
```

Também demonstra por que não devemos assumir extremos:

- field technician não é necessariamente somente observer;
- field technician também não é necessariamente full bench-repair technician.

A solução correta é capability/policy-driven field scope.

### Confidentiality boundary

Não colocar no public core:

- internal ticket fields;
- customer names/configurations;
- internal SLA;
- proprietary workflow;
- escalation contacts;
- entitlement rules;
- service-contract specifics.

Mapear necessidades legítimas para abstrações:

```text
FieldServicePolicy
MaintenancePolicy
EscalationPolicy
ServiceCase
MaintenanceBaseline
ReportTemplate
```

## SOTI Connect

Public SOTI Connect material demonstra multi-vendor lifecycle management para industrial/mobile printers e outros devices.

Publicly presented OEM/device ecosystem inclui fabricantes como Zebra, Honeywell, TSC, SATO, Toshiba e outros, com protocol/integration approaches que variam por família.

### Design implications

- multi-vendor printer management é uma category real;
- common Domain + vendor/protocol adapters faz sentido;
- não forçar um único protocol universal;
- centralized inventory/health/lifecycle têm valor;
- onboarding/discovery precisam de policy/capability awareness;
- Fleet adiciona auth, persistence e operational complexity;
- Portable deve permanecer independente.

## TSC Console / TSC Console Web

Public TSC tools enfatizam capabilities como:

- centralized printer management;
- monitoring;
- configuration;
- troubleshooting;
- rule-based alerts;
- activity logs;
- preventive maintenance;
- printer health information;
- one-click diagnostics em alguns contexts.

### Design implications

- maintenance by exception é boa fleet UX;
- alerts precisam de debounce/dedup/cooldown;
- health precisa drill-down para evidence;
- audit/activity history melhora handoff;
- remote management agrega security/authorization risk;
- vendor health metrics ficam atrás de adapter capability boundary.

## Honeywell

Honeywell é um potencial future adapter por presença no mercado de thermal/industrial printing, mas nenhuma capability deve ser assumida sem official protocol/SDK review e hardware availability.

Before adapter:

- identify supported SDK/protocol;
- license review;
- connection methods;
- status/config capabilities;
- security model;
- HIL device;
- adapter contract mapping.

## TSC

Além das fleet-management patterns, um future TSC adapter deve ser tratado separadamente de TSC Console/Web.

Não copiar product-specific management behavior para o Domain. Implementar apenas capabilities necessárias, oficialmente suportadas e testadas.

## SATO e Outros Vendors

SATO e outros vendors permanecem candidates, não commitments.

Adicionar somente quando houver:

- real demand;
- hardware/test access;
- official docs/SDK/protocol;
- licensing clarity;
- business value;
- adapter test matrix.

## Browser / Local Bridge Pattern

Ferramentas como QZ Tray demonstram um pattern relevante: separar browser/app-facing interface de uma local privileged/action surface e usar explicit trust/signing mechanisms.

### Design implication

ThermalOps não deve expor browser-controlled arbitrary local action. Se future browser integration existir, a privileged plane continua narrow, typed e authenticated.

## Endpoint Management Patterns

Microsoft Intune/Configuration Manager e enterprise software distribution reforçam requirements como:

- silent install/uninstall;
- deterministic exit codes;
- detection rules;
- signed publisher;
- offline/controlled deployment;
- predictable upgrade behavior.

ThermalOps deve produzir standards-compatible packages em vez de embutir vendor-specific deployment logic no app.

## Application Control Patterns

WDAC/AppLocker/EDR environments favorecem:

- stable publisher identity;
- documented behavior;
- signed binaries;
- clear child-process behavior;
- minimal elevation;
- known file/network paths.

Isso influencia Portable/helper design.

## NIST SSDF

NIST Secure Software Development Framework serve como referência de secure development lifecycle.

Relevant patterns:

- prepare organization/project;
- protect software/source/artifacts;
- produce well-secured software;
- respond to vulnerabilities;
- supply-chain awareness.

ThermalOps aplica guidance proporcional ao scope, sem alegar formal compliance/certification sem assessment.

## OWASP Guidance

OWASP ASVS/API guidance se torna especialmente relevante quando Central API/web services aparecerem no Enterprise.

Early Desktop-only code não precisa fingir que é web application, mas future API design deve considerar:

- authentication;
- authorization;
- input validation;
- rate limiting;
- logging;
- secure error behavior;
- secrets;
- transport security.

## Research-to-Implementation Rule

Research gera candidate requirement/pattern.

Antes de virar implementation rule:

```text
Public observation
 -> validate relevance
 -> map to ThermalOps requirement
 -> check Constitution/ADR
 -> define Domain boundary
 -> define tests
 -> implement independently
```

Não copiar code/UI/workflow apenas porque outro produto faz daquela forma.

## Comparison Principles

ThermalOps procura combinar:

```text
Portable field diagnostics
+ Windows print-subsystem evidence
+ vendor-native evidence
+ Preventive Inspection/checklists
+ source-backed maintenance
+ configuration baseline/drift
+ safe Local Remediation
+ ServiceCase/escalation package
+ privacy-first offline operation
+ future multi-vendor Fleet/Condition Monitoring
```

O objetivo inicial não é vencer mature suites em breadth. É ser excepcionalmente confiável em diagnosis, preventive inspection, evidence, safe remediation, deployment simplicity e escalation.

## Research Implications for Roadmap

1. acertar read-only Windows evidence;
2. implementar local remediation somente após privilege/rollback/security design;
3. implementar Zebra native status/capability detection com hardware real;
4. construir Preventive Maintenance com source-backed tasks;
5. construir ServiceCase/baselines/reports;
6. harden packaging/signing/deployment;
7. adicionar Fleet só após persistence/auth/RBAC ADRs;
8. adicionar vendors por real demand;
9. manter AI explanatory;
10. tratar Predictive Maintenance como research até dados/validation justificarem.

## Public Reference Entry Points

Revalidar versões atuais durante implementation:

- https://learn.microsoft.com/windows/win32/printdocs/
- https://learn.microsoft.com/windows/win32/services/service-control-manager
- https://docs.zebra.com/
- https://techdocs.zebra.com/link-os/
- https://www.zebra.com/support-downloads/
- https://support.zebra.com/
- https://www.zebra.com/us/en/support-downloads/software/printer-software/profile-manager-enterprise.html
- https://www.proxion.com.br/servicos-de-manutencao/
- https://www.proxion.com.br/junte-se-a-nos-analista-de-suporte/
- https://www.proxion.com.br/impressoras-termicas-de-etiquetas/
- https://soti.net/products/soti-connect/
- https://tscprinters.com/
- https://csrc.nist.gov/projects/ssdf
- https://owasp.org/

External URLs são referências; capabilities, licensing, terms e paths podem mudar.

## Research Status

Public research não equivale a validated integration.

Até HIL/API validation, usar status apropriados:

- `planned` em roadmap/issue;
- `experimental` para subset testado;
- `not validated` quando implementação não foi validada;
- nunca “supported” apenas por documentação de terceiros.
