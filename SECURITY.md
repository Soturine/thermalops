# Security Policy

ThermalOps is pre-release and is not yet intended for production customer repair, preventive maintenance, fleet monitoring, or service-case automation.

## Reporting a vulnerability

Do not publish sensitive exploit details, customer data, credentials, proprietary service procedures or privilege-escalation proof-of-concept material in a public issue.

A private security-reporting channel should be configured before public preview. Until then, use a private contact channel available to the repository owner.

## High-priority security scope

- arbitrary code/command execution through privileged helper;
- authorization/policy bypass;
- imported policy/baseline leading to code execution or capability expansion;
- unintended cross-queue/global print deletion;
- unsafe elevated file/path/reparse-point handling;
- Portable persistence left behind;
- customer data leakage via logs/bundles/service cases;
- attachment/archive path traversal or execution;
- unauthorized network scanning;
- signature/update-chain weaknesses;
- fleet auth/RBAC/tenant/retention weaknesses once implemented;
- maintenance/disposition logic that can trigger unsafe unauthorized actions.

See `docs/SECURITY_AND_PRIVACY.md`.
