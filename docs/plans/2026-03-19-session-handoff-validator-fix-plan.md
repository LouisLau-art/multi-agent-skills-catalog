# Session Handoff Validator Fix Plan

## Status Update

- Upstream issue filed: `softaworks/agent-toolkit#21`
- Fork created: `LouisLau-art/agent-toolkit`
- Fix branch pushed: `fix/session-handoff-validator-headings`
- Upstream PR opened: `softaworks/agent-toolkit#22`
- Verification completed with:
  - `python -m unittest tests/test_session_handoff_validator.py`
  - real handoff validation against local documents, all returning `100/100`

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reproduce, fix, and upstream or fork-maintain the `session-handoff` validator bug that incorrectly marks valid handoffs as incomplete when required sections use `###` headings.

**Architecture:** Treat this as an upstream-quality bugfix task, not as part of skills curation or blogging work. First confirm the bug with a minimal regression case, then patch the validator to accept deeper Markdown heading levels, then decide whether to contribute upstream or maintain a fork depending on response speed and repo fit.

**Tech Stack:** Python, GitHub, `softaworks/agent-toolkit`, local `session-handoff` skill scripts

---

### Task 1: Record upstream status and bug scope

**Files:**
- Modify: `docs/plans/2026-03-19-session-handoff-validator-fix-plan.md`
- Reference: `/home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`
- Reference: `/home/louis/.codex/skills/session-handoff/references/handoff-template.md`

**Step 1: Capture repo facts**

Record these facts in working notes or issue draft:
- upstream repo: `softaworks/agent-toolkit`
- current public size signals: roughly `1117` stars, `83` forks, `0` open issues, `2` open PRs
- license: MIT
- `session-handoff` exists in `skills/session-handoff/`

**Step 2: Capture bug statement**

Write the bug in one sentence:

`validate_handoff.py` only recognizes required sections when they use `#` or `##` headings, so valid handoffs using `### Important Context` or `### Immediate Next Steps` are incorrectly marked incomplete.

**Step 3: Note current recommendation**

Document:
- upstream issue should be filed because there is no existing open issue for this bug
- repo is small enough to fork if upstream is slow or unresponsive

**Step 4: Validation**

Expected output:
- one clean bug statement
- one clean upstream-status summary
- one explicit go/no-go recommendation on forking

### Task 2: Reproduce the bug with a minimal failing case

**Files:**
- Create: `[fork-or-local-test-area]/tests/test_validate_handoff_heading_levels.py`
- Reference: `/home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`

**Step 1: Write a failing test**

Create a fixture handoff string with:
- `## Current State Summary`
- `### Immediate Next Steps`
- `### Important Context`

Assert that the validator should treat required sections as complete.

**Step 2: Run test to verify it fails**

Run:

```bash
pytest tests/test_validate_handoff_heading_levels.py -v
```

Expected:
- FAIL
- failure should show the validator missing `Important Context` and `Immediate Next Steps`

**Step 3: Add a second control case**

Add a second test using `## Important Context` and `## Immediate Next Steps` to confirm current behavior works for shallower headings.

**Step 4: Validation**

Expected:
- one failing regression case for `###`
- one passing control case for `##`

### Task 3: Patch heading detection

**Files:**
- Modify: `[fork-or-local-test-area]/skills/session-handoff/scripts/validate_handoff.py`
- Test: `[fork-or-local-test-area]/tests/test_validate_handoff_heading_levels.py`

**Step 1: Update section matching**

Replace the current heading regex logic so required and recommended sections accept any Markdown heading level from `#` upward.

Target idea:

```python
pattern = rf'(?:^|\\n)#+\\s*{re.escape(section)}'
```

Do this consistently for:
- required-section detection
- recommended-section detection

**Step 2: Preserve existing behavior**

Do not widen behavior beyond heading depth. Keep:
- section-name matching case-insensitive
- section-content completeness checks
- secret scanning and file validation untouched

**Step 3: Run tests**

Run:

```bash
pytest tests/test_validate_handoff_heading_levels.py -v
```

Expected:
- both tests PASS

### Task 4: Verify against real handoffs

**Files:**
- Reference: `/home/louis/LouisLau-art.github.io/.claude/handoffs/2026-03-19-155027-scholarflow-blog-polish.md`
- Reference: `/home/louis/LouisLau-art.github.io/.claude/handoffs/2026-03-19-155027-homepage-job-search-packaging.md`
- Reference: `/home/louis/multi-cloud-email-sender/.claude/handoffs/2026-03-19-155027-multi-cloud-email-sender-interview-materials.md`
- Reference: `/home/louis/context7-skills-curated-pack/.claude/handoffs/2026-03-19-155027-local-skills-audit-wave3.md`

**Step 1: Re-run validator on real files**

Run the patched validator against the four handoffs above.

Expected:
- `100/100`
- no “missing required sections” false positives

**Step 2: Check for regressions**

Run the validator on a deliberately incomplete handoff if available.

Expected:
- truly missing required sections still fail

### Task 5: Decide upstream path

**Files:**
- Create: `[fork-or-local-test-area]/docs/upstream-session-handoff-validator-bug.md`

**Step 1: Prepare upstream issue draft**

Include:
- minimal repro markdown
- current regex
- proposed fix
- before/after behavior

**Step 2: Choose path**

Use this rule:
- if you want fast local control: fork immediately
- if you prefer reducing maintenance: file upstream issue first, then fork only if needed

**Step 3: If forking**

Fork `softaworks/agent-toolkit` and keep the patch small:
- validator heading-level fix
- regression test
- maybe a short README note if needed

**Step 4: Validation**

Expected:
- one issue draft ready
- one explicit fork-or-upstream decision

### Task 6: Sync local usage decision

**Files:**
- Modify: `docs/plans/2026-03-19-local-skills-audit.md` (only if needed)
- Modify: project notes or handoff docs as needed

**Step 1: Decide local usage**

If patched version is adopted locally, note:
- whether local `session-handoff` should be replaced from fork
- whether current handoff authoring guidance should prefer `##` temporarily or allow `###`

**Step 2: Document outcome**

Add one short note in local planning docs so future agents know:
- bug exists or is fixed
- where the maintained version lives

**Step 3: Validation**

Expected:
- no ambiguity for future sessions about which validator behavior is trusted

## Execution Options

Plan complete and saved to `docs/plans/2026-03-19-session-handoff-validator-fix-plan.md`.

Two execution options:

**1. Subagent-Driven (this session)** - dispatch a fresh agent to reproduce and patch the validator bug, then review results.

**2. Parallel Session (separate)** - open a new session in a dedicated worktree or fork checkout and execute this plan there.
