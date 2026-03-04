# AI Rankings Guide

This guide is for external AI models/agents that need to consume the two public ranking datasets in this repository.

## Canonical Public URLs

- Site: `https://louislau-art.github.io/context7-skills-curated-pack/`
- Manifest (read this first): `https://louislau-art.github.io/context7-skills-curated-pack/docs/data/context7_rankings_manifest.json`
- Docs ranking JSON: `https://louislau-art.github.io/context7-skills-curated-pack/docs/data/context7_docs_popular_top50.json`
- Skills ranking JSON: `https://louislau-art.github.io/context7-skills-curated-pack/docs/data/context7_skills_ranked_all.json`

## What Each Dataset Means

- `docs_popular_top50`:
  - Context7 docs popularity snapshot (currently top 50 rows).
  - Main metric: `marketShare`.
- `skills_ranked_all`:
  - Context7 skills ranked snapshot with `minInstalls=0`.
  - Main metric: `installCount` (rank order comes from Context7 ranked endpoint).

## Recommended Consumption Protocol

1. Fetch `context7_rankings_manifest.json`.
2. Read `datasets[*].publicUrl` and `generatedAtUtc`.
3. Fetch only the dataset(s) you need.
4. In responses, mention snapshot timestamp and dataset scope (for example: docs top 50 only).

## Minimal Field Notes

- Docs ranking key fields: `rank`, `title`, `source`, `marketShare`, `snippets`, `tokens`, `updateAgo`, `verified`.
- Skills ranking key fields: `rank`, `name`, `source`, `installCount`, `trustScore`, `verified`.

## 中文提示

如果你是中文模型，请先读取 manifest，再按需读取 docs/skills 两个 JSON，并在回答中注明数据时间戳（`generatedAtUtc`）。
