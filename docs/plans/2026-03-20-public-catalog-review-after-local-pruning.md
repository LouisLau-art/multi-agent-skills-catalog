# Public Catalog Review After Local Pruning

## Snapshot

Current verified state on `2026-03-20`:

- local Codex default set: `93` skills (excluding `.system`)
- public catalog (`skills_manifest.csv`): `123` skills
- public compatibility export (`skills_selected.txt`): `123` skills
- public profile union: `123` skills
- default public install (`public-default = core-meta + development-core`): `77` skills

This confirms the current repo is already operating as:

- **public catalog**
- **public profiles**
- **private local workspace**

That is the correct product direction. The local `93` should **not** be mirrored directly into the public catalog.

## Main Finding

The public repo does not need a wholesale rewrite. The real problem is narrower:

1. some public profiles still carry broad, overlapping, or project-bound skills that were intentionally removed from the local default set
2. a few high-value modern skills that survived local pruning are missing from the public catalog
3. some profile compositions no longer match their stated job-to-be-done

So the right move is **selective public review**, not “sync local 93 into public 123”.

## Diff Summary

### Local Active But Not Public (`16`)

These are active in `~/.codex/skills` but absent from `skills_manifest.csv`:

- `bash-defensive-patterns`
- `better-auth`
- `bun-next-js`
- `dispatching-parallel-agents`
- `gemini`
- `gemini-api-dev`
- `hybrid-search-implementation`
- `instructor`
- `prompt-engineering-patterns`
- `react-19`
- `resume-ats-optimizer`
- `resume-bullet-writer`
- `self-improvement`
- `subagent-driven-development`
- `tanstack-query-best-practices`
- `writing-skills`

### Public But Not Local (`46`)

These remain in the public catalog but are no longer in the local default set:

- `ai-elements`
- `backend-patterns`
- `backtesting-frameworks`
- `better-auth-best-practices`
- `canvas-design`
- `claude-automation-recommender`
- `claude-opus-4-5-migration`
- `coding-standards`
- `content-strategy`
- `context7-mcp`
- `convex-best-practices`
- `create-auth-skill`
- `dotnet-backend-patterns`
- `e2e-testing-patterns`
- `frontend-patterns`
- `frontend-testing`
- `gsap`
- `implement-design`
- `internal-comms`
- `laravel`
- `motion`
- `nuxt`
- `nuxt-better-auth`
- `nuxt-ui`
- `polars`
- `postgresql-table-design`
- `react-modernization`
- `redis-js`
- `remotion-best-practices`
- `send-email`
- `senior-architect`
- `senior-backend`
- `senior-computer-vision`
- `senior-data-engineer`
- `senior-data-scientist`
- `senior-ml-engineer`
- `senior-prompt-engineer`
- `senior-security`
- `sql-optimization-patterns`
- `stripe-best-practices`
- `stripe-integration`
- `svelte-code-writer`
- `ui-design-system`
- `ux-researcher-designer`
- `vue`
- `web-artifacts-builder`

## High-Confidence Conclusions

### Keep Public Even If Not Local

These do **not** need to be in the maintainer’s default daily workspace, but still make sense in a public distribution repo:

- `ai-elements`
  - strong, clear library-specific value for public AI UI work
  - better fit for public `design-ui` than for local default coding context
- `context7-mcp`
  - very strong public install story
  - belongs in `context7-integration` even if not needed in the local default skill set
- `send-email`
  - public-facing product builders routinely need email workflows
  - valid optional public profile member even if low-frequency locally
- `stripe-integration`
  - same logic as `send-email`
  - strong public utility for SaaS and indie-product users

### Promote From Local To Public

These are the strongest current promotion candidates:

- `better-auth`
  - better modern “single library truth” than the current fragmented `better-auth-best-practices` + `create-auth-skill` pair
- `gemini-api-dev`
  - specific, current, public-facing API skill
  - better public value than the generic local `gemini` CLI wrapper
- `resume-ats-optimizer`
  - should be in `resume-job-search`
  - it covers a real step in the resume pipeline that the public profile currently misses
- `resume-bullet-writer`
  - also belongs in `resume-job-search`
  - it complements `resume-builder` and `tailored-resume-generator`

### Demote From Public Catalog

