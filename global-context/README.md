# Global Context

这个目录保存本机多 agent 共享的全局真源，并同步到 GitHub。

- `AGENTS.md` 是四端统一的唯一正文真源。
- `mcp-servers.json` 是四端统一的 MCP 真源，目前托管 `context7` 和 `github`。
- 上下文同步目标：
  - `~/.codex/AGENTS.md`
  - `~/.claude/CLAUDE.md`
  - `~/.gemini/GEMINI.md`
  - `~/.config/opencode/AGENTS.md`
- OpenCode 需要额外把 `~/.config/opencode/AGENTS.md` 写入 `opencode.jsonc` 的 `instructions`，因为它不会自动发现全局 `AGENTS.md`。
- 推荐同步命令：
  - `python scripts/sync_agent_context.py --mode symlink`
  - `python scripts/sync_mcp.py`
