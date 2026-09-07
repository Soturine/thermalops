# Security Policy

ThermalOps is pre-release and not yet intended for production customer repair.

## Reporting a vulnerability

Do not publish sensitive exploit details, customer data, credentials, or privilege-escalation proof-of-concept material in a public issue.

A private security-reporting channel should be configured before the first public preview release. Until then, contact the repository owner through a private channel available on their GitHub profile.

## Scope priorities

High priority includes:

- arbitrary code/command execution through the privileged helper;
- authorization or policy bypass;
- unintended cross-queue/global print deletion;
- unsafe file/path handling at elevated privilege;
- persistence left by Portable;
- customer-data leakage;
- signature/update-chain weaknesses once release signing/updating exists.

See `docs/SECURITY_AND_PRIVACY.md` for the design threat model.
