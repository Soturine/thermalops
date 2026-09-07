# ThermalOps Engineering Constitution

Esta Constitution define o padrão de engenharia do ThermalOps. Ela se aplica ao Desktop, Portable, Enterprise, adapters, preventive maintenance, field service, fleet, AI, testes, CI/CD, packaging, documentação e releases.

O objetivo é impedir que velocidade, aparência de progresso ou conveniência local enfraqueçam business correctness, safety, privacy, authorization, recoverability e testability.

## 1. Ordem de prioridade

Quando objetivos entrarem em conflito, decidir nesta ordem:

1. business/domain correctness;
2. safety e security;
3. authorization e privacy;
4. reliability e recoverability;
5. maintainability e testability;
6. UX e accessibility;
7. performance/efficiency;
8. delivery speed.

Código rápido que pode afetar a queue errada, inventar maintenance advice, ultrapassar autoridade do técnico, vazar customer data ou deixar um endpoint degradado **não é progresso**.

## 2. Domain como fonte de verdade

O Domain define o significado de:

- printer identity e capability;
- print jobs;
- evidence;
- findings;
- maintenance task/inspection/baseline/due;
- TechnicianObservation;
- HealthAssessment;
- ServiceDisposition;
- ServiceCase;
- policy;
- RepairPlan/RepairAction;
- post-condition;
- validation status.

UI, Windows APIs, vendor SDKs, files, AI, database e fleet infrastructure são interfaces/implementações. Não redefinem business truth.

## 3. Arquitetura padrão

A arquitetura default é **modular monolith**.

Responsabilidades:

- Domain possui regras e invariants;
- Application orquestra use cases;
- Infrastructure implementa OS/external boundaries;
- Vendor Adapters isolam protocolos/capabilities específicos;
- UI é delivery mechanism;
- entry point é composition root;
- privileged execution é uma trust boundary separada;
- Fleet/distributed services só surgem quando houver necessidade real e ADR.

Não criar microservices, brokers, cloud services ou distributed state por aparência arquitetural.

## 4. Dependency direction

Dependências apontam para dentro:

```text
Desktop -> Application -> Domain
Windows Infrastructure -> ports definidos para dentro
Vendor Adapters -> ports definidos para dentro
Privileged Helper -> tiny typed privileged contract
```

`ThermalOps.Domain` não referencia:

- WPF;
- P/Invoke implementation;
- filesystem implementation;
- network stack implementation;
- vendor SDK;
- database;
- installer technology;
- AI SDK.

## 5. Evidence integrity

Nunca colapsar fontes distintas em um status opaco.

Preservar, conforme aplicável:

- source;
- timestamp;
- target;
- normalized value;
- safe raw representation;
- collection outcome/error;
- rule/schema version;
- certainty semantics quando houver inference.

Manter separados:

```text
Observed fact
TechnicianObservation
Derived Finding
Recommendation
ServiceDisposition
Operator intent
Executed action
Verified outcome
```

`Unknown` não é sinônimo de `Healthy`, `Pass`, `NotDue` ou sucesso.

## 6. Preventive Maintenance integrity

Preventive Maintenance é read-only-first.

Regras:

- interval, threshold e component lifetime exigem approved source + applicability;
- não inventar replacement schedule;
- uma regra de um modelo não vira regra universal;
- baseline drift é finding, não fault proof;
- technician physical check é human evidence;
- software não assume autorização para disassembly;
- manufacturer safety notes devem ser preservadas/referenciadas quando relevantes;
- `MaintenanceDue` deve representar `Unknown` quando dados obrigatórios faltarem;
- HealthAssessment precisa ser explicável por componentes;
- numeric Health Score, se existir, é secondary, deterministic, versioned e auditável;
- predictive claims exigem programa de validação separado.

## 7. Field Service scope

ThermalOps apoia:

- diagnosis;
- Preventive Inspection;
- field triage;
- evidence collection;
- local authorized remediation;
- reporting;
- ServiceDisposition;
- escalation assistance.

`Repair` no produto não implica bench/internal hardware repair.

Não hard-code no public core:

- RMA workflow específico;
- customer/company SLA;
- entitlement;
- internal ticket schema;
- quem transporta equipamento;
- quem contata fabricante;
- regras proprietárias de peças/substituição.

Esses comportamentos entram por policy/configuration privada quando legítimos.

## 8. Least privilege e safe defaults

