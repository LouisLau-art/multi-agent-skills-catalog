# Handoff: Agent Automation Recommender And Workflow Notes

## Session Metadata
- Created: 2026-03-22 02:23:06
- Project: /home/louis/context7-skills-curated-pack
- Branch: main
- Session duration: about 3 hours

### Recent Commits (for context)
  - c8b9126 docs(find-skills): clarify skillsbench alignment
  - d85df58 docs(catalog): add blog post rewrite review
  - 83e3b34 docs(catalog): record figma overlap decision
  - 4614a38 refactor(catalog): remove claude-only meta skills
  - 4592c07 feat(catalog): add technical blog writing profile

## Handoff Chain

- **Continues from**: [2026-03-22-022243-public-catalog-skillsbench-alignment.md](./2026-03-22-022243-public-catalog-skillsbench-alignment.md)
  - Previous title: Public Catalog Skillsbench Alignment
- **Supersedes**: None

> Review the previous handoff for full context before filling this one.

## Current State Summary

This session had two connected tracks. First, we evaluated Anthropic's `claude-automation-recommender`, compared how much of its method transfers to Gemini CLI, Codex, and OpenCode, then wrote repo-local design/plan docs and built a local draft skill `agent-automation-recommender` under `~/.codex/skills/`. Second, we clarified how these workflow skills relate to `github/spec-kit` and `obra/superpowers`, plus how `npx`, `ctx7`, `skills`, Codex system skills, GitHub downloads, proxies, `curl`, and Clash interact. The draft skill is usable and manually invoked once, but it is still alpha-level because it has not been pressure-tested across multiple repos and real target runtimes yet.

## Codebase Understanding

### Architecture Overview

`context7-skills-curated-pack` is a catalog/curation repo rather than an app. The main architecture is: `skills_manifest.csv` and `profiles/` describe installable sets, `scripts/` implements install/validation/sync flows, `tests/` protects key validators, `docs/plans/` stores design and planning artifacts, `global-context/AGENTS.md` captures reusable instruction baselines, and `.claude/` contains repo-local automation such as agents, settings, skills, and now handoffs. A recurring pattern in this repo is to keep speculative or alpha work local first, validate it, then decide whether it should become public catalog content.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| docs/plans/2026-03-22-agent-automation-recommender-design.md | Design rationale for the new cross-agent automation recommender skill | Explains why we chose one shared core skill plus thin per-platform adapters |
| docs/plans/2026-03-22-agent-automation-recommender.md | Implementation plan for the draft skill | Defines scope, outputs, and validation path |
| docs/plans/2026-03-22-agent-automation-recommender-baseline-notes.md | Baseline guardrails for the draft | Captures failure modes and authoring constraints |
| /home/louis/.codex/skills/agent-automation-recommender/SKILL.md | Local draft skill entrypoint | This is the current working draft that should be tested next |
| /home/louis/.codex/skills/agent-automation-recommender/references/claude-code.md | Claude adapter reference | Maps recommendations into Claude-native surfaces |
| /home/louis/.codex/skills/agent-automation-recommender/references/gemini-cli.md | Gemini adapter reference | Maps recommendations into Gemini-native surfaces |
| /home/louis/.codex/skills/agent-automation-recommender/references/codex.md | Codex adapter reference | Maps recommendations into Codex-native surfaces |
| /home/louis/.codex/skills/agent-automation-recommender/references/opencode.md | OpenCode adapter reference | Maps recommendations into OpenCode-native surfaces |
| /home/louis/.codex/AGENTS.md | Codex global instructions | Patched to prefer `gh` or GitHub MCP when user gives a GitHub repo URL |
| /home/louis/.claude/CLAUDE.md | Claude global instructions | Patched with the same GitHub URL rule |
| /home/louis/.gemini/GEMINI.md | Gemini global instructions | Patched with the same GitHub URL rule |
| /home/louis/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py | Built-in Codex skill installer implementation | Used to confirm install flow is Python `urllib` plus zip/git fallback, not `curl` |
| /home/louis/context7-skills-curated-pack/.claude/handoffs/2026-03-22-022306-agent-automation-recommender-and-workflow-notes.md | This handoff | Start here when resuming this exact thread |

### Key Patterns Discovered

- This repo prefers design and plan artifacts before promotion into the public catalog.
- Cross-agent work should preserve a shared method while using platform-native terminology instead of forcing one vocabulary everywhere.
- For GitHub repository URLs, the preferred lookup path is `gh` or GitHub MCP first, then only fall back if those are insufficient.
- For live docs and tool behavior, Context7 or primary-source docs are preferred over generic search.
- Public/publishable boundaries matter. Local experiments can live under `~/.codex/skills/` without immediately becoming repo content.
- Trust and fit matter more than raw install counts when judging candidate skills for curation.

## Work Completed

### Tasks Finished

