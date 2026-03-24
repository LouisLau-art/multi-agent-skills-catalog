# Handoff: Three-Agent Skills Purification and Hardening

## Session Metadata
- Created: 2026-03-23 03:24:35
- Project: /home/louis/context7-skills-curated-pack
- Branch: main
- Session duration: ~4 hours

### Recent Commits (for context)
  - 0146c33 docs: add context7 to skill discovery instructions in global context
  - 5d60ff5 chore: fix source attribution for react-19 and tanstack-query
  - 7b3fdcc feat(catalog): strictly synchronize manifest with the 50 hardened local skills
  - 5d1dc7b feat(catalog): add official better-auth-best-practices
  - cb18f5d feat(catalog): restore critical infra skills from wshobson

## Handoff Chain

- **Continues from**: [2026-03-22-022306-agent-automation-recommender-and-workflow-notes.md](./2026-03-22-022306-agent-automation-recommender-and-workflow-notes.md)
  - Previous title: Agent Automation Recommender And Workflow Notes
- **Supersedes**: None

> Review the previous handoff for full context before filling this one.

## Current State Summary

This session performed a radical "purification" of the agent environment. The scope was reduced from five agents to three (Codex, Claude, Gemini), removing OpenCode and Amp. Local skills were pruned from 95 down to 50 "battle-hardened" items, focusing on official sources and top-tier maintainers. The `self-improvement` skill was upgraded to the highly advanced `charon-fan` version with full hook integration. The repository manifest and profiles were strictly synchronized with this hardened 50-skill set and pushed to GitHub. The global instruction true source (`global-context/AGENTS.md`) was updated with critical discovery and interaction rules.

## Codebase Understanding

### Architecture Overview

The repository is now the definitive "curated source of truth" for a three-agent (Codex, Claude, Gemini) runtime. It uses `scripts/sync_agent_context.py` and `scripts/sync_mcp.py` to align global instructions and MCP configurations. Skills are physically synchronized (copied) across agents to ensure 100% parity.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `global-context/AGENTS.md` | Universal instruction source | Contains new rules for checking backup before downloading and non-interactive terminal usage. |
| `skills_manifest.csv` | Canonical public catalog | Now reflects the hardened 50-skill elite set. |
| `~/.claude/settings.json` | Claude Code global config | Updated with `self-improving-agent` lifecycle hooks. |
| `scripts/sync_agent_context.py` | Context sync tool | Patched to support only three agents (Codex, Claude, Gemini). |
| `scripts/sync_mcp.py` | MCP sync tool | Patched to align Context7 and GitHub MCP across three agents. |

### Key Patterns Discovered

- **Skill Parity**: All three agents now share the exact same 50 skills in their respective `skills/` directories.
- **Backup first**: The system is instructed to check `~/.<agent>/skills_backup` before fetching new skills from the web.
- **Official preference**: Low-quality or unofficial skills (like previous Prisma/Better-Auth/React-19 variants) were replaced with official or definitive-maintainer versions.
- **Non-interactive mandate**: Agents are now instructed to always use non-interactive flags (e.g., `-y`, `--yes`) to avoid terminal hangs.

## Work Completed

### Tasks Finished

- [x] Removed OpenCode and Amp support from all docs, scripts, and configurations.
- [x] Pruned local skills from 95 to 50, moving unused ones to `skills_backup`.
- [x] Synchronized the 50 skills across Codex, Claude, and Gemini.
- [x] Upgraded `self-improving-agent` to `charon-fan` version and configured hooks in `~/.claude/settings.json`.
- [x] Restored official/ definitive skills: `prisma-database-setup` (official), `better-auth-best-practices` (official), `vercel-react-best-practices`, `react-19` (gentleman-programming), `tanstack-query-best-practices` (deckardger).
- [x] Installed `claude-md-improver` across all three agents.
- [x] Updated `global-context/AGENTS.md` with Context7 discovery rules and non-interactive terminal preference.
- [x] Synchronized `skills_manifest.csv` and `skills_selected.txt` with the hardened 50-skill local set.
- [x] Pushed all changes to `origin/main`.

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `global-context/AGENTS.md` | Added rules for backup-first discovery and non-interactive terminal preference. | Improve efficiency and reduce context noise. |
| `skills_manifest.csv` | Massive cleanup; updated to match the elite 50-skill set. | Align public catalog with proven local baseline. |
| `README.md` / `README.zh-CN.md` | Updated to reflect three-agent architecture. | Accurate documentation. |
| `scripts/*.py` | Removed Amp/OpenCode targets and fixed sync logic. | Focus on active agents. |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Reduce to Three Agents | Keep 5 vs Reduce to 3 | OpenCode and Amp were removed by the user; focusing on Codex, Claude, Gemini simplifies the sync architecture. |
| Aggressive Skill Pruning | Keep 95 vs Prune to 50 | SkillsBench evidence shows too many skills hurt performance; 50 high-quality skills are more effective. |
| Use `charon-fan` version of self-improvement | Simple vs Research-based | The research-based multi-memory architecture is significantly more powerful for long-term agent evolution. |
| Check Backup First | Always download vs Check local | Saves bandwidth and preserves the "elite set" philosophy. |

## Pending Work

### Immediate Next Steps

1. Test the `self-improving-agent` hooks in a real Claude Code session to ensure error capturing works as expected.
2. Verify if any additional skills from `skills_backup` are truly missed in daily work.
3. Consider if any remaining "generic" skills in the 50-set can be further refined.

### Blockers/Open Questions

- [ ] Does the user want to restore any specific "soft skills" or "methodology" skills that were moved to backup?
- [ ] Should `self-improving-agent` hooks be ported to Codex/Gemini if they support similar mechanisms?

### Deferred Items

- Testing `browser-use` was deferred because `agent-browser` and `webapp-testing` already cover the requirements.
- Integration of `impeccable` was added to the public catalog/profile but deferred for local installation to avoid design-system conflicts.

## Context for Resuming Agent

### Important Context

The most important fact is that **the environment is now strictly hardened**. Do not randomly install new skills from the web without checking the `skills_backup` first. The system is designed for high success rates by minimizing instruction overlap. The `self-improving-agent` is now active via hooks; pay attention to `.learnings/` or the `memory/` directory for evolving project context.

### Assumptions Made

- The three active agents (Codex, Claude, Gemini) are the only ones currently in use.
- The 50 skills currently in the `skills/` directory represent the "elite" baseline for the user's stack (Next.js, Tailwind, Prisma, Supabase, AI).

### Potential Gotchas

- **Hook Overhead**: The `self-improving-agent` hooks in `settings.json` add a small token overhead to each turn.
- **Physical Sync**: Skills are copied, not symlinked. If you manually edit a skill in one agent's directory, you MUST run `scripts/sync_from_codex.py` (or similar) to propagate the change.

## Environment State

### Tools/Services Used

- `npx skills`: used for discovery and ranking verification.
- `npx ctx7`: used for advanced skill discovery.
- `git`: used for catalog management.
- `charon-fan/self-improving-agent` hooks: active in Claude Code.

### Active Processes

- None.

### Environment Variables

- `SKILLS_DIR`: referenced in `~/.claude/settings.json`.

## Related Resources

- [charon-fan/agent-playbook](https://github.com/charon-fan/agent-playbook)
- [obra/superpowers](https://github.com/obra/superpowers)
- [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills)

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
