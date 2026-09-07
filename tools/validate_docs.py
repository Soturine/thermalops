#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "ENGINEERING_CONSTITUTION.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/README.md",
    "docs/produto/visao-do-produto.md",
    "docs/produto/portable.md",
    "docs/produto/manutencao-preventiva.md",
    "docs/produto/field-service-e-escalation.md",
    "docs/produto/fleet-e-condition-monitoring.md",
    "docs/produto/ai-e-knowledge-assistance.md",
    "docs/produto/localizacao-e-terminologia.md",
    "docs/engenharia/arquitetura.md",
    "docs/engenharia/diagnostico-e-remediacao-local.md",
    "docs/engenharia/deployment-e-lifecycle.md",
    "docs/engenharia/support-bundles-e-service-cases.md",
    "docs/engenharia/testing.md",
    "docs/engenharia/release-engineering.md",
    "docs/seguranca/security-e-privacy.md",
    "docs/pesquisa/referencias-e-padroes.md",
    "docs/planejamento/roadmap.md",
    "docs/adr/0001-stack-and-desktop-ui.md",
    "docs/adr/0002-privileged-helper.md",
    "docs/adr/0003-field-service-and-preventive-scope.md",
    "docs/adr/0004-maintenance-and-health-model.md",
    "docs/adr/0005-localization-and-technical-language.md",
    "docs/assets/thermalops-concept-overview.png",
]

REQUIRED_DIRS = [
    "docs/produto",
    "docs/engenharia",
    "docs/seguranca",
    "docs/pesquisa",
    "docs/planejamento",
    "docs/adr",
    "docs/assets",
]

LEGACY_PATHS = [
    "docs/AI.md",
    "docs/ARCHITECTURE.md",
    "docs/DEPLOYMENT_AND_LIFECYCLE.md",
    "docs/DIAGNOSTICS_AND_REPAIR.md",
    "docs/FIELD_SERVICE_AND_ESCALATION.md",
    "docs/FLEET_AND_CONDITION_MONITORING.md",
    "docs/PORTABLE.md",
    "docs/PREVENTIVE_MAINTENANCE.md",
    "docs/PRODUCT.md",
    "docs/RELEASE_ENGINEERING.md",
    "docs/RESEARCH.md",
    "docs/ROADMAP.md",
    "docs/SECURITY_AND_PRIVACY.md",
    "docs/SUPPORT_BUNDLE.md",
    "docs/TESTING.md",
    "docs/assets/1f372e2b-34da-4fe2-a2d0-050ecc9a300b.png",
    "docs/assets/readme",
    "docs/.reorg-marker",
    "README.pt.reorg.tmp",
]

ALLOWED_DOCS_ROOT_MARKDOWN = {"README.md"}

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def validate_required(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for relative in REQUIRED_DIRS:
        if not (ROOT / relative).is_dir():
            errors.append(f"missing required directory: {relative}")


def validate_legacy_cleanup(errors: list[str]) -> None:
    for relative in LEGACY_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"legacy/temporary path must not exist: {relative}")


def validate_docs_layout(errors: list[str]) -> None:
    if not DOCS.is_dir():
        return

    for path in sorted(DOCS.glob("*.md")):
        if path.name not in ALLOWED_DOCS_ROOT_MARKDOWN:
            errors.append(
                f"docs layout violation: {path.relative_to(ROOT)} must live in a responsibility subfolder"
            )


def validate_text_files(errors: list[str]) -> None:
    text_extensions = {".md", ".py", ".yml", ".yaml", ".json", ".txt"}

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in text_extensions:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path.relative_to(ROOT)}: expected UTF-8 text")
            continue

        relative = path.relative_to(ROOT)

        if "\t" in text and path.suffix.lower() in {".md", ".yml", ".yaml"}:
            errors.append(f"{relative}: contains tab characters")

        for line_no, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{relative}:{line_no}: trailing whitespace")


def validate_markdown_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)

        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue

            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue

            destination = (path.parent / clean).resolve()

            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{relative}: link escapes repository: {target}")
                continue

            if not destination.exists():
                errors.append(f"{relative}: broken internal link: {target}")


def validate_root_readme(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return

    text = readme.read_text(encoding="utf-8")
    expected_image = "docs/assets/thermalops-concept-overview.png"
    if expected_image not in text:
        errors.append("README.md: conceptual product image is not referenced")

    if "Imagem conceitual" not in text:
        errors.append("README.md: conceptual image disclaimer is missing")


def validate_language_contract(errors: list[str]) -> None:
    localization = ROOT / "docs/produto/localizacao-e-terminologia.md"
    constitution = ROOT / "ENGINEERING_CONSTITUTION.md"

    if localization.is_file():
        text = localization.read_text(encoding="utf-8")
        required_terms = ["pt-BR", "MaintenanceInspection", "ServiceDisposition", "schema"]
        for term in required_terms:
            if term not in text:
                errors.append(
                    f"docs/produto/localizacao-e-terminologia.md: missing language-contract term: {term}"
                )

    if constitution.is_file():
        text = constitution.read_text(encoding="utf-8")
        if "Documentation governance" not in text:
            errors.append("ENGINEERING_CONSTITUTION.md: documentation governance section missing")
        if "Localization" not in text:
            errors.append("ENGINEERING_CONSTITUTION.md: localization rule missing")


def main() -> int:
    errors: list[str] = []

    validate_required(errors)
    validate_legacy_cleanup(errors)
    validate_docs_layout(errors)
    validate_text_files(errors)
    validate_markdown_links(errors)
    validate_root_readme(errors)
    validate_language_contract(errors)

    if errors:
        print("Repository documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
