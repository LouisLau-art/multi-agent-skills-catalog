# Multi-Agent Installer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make this repository a real one-command installer that installs the curated Context7 skills pack once and syncs it across supported agent skill directories.

**Architecture:** Use `scripts/install_curated.py` as the canonical installer so the workflow is cross-platform. Keep `scripts/install_curated.sh` only as a thin Unix wrapper. The Python installer reads `skills_manifest.csv`, installs each curated skill from upstream Context7 sources, then syncs the resulting local skill tree into compatible agent directories (`codex`, `gemini`/`qwen`, `opencode`, `amp`). The repo remains manifests + installer + sync logic only; it does not vendor upstream `SKILL.md` files.

**Tech Stack:** Python 3, Bash wrapper, Context7 CLI (`npx ctx7`), CSV manifest, local filesystem sync

---

### Task 1: Build the canonical Python installer

**Files:**
- Create: `scripts/install_curated.py`
- Test: `skills_manifest.csv`

**Step 1: Write the failing check**

Run:
```bash
python scripts/install_curated.py --help
```
Expected: command fails because the file does not exist.

**Step 2: Implement manifest-driven install logic**

Write a Python script that:
- parses target strings such as `claude`, `all`, `claude+codex+gemini+opencode+amp`, `qwen`
- reads `skills_manifest.csv`
- installs each skill with `npx ctx7 skills install`
- supports `DRY_RUN=1` or `--dry-run`
- resolves agent directory defaults and supports env var overrides

**Step 3: Add sync support**

Support these sync targets:
- `codex` -> Codex skills dir
- `gemini` -> Gemini skills dir
- `qwen` -> Gemini skills dir alias
- `opencode` -> OpenCode skills dir
- `amp` / `ampcode` -> Amp skills dir

**Step 4: Add verification output**

Print:
- base target used
- expected curated count
- manifest path
- synced target directories

**Step 5: Commit**

```bash
git add scripts/install_curated.py
git commit -m "feat: add cross-platform curated installer"
```

### Task 2: Convert the shell installer into a thin wrapper

**Files:**
- Modify: `scripts/install_curated.sh`

**Step 1: Replace hardcoded shell logic**

Update the shell script to:
- detect `python3` or `python`
- execute `scripts/install_curated.py`
- keep argument passthrough unchanged

**Step 2: Verify shell syntax**

Run:
```bash
bash -n scripts/install_curated.sh
```
Expected: no output.

**Step 3: Commit**

```bash
git add scripts/install_curated.sh
git commit -m "refactor: wrap installer shell entry around python"
```

### Task 3: Update repository documentation for end users

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Step 1: Update counts and entrypoints**

Document the current snapshot as 170 installable skills and 171 local dirs including `.system`.

**Step 2: Document the multi-agent workflow**

Explain that the repo installs from upstream via Context7, then syncs locally to compatible agent directories.

**Step 3: Add concrete install examples**

Include commands for:
- `claude`
- `all`
- `opencode`
- `amp`
- `qwen`
- `DRY_RUN=1`

**Step 4: Document directory overrides**

List:
- `CLAUDE_SKILLS_DIR`
- `CODEX_SKILLS_DIR`
- `GEMINI_SKILLS_DIR`
- `OPENCODE_SKILLS_DIR`
- `AMP_SKILLS_DIR`

**Step 5: Commit**

```bash
git add README.md README.zh-CN.md
git commit -m "docs: describe cross-platform multi-agent installer"
```

### Task 4: Final verification

**Files:**
- Modify: none

**Step 1: Check syntax**

Run:
```bash
bash -n scripts/install_curated.sh
python3 -m py_compile scripts/install_curated.py
```
Expected: no output.

**Step 2: Smoke-test manifest consistency**

Run:
```bash
python3 - <<'PY'
import csv
with open('skills_manifest.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
print(len(rows))
PY
python3 - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('manifest_summary.json').read_text())['skills_count'])
PY
```
Expected: both report 170.

**Step 3: Manual dry-run verification**

Run:
```bash
DRY_RUN=1 python3 scripts/install_curated.py all
DRY_RUN=1 python3 scripts/install_curated.py claude+opencode+amp+qwen
```
Expected: printed commands come from the manifest and sync targets match the requested agents.

**Step 4: Final commit**

```bash
git add docs/plans/2026-03-06-multi-agent-installer.md scripts/install_curated.py scripts/install_curated.sh README.md README.zh-CN.md
git commit -m "feat: complete one-click multi-agent skills installer"
```
