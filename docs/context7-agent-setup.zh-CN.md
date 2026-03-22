# Codex、Gemini CLI、Claude Code 的 Context7 接法

这份文档说明这个工作区里四种目标 agent 应该如何统一接入 Context7：

- Codex
- Gemini CLI
- Claude Code
- OpenCode

## 推荐结论

优先级建议如下：

1. **Context7 MCP + 薄的一层指令/skill**
2. **只有在 MCP 不方便时，才退回 skill-only**

原因很直接：

- MCP 负责统一的外部工具能力
- 一份共享上下文真源负责稳定三端行为规则
- skill 适合做工作流包装，但不该被当成 MCP 的通用替代品

## 对应到本 repo 的真源

这个 repo 现在把下面几项当作三端运行时基线：

- `global-context/AGENTS.md`：统一全局上下文真源
- `global-context/mcp-servers.json`：统一 MCP 真源
- `scripts/sync_agent_context.py`：把上下文真源同步到三端
- `scripts/sync_mcp.py`：把受管 MCP servers 同步到三端

推荐同步顺序：

```bash
python scripts/install_curated.py all --profiles context7-integration
python scripts/sync_agent_context.py --mode symlink
python scripts/sync_mcp.py
```

## 对应到本 repo 的公开 profile

这个 repo 仍然提供一个可选公开 profile：

- `context7-integration`

当前包含：

- `context7-docs-lookup`
- `context7-mcp`
- `find-docs`

示例：

```bash
python scripts/install_curated.py codex --profiles context7-integration
python scripts/install_curated.py gemini --profiles context7-integration
python scripts/install_curated.py claude --profiles context7-integration
python scripts/install_curated.py all --profiles context7-integration
```

## Codex

### 全局规则

共享文件放在：

- `~/.codex/AGENTS.md`

### MCP 配置

受管 MCP servers 放在：

- `~/.codex/config.toml`

Context7 示例：

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"

[mcp_servers.context7.http_headers]
CONTEXT7_API_KEY = "YOUR_API_KEY"
```

## Gemini CLI

### 全局规则

共享文件放在：

- `~/.gemini/GEMINI.md`

### MCP 配置

受管 MCP servers 放在：

- `~/.gemini/settings.json`

Context7 示例：

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

常用内建命令：

- `/mcp list`
- `/mcp refresh`
- `/memory show`
- `/memory refresh`
- `/memory add`

## Claude Code

### 全局规则

共享文件放在：

- `~/.claude/CLAUDE.md`

### MCP 配置

Claude 更适合走 user-scope CLI 入口：

```bash
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

校验：

```bash
claude mcp list
```

### Plugin 说明

Claude 也可以通过 plugin 暴露 Context7。  
如果你想追求和另外三端严格的一对一 MCP 对齐，优先保留原生 user MCP，删除重复的 plugin 管理入口。
