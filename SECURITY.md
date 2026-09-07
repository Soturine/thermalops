# Security Policy

ThermalOps está em pre-release e **ainda não deve ser tratado como ferramenta production-ready** para customer repair, preventive maintenance, fleet monitoring, ServiceCase automation ou ações privilegiadas.

## Como reportar uma vulnerabilidade

Não publique em issue pública:

- exploit details sensíveis;
- credentials/tokens;
- customer/employer data;
- proprietary service procedures;
- privilege-escalation proof of concept;
- material que permita abuso imediato do Temporary Privileged Helper.

Um private security-reporting channel deve ser configurado antes do primeiro public preview. Até lá, use um canal privado disponível ao maintainer do repositório.

## Escopo de alta prioridade

Vulnerabilidades de prioridade alta incluem, sem se limitar a:

- arbitrary code/command execution através do helper;
- authorization/policy bypass;
- confused-deputy entre UI e helper;
- imported policy/baseline resultando em code execution ou capability expansion;
- unintended cross-queue/global print deletion;
- unsafe elevated file/path/reparse-point handling;
- Portable deixando persistence intencional/não esperada;
- customer-data leakage por logs, reports, bundles ou ServiceCases;
- attachment/archive path traversal;
- attachment execution;
- unauthorized network scanning;
- insecure update/signature chain;
- fleet authentication/RBAC/retention/tenant-boundary weakness quando implementado;
- maintenance/disposition logic levando a ação unsafe/unauthorized;
- forged evidence sendo apresentado como trustworthy automatic evidence;
- bypass de `--readonly` ou Customer Safe;
- privilege retained além do tempo necessário;
- cleanup que remove arquivo/recurso que não pertence ao ThermalOps.

## Princípios de triagem

Ao avaliar um report, considerar:

- impacto;
- exploitability;
- privilege required;
- customer-data exposure;
- scope afetado;
- recoverability;
- whether Portable/Enterprise behavior differs;
- whether the issue can affect unrelated queues/devices;
- whether evidence or disposition can be falsified.

## Divulgação

Não prometemos prazo de correção enquanto o projeto estiver pre-release, mas safety/security findings devem ser tratados antes de declarar uma capability estável.

Fixes de security não devem remover testes ou enfraquecer guardrails apenas para restaurar o happy path.

## Documentação relacionada

Veja:

- `ENGINEERING_CONSTITUTION.md`;
- `docs/seguranca/security-e-privacy.md`;
- `docs/engenharia/testing.md`;
- `docs/engenharia/release-engineering.md`.
