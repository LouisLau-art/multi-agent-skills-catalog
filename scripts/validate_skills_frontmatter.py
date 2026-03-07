#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import yaml


DESCRIPTION_PREFIX = "description:"
KEYWORDS_PATTERN = re.compile(r"^\s+Keywords:\s*(.*)$")


@dataclass(frozen=True)
class RepairResult:
    content: str
    changed: bool
    repairs: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class FileValidationResult:
    path: Path
    status: str
    repairs: list[str] = field(default_factory=list)
    error: str = ""


@dataclass(frozen=True)
class ValidationSummary:
    checked: int
    valid: int
    fixed: int
    invalid: int
    missing: int
    results: list[FileValidationResult]


def parse_frontmatter(text: str) -> tuple[list[str], str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            frontmatter = lines[1:index]
            body = "\n".join(lines[index + 1 :])
            if text.endswith("\n"):
                body += "\n"
            return frontmatter, body
    return None


def dump_frontmatter(frontmatter_lines: list[str], body: str) -> str:
    return "---\n" + "\n".join(frontmatter_lines) + "\n---\n" + body


def validate_frontmatter_yaml(frontmatter_lines: list[str]) -> None:
    yaml.safe_load("\n".join(frontmatter_lines))


def repair_keywords_block(frontmatter_lines: list[str]) -> tuple[list[str], bool]:
    repaired: list[str] = []
    changed = False
    index = 0
    while index < len(frontmatter_lines):
        line = frontmatter_lines[index]
        match = KEYWORDS_PATTERN.match(line)
        if not match:
            repaired.append(line)
            index += 1
            continue

        values = [match.group(1).strip()]
        index += 1
        while index < len(frontmatter_lines) and frontmatter_lines[index].startswith("  "):
            values.append(frontmatter_lines[index].strip())
            index += 1

        merged = " ".join(part for part in values if part).strip()
        repaired.append("keywords: >")
        repaired.append(f"  {merged}")
        changed = True
    return repaired, changed


def repair_description_scalar(frontmatter_lines: list[str]) -> tuple[list[str], bool]:
    repaired: list[str] = []
    changed = False

    for line in frontmatter_lines:
        if not line.startswith(DESCRIPTION_PREFIX):
            repaired.append(line)
            continue

        value = line[len(DESCRIPTION_PREFIX) :].strip()
        if (
            not value
            or value.startswith((">", "|", "'", '"'))
            or ": " not in value
        ):
            repaired.append(line)
            continue

        repaired.append("description: >")
        for wrapped in textwrap.wrap(value, width=78) or [value]:
            repaired.append(f"  {wrapped}")
        changed = True

    return repaired, changed


def sanitize_frontmatter_text(text: str) -> RepairResult:
    parsed = parse_frontmatter(text)
    if parsed is None:
        return RepairResult(content=text, changed=False, repairs=[])

    frontmatter_lines, body = parsed
    try:
        validate_frontmatter_yaml(frontmatter_lines)
        return RepairResult(content=text, changed=False, repairs=[])
    except yaml.YAMLError:
        pass

    working = list(frontmatter_lines)
    repairs: list[str] = []

    working, keywords_changed = repair_keywords_block(working)
    if keywords_changed:
        repairs.append("keywords_block")

    working, description_changed = repair_description_scalar(working)
    if description_changed:
        repairs.append("description_folded_scalar")

    content = dump_frontmatter(working, body)
    return RepairResult(content=content, changed=bool(repairs), repairs=repairs)


def validate_skill_file(path: Path, check_only: bool = False) -> FileValidationResult:
    text = path.read_text(encoding="utf-8")
    parsed = parse_frontmatter(text)
    if parsed is None:
        return FileValidationResult(path=path, status="skipped")

    frontmatter_lines, _ = parsed
    try:
        validate_frontmatter_yaml(frontmatter_lines)
        return FileValidationResult(path=path, status="valid")
    except yaml.YAMLError as exc:
        original_error = str(exc)

    if check_only:
        return FileValidationResult(path=path, status="invalid", error=original_error)

    repair = sanitize_frontmatter_text(text)
    if not repair.changed:
        return FileValidationResult(path=path, status="invalid", error=original_error)

    repaired_parsed = parse_frontmatter(repair.content)
    assert repaired_parsed is not None
    repaired_frontmatter, _ = repaired_parsed
    try:
        validate_frontmatter_yaml(repaired_frontmatter)
    except yaml.YAMLError as exc:
        return FileValidationResult(
            path=path,
            status="invalid",
            repairs=repair.repairs,
            error=str(exc),
        )

    path.write_text(repair.content, encoding="utf-8")
    return FileValidationResult(path=path, status="fixed", repairs=repair.repairs)


def validate_skill_tree(
    skills_dir: Path,
    slugs: list[str] | None = None,
    check_only: bool = False,
) -> ValidationSummary:
    requested = slugs or sorted(
        p.name for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    results: list[FileValidationResult] = []
    missing = 0

    for slug in requested:
        skill_path = skills_dir / slug / "SKILL.md"
        if not skill_path.exists():
            results.append(
                FileValidationResult(
                    path=skill_path,
                    status="missing",
                    error="SKILL.md not found",
                )
            )
            missing += 1
            continue
        results.append(validate_skill_file(skill_path, check_only=check_only))

    return ValidationSummary(
        checked=len(requested),
        valid=sum(1 for result in results if result.status == "valid"),
        fixed=sum(1 for result in results if result.status == "fixed"),
        invalid=sum(1 for result in results if result.status == "invalid"),
        missing=missing,
        results=results,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and optionally sanitize installed SKILL.md frontmatter."
    )
    parser.add_argument(
        "--skills-dir",
        required=True,
        help="Root directory containing installed skill subdirectories.",
    )
    parser.add_argument(
        "--slugs",
        default="",
        help="Optional comma-separated subset of skill slugs to validate.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate only; do not write repairs.",
    )
    return parser.parse_args()


def print_summary(summary: ValidationSummary) -> None:
    print(
        "Checked {checked} skill(s): valid={valid} fixed={fixed} invalid={invalid} missing={missing}".format(
            checked=summary.checked,
            valid=summary.valid,
            fixed=summary.fixed,
            invalid=summary.invalid,
            missing=summary.missing,
        )
    )
    for result in summary.results:
        if result.status == "valid":
            continue
        line = f"{result.status.upper()}: {result.path}"
        if result.repairs:
            line += f" repairs={','.join(result.repairs)}"
        if result.error:
            line += f" error={result.error}"
        print(line)


def main() -> int:
    args = parse_args()
    skills_dir = Path(args.skills_dir).expanduser().resolve()
    if not skills_dir.is_dir():
        print(f"ERROR: skills directory not found: {skills_dir}", file=sys.stderr)
        return 1

    slugs = [slug.strip() for slug in args.slugs.split(",") if slug.strip()] or None
    summary = validate_skill_tree(skills_dir, slugs=slugs, check_only=args.check_only)
    print_summary(summary)
    return 1 if summary.invalid or summary.missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
