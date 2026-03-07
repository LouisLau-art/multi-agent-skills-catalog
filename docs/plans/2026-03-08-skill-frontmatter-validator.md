# Skill Frontmatter Validator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a post-install frontmatter validator/sanitizer and troubleshooting docs for broken upstream `SKILL.md` YAML.

**Architecture:** A standalone Python script in `scripts/` validates frontmatter for selected skill directories and applies narrowly-scoped repairs for known upstream formatting bugs. The installer calls the validator after Claude-base installation and before sync so repaired files fan out to downstream agent directories.

**Tech Stack:** Python 3 stdlib, PyYAML, existing `install_curated.py`

---

### Task 1: Add failing tests for validator behavior

**Files:**
- Create: `tests/test_validate_skills_frontmatter.py`

**Step 1: Write the failing test**

Cover:
- valid frontmatter passes unchanged
- indented `Keywords:` block is repaired into valid YAML
- YAML-breaking `description:` line is rewritten into a folded scalar

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_validate_skills_frontmatter -v`
Expected: FAIL because validator module does not exist yet

### Task 2: Implement validator/sanitizer script

**Files:**
- Create: `scripts/validate_skills_frontmatter.py`

**Step 1: Write minimal implementation**

Implement:
- frontmatter extraction
- YAML validation
- known-issue sanitizers
- CLI for `--skills-dir`, `--slugs`, `--check-only`

**Step 2: Run tests**

Run: `python3 -m unittest tests.test_validate_skills_frontmatter -v`
Expected: PASS

### Task 3: Integrate validator into installer

**Files:**
- Modify: `scripts/install_curated.py`

**Step 1: Add failing test coverage if feasible**

If direct installer tests are too heavy, validate through a focused CLI smoke run after implementation.

**Step 2: Implement minimal integration**

Run validator:
- only when base target is `claude`
- after install
- before sync
- skip in `--dry-run` with a clear message

**Step 3: Verify integration**

Run: `python3 scripts/install_curated.py claude --dry-run`
Expected: dry-run install output plus validator skip/plan output

### Task 4: Document troubleshooting and script availability

**Files:**
- Create: `docs/troubleshooting.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Step 1: Add troubleshooting content**

Document:
- GitHub auth mismatch (`gh` logged in but repo remote still HTTPS)
- invalid `SKILL.md` YAML and how to run validator manually

**Step 2: Update README**

Add:
- validator script to file list
- brief note that installer sanitizes known frontmatter issues in Claude-base installs

### Task 5: Final verification

**Files:**
- Test: `tests/test_validate_skills_frontmatter.py`

**Step 1: Run tests**

Run: `python3 -m unittest tests.test_validate_skills_frontmatter -v`
Expected: PASS

**Step 2: Run validator CLI**

Run: `python3 scripts/validate_skills_frontmatter.py --skills-dir ~/.codex/skills --check-only`
Expected: zero invalid files or a clear report

**Step 3: Commit**

```bash
git add tests/test_validate_skills_frontmatter.py scripts/validate_skills_frontmatter.py scripts/install_curated.py docs/troubleshooting.md README.md README.zh-CN.md docs/plans/2026-03-08-skill-frontmatter-validator-design.md docs/plans/2026-03-08-skill-frontmatter-validator.md
git commit -m "feat: validate and sanitize installed skill frontmatter"
```
