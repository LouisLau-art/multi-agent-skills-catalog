# Context7 Setup for Codex, Gemini CLI, Claude Code

This document explains the recommended Context7 setup for the four agent environments used in this workspace:

- Codex
- Gemini CLI
- Claude Code
- OpenCode

## Recommendation

Use this order of preference:

1. **Context7 MCP + thin instruction/skill layer** for the default setup
2. **Skill-only fallback** only when MCP is unavailable or inconvenient

Rationale:

- MCP gives a consistent external tool surface
- one tracked context source keeps behavior stable across four agents
- skills remain useful as reusable workflow wrappers, but should not be treated as a universal replacement for MCP

## Tracked Source Of Truth In This Repo

This repo now treats these files as the five-agent runtime baseline:

- `global-context/AGENTS.md` for shared global context
- `global-context/mcp-servers.json` for managed MCP servers
- `scripts/sync_agent_context.py` to sync the shared context into local runtimes
- `scripts/sync_mcp.py` to sync managed MCP servers into local runtimes

Recommended sync flow:

```bash
python scripts/install_curated.py all --profiles context7-integration
python scripts/sync_agent_context.py --mode symlink
python scripts/sync_mcp.py
```

## Public Repo Mapping

This repository exposes an optional public profile for Context7-oriented setup:

- `context7-integration`

It currently includes:

- `context7-docs-lookup`
- `context7-mcp`
- `find-docs`

Example:

```bash
python scripts/install_curated.py codex --profiles context7-integration
python scripts/install_curated.py gemini --profiles context7-integration
python scripts/install_curated.py claude --profiles context7-integration
python scripts/install_curated.py all --profiles context7-integration
```

## Codex

### Global instructions

Put the shared file at:

- `~/.codex/AGENTS.md`

### MCP configuration

Put managed MCP servers in:

- `~/.codex/config.toml`

Context7 example:

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"

[mcp_servers.context7.http_headers]
CONTEXT7_API_KEY = "YOUR_API_KEY"
```

## Gemini CLI

### Global instructions

Put the shared file at:

- `~/.gemini/GEMINI.md`

### MCP configuration

Put managed MCP servers in:

- `~/.gemini/settings.json`

Context7 example:

```json
{
  "mcpServers": {
    "context7": {
      "httpUrl": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

Useful built-ins:

- `/mcp list`
- `/mcp refresh`
- `/memory show`
- `/memory refresh`
- `/memory add`

## Claude Code

### Global instructions

Put the shared file at:

- `~/.claude/CLAUDE.md`

### MCP configuration

Claude's native user-scope flow is CLI-driven:

```bash
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

Verification:

```bash
claude mcp list
```

### Plugin note

Claude can also expose Context7 through a plugin-oriented integration. If you want strict one-to-one parity with the other four agents, prefer the native user MCP entry and remove duplicate plugin-managed entries.

## When Skill-Only Is Acceptable

Skill-only is acceptable when:

- you want the fastest personal setup
- MCP is blocked by environment restrictions
- you only need lightweight docs lookup

It is not the best default when you want:

- cross-agent consistency
- team-standardized behavior
- a shared documented setup

## Sources

- Codex docs: https://context7.com/openai/codex/llms.txt
- Gemini CLI docs: https://context7.com/google-gemini/gemini-cli/llms.txt
- Claude Code Context7 guide: https://context7.com/docs/clients/claude-code
- Context7 all-clients MCP configs: https://context7.com/docs/resources/all-clients
- Context7 best practices: https://context7.com/docs/tips
