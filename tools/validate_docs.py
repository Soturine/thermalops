#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "ENGINEERING_CONSTITUTION.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/PRODUCT.md",
    "docs/ARCHITECTURE.md",
    "docs/PORTABLE.md",
    "docs/SECURITY_AND_PRIVACY.md",
    "docs/DIAGNOSTICS_AND_REPAIR.md",
    "docs/SUPPORT_BUNDLE.md",
    "docs/AI.md",
    "docs/TESTING.md",
    "docs/RELEASE_ENGINEERING.md",
    "docs/ROADMAP.md",
]

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")

    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)

        if "\t" in text:
            errors.append(f"{relative}: contains tab characters")

        for line_no, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{relative}:{line_no}: trailing whitespace")

        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
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

    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
