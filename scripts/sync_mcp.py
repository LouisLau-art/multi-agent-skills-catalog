#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from context7_auth import resolve_context7_api_key

try:
    import tomllib
except Exception:
    tomllib = None  # type: ignore[assignment]


TARGETS = ("codex", "claude", "gemini", "opencode")
ALIASES = {
        "qwen": "gemini",
}
SECTION_RE = re.compile(r"^\[mcp_servers\.([A-Za-z0-9_-]+)(?:\.[^\]]+)?\]\s*$")


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Sync the tracked MCP source of truth into Codex, Claude, Gemini, OpenCode, and OpenCode."
    )
    parser.add_argument(
        "--manifest",
        default=str(repo_root / "global-context" / "mcp-servers.json"),
        help="Path to the tracked MCP server manifest.",
    )
    parser.add_argument(
        "--targets",
        default="all",
        help="Comma- or plus-separated targets. Supported: codex, claude, gemini, opencode, all.",
    )
    parser.add_argument(
        "--servers",
        default="all",
        help="Comma- or plus-separated managed server names from the manifest, or 'all'.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without modifying files.",
    )
    return parser.parse_args()


def parse_compound(raw: str, valid: tuple[str, ...] | list[str], aliases: dict[str, str] | None = None) -> list[str]:
    alias_map = aliases or {}
    normalized = (raw or "all").replace(",", "+").strip().lower()
    tokens = [alias_map.get(token.strip(), token.strip()) for token in normalized.split("+") if token.strip()]
    if not tokens or tokens == ["all"]:
        return list(valid)

    out: list[str] = []
    for token in tokens:
        if token == "all":
            for item in valid:
                if item not in out:
                    out.append(item)
            continue
        if token not in valid:
            raise SystemExit(f"Unsupported value: {token}")
        if token not in out:
            out.append(token)
    return out


def codex_config_path() -> Path:
    return Path(os.getenv("CODEX_CONFIG_FILE", str(Path.home() / ".codex" / "config.toml"))).expanduser()


def gemini_settings_path() -> Path:
    return Path(os.getenv("GEMINI_SETTINGS_FILE", str(Path.home() / ".gemini" / "settings.json"))).expanduser()


def opencode_config_path() -> Path:
    return Path(
        os.getenv("OPENCODE_CONFIG_FILE", str(Path.home() / ".config" / "opencode" / "opencode.jsonc"))
    ).expanduser()


def claude_settings_path() -> Path:
    return Path(os.getenv("CLAUDE_SETTINGS_FILE", str(Path.home() / ".claude.json"))).expanduser()


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return payload


def load_context7_key_from_local_configs() -> str:
    codex_cfg = codex_config_path()
    if tomllib is not None and codex_cfg.exists():
        try:
            payload = tomllib.loads(codex_cfg.read_text(encoding="utf-8"))
            key = (
                payload.get("mcp_servers", {})
                .get("context7", {})
                .get("http_headers", {})
                .get("CONTEXT7_API_KEY", "")
            )
            if isinstance(key, str) and key.strip():
                return key.strip()
        except Exception:
            pass

    for path_getter, key_path in (
        (gemini_settings_path, ("mcpServers", "context7", "headers", "CONTEXT7_API_KEY")),
        (opencode_config_path, ("mcp", "context7", "headers", "CONTEXT7_API_KEY")),
    ):
        try:
            payload = load_jsonc_object(path_getter())
        except Exception:
            continue
        current: Any = payload
        for part in key_path:
            if not isinstance(current, dict):
                current = ""
                break
            current = current.get(part, "")
        if isinstance(current, str) and current.strip():
            return current.strip()
    return ""


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
            elif ch == "\\":
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


