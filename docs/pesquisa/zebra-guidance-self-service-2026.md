# Pesquisa 2026 — Zebra Guided Operations, Lifecycle e Self-Service Corporativo

## Objetivo

Este documento registra pesquisa pública atual que sustenta as novas directions de Guided Operations, Lifecycle/Health e Self-Service. Research serve como **reference/pattern evidence**, não como business rule automática e não como autorização para copiar proprietary implementation.

Toda capability citada abaixo precisa ser revalidada no momento da implementação, porque SDKs, product names, support matrices e URLs podem mudar.

## Zebra Nucleus Connector / Printer Setup Utilities

A Zebra informa publicamente que **Zebra Printer Setup Utility is now Nucleus Connector**, posicionando a ferramenta para setup rápido de printers. A página também mantém referência aos Setup Utilities, que facilitam configuração de select industrial, mobile e desktop printers.

Referências:

- https://www.zebra.com/us/en/support-downloads/software/printer-software/zebra-nucleus-connector.html
- https://www.zebra.com/us/en/software/printer-software/zebra-setup-utility.html
- https://www.zebra.com/us/en/support-downloads/software/printer-software/printer-setup-utilities.html

Design lessons:

- Guided Setup/Commissioning é uma necessidade real;
- model support pode ser select/limited, então capability discovery é obrigatório;
- setup wizard pattern é útil, mas ThermalOps deve separar read-only discovery, driver/queue provisioning, printer writes, calibration e validation em phases com privilege/rollback semantics próprios;
- product names/migration de vendor tools mudam, então direct integration precisa de current API/licensing review.

## Zebra onboard printer tools

Official Zebra docs para modelos compatíveis mostram uma categoria rica de onboard tools, incluindo:

- Printer Diagnostics;
- SmartCal Media Calibration;
- Configuration Report;
- Network/Bluetooth Configuration Report;
- factory-default reset;
- network-default reset;
- Print Quality Report/self-test;
- Advanced Mode;
- Manual Media Calibration.

Referência:

- https://docs.zebra.com/us/en/printers/desktop/zd611r-ug/c-mlk-ug-onboard-printer-tools.html
- https://docs.zebra.com/br/pt/printers/desktop/zd611r-ug/c-mlk-ug-onboard-printer-tools.html

Design lessons:

- Native diagnostic actions merecem catálogo próprio;
- calibration/test printing podem consumir media ou alterar state e não devem ser classificados como read-only por aparência;
- factory/network reset são HighImpact;
- uma operation existir no front panel/manual **não prova** que exista SDK method equivalente para todos os models;
- capability/action applicability precisa de model/firmware/interface/HIL matrix.

## Zebra Link-OS — odometer/counters

Official Link-OS TechDocs documenta `PrinterUtil.GetOdometerStatus`/`getOdometerStatus`. A descrição pública inclui:

- total print length;
- head clean counter;
- label dot length;
- head new;
- latch open counter;
- two user resettable counters.

Referências:

- https://techdocs.zebra.com/link-os/latest/pc_net/content/v503685/html/3e06cf91-c7ad-80c8-f5ad-72edb4933da7
- https://techdocs.zebra.com/link-os/2-14/pc_net/content/html/47cfc029-0065-576f-fdfa-37e7f1a93dce

A documentação também deixa claro em versões do SDK que a capability é Link-OS-specific e pode lançar `NotALinkOsPrinterException`.

Design lessons:

- `UsageMetrics` é justified;
- lifetime/resettable counter semantics precisam ser preserved;
- `OperatingHours`/`PowerOnHours` não podem ser assumidos como universais;
- missing metric != zero;
- unit normalization requer context (por exemplo DPI quando converting dots/distance);
- HIL/model support matrix necessária.

## Zebra Link-OS — PrinterStatus

Zebra Link-OS fornece status APIs para obter current printer condition. TechDocs também documenta `PrinterUtil.GetPrinterStatus` e APIs relacionadas.

Referência geral:

- https://techdocs.zebra.com/link-os/latest/

Design lesson:

- vendor-native evidence deve permanecer separada de Windows queue evidence;
- ready-to-print/device errors são mais próximos da physical/device truth do que um Windows queue idle flag, mas ainda são capability/source-specific;
- status parsing deve ser bounded e resilient.

## Zebra Link-OS — SettingsProvider

Official TechDocs `SettingsProvider` expõe methods para:

```text
getAllSettings
getAllSettingValues
getAvailableSettings
getSettingRange
getSettingsValues
getSettingType
getSettingValue
isSettingReadOnly
isSettingValid
isSettingWriteOnly
```

Referência:

- https://techdocs.zebra.com/link-os/latest/pc/content/v2155569/com/zebra/sdk/settings/settingsprovider

Design lessons:

