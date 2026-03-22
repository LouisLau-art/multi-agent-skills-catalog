#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


TARGETS = ("codex", "claude", "gemini", "opencode")
ALIASES = {
        "qwen": "gemini",
}


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Sync the tracked global AGENTS.md source of truth into five local agent runtimes."
    )
    parser.add_argument(
        "--source",
        default=str(repo_root / "global-context" / "AGENTS.md"),
        help="Path to the canonical AGENTS.md source file.",
    )
    parser.add_argument(
        "--targets",
        default="all",
        help="Comma- or plus-separated targets. Supported: codex, claude, gemini, opencode, all.",
    )
    parser.add_argument(
        "--mode",
        choices=("symlink", "copy"),
        default="symlink",
        help="How to mirror the source file into each target runtime.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without modifying files.",
    )
    return parser.parse_args()


def parse_targets(raw: str) -> list[str]:
    normalized = (raw or "all").replace(",", "+").strip().lower()
    tokens = [ALIASES.get(token.strip(), token.strip()) for token in normalized.split("+") if token.strip()]
    if not tokens or tokens == ["all"]:
        return list(TARGETS)

    out: list[str] = []
    for token in tokens:
        if token == "all":
            for target in TARGETS:
                if target not in out:
                    out.append(target)
            continue
        if token not in TARGETS:
            raise SystemExit(f"Unsupported target: {token}")
        if token not in out:
            out.append(token)
    return out


def target_files() -> dict[str, Path]:
    home = Path.home()
    return {
        "codex": Path(os.getenv("CODEX_AGENTS_FILE", str(home / ".codex" / "AGENTS.md"))).expanduser(),
        "claude": Path(os.getenv("CLAUDE_AGENTS_FILE", str(home / ".claude" / "CLAUDE.md"))).expanduser(),
        "gemini": Path(os.getenv("GEMINI_AGENTS_FILE", str(home / ".gemini" / "GEMINI.md"))).expanduser(),
        "opencode": Path(
            os.getenv("OPENCODE_AGENTS_FILE", str(home / ".config" / "opencode" / "AGENTS.md"))
        ).expanduser(),
            }


def opencode_config_path() -> Path:
    return Path(
        os.getenv("OPENCODE_CONFIG_FILE", str(Path.home() / ".config" / "opencode" / "opencode.jsonc"))
    ).expanduser()


def remove_path(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY_RUN remove: {path}")
        return
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
        return
    if path.is_dir():
        shutil.rmtree(path)


def sync_file(source: Path, target: Path, mode: str, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY_RUN ensure parent: {target.parent}")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() or target.is_symlink():
        if mode == "symlink" and target.is_symlink() and target.resolve(strict=False) == source.resolve(strict=False):
            return
        remove_path(target, dry_run)

    if mode == "symlink":
        if dry_run:
            print(f"DRY_RUN symlink: {target} -> {source}")
        else:
            target.symlink_to(source)
        return

    if dry_run:
        print(f"DRY_RUN copy: {source} -> {target}")
        return
    shutil.copy2(source, target)


def strip_jsonc(text: str) -> str:
    out: list[str] = []
    i = 0
    in_string = False
    escape = False

    while i < len(text):
        ch = text[i]
        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":  # keep escaped characters inside strings
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue

        if ch == "/" and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt == "/":
                i += 2
                while i < len(text) and text[i] not in "\r\n":
                    i += 1
                continue
            if nxt == "*":
                i += 2
                while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i += 2
                continue

        out.append(ch)
        i += 1

    return "".join(out)


def load_jsonc_object(path: Path) -> dict:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    stripped = strip_jsonc(raw).strip()
    if not stripped:
        return {}
    payload = json.loads(stripped)
    if not isinstance(payload, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return payload


def write_json(path: Path, payload: dict, dry_run: bool) -> None:
    body = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if dry_run:
        print(f"DRY_RUN write JSON: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def ensure_opencode_instruction(config_path: Path, instruction_path: Path, dry_run: bool) -> None:
    payload = load_jsonc_object(config_path)
    payload.setdefault("$schema", "https://opencode.ai/config.json")

    instructions = payload.get("instructions")
    if instructions is None:
        instructions_list: list[str] = []
    elif isinstance(instructions, list) and all(isinstance(item, str) for item in instructions):
        instructions_list = list(instructions)
    else:
        raise SystemExit(f"Expected 'instructions' to be a string array in {config_path}")

    target_string = str(instruction_path.expanduser())
    if target_string in instructions_list:
        if dry_run:
            print(f"DRY_RUN opencode instructions already contains: {target_string}")
        return

    instructions_list.append(target_string)
    payload["instructions"] = instructions_list
    write_json(config_path, payload, dry_run)


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Canonical AGENTS file not found: {source}")

    targets = parse_targets(args.targets)
    paths = target_files()

    print(f"Source of truth: {source}")
    print(f"Targets: {', '.join(targets)}")
    print(f"Mode: {args.mode}")

    for target in targets:
        sync_file(source, paths[target], args.mode, args.dry_run)

    if "opencode" in targets:
        ensure_opencode_instruction(opencode_config_path(), paths["opencode"], args.dry_run)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