These are the highest-confidence removal candidates from the public catalog itself, not just from local defaults:

- `frontend-testing`
  - explicitly bound to the Dify frontend project
  - not appropriate as a general public catalog item
- `internal-comms`
  - explicitly written around company-internal update formats
  - poor fit for a public distribution repo
- `coding-standards`
  - too generic
  - weak procedural value relative to overlap noise
- `backend-patterns`
  - broad overlap with stronger kept backend and architecture skills
- `frontend-patterns`
  - broad overlap with stronger React/Next/frontend skills
- `better-auth-best-practices`
  - fragmented partial sub-skill
  - should be replaced by `better-auth` if promoted
- `create-auth-skill`
  - same issue as above
  - creates auth-trigger fragmentation instead of clarity

## Medium-Confidence Re-Review Cluster

These should be revisited in a second pass, but not mixed into the first patch set:

- broad senior/role skills:
  - `senior-architect`
  - `senior-backend`
  - `senior-prompt-engineer`
  - `senior-security`
  - `senior-data-engineer`
  - `senior-data-scientist`
  - `senior-ml-engineer`
- vertical or specialized domain skills:
  - `backtesting-frameworks`
  - `senior-computer-vision`
  - `dotnet-backend-patterns`
  - `laravel`
  - `svelte-code-writer`
  - `vue`
  - `nuxt`
  - `nuxt-better-auth`
  - `nuxt-ui`
- design/artifact edge cases:
  - `web-artifacts-builder`
  - `ui-design-system`
  - `ux-researcher-designer`
  - `canvas-design`
  - `motion`
  - `gsap`
  - `remotion-best-practices`

These are not necessarily wrong for the public repo, but they require product judgment rather than simple cleanup.

## Profile-Specific Issues

### `development-core`

This profile is currently too broad for something named “core”.

Most obvious mismatches:

- `backend-patterns`
- `coding-standards`
- `frontend-patterns`
- `frontend-testing`
- `better-auth-best-practices`
- `create-auth-skill`
- `backtesting-frameworks`

It also still carries several broad “senior-*” personas that likely deserve a second-pass review.

### `resume-job-search`

This profile is currently missing two important practical steps:

- `resume-ats-optimizer`
- `resume-bullet-writer`

At the same time, it still includes `internal-comms`, which is not a good fit for the profile’s stated purpose.

### `writing-blog`

`internal-comms` does not belong here.  
It mixes public writing/blogging with company-internal communication templates.

### `docs-office`

Also should not contain `internal-comms`.  
The rest of the profile has a clean office/document-tools story without it.

## Recommended Round A Patch Set

Do **not** apply broad product-policy changes first. Start with the highest-confidence patch set:

### Add

- `better-auth`
- `gemini-api-dev`
- `resume-ats-optimizer`
- `resume-bullet-writer`

### Remove

- `frontend-testing`
- `internal-comms`
- `coding-standards`
- `backend-patterns`
- `frontend-patterns`
- `better-auth-best-practices`
- `create-auth-skill`

### Profile Adjustments

- add `resume-ats-optimizer` to `resume-job-search`
- add `resume-bullet-writer` to `resume-job-search`
- add `better-auth` to `development-core`
- add `gemini-api-dev` to `cloud-platform`
- remove `internal-comms` from:
  - `resume-job-search`
  - `writing-blog`
  - `docs-office`

## Expected Round A Impact

If only the Round A patch set is applied:

- public catalog: `123 -> 120`
- `development-core`: `62 -> 57`
- `resume-job-search`: `8 -> 9`
- `writing-blog`: `10 -> 9`
- `docs-office`: `9 -> 8`
- `cloud-platform`: `8 -> 9`
- `public-default`: `77 -> 72`

This would make the public repo tighter without collapsing its product breadth.

## Recommended Next Step

Proceed in this order:

1. apply **Round A** only
2. regenerate/verify:
   - `skills_selected.txt`
   - public profile counts
   - README count text
3. dry-run installer for:
   - `public-default`
   - `resume-job-search`
   - `public-default+cloud-platform`
4. only then start a second-pass review on the medium-confidence cluster

This keeps the public repo moving toward a cleaner product surface without overfitting it to the maintainer’s local `93`.
