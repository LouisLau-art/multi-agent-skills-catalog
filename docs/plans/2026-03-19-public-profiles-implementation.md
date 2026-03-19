# Public Profiles Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reposition this repository from a single curated pack into a public skills distribution repo with scenario-based profiles, while preserving backward compatibility and leaving room for a private local overlay.

**Architecture:** Keep `skills_manifest.csv` as the canonical public catalog, introduce `profiles/*.txt` as install bundles, and update the installer to resolve one or more profiles into a concrete install set. Preserve `skills_selected.txt` as a compatibility export of the union of public profiles. Add a git-ignored local overlay mechanism so the maintainer can keep a larger personal workspace without forcing it into the public product.

**Tech Stack:** Python, text manifests, existing installer/sync scripts, Markdown docs, GitHub Pages

---

### Task 1: Define the public profile data model

**Files:**
- Create: `profiles/core-meta.txt`
- Create: `profiles/development-core.txt`
- Create: `profiles/writing-blog.txt`
- Create: `profiles/resume-job-search.txt`
- Create: `profiles/docs-office.txt`
- Create: `profiles/cloud-platform.txt`
- Create: `profiles/design-ui.txt`
- Create: `profiles/database-data.txt`
- Create: `profiles/README.md`

**Step 1: Create the profile directory and README**

Document:
- what a profile is
- how profiles compose
- which profile is the default starting point

**Step 2: Create initial profile manifests**

Populate each file with curated skill slugs only. Keep each profile intentionally small and understandable.

**Step 3: Verify profile slugs exist in `skills_manifest.csv`**

Run a check script or one-off verification command to confirm every profile slug is present in the public catalog.

### Task 2: Add compatibility and local-overlay conventions

**Files:**
- Modify: `.gitignore`
- Create: `profiles.local/.gitkeep`
- Create: `docs/public-profiles.md`

**Step 1: Define ignored local-only profile paths**

Ignore local overlay files such as:
- `profiles.local/*.txt`
- optional local notes or exports

**Step 2: Document promotion rules**

Explain when a local-only skill should be:
- promoted into the public catalog
- kept local-only
- rejected

### Task 3: Update the installer for profile-based installs

**Files:**
- Modify: `scripts/install_curated.py`
- Modify: `scripts/install_curated.sh`
- Modify: `scripts/install_curated.ps1`

**Step 1: Add a `--profiles` argument**

Support inputs such as:
- `public-default`
- `core-meta+writing-blog`
- `all-public`

**Step 2: Resolve profile files into unique slugs**

The installer should:
- read the selected profile manifests
- de-duplicate slugs
- look up matching catalog entries in `skills_manifest.csv`

**Step 3: Preserve current target handling**

Do not break:
- `claude`
- `codex`
- `gemini`
- `qwen`
- `opencode`
- `amp`
- `codebuddy`
- `all`

**Step 4: Keep a safe default**

If `--profiles` is omitted, install `public-default`.

### Task 4: Define public aliases and compatibility exports

**Files:**
- Modify: `skills_selected.txt`
- Modify: `manifest_summary.json`
- Create: `scripts/build_profile_exports.py`

**Step 1: Build `all-public`**

Generate the union of all public profiles.

**Step 2: Export `skills_selected.txt` from the union**

This keeps existing tooling working while changing the meaning from “single default pack” to “public compatibility export.”

**Step 3: Update summary metadata**

Record:
- public catalog count
- default profile count
- all-public count

### Task 5: Reframe repo documentation around profiles

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `AGENT.md`

**Step 1: Rewrite repo positioning**

Lead with:
- public distribution repo
- scenario-based profiles
- small default baseline

**Step 2: Add installation examples by profile**

Document examples for:
- developers
- blog/writing users
- resume/job-search users
- docs/office users
- cloud users

**Step 3: Explain public vs local**

State clearly:
- public repo != maintainer's full local workspace
- local overlay exists and is intentionally separate

### Task 6: Add profile guidance to the site

**Files:**
- Modify: `docs/index.html`
- Modify: `docs/data/context7_rankings_manifest.json`

**Step 1: Add a profile overview section**

Show:
- `public-default`
- optional add-on profiles
- what each profile is for

**Step 2: Link profiles to actual skill slugs**

Render profile cards using existing skill datasets and public skill links.

### Task 7: Curate the first public/local split

**Files:**
- Modify: `skills_manifest.csv`
- Modify: profile files under `profiles/`

**Step 1: Keep current public 120 as the starting public catalog**

Do not blindly import all local extras.

**Step 2: Promote only obvious public wins from the current local-only set**

Candidates to evaluate first:
- `wrangler`
- `writing-skills`
- `content-strategy`
- `resume-bullet-writer`
- `find-docs`
- `context7-mcp`

**Step 3: Leave personal or experimental skills out**

Examples:
- highly agent-specific meta skills
- low-signal personal workflow experiments

### Task 8: Verify and ship

**Files:**
- Modify: all touched files above

**Step 1: Verify installer help and profile parsing**

Run:
```bash
python scripts/install_curated.py --help
```

**Step 2: Dry-run profile installs**

Run:
```bash
python scripts/install_curated.py claude --profiles public-default --dry-run
python scripts/install_curated.py all --profiles public-default+writing-blog --dry-run
```

**Step 3: Verify exported counts**

Check:
- catalog count
- public-default count
- all-public count

**Step 4: Review docs and site copy**

Ensure a new user can answer:
- what this repo is
- what to install first
- how profiles differ

**Step 5: Commit and push**