- read-only é default;
- Portable Lite é permanentemente read-only;
- Portable Pro eleva somente quando uma ação específica realmente exigir;
- Desktop UI permanece standard-user;
- helper capabilities são enumeradas, typed e schema-validated;
- deny generic command execution;
- destructive/broad action exige preview, scope, impact, confirmation e verification;
- targeted remediation precede global reset;
- imported policy nunca amplia capability do executable.

## 9. Privileged boundary

O Temporary Privileged Helper não é um general-purpose utility process.

É proibido expor generic capabilities como:

```text
ExecuteCommand(string)
RunPowerShell(string)
RunCmd(string)
DeletePath(string)
WriteRegistry(path, value)
StartArbitraryService(name)
InstallArbitraryDriver(path)
```

Cada nova privileged capability exige code/API change, review, tests, registration e threat analysis proporcional ao risco.

## 10. Repair transaction discipline

Toda state-changing action deve ser modelada com:

- preconditions;
- affected resources;
- impact level;
- snapshot requirements;
- ordered actions;
- timeouts;
- expected post-conditions;
- verification method;
- recovery/rollback path;
- audit events;
- policy decision.

Fluxo canônico:

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

API success, process exit code `0` ou ausência de exception não substituem post-condition verification.

## 11. Portable purity

Uma Portable session encerrada com sucesso não deixa intencionalmente:

- installed service;
- scheduled task;
- startup/Run entry;
- persistent helper/daemon;
- temporary IPC endpoint;
- customer logs;
- temporary executable copies;
- app-owned registry persistence;
- arquivos de sessão ao lado do executable ou no USB sem explicit export.

Cleanup failure é um resultado reportável, não um detalhe a esconder.

Não prometer forensic secure erase quando o filesystem/OS não permite garantia.

## 12. Privacy by design

- collect only what is needed;
- session-local processing por default;
- sanitized export por default;
- full technical e ServiceCase export explícitos;
- no automatic upload;
- telemetry não é requerida;
- Enterprise retention é policy-controlled;
- redact/pseudonymize identities quando não forem necessárias;
- não coletar document/label contents sem necessidade aprovada.

## 13. Imported data é untrusted

Policy, baseline, maintenance catalog, support bundle e attachment importados devem ser tratados como untrusted input.

Controles:

- schema/version validation;
- bounded sizes;
- safe parsing;
- no embedded script/expression engine;
- no arbitrary path/process execution;
- signature/trust validation quando a feature existir;
- compatibility/applicability check antes de usar baseline;
- imported data pode informar/restringir, nunca criar code capability.

## 14. Security engineering

Aplicar, quando relevantes:

- NIST SSDF;
- Microsoft Windows security guidance;
- OWASP guidance para futuros APIs/services;
- vendor security documentation.

Expected controls:

- explicit trust boundaries;
- IPC ACLs e caller/session validation;
- allowlists;
- schema validation;
- bounded input/timeouts;
- path/reparse-point safety;
- code signing;
- SHA-256 checksums;
- SBOM;
- dependency/license review;
- secret scanning;
- static analysis/CodeQL;
- vulnerability scanning;
- secure update design antes de auto-update.

## 15. Network safety

- local evidence primeiro;
- known endpoint checks quando possível;
- broader discovery apenas com explicit operator/policy authorization;
- bounded range/subnet se discovery for implementado;
- Customer Safe sem automatic scan;
- discovery initiation deve ser auditável quando aplicável.

ICMP não equivale a printer health.

## 16. Reliability e recoverability

Cada external operation deve definir:

- timeout;
- cancellation behavior;
- retry policy quando seguro;
- failure state;
- observability suficiente para diagnóstico.

Retry/backoff é bounded e adequado ao tipo de operação. Nunca repetir destructive action cegamente.

Ao alterar service/configuration, preservar original/policy state. Exemplo: Spooler restart não termina automaticamente em `Running` se o estado/policy original exigir outra coisa.

## 17. Observability

Use structured events, não somente free-form text.

Eventos importantes devem carregar, conforme aplicável:

- session/correlation ID;
- timestamp;
- component;
- event/action/finding type;
- target ID;
- outcome;
- duration;
- sanitized error detail;
- before/after references;
- rule/schema/policy version.

Fleet adiciona health/readiness/metrics apenas para componentes distribuídos que realmente existirem.

## 18. Testing

Testing segue risco, não quantidade de UI screens.

Esperado:

