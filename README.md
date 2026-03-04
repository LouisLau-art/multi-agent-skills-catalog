# Context7 Skills Curated Pack

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Installable Skills](https://img.shields.io/badge/installable_skills-163-blue)
![Local Total](https://img.shields.io/badge/local_total_with__.system-164-6f42c1)
![Curation](https://img.shields.io/badge/curation-Installs%2BTrust%2BVerified-orange)
![Context7](https://img.shields.io/badge/source-Context7-black)

A curated, deduplicated Context7 skills pack for software development workflows.

Current snapshot: **163 installable skills** (plus internal `.system`, total local dirs = 164).

This repository intentionally contains:
- `skills_manifest.csv` (selected skills with source/score)
- `skills_selected.txt` (plain list)
- `scripts/install_curated.sh` (one-click installer)
- docs for de-dup policy and stack classification

It intentionally does **not** contain third-party `SKILL.md` contents.

## Why this approach

- lighter and easier to maintain
- deterministic reinstall from source
- avoids re-hosting third-party skill files

## Quick Start

```bash
# install to Claude target
bash scripts/install_curated.sh claude

# dry-run first
DRY_RUN=1 bash scripts/install_curated.sh claude
```

Supported targets:
- `claude` (default)
- `universal`
- `global`
- `auto`

## Files

- `skills_manifest.csv`: `slug, skill_name, source, installs, trust, score`
- `skills_selected.txt`: current selected slugs
- `manifest_summary.json`: generation metadata
- `docs/dedup-policy.md`: de-dup rule
- `docs/skills-by-stack-zh.md`: Chinese stack/language categorization

## Selection Rule

`0.50*Installs(log-normalized) + 0.30*Trust + 0.10*OfficialSource + 0.10*(Trust>=9)`

Used for high-overlap groups only, not blanket deletion.

## License

MIT for scripts/manifests in this repo.

Upstream skills remain under their original licenses and repositories.