- [x] Evaluated `claude-automation-recommender` from Anthropic and mapped its portability to Gemini CLI, Codex, and OpenCode.
- [x] Wrote three repo-local planning artifacts for `agent-automation-recommender`.
- [x] Created a local draft skill with one shared entrypoint and four thin platform reference files.
- [x] Manually invoked `$agent-automation-recommender` against this repo and confirmed it produces sane, platform-specific recommendations.
- [x] Patched `/home/louis/.codex/AGENTS.md`, `/home/louis/.claude/CLAUDE.md`, and `/home/louis/.gemini/GEMINI.md` to prefer `gh` or GitHub MCP for direct GitHub repo URLs.
- [x] Investigated `github/spec-kit`, `obra/superpowers`, `vercel-labs/skills`, `upstash/context7`, Codex system skills, and the proxy/download path for GitHub-based skill installs.

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| docs/plans/2026-03-22-agent-automation-recommender-design.md | Added new design note in repo | Records the chosen architecture and tradeoffs |
| docs/plans/2026-03-22-agent-automation-recommender.md | Added implementation plan in repo | Defines scope and next validation steps |
| docs/plans/2026-03-22-agent-automation-recommender-baseline-notes.md | Added baseline notes in repo | Prevents the draft from drifting into a giant conditional or overly Claude-centric model |
| /home/louis/.codex/skills/agent-automation-recommender/SKILL.md | Added local draft skill entrypoint | Keeps the experiment local until validated |
| /home/louis/.codex/skills/agent-automation-recommender/references/claude-code.md | Added local Claude adapter notes | Captures Claude-native output buckets |
| /home/louis/.codex/skills/agent-automation-recommender/references/gemini-cli.md | Added local Gemini adapter notes | Captures Gemini-native output buckets |
| /home/louis/.codex/skills/agent-automation-recommender/references/codex.md | Added local Codex adapter notes | Captures Codex-native output buckets |
| /home/louis/.codex/skills/agent-automation-recommender/references/opencode.md | Added local OpenCode adapter notes | Captures OpenCode-native output buckets |
| /home/louis/.codex/AGENTS.md | Inserted GitHub URL handling rule | Reduces noisy web search when the user already supplied a repo URL |
| /home/louis/.claude/CLAUDE.md | Inserted GitHub URL handling rule | Keeps cross-agent behavior aligned |
| /home/louis/.gemini/GEMINI.md | Inserted GitHub URL handling rule | Keeps cross-agent behavior aligned |
| .claude/handoffs/2026-03-22-022306-agent-automation-recommender-and-workflow-notes.md | Added this handoff | Preserves session context for the next agent |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Use one shared core skill plus four thin adapters | Four separate skills, one giant conditional skill, hybrid shared-core design | Four separate skills would drift; one giant skill would become noisy and easy for the model to misread; a shared core with thin adapters preserves reuse without hiding platform differences |
| Keep the draft local under `~/.codex/skills/` for now | Immediate repo/catalog promotion, local-first draft | The draft is still alpha and should be validated before it affects the public catalog |
| Treat `superpowers` as methodology-shaped, not just a skill dump | "Random popular skills" framing, methodology framing | The repo and README explicitly present it as a development methodology built from workflow skills |
| Do not recommend installing every `obra/superpowers` skill by default | Full install, minimal curated subset | Full install would add routing noise and duplicate local equivalents; a small subset is more maintainable |
| Prefer `gh` or GitHub MCP for direct GitHub repo URLs | Start with generic web search, start with repo-native tooling | Repo-native tooling exposes README, tree, issues, PRs, and releases with less noise |
| Describe current draft state as alpha usable, not fully validated | Claim it is done, mark it unusable | The skill triggers and gives reasonable output, but we have not pressure-tested it enough to call it stable |

## Pending Work

### Immediate Next Steps

1. Pressure-test `/home/louis/.codex/skills/agent-automation-recommender/SKILL.md` on at least one non-catalog repo and compare Codex vs Gemini-style outputs for cross-platform bleed.
2. Decide whether to implement the highest-value recommendations the draft produced for this repo, especially a root `AGENTS.md` and stronger repo-local automation hooks/config stubs.
3. If the draft survives testing, decide whether it should remain local-only or be promoted into the repo as a documented/public-facing artifact.

### Blockers/Open Questions

- [ ] Open question: Should `agent-automation-recommender` stay as a local Codex draft only, or should equivalent drafts be synced into Claude/Gemini/OpenCode locations later?
- [ ] Open question: Should the repo adopt the draft skill's own recommendations now, or wait until the skill is validated on additional repos?
- [ ] Open question: The earlier handoff `2026-03-22-022243-public-catalog-skillsbench-alignment.md` still contains placeholders and may need cleanup if that thread matters later.

### Deferred Items

- Full cross-platform runtime validation inside Claude Code, Gemini CLI, and OpenCode was deferred because this session focused on design and reasoning, not end-to-end runtime verification.
- Promotion into `skills_manifest.csv`, `profiles/`, or installer scripts was deferred because the draft is not stable enough yet.
- A repo doc explicitly mapping `spec-kit` phases to workflow skills was deferred because the user asked for explanation first, not a repo documentation patch.