- muitos Domain unit tests;
- Application tests;
- adapter contract tests;
- real Windows integration tests;
- security/failure-path tests;
- preventive applicability/baseline tests;
- redaction/ServiceCase tests;
- poucos E2E significativos;
- hardware-in-the-loop para physical/vendor-native claims;
- lifecycle tests para Enterprise installer/upgrade/uninstall.

Negative paths são obrigatórios para privileged/remediation logic.

Mocks servem para external boundaries verdadeiras, não para esconder integração interna quebrada.

## 19. CI/CD e Git

Fluxo padrão:

```text
logical change -> commit -> push -> CI -> next logical change
```

Regras:

- WIP baixo;
- logical commits;
- preserve last-known-green;
- CI green antes de release tag;
- tag aponta para validated source SHA;
- no safety-sensitive auto-merge;
- não transformar failed required check em optional sem ADR/rationale;
- milestone close exige main/origin synchronized e audit de status.

## 20. Supply chain e releases

Uma production distribution deve expor:

- Semantic Version;
- source commit SHA;
- build ID;
- architecture/RID;
- edition/mode;
- Authenticode quando signing identity estiver disponível;
- SHA-256;
- SBOM;
- release notes;
- supported OS/architecture matrix;
- known limitations;
- provenance/attestation quando viável.

Não alegar reproducibility, compatibility ou certification sem validação real.

## 21. Deployment lifecycle

Portable:

- no installer;
- self-contained;
- offline-first;
- no hidden persistence.

Enterprise:

- packaging decision via ADR;
- interactive e silent install;
- silent uninstall;
- offline deployment;
- upgrade/migration/recovery;
- explicit retention behavior;
- clean uninstall;
- predictable exit codes/logs;
- no-reboot normal path quando tecnicamente possível.

No early silent self-update.

## 22. UX e accessibility

A UI deve mostrar evidence, uncertainty, impact e scope.

- N1: progressive disclosure e guided workflows;
- N2/N3: deep evidence e export;
- destructive actions são secundárias/contextuais;
- não usar green/red state sem explicação;
- keyboard navigation;
- readable contrast;
- scaling/DPI awareness;
- screen-reader semantics;
- localization readiness.

## 23. Localization e technical language

A UI e documentação são pt-BR-first, mas localization-ready.

- código e internal contracts em inglês;
- Domain type names em inglês;
- technical terms consolidados preservados em inglês;
- evitar tradução literal que reduza precisão;
- user-facing strings ficam fora do business logic;
- schemas/log event types não mudam com locale;
- reports podem ser localized sem alterar machine-readable schema.

## 24. AI

AI é optional e downstream de deterministic evidence/rules.

AI pode:

- explain findings;
- summarize support/preventive/service-case data;
- retrieve approved docs;
- draft support notes;
- traduzir/simplificar evidence.

AI não pode:

- executar ou autorizar repair;
- definir maintenance interval/due por intuição;
- atribuir ServiceDisposition sem deterministic policy;
- inventar device state;
- override policy;
- habilitar capability;
- upload customer data por default;
- transformar trend em proven failure cause.

LLM output não é predictive maintenance.

## 25. Documentation governance

Documentação é parte da entrega, não cleanup posterior.

Estrutura:

- `docs/produto/` — product behavior e operational concepts;
- `docs/engenharia/` — architecture implementation contracts, testing e lifecycle;
- `docs/seguranca/` — threat/security/privacy model;
- `docs/pesquisa/` — referências externas e patterns;
- `docs/planejamento/` — roadmap;
- `docs/adr/` — decisions aceitas/propostas.

Não deixar documentos técnicos soltos no root de `docs/` além do índice.

Behavior change atualiza docs na mesma change. Decisões arquiteturais relevantes recebem ADR.

## 26. Project management

Usar lightweight Kanban/milestones, WIP baixo, Definition of Ready e Definition of Done proporcionais ao risco.

Em milestone boundaries, auditar:

- business-rule drift;
- gaps;
- duplication;
- unnecessary complexity;
- security/privacy;
- test debt;
- observability;
- accessibility/UX;
- performance;
- docs;
- licensing;
- supply chain;
- release readiness.

## 27. Honest status

Use somente status precisos:

- **fixed** — implementado e validado;
- **partial** — acceptance criteria restantes;
- **experimental** — suporte limitado/controlado;
- **deferred** — adiado intencionalmente com rationale;
- **not validated** — implementação existe sem validação requerida.

Uma screen pronta ou happy path executado uma vez não torna feature production-ready.
