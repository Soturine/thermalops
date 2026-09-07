# AI e Knowledge Assistance

AI é opcional e sempre downstream de deterministic evidence, approved maintenance rules e authorization policy.

O ThermalOps precisa continuar funcional sem AI, cloud ou internet. AI existe para explicar, resumir e ajudar a navegar evidence; não é control plane.

## Authority Model

```text
Windows APIs + Vendor APIs + TechnicianObservation + Approved Policy/Rules
                              |
                              v
                       Evidence / Findings
                    +---------+----------+
                    |                    |
                    v                    v
        Deterministic decision        AI explanation
        / plan / due / disposition    (optional)
```

AI nunca é privileged authority, maintenance authority ou ServiceDisposition authority.

## Allowed Uses

AI pode:

- explicar uma normalized Finding em linguagem adequada ao técnico;
- resumir Diagnostic Report, Preventive Report ou ServiceCase;
- recuperar relevant approved manuals/runbooks;
- sugerir qual deterministic evidence view deve ser inspecionada em seguida;
- traduzir/simplificar technical evidence;
- gerar draft support note a partir de verified session facts;
- explicar por que MaintenanceTask está due usando source-backed rule;
- resumir configuration/baseline diff;
- destacar missing evidence e uncertainty;
- produzir uma versão localizada de texto já fundamentado;
- correlacionar referências aprovadas sem transformar correlation em fact.

## Forbidden Uses

AI não pode:

- executar repair autonomamente;
- gerar PowerShell/cmd e encaminhar ao helper;
- habilitar disabled capability;
- override organization/customer policy;
- inventar device state;
- inventar TechnicianObservation;
- definir maintenance interval por intuição;
- inventar component lifetime;
- declarar `RemoveFromService` sem deterministic authority;
- transformar trend em confirmed failure cause;
- alterar firmware/driver/config automaticamente;
- enviar customer evidence para provider externo por default;
- esconder uncertainty;
- alterar machine-readable evidence para “ficar mais coerente”.

## Explainability

Uma AI response relevante deve apontar para a evidence/source que sustentou a explicação.

Exemplo:

```text
Finding: HeadOpen
Evidence: ZebraNative/HeadState=Open
Windows: Spooler=Running
QueueJobs=0
```

AI pode explicar:

```text
A evidência atual indica uma condição reportada pelo próprio equipamento. O Spooler está ativo e não há backlog na queue selecionada. Siga o procedimento aprovado de verificação do printhead antes de alterar o estado do Windows.
```

AI não pode concluir que o hardware está quebrado se a evidence não suporta isso.

## Maintenance Guardrail

Permitido:

```text
Esta cleaning task está Due porque MaintenancePolicy X, baseada na fonte Y para este device family/context, atingiu o trigger registrado.
```

Proibido:

```text
Troque o printhead depois de 2.000.000 labels.
```

se esse threshold não for uma approved source-backed rule para o context aplicável.

## ServiceDisposition Guardrail

AI pode explicar:

```text
A rule de escalation foi acionada porque a fault persistiu após os checks permitidos e a active FieldServicePolicy não autoriza internal hardware service.
```

AI não escolhe arbitrariamente `EscalateToAuthorizedService` nem `RemoveFromService`.

## Offline-first Knowledge

Uma future local knowledge pack pode indexar:

- vendor manuals;
- approved troubleshooting guides;
- internal generic runbooks permitidos;
- schema documentation;
- product docs;
- release notes.

Requisitos:

- redistribution/licensing permitido;
- source/version preservado;
- citation para section/document quando possível;
- update/version lifecycle definido;
- untrusted document parsing seguro;
- no proprietary employer/customer docs no public repository.

## RAG / Retrieval

Se houver retrieval:

```text
Question
  -> retrieve approved sources
  -> rank/context filter
  -> generate explanation
  -> cite source/evidence
```

Guardrails:

- retrieved text não vira executable instruction automaticamente;
- prompt injection em documents é tratada como untrusted content;
- source trust/classification é preservada;
- missing source produz uncertainty;
- user deve conseguir abrir source/citation;
- answer não substitui deterministic machine state.

## Cloud AI

Cloud AI só poderá ser habilitada quando houver:

- explicit organization/user opt-in;
- provider configuration;
- data classification;
- redaction before transmission;
- provider retention/contract review;
- secret exclusion;
- source/evidence citations;
- timeout/failure handling;
- feature nonessential to core workflows.

Se cloud AI estiver unavailable:

```text
Diagnosis: continues
Preventive Inspection: continues
RepairPlan: continues
ServiceDisposition: continues
Reports: continues
```

Somente a explanatory assistance fica indisponível.

## Data Minimization

Antes de qualquer AI transmission, future implementation deve determinar:

- quais fields são necessários;
- quais podem ser pseudonymized;
- quais são prohibited;
- provider destination;
- retention semantics;
- consent/policy.

Nunca enviar por default:

- credentials;
- document contents;
- unrelated printer data;
- raw customer filesystem paths;
- full environment variables;
- attachments;
- proprietary procedures.

## Model Output Handling

AI output é untrusted suggestion text.

Não deve ser:

- passed directly to shell;
- parsed como privileged command;
- tratado como device state;
- persisted como Finding sem provenance;
- usado como maintenance source;
- usado como policy.

Se uma suggestion gerar uma future deterministic action, a action deve ser re-resolved por typed Domain/Application workflow e policy, não pelo texto do model.

## Predictive Maintenance

LLM output não é Predictive Maintenance.

M9 exige programa específico com:

- defined prediction target;
- labeled representative dataset;
- train/validation/test split;
- deterministic baseline comparison;
- calibration;
- false-positive/false-negative cost analysis;
- device/model applicability;
- drift monitoring;
- human review;
- rollback/disable criteria.

Até isso existir, AI pode resumir trends, mas não afirmar:

```text
remaining useful life
failure in N days
part X will fail next week
```

## Localization

AI pode ajudar a explicar em pt-BR, en-US ou outro locale, mas localization não altera:

- evidence keys;
- Domain enums;
- schema fields;
- rule IDs;
- policy IDs;
- timestamps/units semantics.

A camada de tradução ocorre na presentation/explanation, não no Domain truth.

## Evaluation

Antes de liberar AI feature, avaliar:

- groundedness;
- citation correctness;
- unsupported-claim rate;
- refusal/uncertainty behavior;
- prompt-injection robustness;
- privacy/redaction;
- multilingual consistency;
- deterministic fallback;
- latency e availability.

Uma AI feature não é production-ready apenas porque gera respostas convincentes.

## Example End-to-End

Evidence:

```text
HEAD_OPEN=true
MEDIA_OUT=false
SPOOLER=RUNNING
QUEUE_JOBS=0
```

Deterministic Finding:

```text
Device reports printhead open. Windows Spooler is running and no queue backlog is observed.
```

Deterministic Recommendation:

```text
Follow approved device check before Windows remediation.
```

AI Explanation:

```text
O problema atual parece estar do lado do equipamento, não em uma queue bloqueada. A impressora reporta o printhead aberto, enquanto o Spooler está ativo e sem jobs acumulados. Verifique o fechamento/condição do printhead conforme o procedimento aprovado antes de reiniciar serviços do Windows.
```

Enabled buttons e disposition continuam vindo de policy/rules, não do model output.
