## [LRN-20260320-001] correction

**Logged**: 2026-03-20T00:00:00+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Local skill pruning should remove broad overlap-heavy skills before narrow low-trigger niche utilities.

### Details
During local Codex skill pruning, `algorithmic-art` and `slack-gif-creator` were removed in the same wave as broader data/ML skills. User feedback clarified that this drifted from the intended pruning principle. Those two skills are niche and low-frequency, but they are also narrow and unlikely to create routing noise. The better deletion targets are broad umbrella skills, duplicated trigger surfaces, or skills misaligned with the current environment.

### Suggested Action
When pruning the default local skill set, treat download/popularity as a weak signal. Prefer deleting broad senior/meta/umbrella skills, real overlaps, and environment-misaligned skills before deleting narrow specialized tools.

### Metadata
- Source: user_feedback
- Related Files: docs/plans/2026-03-19-local-skills-audit.md
- Tags: skills, pruning, correction, trigger-overlap

---

## [LRN-20260320-002] correction

**Logged**: 2026-03-20T11:00:32+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Skill pruning and public-catalog decisions must not default to a coding-first view of agent capability.

### Details
User clarified that agent value extends well beyond coding. In this repo, skill selection should account for research, writing, product thinking, internal/external communication, content workflows, and artifact production, rather than treating non-coding skills as inherently lower-value. Deletions should be justified by overlap, environmental mismatch, or poor fit to the intended default set, not by an implicit assumption that code-oriented skills matter more.

### Suggested Action
When reviewing future pruning waves or public-catalog changes, explicitly separate "broad but useful non-coding capability" from "true noise". Re-evaluate borderline removals like blog/artifact/content skills through an agent-capability lens, not only a software-engineering lens.

### Metadata
- Source: user_feedback
- Related Files: docs/plans/2026-03-19-local-skills-audit.md, docs/plans/2026-03-20-public-catalog-review-after-local-pruning.md
- Tags: skills, pruning, correction, agents, non-coding

---
