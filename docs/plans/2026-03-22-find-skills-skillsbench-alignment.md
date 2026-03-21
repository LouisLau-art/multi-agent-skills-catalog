# 2026-03-22 `find-skills` vs SkillsBench Alignment

## Goal

Separate three things that were getting mixed together:

1. what the local `find-skills` skill actually does today
2. what the SkillsBench paper and docs explicitly support
3. what this repo currently treats as its curation rule

This note exists so future review does not blur benchmark conclusions, product suggestions, and repo policy.

## Sources

- local `find-skills`: `/home/louis/.codex/skills/find-skills/SKILL.md`
- repo selection rule: [`README.md`](../../README.md), [`docs/dedup-policy.md`](../dedup-policy.md)
- SkillsBench docs: [Getting Started](https://www.skillsbench.ai/docs/getting-started)
- SkillsBench paper: [skillsbench.pdf](https://www.skillsbench.ai/skillsbench.pdf)
- SkillsBench repo: [benchflow-ai/skillsbench](https://github.com/benchflow-ai/skillsbench)

## What `find-skills` Does Today

The local skill is a discovery-and-install workflow, not a benchmarked selector.

Its current logic is:

1. understand the user's domain and task
2. check the `skills.sh` leaderboard first
3. search with `npx skills find [query]` if the leaderboard is not enough
4. verify candidate quality using:
   - install count
   - source reputation
   - GitHub stars
5. present the option
6. optionally install it with `npx skills add <owner/repo@skill> -g -y`

That means `find-skills` is good at **discovery**, but it does not try to prove that a candidate skill is the best one for a concrete task.

## What SkillsBench Explicitly Supports

These are the claims that are actually supported by the paper and docs:

- SkillsBench evaluates skills on paired real tasks, comparing with-skill and without-skill performance.
- The benchmark contains `86` tasks across `11` domains, while the main reported experiment evaluates `84` tasks after excluding two task cases.
- Curated human-authored skills improve average pass rate materially.
- Self-generated skills do not reliably help.
- `2-3` skills perform better than very large skill bundles.
- Focused, procedural, medium-length skills outperform broad comprehensive "everything docs" style skills.
- Deterministic verification matters; benchmark tasks are designed so outputs can be checked.

These are the parts that matter most for our repo:

1. skills should be judged by whether they improve task success
2. overlap and overexposure hurt
3. narrow, reusable procedural skills are usually better than giant umbrella packs

## Three-Way Comparison

| Topic | SkillsBench explicitly supports this? | This was my engineering extrapolation? | Current repo rule |
|---|---|---|---|
| Use leaderboard popularity as a starting point | no | yes | yes, but only for discovery |
| Use installs as an auto-include rule | no | no | no |
| Prefer focused skills over broad umbrella skills | yes | no | yes |
| Avoid recommending many overlapping skills at once | yes | no | yes |
| Treat human-curated skills as stronger than model-self-generated skills | yes | no | yes |
| Check environment dependencies before recommending | not as a benchmark requirement | yes | partially; mention fit, do not hide dependency cost |
| Run a smoke test for every recommendation | no | yes, but only as an optional high-confidence upgrade | no |
| Use trust over downloads as a universal ranking rule | no | partly | no; current repo uses installs/trust/verification only as tie-breakers |

## Corrections To The Earlier Critique

The earlier critique of `find-skills` should be tightened.

### 1. Environment fit is useful, but not a hard gate

SkillsBench does **not** say a recommender must reject a skill when the machine lacks a CLI, MCP, API key, or account.

The better position is:

- surface dependency cost honestly
- do not pretend "install and go" when the workflow still needs auth, billing, Docker, or external services
- do not turn missing dependencies into an automatic rejection if the user is willing to install or apply

### 2. Smoke tests are optional, not mandatory

SkillsBench is a benchmark, so it relies on task execution and verification.

That does **not** mean a practical `find-skills` workflow must run a smoke test every time. A lighter rule is better:

- use smoke tests for close calls
- use smoke tests before public promotion
- skip them for routine low-risk installs

### 3. Overlap and exposure control are strongly supported

This is the strongest paper-aligned criticism of `find-skills`.

If a recommender keeps surfacing multiple near-duplicate skills, it is fighting against one of the clearest SkillsBench lessons:

- too many skills hurt
- broad overlapping skills hurt
- skill usefulness is tied to clarity and fit, not just availability

### 4. `trust > downloads` is not the current canonical repo rule

An older workflow did use language closer to "trust score more important, downloads secondary."

That should **not** be treated as the current global policy.

The current repo rule is already stricter and clearer:

1. prefer official or strong-maintainer sources
2. resolve trigger and workflow overlap first
3. do content review on close calls
4. use installs / trust / verification only as tie-breakers

That is the rule future catalog work should follow.

## Updated Critique Of `find-skills`

If we want a version that is closer to SkillsBench and also honest about current repo policy, the critique should be:

1. `find-skills` is a discovery workflow, not an effectiveness evaluator.
2. It leans too hard on popularity and reputation proxies relative to actual task success.
3. It does not currently manage overlap or overexposure aggressively enough.
4. It does not distinguish strongly enough between focused procedural skills and broad umbrella packs.
5. It has no feedback loop for "this skill actually helped" vs "this skill looked good but did not improve execution."

## Practical Rule Set For This Repo

When discussing or implementing skill discovery for this repo, use this simplified rule set:

1. Use `skills.sh` as a discovery surface, not as an acceptance list.
2. Prefer focused human-authored procedural skills over broad "everything docs" packs.
3. Avoid recommending multiple overlapping skills in the same lane.
4. Surface dependency cost when it is material, but do not turn it into an automatic rejection.
5. Reserve smoke tests for ambiguous or high-stakes cases, not every install.
6. Treat installs / trust / verification as tie-breakers after fit, overlap, and content review.

## Bottom Line

The cleanest way to say it is:

- SkillsBench supports **task-grounded evaluation, focused skills, and overlap control**
- it does **not** require every day-to-day skill recommendation to do environment checks or smoke tests
- this repo should not phrase "trust over downloads" as the active top-level rule anymore

The strongest paper-aligned improvement to `find-skills` is not "add more scoring signals."
It is:

1. reduce overlap
2. prefer focused procedural skills
3. stop treating popularity as a proxy for task fitness