def load_jsonc_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    stripped = strip_jsonc(path.read_text(encoding="utf-8")).strip()
    if not stripped:
        return {}
    payload = json.loads(stripped)
    if not isinstance(payload, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any], dry_run: bool) -> None:
    body = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if dry_run:
        print(f"DRY_RUN write JSON: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def resolve_named_value(name: str) -> str:
    if name == "context7_api_key":
        os.environ.setdefault("CONTEXT7_ALLOW_CODEX_MCP_FALLBACK", "1")
        value = resolve_context7_api_key() or load_context7_key_from_local_configs()
        if not value:
            raise SystemExit(
                "Could not resolve CONTEXT7_API_KEY. Set CONTEXT7_API_KEY, CONTEXT7_API_KEY_FILE, "
                "or configure Context7 in one local agent config first."
            )
        return value
    if name.startswith("env:"):
        env_name = name.split(":", 1)[1]
        value = os.getenv(env_name, "").strip()
        if not value:
            raise SystemExit(f"Required environment variable is missing: {env_name}")
        return value
    raise SystemExit(f"Unsupported secret resolver: {name}")


def expand_string(value: str) -> str:
    return os.path.expanduser(os.path.expandvars(value))


def resolve_server(spec: dict[str, Any]) -> dict[str, Any]:
    transport = spec.get("transport")
    if transport not in {"http", "stdio"}:
        raise SystemExit(f"Unsupported transport: {transport}")

    resolved: dict[str, Any] = {"transport": transport}

    if transport == "http":
        url = spec.get("url")
        if not isinstance(url, str) or not url.strip():
            raise SystemExit("HTTP MCP server is missing 'url'")
        resolved["url"] = expand_string(url)
        headers: dict[str, str] = {}
        for key, value in (spec.get("headers") or {}).items():
            headers[str(key)] = expand_string(str(value))
        for key, resolver in (spec.get("headersFrom") or {}).items():
            headers[str(key)] = resolve_named_value(str(resolver))
        if headers:
            resolved["headers"] = headers
    else:
        command = spec.get("command")
        if not isinstance(command, str) or not command.strip():
            raise SystemExit("stdio MCP server is missing 'command'")
        resolved["command"] = expand_string(command)
        args = spec.get("args") or []
        if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
            raise SystemExit("stdio MCP server 'args' must be a string array")
        resolved["args"] = [expand_string(item) for item in args]
        env_map: dict[str, str] = {}
        for key, value in (spec.get("env") or {}).items():
            env_map[str(key)] = expand_string(str(value))
        for key, resolver in (spec.get("envFrom") or {}).items():
            env_map[str(key)] = resolve_named_value(str(resolver))
        if env_map:
            resolved["env"] = env_map

    for platform in ("codex", "gemini", "opencode", "claude"):
        extra = spec.get(platform)
        if extra is not None:
            if not isinstance(extra, dict):
                raise SystemExit(f"Expected '{platform}' override to be an object")
            resolved[f"{platform}_extra"] = extra
    return resolved


def toml_escape(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, str):
        return toml_escape(value)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    raise SystemExit(f"Unsupported TOML value: {value!r}")


def strip_codex_mcp_sections(text: str, names: set[str]) -> str:
    lines = text.splitlines()
    out: list[str] = []
    skip = False

    for line in lines:
        stripped = line.strip()
        match = SECTION_RE.match(stripped)
        if match:
            skip = match.group(1) in names
            if skip:
                continue
        if skip:
            if stripped.startswith("[") and stripped.endswith("]"):
                skip = False
            else:
                continue
        out.append(line)

    while out and not out[-1].strip():
        out.pop()
    if out:
        return "\n".join(out) + "\n"
    return ""


def render_codex_server(name: str, server: dict[str, Any]) -> str:
    lines = [f"[mcp_servers.{name}]"]
    if server["transport"] == "http":
        lines.append(f"url = {toml_value(server['url'])}")
    else:
        lines.append(f"command = {toml_value(server['command'])}")
        args = server.get("args") or []
        if args:
            lines.append(f"args = {toml_value(args)}")

    for key, value in (server.get("codex_extra") or {}).items():
        lines.append(f"{key} = {toml_value(value)}")

    headers = server.get("headers") or {}
    if headers:
        lines.append("")
        lines.append(f"[mcp_servers.{name}.http_headers]")
        for key, value in headers.items():
            lines.append(f"{key} = {toml_value(value)}")

    env_map = server.get("env") or {}
    if env_map:
        lines.append("")
        lines.append(f"[mcp_servers.{name}.env]")
        for key, value in env_map.items():
            lines.append(f"{key} = {toml_value(value)}")

    return "\n".join(lines)


def sync_codex(path: Path, servers: dict[str, dict[str, Any]], dry_run: bool) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    body = strip_codex_mcp_sections(existing, set(servers))
    rendered = "\n\n".join(render_codex_server(name, server) for name, server in servers.items())
    final = body + ("\n" if body and not body.endswith("\n\n") else "") + rendered + "\n"
    if dry_run:
        print(f"DRY_RUN write TOML: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(final, encoding="utf-8")


def sync_gemini(path: Path, servers: dict[str, dict[str, Any]], dry_run: bool) -> None:
    payload = load_jsonc_object(path)
    mcp_servers = payload.get("mcpServers")
    if mcp_servers is None:
        mcp_servers = {}
    if not isinstance(mcp_servers, dict):
        raise SystemExit(f"Expected 'mcpServers' to be an object in {path}")

    for name, server in servers.items():
        if server["transport"] == "http":
            entry: dict[str, Any] = {"httpUrl": server["url"]}
            headers = server.get("headers") or {}
            if headers:
                entry["headers"] = headers
        else:
            entry = {"command": server["command"]}
            args = server.get("args") or []
            if args:
                entry["args"] = args
            env_map = server.get("env") or {}
            if env_map:
                entry["env"] = env_map
        mcp_servers[name] = entry

    payload["mcpServers"] = mcp_servers
    write_json(path, payload, dry_run)


def sync_opencode(path: Path, servers: dict[str, dict[str, Any]], dry_run: bool) -> None:
    payload = load_jsonc_object(path)
    payload.setdefault("$schema", "https://opencode.ai/config.json")
    mcp_servers = payload.get("mcp")
    if mcp_servers is None:
        mcp_servers = {}
    if not isinstance(mcp_servers, dict):
        raise SystemExit(f"Expected 'mcp' to be an object in {path}")

    for name, server in servers.items():
        if server["transport"] == "http":
            entry = {"type": "remote", "url": server["url"]}
            headers = server.get("headers") or {}
            if headers:
                entry["headers"] = headers
        else:
            entry = {"type": "local", "command": [server["command"], *(server.get("args") or [])]}
            env_map = server.get("env") or {}
            if env_map:
                entry["environment"] = env_map
        mcp_servers[name] = entry

    payload["mcp"] = mcp_servers
    write_json(path, payload, dry_run)


def redact_server(server: dict[str, Any]) -> dict[str, Any]:
    out = dict(server)
    if "headers" in out:
        out["headers"] = {key: "***" for key in out["headers"]}
    if "env" in out:
        redacted_env = {}
        for key, value in out["env"].items():
            redacted_env[key] = "***" if "KEY" in key or "TOKEN" in key or "SECRET" in key else value
        out["env"] = redacted_env
    return out


def sync_claude(path: Path, servers: dict[str, dict[str, Any]], dry_run: bool) -> None:
    payload = load_jsonc_object(path)
    mcp_servers = payload.get("mcpServers")
    if mcp_servers is None:
        mcp_servers = {}
    if not isinstance(mcp_servers, dict):
        raise SystemExit(f"Expected 'mcpServers' to be an object in {path}")

    for name, server in servers.items():
        if server["transport"] == "http":
            entry = {"type": "http", "url": server["url"]}
            headers = server.get("headers") or {}
            if headers:
                entry["headers"] = headers
        else:
            entry = {"type": "stdio", "command": server["command"]}
            args = server.get("args") or []
            if args:
                entry["args"] = args
            env_map = server.get("env") or {}
            if env_map:
                entry["env"] = env_map
        mcp_servers[name] = entry

    payload["mcpServers"] = mcp_servers
    write_json(path, payload, dry_run)


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    if not manifest_path.is_file():
        raise SystemExit(f"MCP manifest not found: {manifest_path}")

    manifest = load_manifest(manifest_path)
    servers_payload = manifest.get("servers")
    if not isinstance(servers_payload, dict):
        raise SystemExit(f"Manifest is missing 'servers': {manifest_path}")

    known_servers = tuple(servers_payload.keys())
    selected_targets = parse_compound(args.targets, TARGETS, aliases=ALIASES)
    selected_server_names = parse_compound(args.servers, known_servers)
    resolved_servers = {
        name: resolve_server(servers_payload[name]) for name in selected_server_names
    }

    print(f"Manifest: {manifest_path}")
    print(f"Targets: {', '.join(selected_targets)}")
    print(f"Servers: {', '.join(selected_server_names)}")
    for name, server in resolved_servers.items():
        print(f"Resolved {name}: {json.dumps(redact_server(server), ensure_ascii=False)}")

    if "codex" in selected_targets:
        sync_codex(codex_config_path(), resolved_servers, args.dry_run)
    if "gemini" in selected_targets:
        sync_gemini(gemini_settings_path(), resolved_servers, args.dry_run)
    if "opencode" in selected_targets:
        sync_opencode(opencode_config_path(), resolved_servers, args.dry_run)
    if "claude" in selected_targets:
        sync_claude(claude_settings_path(), resolved_servers, args.dry_run)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
