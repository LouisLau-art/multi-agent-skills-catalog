# Skill Frontmatter Validator Design

**Goal:** Add a safe post-install validator/sanitizer for `SKILL.md` frontmatter so broken upstream YAML does not silently disable installed skills.

**Scope:**
- Validate `SKILL.md` frontmatter for curated skills installed into the Claude-compatible skills directory.
- Auto-fix only known, low-risk formatting issues discovered in this pack:
  - indented `Keywords:` blocks that should be a top-level `keywords` field
  - single-line `description:` values that contain YAML-breaking `: ` sequences
- Surface what was fixed and what still failed.

**Non-goals:**
- Rewriting arbitrary third-party skill bodies
- Normalizing all frontmatter style differences
- Validating unknown base targets whose install path is not deterministic in this repo

**Integration point:**
- Run after installing curated skills into the Claude-compatible base directory
- Run before sync to Codex/Gemini/OpenCode/Amp so sanitized files propagate downstream

**Verification:**
- Add Python unit tests for detection and auto-fix behavior
- Run validator tests
- Run installer in dry-run and direct validator CLI checks
