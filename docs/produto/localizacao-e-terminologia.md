# Localização e Terminologia

ThermalOps é **pt-BR-first na experiência do usuário**, mas o produto, código e documentação técnica não devem traduzir termos consolidados de forma literal apenas para parecer “100% em português”.

A estratégia é separar claramente:

```text
User-facing language
        |
        v
Localization resources
        |
        v
Application / Domain contracts
        |
        v
Windows / Vendor APIs / Protocols
```

## Objetivos

A localization strategy deve permitir:

- UI natural para técnicos brasileiros;
- manutenção de codebase consistente com .NET/Windows/vendor ecosystem;
- reports localizados;
- schemas estáveis entre locales;
- futura adição de `en-US`, `es` e outros locales;
- terminology consistente;
- nenhuma duplicação de business logic por idioma.

## Locale inicial

`pt-BR` é o locale inicial de referência para UI e human-readable reports.

Isso não significa que o aplicativo será hard-coded em português.

A arquitetura deve permitir, futuramente:

```text
pt-BR
 en-US
 es
```

sem alterar Domain logic.

## O que fica em português

User-facing texts como:

- títulos de telas;
- descriptions;
- warnings;
- confirmation dialogs;
- onboarding;
- help text;
- preventive checklist text;
- report narrative;
- accessibility labels;
- release notes voltadas ao usuário brasileiro.

Exemplos:

```text
Diagnóstico Rápido
Diagnóstico Avançado
Manutenção Preventiva
Analisar Falha
Coletar Evidências
Preparar Escalonamento
Relatório Técnico
Atenção recomendada
```

## O que permanece em inglês

### Code identifiers

- namespaces;
- classes;
- interfaces;
- methods;
- properties;
- enums;
- test type names;
- internal event types;
- schema field names.

Examples:

```text
MaintenanceInspection
MaintenanceTaskDefinition
MaintenanceBaseline
DiagnosticEvidence
DiagnosticFinding
TechnicianObservation
ServiceDisposition
ServiceCase
RepairPlan
HealthAssessment
ConditionTrend
```

Não usar versões traduzidas como:

```text
InspecaoDeManutencao
DisposicaoDeServico
EvidenciaDiagnostica
```

### Technical terms consolidados

Preservar em inglês quando a tradução prejudicar precisão ou correspondência com documentação externa:

```text
Domain
Application
Infrastructure
Adapter
Policy
Baseline
ServiceCase
ServiceDisposition
RepairPlan
HealthAssessment
Quick Diagnosis
Preventive Inspection
Spooler
WinSpool
PnP
Event Log
Link-OS
SGD
ZPL
CI/CD
SBOM
RBAC
TLS
IPC
UAC
EDR/XDR
WDAC
AppLocker
```

Em texto corrido, esses terms podem conviver naturalmente com português.

Exemplo preferido:

> O `ServiceDisposition` é calculado a partir de Findings, active policy e field scope.

Em vez de:

> A “disposição de serviço” é calculada...

quando a tradução não ajuda o leitor técnico.

## Terms que podem ter label localizado

Um Domain enum pode permanecer em inglês enquanto a UI apresenta tradução.

Example:

```text
Domain value: ContinueInService
pt-BR label: Continuar em serviço
en-US label: Continue in service
```

Outro exemplo:

```text
Domain value: InsufficientEvidence
pt-BR label: Evidências insuficientes
en-US label: Insufficient evidence
```

A persisted value/schema usa o canonical English identifier.

## Resource Strategy

WPF deve usar localization resources em vez de hard-coded strings distribuídas no ViewModel/code-behind.

Uma direção possível:

```text
Resources/
  Strings.resx
  Strings.pt-BR.resx
  Strings.en-US.resx
```

ou outra mechanism compatível com .NET/WPF escolhida durante implementation.

A decisão final de tooling não muda os invariants:

- resource keys estáveis;
- fallback locale definido;
- no business rule em string localizada;
- UI state não depende de comparar display text;
- logs/schemas não usam translated labels como identifiers.

## Resource Keys

Preferir semantic keys:

