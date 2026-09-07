# Contribuindo com o ThermalOps

ThermalOps é software de suporte técnico sensível a segurança. Uma contribuição pode afetar Windows printing, filas, serviços, customer data, maintenance recommendations, privileged actions e service disposition. Por isso, “funciona no meu computador” não é suficiente como Definition of Done.

## Antes de alterar código

Leia:

1. `AGENTS.md`;
2. `ENGINEERING_CONSTITUTION.md`;
3. `docs/README.md`;
4. o documento funcional/engineering da área alterada;
5. ADRs relevantes;
6. milestone/issue correspondente.

Exemplos:

- preventive: `docs/produto/manutencao-preventiva.md`;
- field/escalation: `docs/produto/field-service-e-escalation.md`;
- remediation: `docs/engenharia/diagnostico-e-remediacao-local.md`;
- packaging: `docs/engenharia/deployment-e-lifecycle.md`;
- fleet: `docs/produto/fleet-e-condition-monitoring.md`.

## Idioma e code style

A documentação narrativa é pt-BR, preservando technical terms em inglês quando apropriado. Código, Domain types, interfaces, methods, schemas e internal contracts permanecem em inglês.

Não traduza identificadores apenas para acompanhar o idioma da documentação.

## Expectativas para mudanças

Toda mudança deve:

- ter scope claro e pequeno o suficiente para revisão;
- preservar Domain authority;
- manter read-only guarantees;
- adicionar/atualizar testes relevantes;
- incluir negative/unknown/failure cases quando aplicável;
- atualizar documentação no mesmo logical change;
- usar ADR para architecture/security/lifecycle decision relevante;
- manter automatic evidence distinto de TechnicianObservation;
- registrar source/applicability para maintenance rules;
- explicar impacto de security/privacy para writes, exports e fleet;
- evitar unrelated refactor em safety-sensitive fix;
- reportar limitation/status honestamente.

## Commits

Commits podem continuar em inglês para manter consistência com codebase e tooling.

Exemplos:

```text
feat(domain): model maintenance due states
feat(service): add service disposition policy
fix(spooler): preserve original service state
security(helper): reject unknown capabilities
test(portable): verify no-persistence cleanup
docs(adr): define localization strategy
```

Cada commit deve representar uma unidade lógica compreensível e deixar o repositório em estado coerente.

## Pull Requests

Uma PR deve informar:

- problema;
- scope;
- milestone;
- design/ADR quando relevante;
- testes executados;
- security/privacy impact;
- source de maintenance rule quando aplicável;
- hardware validation realizada ou ainda faltante;
- known limitations;
- validation status (`fixed`, `partial`, `experimental`, `deferred`, `not validated`).

Não esconda limitation para tornar a PR aparentemente mais completa.

## Third-party code e dependencies

Código público não é automaticamente reutilizável.

Antes de adicionar dependency/código externo, revisar:

- license;
- attribution;
- maintenance activity;
- security posture;
- supply-chain risk;
- necessidade real;
- alternativas nativas/oficiais;
- compatibilidade com target runtime/platform.

Prefira official Windows/vendor APIs e implementação independente.

A licença do ThermalOps ainda precisa ser decidida; até lá, não assuma permissões de contribuição/reuso além das decisões explícitas do maintainer.

## Maintenance data externa

Ao adicionar `MaintenanceTaskDefinition`, threshold ou regra:

- cite source aprovado/oficial;
- registre source version/date quando possível;
- registre vendor/model/family/capability applicability;
- inclua safety notes relevantes;
- teste applicability mismatch/unknown;
- não generalize uma regra de um modelo para toda a frota;
- não transforme guideline em garantia de component lifetime.

## Vendor-native support

Não declare modelo/capability “supported” somente porque parser/unit test passou.

Para claims físicos/vendor-native, a Definition of Validated exige real hardware compatibility conforme `docs/engenharia/testing.md`.

## Customer/employer data

É proibido commit de dados reais de cliente/empregador, incluindo:

- hostname/username/IP;
- serial number;
- ticket/chamado;
- customer configuration;
- credentials/tokens;
- logs reais;
- fotos/screenshots;
- internal procedures;
- SLA/contract details;
- proprietary policy.

Use synthetic fixtures e generic policy abstractions.

## Security-sensitive changes

Mudanças no helper, privileged IPC, path handling, updater, attachments, export privacy, network discovery, installer ou fleet auth exigem revisão de threat model e testes específicos.

Nunca “temporariamente” adicione generic shell/process execution para acelerar uma implementação.