## Context for Resuming Agent

### Important Context

The most important thing to preserve is that this session produced a coherent but still provisional design direction. The user accepted the architecture of `agent-automation-recommender` as one shared analysis workflow plus thin platform adapters, not four separate skills and not one large `if/switch` document. The authoritative draft lives outside this repo in `/home/louis/.codex/skills/agent-automation-recommender/`, while the repo only contains design/plan/baseline notes under `docs/plans/`. The draft has already been invoked once with `$agent-automation-recommender` against this repo and produced reasonable suggestions, so it is usable, but it should still be treated as alpha until it survives pressure tests on other repos and runtimes. The session also established a cross-agent behavior rule now written into `/home/louis/.codex/AGENTS.md`, `/home/louis/.claude/CLAUDE.md`, and `/home/louis/.gemini/GEMINI.md`: when the user provides a GitHub repository URL directly, prefer `gh` or GitHub MCP to inspect the repo rather than starting with generic web search. Finally, the user spent substantial time understanding workflow methodology. The key conclusion was that `github/spec-kit` is a spec-driven lifecycle/toolkit, while `obra/superpowers` is a methodology expressed as installable workflow skills; they are closely related in spirit but operate at different layers.

### Assumptions Made

- Assumption: Local-only incubation is safer than immediate public-catalog promotion for new cross-agent skills.
- Assumption: The current shell proxy environment (`http_proxy`, `https_proxy`, `ALL_PROXY`) remains active, so most HTTPS GitHub fetches will route through the local proxy while SSH fallback may behave differently.
- Assumption: The user values a default best-practice answer plus fallback conditions rather than a menu of equally weighted options.
- Assumption: Popular workflow skills from `obra/superpowers` overlap enough with existing local skills that full reinstallation is unnecessary.

### Potential Gotchas

- `rg` is not installed in this shell, so use `grep`, `find`, or `git grep` when needed.
- Repo `git status` only shows repo-tracked or repo-local untracked changes. The modified global instruction files under `/home/louis/.codex`, `/home/louis/.claude`, and `/home/louis/.gemini` will not appear there.
- `.claude/` is untracked in this repo, so new handoffs also appear as untracked content.
- Several unrelated `docs/plans/*.md` files and `.learnings/` are already untracked; do not revert or assume they were created in this exact thread.
- Codex built-in skills are hidden under `/home/louis/.codex/skills/.system/`; a plain `ls ~/.codex/skills` can mislead you into thinking there are no built-ins.
- The built-in `skill-installer` prefers Python `urllib` zip download from GitHub and only later falls back to git, so proxy behavior depends on whether the path stays on HTTPS or falls back to SSH.
- The handoff validator had been patched in a prior run to accept any Markdown heading depth; still run it before claiming completion.

## Environment State

### Tools/Services Used

- `gh`: used to inspect GitHub repositories and README content for `github/spec-kit`, `obra/superpowers`, and `vercel-labs/skills`.
- GitHub MCP and Context7: used earlier in the session when comparing skill portability and live docs.
- `git`, `sed`, `grep`, `find`, `npm`, `npx`, `curl`: used to inspect local files, CLI behavior, versions, and network/proxy configuration.
- Codex built-in `session-handoff` scripts: used to scaffold this handoff and should be used again for validation.

### Active Processes

- No intentional long-running dev servers or watchers were left running for this task.

### Environment Variables

- `http_proxy`
- `https_proxy`
- `ALL_PROXY`
- `NO_PROXY`
- `GITHUB_TOKEN`
- `GH_TOKEN`

## Related Resources

- docs/plans/2026-03-22-agent-automation-recommender-design.md
- docs/plans/2026-03-22-agent-automation-recommender.md
- docs/plans/2026-03-22-agent-automation-recommender-baseline-notes.md
- /home/louis/.codex/skills/agent-automation-recommender/SKILL.md
- /home/louis/.codex/skills/agent-automation-recommender/references/claude-code.md
- /home/louis/.codex/skills/agent-automation-recommender/references/gemini-cli.md
- /home/louis/.codex/skills/agent-automation-recommender/references/codex.md
- /home/louis/.codex/skills/agent-automation-recommender/references/opencode.md
- /home/louis/.codex/AGENTS.md
- /home/louis/.claude/CLAUDE.md
- /home/louis/.gemini/GEMINI.md
- /home/louis/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py
- /home/louis/.codex/skills/.system/skill-installer/scripts/github_utils.py
- /home/louis/.codex/skills/.system/skill-installer/scripts/list-skills.py
- https://github.com/github/spec-kit
- https://github.com/obra/superpowers
- https://github.com/vercel-labs/skills
- https://github.com/upstash/context7
- https://github.com/anthropics/claude-plugins-official

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
