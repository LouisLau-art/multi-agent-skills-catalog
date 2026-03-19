#!/usr/bin/env python3
"""Shared auth helpers for Context7 API scripts.

Resolution order:
1) Explicit environment variable: CONTEXT7_API_KEY
2) Explicit key file path: CONTEXT7_API_KEY_FILE
3) Optional Codex MCP fallback (only when CONTEXT7_ALLOW_CODEX_MCP_FALLBACK=1)
"""

from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.request import Request

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


_SECTION = "[mcp_servers.context7.env]"
_KEY_RE = re.compile(r'^\s*CONTEXT7_API_KEY\s*=\s*["\']?(.*?)["\']?\s*$')


def _strip(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _is_truthy(value: Any) -> bool:
    s = _strip(value).lower()
    return s in {"1", "true", "yes", "on"}


def _from_key_file(path_value: str) -> str:
    path = Path(path_value).expanduser()
    if not path.exists():
        return ""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    # Common key-file format: first line is the token.
    line = raw.splitlines()[0] if raw.splitlines() else raw
    return _strip(line)


def _config_candidates() -> list[Path]:
    codex_home = _strip(os.environ.get("CODEX_HOME")) or str(Path.home() / ".codex")
    candidates = [
        Path(codex_home) / "config.toml",
        Path.home() / ".codex" / "config.toml",
    ]
    out: list[Path] = []
    for path in candidates:
        if path not in out:
            out.append(path)
    return out


def _from_toml(path: Path) -> str:
    if tomllib is None or not path.exists():
        return ""
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    if not isinstance(payload, dict):
        return ""
    mcp_servers = payload.get("mcp_servers")
    if not isinstance(mcp_servers, dict):
        return ""
    context7 = mcp_servers.get("context7")
    if not isinstance(context7, dict):
        return ""
    env = context7.get("env")
    if not isinstance(env, dict):
        return ""
    return _strip(env.get("CONTEXT7_API_KEY"))


def _from_plain_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ""

    in_section = False
    for line in lines:
        raw = line.strip()
        if raw.startswith("[") and raw.endswith("]"):
            in_section = raw == _SECTION
            continue
        if not in_section:
            continue
        # Remove inline comments safely for common TOML patterns.
        body = raw.split("#", 1)[0].strip()
        m = _KEY_RE.match(body)
        if not m:
            continue
        return _strip(m.group(1))
    return ""


@lru_cache(maxsize=1)
def resolve_context7_api_key() -> str:
    env_key = _strip(os.environ.get("CONTEXT7_API_KEY"))
    if env_key:
        return env_key

    key_file = _strip(os.environ.get("CONTEXT7_API_KEY_FILE"))
    if key_file:
        file_key = _from_key_file(key_file)
        if file_key:
            return file_key

    if not _is_truthy(os.environ.get("CONTEXT7_ALLOW_CODEX_MCP_FALLBACK")):
        return ""

    for cfg_path in _config_candidates():
        key = _from_toml(cfg_path)
        if key:
            return key
        key = _from_plain_text(cfg_path)
        if key:
            return key
    return ""


def build_context7_request(url: str, user_agent: str = "multi-agent-skills-catalog/1.0") -> Request:
    headers = {"User-Agent": user_agent}
    api_key = resolve_context7_api_key()
    if api_key:
        headers["CONTEXT7_API_KEY"] = api_key
        headers["Authorization"] = f"Bearer {api_key}"
    return Request(url, headers=headers)
