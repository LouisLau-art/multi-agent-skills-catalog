# 2026-03-21 Blog Post Rewrite Review

## Goal

Decide whether `blog-post` should be rewritten and eventually promoted into the public catalog, now that `technical-blog-writing` already covers the technical/developer-content lane.

## Current Situation

The old `blog-post` skill was removed from the local default set for two good reasons:

1. it depended on a non-portable research contract (`task` with `subagent_type="researcher"`)
2. it depended on a non-portable cover-image contract (`generate_cover`)

Those were strong reasons to remove it from the tiny local default set, but they are **not** strong reasons to permanently reject the capability.

## What The Old Skill Actually Did

The old skill bundled four things together:

1. long-form blog structure
2. mandatory delegated research
3. mandatory output folder structure (`blogs/<slug>/post.md`)
4. mandatory hero image generation (`blogs/<slug>/hero.png`)

The packaging was too rigid. The underlying capability is still valid.

## Overlap Boundary With `technical-blog-writing`

Now that `technical-blog-writing` is already public in `writing-blog`, `blog-post` should **not** be promoted as a second generic writing skill that triggers on the same developer-content requests.

The clean boundary is:

- `technical-blog-writing`
  - developer-facing posts
  - tutorials, architecture posts, benchmarks, engineering explainers
  - code examples and technical credibility
  - relies on `infsh`-style research and asset generation workflows

- `blog-post` (if rewritten)
  - broader long-form publishing workflow
  - idea framing, hook, narrative structure, CTA, packaging
  - can support thought leadership, opinion pieces, product announcements, broad educational articles
  - should not require developer-specific code examples to be useful

In other words: `technical-blog-writing` should own the **developer-content** lane; `blog-post` should only come back if it is rewritten into a more **general publishing workflow**.

## Rewrite Recommendation

If `blog-post` is rewritten, it should change in these ways:

### 1. Remove agent-specific research requirements

Replace:

- mandatory `task(subagent_type="researcher")`

With:

- “Research first using whatever research tools are available”
- optional delegation if the host agent supports subagents
- no hard-coded required save path

### 2. Make cover generation optional

Replace:

- mandatory `generate_cover`
- “blog post is not complete without its cover image”

With:

- optional hero/cover asset generation
- allow the post to be considered complete without generated media
- if image tooling exists, suggest a hero asset as an enhancement rather than a hard requirement

### 3. Loosen output path assumptions

Replace:

- required `blogs/<slug>/post.md`

With:

- recommended output structure only
- allow the host repo or user to decide final location

### 4. Narrow the trigger surface

Replace:

- generic “technical writeup, tutorial, article, long-form content”

With:

- broader editorial / product / narrative blog scenarios
- avoid stepping on `technical-blog-writing`

## Recommended New Positioning

If rewritten, the skill should be described more like:

> “Plan and draft polished long-form blog posts for publication, including hooks, narrative flow, section structure, CTA, and optional packaging assets. Best for general blog posts, product thought pieces, announcements, educational articles, and broader content workflows.”

That positioning keeps it useful without duplicating the technical-writing lane.

## Public Catalog Decision

Current recommendation:

- do **not** promote the old `blog-post` as-is
- do **not** add it to `writing-blog` yet
- keep it in `candidate-restore-or-rewrite`
- only reconsider promotion after the rewrite is complete

## Acceptance Criteria For Future Promotion

Before `blog-post` is added to the public catalog, it should satisfy all of the following:

- no hard dependency on `task` researcher delegation
- no hard dependency on `generate_cover`
- post output can stand alone without hero image generation
- role and triggers are clearly differentiated from `technical-blog-writing`
- wording is agent-neutral and portable across Codex / Claude / Gemini style hosts

## Conclusion

`blog-post` is still a real capability, but the old version is too environment-bound and overlaps too much with the newly promoted `technical-blog-writing`.

The right move is not “promote now,” but “rewrite first, then reconsider.”
