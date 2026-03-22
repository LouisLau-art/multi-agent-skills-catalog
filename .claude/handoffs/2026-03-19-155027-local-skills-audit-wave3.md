# Handoff: Local Skills Audit Wave 3

## Session Metadata
- Created: 2026-03-19 15:50:27
- Project: /home/louis/context7-skills-curated-pack
- Branch: main
- Session duration: ~90 minutes across two completed audit waves

## Recent Commits (for context)
  - 82fac3e document context7 setup across agents
  - e3b8e72 add context7 integration profile
  - db76d3c promote blog resume and cloud skills
  - d8c0c6b add profile-based public installer
  - fe57e4c add public profile packaging design

## Handoff Chain

- **Continues from**: None (fresh start)
- **Supersedes**: None

> This is the first handoff for this task.

## Current State Summary

Two cleanup waves are already complete. Local user skills are down from 186 to 180, and all synced agent directories now match the Codex source-of-truth tree. The next wave should not revisit the same obvious duplicate clusters. It should focus on broader-but-still-low-risk cleanup among generic advisor, toolkit, and weakly scoped skills that are still installed locally. This is a local-tree task first; do not assume repo public catalog changes are needed.

## Codebase Understanding

## Architecture Overview

This repo now serves as the public catalog, profile system, and tooling layer for multi-agent skill management. The local machine uses `~/.codex/skills` as the source of truth, and `scripts/sync_from_codex.py` propagates that set to `claude`, `gemini`, `qwen`, `opencode`, `amp`, and `codebuddy`. The public catalog is deliberately more conservative than the local install set. Local cleanup work should therefore be documented here, but not automatically promoted into public-catalog decisions.

## Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| docs/plans/2026-03-19-local-skills-audit.md | Current audit record with waves 1 and 2 | Starting point for wave 3 |
| scripts/sync_from_codex.py | Syncs `~/.codex/skills` to other agent directories | Must be used after any local deletions |
| skills_selected.txt | Public catalog compatibility export | Do not modify unless a local decision clearly generalizes |
| profiles/context7-integration.txt | Public Context7 profile | Relevant because local Context7 duplication was already resolved |
| README.md | Public positioning and selection rules | Reference for keeping local and public policy aligned |

## Key Patterns Discovered

The strongest local cleanup decisions so far have not been based on name collisions. They have been based on workflow overlap, trigger conflict, and whether a skill is focused/procedural enough to reduce execution failure. That standard already removed `shadcn-ui`, `documentation-lookup`, `playwright-best-practices`, `code-review`, `context7`, and `context7-mcp`. The next agent should continue using that same standard and avoid getting distracted by install counts or popularity.

## Work Completed

## Tasks Finished

- [x] Completed first-wave local cleanup: `shadcn-ui`, `documentation-lookup`, `playwright-best-practices`, `code-review`
- [x] Completed second-wave local cleanup: `context7`, `context7-mcp`
- [x] Synced and pruned all managed agent directories after each wave
- [x] Updated the local audit document to reflect current count and wave outcomes

## Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| docs/plans/2026-03-19-local-skills-audit.md | Added wave 1 and wave 2 execution results and current count | Keeps the audit state current and reviewable |
| .claude/handoffs/2026-03-19-155027-local-skills-audit-wave3.md | Added this handoff | Enables a fresh agent to continue the next cleanup pass |

## Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Keep `context7-docs-lookup` and `find-docs`, remove `context7` and `context7-mcp` | Keep all four, remove all but one, keep two with clear roles | The kept pair has distinct value: Codex-native lookup plus cross-agent CLI fallback |
| Keep `tailwind-v4-shadcn` | Remove as duplicate, keep conditionally, keep unconditionally | `scholar-flow/frontend` really uses Tailwind v4 plus shadcn, so the skill has real project-specific value |
| Keep local cleanup separate from public-catalog promotion | Sync everything into repo, split local/public, stop auditing | Local workbench needs remain broader than the public baseline |

## Pending Work

## Immediate Next Steps

1. Identify the strongest remaining generic advisor/toolkit candidates with weak trigger discipline, especially among broad business or design-adjacent skills.
2. Read the corresponding `SKILL.md` files and judge them by the same criteria: focused, procedural, low-overlap, low-trigger-conflict, useful for reducing failures.
3. If a deletion wave is justified, remove those skills from `~/.codex/skills`, run `python scripts/sync_from_codex.py --prune`, and append the results to `docs/plans/2026-03-19-local-skills-audit.md`.

## Blockers/Open Questions

- [ ] Some remaining broad skills may still be useful in niche conversations, so the next agent must distinguish “rare but sharp” from “generic and noisy”.
- [ ] The repo public catalog should only be touched if a wave-3 conclusion clearly generalizes beyond Louis’s local machine.

## Deferred Items

- Re-checking writing/blog clusters is deferred until the active blog-writing work progresses further.
- Any public catalog or profile changes are deferred unless a local-only conclusion obviously applies to the public package.

## Context for Resuming Agent

## Important Context

This task is highly parallelizable because it only affects local skill hygiene and synced agent directories; it does not block the blog-writing or homepage-packaging work. The next agent should continue from the current audit state rather than reopen settled clusters. The best wave-3 candidates will probably come from generic advisor or toolkit skills that read like broad roleplay manuals instead of concrete execution aids. The goal is not to drive the number down for its own sake. The goal is to reduce context load and trigger ambiguity while preserving genuinely useful specialist skills.

## Assumptions Made

- `~/.codex/skills` remains the source of truth for local skills.
- All managed agent directories should stay pruned to match Codex after each cleanup wave.
- The current local count of 180 is correct at handoff time.

## Potential Gotchas

- Do not judge by name alone; role overlap and trigger conflict are the real criteria.
- Avoid deleting project-specific skills such as `tailwind-v4-shadcn` unless you can prove they no longer match active repos.
- Remember that some skills are already absent locally even if they appeared in earlier discussions; verify presence before making deletion plans.

## Environment State

## Tools/Services Used

- `scripts/sync_from_codex.py --prune`
- Local skill directories under `~/.codex/skills`
- Standard shell tools for counting and comparing directories

## Active Processes

- No required long-running processes at handoff time

## Environment Variables

- None required for local audit work

## Related Resources

- `docs/plans/2026-03-19-local-skills-audit.md`
- `scripts/sync_from_codex.py`
- `skills_selected.txt`
- `profiles/context7-integration.txt`
- `README.md`

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
