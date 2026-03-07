# Troubleshooting

## `gh` is logged in, but `git push` still asks for GitHub username

**Symptom**
- `gh auth status` shows an active GitHub login
- `git push origin main` fails with:
  `fatal: could not read Username for 'https://github.com': No such device or address`

**Root cause**
- `gh` is authenticated, but the repository remote is still using HTTPS instead of SSH.
- In that case, git uses the HTTPS credential flow rather than the SSH key configured through `gh`.

**Fix**

Check the current remote:

```bash
git remote -v
```

If it shows `https://github.com/...`, switch it to SSH:

```bash
git remote set-url origin git@github.com:OWNER/REPO.git
```

Then verify again:

```bash
git remote -v
gh auth status
git push origin main
```

## Skills skipped because of invalid `SKILL.md` YAML

**Symptom**
- Skill loader prints warnings like:
  `Skipped loading N skill(s) due to invalid SKILL.md files`
- Example parser error:
  `invalid YAML: mapping values are not allowed in this context`

**Common causes seen in this pack**
- indented `Keywords:` block inside frontmatter instead of a top-level `keywords` field
- `description:` plain scalar containing YAML-breaking `: ` sequences

**Automatic behavior**
- `scripts/install_curated.py` now runs a post-install frontmatter validator/sanitizer for the Claude-compatible base install.
- This happens after install and before sync, so repaired files propagate to Codex/Gemini/OpenCode/Amp.

**Manual validation**

Check only:

```bash
python3 scripts/validate_skills_frontmatter.py \
  --skills-dir ~/.claude/skills \
  --check-only
```

Validate and auto-fix known issues:

```bash
python3 scripts/validate_skills_frontmatter.py \
  --skills-dir ~/.claude/skills
```

Validate only a subset:

```bash
python3 scripts/validate_skills_frontmatter.py \
  --skills-dir ~/.claude/skills \
  --slugs ai-sdk-core,nextjs,tanstack-query
```

**Current scope**
- The sanitizer is intentionally narrow.
- It only fixes known, low-risk frontmatter formatting issues discovered in this curated pack.
- Unknown YAML problems are reported but not rewritten aggressively.
