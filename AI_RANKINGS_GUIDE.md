# AI Rankings Guide

This guide is for external AI models/agents that need to consume the public ranking datasets in this repository.

## Canonical Public URLs

- Site: `https://louislau-art.github.io/multi-agent-skills-catalog/`
- Manifest (read this first): `https://louislau-art.github.io/multi-agent-skills-catalog/data/context7_rankings_manifest.json`
- Primary skills ranking JSON: `https://louislau-art.github.io/multi-agent-skills-catalog/data/skills_sh_all_time_top2000.json`
- Secondary Context7 skills JSON: `https://louislau-art.github.io/multi-agent-skills-catalog/data/context7_skills_ranked_all.json`
- Docs ranking JSON: `https://louislau-art.github.io/multi-agent-skills-catalog/data/context7_docs_popular_top50.json`
- Docs extended JSON (full target): `https://louislau-art.github.io/multi-agent-skills-catalog/data/context7_docs_extended_top1000.json`
- Docs extended runtime JSON (temporary 51+ source): `https://louislau-art.github.io/multi-agent-skills-catalog/data/context7_docs_extended_top100.runtime.json`

Raw GitHub fallback (if Pages cache/deploy lags):
- Manifest: `https://raw.githubusercontent.com/LouisLau-art/multi-agent-skills-catalog/main/docs/data/context7_rankings_manifest.json`
- Primary skills ranking: `https://raw.githubusercontent.com/LouisLau-art/multi-agent-skills-catalog/main/docs/data/skills_sh_all_time_top2000.json`
- Secondary Context7 skills ranking: `https://raw.githubusercontent.com/LouisLau-art/multi-agent-skills-catalog/main/docs/data/context7_skills_ranked_all.json`
- Docs ranking: `https://raw.githubusercontent.com/LouisLau-art/multi-agent-skills-catalog/main/docs/data/context7_docs_popular_top50.json`
- Docs extended (full target): `https://raw.githubusercontent.com/LouisLau-art/multi-agent-skills-catalog/main/docs/data/context7_docs_extended_top1000.json`
- Docs extended runtime (temporary 51+ source): `https://raw.githubusercontent.com/LouisLau-art/multi-agent-skills-catalog/main/docs/data/context7_docs_extended_top100.runtime.json`

## What Each Dataset Means

- `skills_sh_all_time_top2000`:
  - Primary skills leaderboard for this repo/site.
  - Starts from the prerendered `skills.sh` all-time leaderboard payload, then continues via the public pagination API.
  - Contains the first 2000 rows, plus `totalSkills`.
- `docs_popular_top50`:
  - Context7 docs popularity snapshot (currently top 50 rows).
  - Main metric: `marketShare`.
- `docs_extended_top1000`:
  - Rows 1-50 are official rankings from Context7.
  - Rows >50 are estimated and directional (not official market-share rows).
  - Check `estimatedRows` in payload/meta. If `estimatedRows = 0`, the file is a temporary official-only snapshot.
- `docs_extended_top100_runtime`:
  - Runtime snapshot currently used when `docs_extended_top1000` is official-only.
  - Includes 1-50 official + 51-100 estimated rows.
- `skills_ranked_all`:
  - Secondary Context7 skills ranked snapshot with `minInstalls=0`.
  - Use this for Context7-specific comparison and long-tail lookup beyond the primary `skills.sh` snapshot.
  - Main metric: `installCount` (rank order comes from Context7 ranked endpoint).

## Recommended Consumption Protocol

1. Fetch `context7_rankings_manifest.json`.
2. Read `datasets[*].publicUrl` and `generatedAtUtc`.
3. For skills, prefer `skills_sh_all_time_top2000` first.
4. If you need Context7-specific fields (`trustScore`, `verified`, `benchmarkScore`) or a long-tail skill not present in the skills.sh snapshot, fall back to `skills_ranked_all`.
5. For docs 51+, if `docs_extended_top1000.estimatedRows = 0`, switch to `docs_extended_top100_runtime`.
6. Fetch only the dataset(s) you need.
7. In responses, mention snapshot timestamp and dataset scope (for example: skills.sh top 2000 snapshot, Context7 full skills snapshot, or docs top 100 runtime).

## Minimal Field Notes

- Docs ranking key fields: `rank`, `title`, `source`, `marketShare`, `snippets`, `tokens`, `updateAgo`, `verified`.
- Skills.sh key fields: `rank`, `name`, `skillId`, `source`, `installCount`, `detailUrl`.
- Context7 skills key fields: `rank`, `name`, `source`, `installCount`, `trustScore`, `verified`.

## 中文提示

如果你是中文模型，请先读取 manifest，再按需读取对应数据集，并在回答中注明数据时间戳（`generatedAtUtc`）。技能榜默认先用 `skills_sh_all_time_top2000`；只有在需要 Context7 专属字段或长尾技能时，再改用 `context7_skills_ranked_all.json`。如果 `docs_extended_top1000` 的 `estimatedRows=0`，请改用 `docs_extended_top100.runtime.json` 获取 51+。