- excellent capability discovery/read evidence source;
- `VendorCanWrite(X)` must remain distinct from `PolicyAllowsWrite(X)`;
- do not build generic arbitrary setting writer;
- range/read-only/type metadata can help safe UI/preflight;
- exact SDK/model behavior still needs HIL.

## Zebra PrintSecure

Zebra publicly describes PrintSecure as part of its printer security ecosystem. The page includes a **Security Assessment Wizard** intended to uncover vulnerabilities and compare printer settings against security best practices.

Referência:

- https://www.zebra.com/us/en/software/printer-software/printsecure.html

Design lessons:

- a read-only `Printer Security Assessment`/`SecurityBaseline` is a legitimate future ThermalOps category;
- security drift should produce `SecurityFinding` before any hardening write;
- automatic hardening must be separate, high-impact and policy-controlled;
- security assessment source/version/applicability need tracking.

## Zebra Support Center

Zebra's support portal separates:

- drivers/downloads;
- documentation/manuals;
- product support;
- repair request.

Referência:

- https://support.zebra.com/pt-BR

Design lessons:

- diagnosis/knowledge/support and repair are distinct lifecycle stages;
- ThermalOps `ServiceCase` is a useful interoperability boundary before direct vendor portal integration;
- direct RMA/repair submission should remain deferred until official supported interface/auth/privacy/licensing are understood.

## Zebra printer setup and Windows installation

Official Zebra documentation also shows guided procedures for adding printers through Setup Utilities and Windows driver workflow.

Example:

- https://docs.zebra.com/br/pt/printers/mobile/zq610-620-630-plus/c-zq6x0plus-getting-started/t-installing-drivers-and-connecting-to-a-windows-based-computer/c-zq6x0plus-zebra-setup-utilities/t-adding-a-printer-through-zebra-setup-utilities.html

Design lesson:

- `CommissioningPlan` should model driver/queue/transport/config/calibration/test/validation as separate phases;
- avoid one monolithic privileged “configure printer” action.

## Microsoft Intune Company Portal pattern

Microsoft documents a managed enterprise pattern where an organization makes apps available in Company Portal; users can view/install apps made available to them, while required apps can be deployed automatically.

References:

- https://learn.microsoft.com/en-us/intune/intune-service/user-help/manage-apps-cpweb
- https://learn.microsoft.com/en-us/windows/application-management/private-app-repository-mdm-company-portal-windows-11

Design lessons for ThermalOps:

- supports the concept of **organization pre-approval + user self-service**, rather than bypass;
- managed Self-Service client can be distributed via standard enterprise software channels;
- ThermalOps should remain compatible with multiple deployment systems and not embed Intune-specific logic in the Domain;
- standard-user normal flow remains a product goal.

## Windows App Control / AppLocker

Microsoft documents App Control for Business and AppLocker as Windows technologies for controlling which apps/code can execute. AppLocker can allow/deny executables/scripts/installers/DLLs and can apply user/group-aware rules in applicable scenarios.

References:

- https://learn.microsoft.com/pt-br/windows/security/application-security/application-control/app-control-for-business/
- https://learn.microsoft.com/pt-br/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview
- https://learn.microsoft.com/pt-br/windows/security/application-security/application-control/app-control-for-business/appcontrol-and-applocker-overview

Design lessons:

- Self-Service must not promise universal runability on locked-down endpoints;
- code signing/publisher identity materially help enterprise allowlisting/governance;
- `BlockedByPolicy` is a valid product outcome;
- product docs must never recommend disabling application controls to make ThermalOps work.

## Synthesis for ThermalOps

Research supports the following combination:

```text
Windows read-only diagnosis
+ vendor-native capability/status/counters
+ source-backed Preventive Maintenance
+ Guided Troubleshooting
+ model-aware Knowledge
+ safe native diagnostic actions
+ Lifecycle & Health indicators
+ standard-user Self-Service under organization policy
+ ServiceCase/helpdesk handoff
+ future Fleet/Condition Monitoring
```

Important non-inferences:

```text
Zebra has odometer counters
  != every printer has operating hours

Zebra manual shows a self-test
  != ThermalOps can invoke it programmatically on every model

SettingsProvider says setting is writable
  != ThermalOps is authorized to write it

Company Portal enables user app access
  != ThermalOps may bypass corporate policy

Health indicators exist
  != Remaining Useful Life is known
```

## Research maintenance

At implementation time, re-check:

- current Link-OS SDK version and .NET compatibility;
- Zebra model/firmware support matrix;
- Nucleus Connector/Setup Utility product changes;
- PrintSecure/security tooling behavior;
- SDK redistribution/license terms;
- documentation redistribution rights;
- current Microsoft deployment/application-control guidance.

Research links may rot/change. Product behavior should rely on versioned Domain/application contracts and validated adapters, not live web wording.