```text
Diagnosis.Quick.Title
Diagnosis.Quick.Description
Maintenance.Preventive.Title
ServiceDisposition.ContinueInService
RepairPlan.Confirm.Title
Export.Privacy.FullTechnical.Warning
```

Evitar keys frágeis baseadas no texto original.

## Machine-readable Outputs

JSON/schema permanece locale-neutral.

Example:

```json
{
  "serviceDisposition": "ContinueWithObservation",
  "maintenanceDue": "DueSoon",
  "evidenceSource": "ZebraNative"
}
```

Human-readable report pode renderizar:

```text
Disposição: Continuar com observação
Manutenção: Vence em breve
Fonte: Zebra Native
```

## Logs

Structured logs devem preferir event IDs/types estáveis em inglês:

```text
MaintenanceInspectionStarted
EvidenceCollectionFailed
ServiceCaseExported
RepairPlanVerified
```

A mensagem human-readable pode ser localizada em UI/report, mas machine correlation não depende dela.

## Errors

Errors devem ter duas camadas quando apropriado:

```text
stable error code/type
+ localized user message
```

Exemplo:

```text
Code: PORTABLE_TEMP_UNAVAILABLE
pt-BR: Não foi possível criar a área temporária segura para esta sessão.
```

Isso ajuda support bundles, tests e troubleshooting em diferentes locales.

## Units e Formats

Localization deve considerar:

- date/time display;
- decimal separator;
- units;
- paper/media dimensions;
- timezone;
- number formatting.

Machine-readable fields devem usar format estável/documentado, por exemplo ISO 8601 UTC quando apropriado.

Não misturar localized number string com numeric Domain value.

## Technical Documentation

A documentação fica em pt-BR, mantendo technical terms em inglês.

Exemplo de estilo desejado:

> O Temporary Privileged Helper é uma trust boundary separada e só recebe typed requests para allowlisted capabilities.

Isso é preferível a traduções artificiais que tornam a documentação menos reconhecível para quem consulta Microsoft/Zebra/.NET docs.

## Glossary

### Adapter

Implementação que traduz capabilities/protocols de um vendor ou infrastructure boundary para interfaces usadas pelo Application/Domain.

### Baseline

Reference/approved state usado para comparação; uma diferença é drift, não necessariamente fault.

### Finding

Conclusão derivada de evidence. Não é raw evidence.

### Policy

Conjunto versionado de regras/permissions que restringe behavior. Não cria executable capability.

### RepairPlan

Plano typed para uma local remediation com scope, impact, preconditions, confirmation, actions, validation e recovery.

### ServiceCase

Pacote estruturado de handoff/escalation com evidence, findings, actions, observations e disposition.

### ServiceDisposition

Outcome de field service, separado de device status.

### TechnicianObservation

Evidence registrada manualmente por um técnico, distinta de automatic evidence.

### HealthAssessment

Resumo explicável por componentes. Numeric score, se houver, é secondary.

### ConditionTrend

Interpretação de série histórica. Não equivale a causation.

## Translation Review

Antes de adicionar novo user-facing term:

1. identificar se é technical canonical term;
2. verificar wording já usado no produto;
3. escolher resource key;
4. evitar literal translation estranha;
5. manter Domain identifier estável;
6. atualizar glossary quando o term for central;
7. adicionar localization test quando necessário.

## Testing

Localization tests devem incluir:

- missing resource key;
- fallback behavior;
- format strings;
- long translated text/layout;
- DPI/scaling;
- screen reader label;
- report rendering;
- machine schema invariance entre locales;
- locale change sem alterar business decisions.

## Non-goals

- traduzir code identifiers;
- traduzir vendor API/command names;
- duplicar docs completas por idioma antes de existir manutenção sustentável;
- usar AI translation como única revisão de safety-critical warnings;
- alterar schema enum values por locale.

## Regra prática

Escreva para um técnico brasileiro sem apagar a linguagem do ecossistema técnico.

Se a tradução literal tornar o texto menos claro, preserve o technical term em inglês e explique-o quando necessário.
