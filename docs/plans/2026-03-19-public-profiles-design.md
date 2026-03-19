# Public Profiles Design

## Context

This repository currently does three jobs at once:

1. It maintains a curated public skills list.
2. It provides install and sync tooling for multiple agents.
3. It publishes ranking and curation research via GitHub Pages.

That is workable, but the product story is still muddy. The current structure centers on a single curated pack (`skills_selected.txt` + `skills_manifest.csv`), while the real local workspace already contains many more skills than the public set.

As of 2026-03-19:

- public curated repo set: `120`
- local Codex user skills: `187`

Blindly syncing the entire local workspace into the public repo would lower signal quality. Many local skills are situational, experimental, overlapping, or tuned for one operator rather than broad public use.

## Goals

- Reposition the repo as a **public multi-agent skills distribution repo**.
- Keep the repo installable by other people without requiring them to understand the maintainer's personal workspace.
- Replace the “one big selected pack” mental model with **small public profiles**.
- Preserve compatibility for existing users of the current curated pack.
- Support a private local overlay for the maintainer without forcing it into the public product.

## Non-Goals

- Publishing every locally installed skill.
- Vendoring third-party `SKILL.md` files into the repo.
- Building a full marketplace taxonomy.
- Auto-classifying every skill using embeddings or LLM-generated tags.

## Approaches

### Option A: Keep a single public curated pack

Keep the current `skills_selected.txt` / `skills_manifest.csv` model and only improve documentation.

Pros:
- Lowest implementation cost.
- No installer redesign.

Cons:
- Public users still do not know which subset to install for their use case.
- The pack will keep drifting toward a grab bag.
- The repo positioning remains unclear.

### Option B: Mirror the local workspace into the public repo

Treat the local `~/.codex/skills` state as the public truth and sync it into repo manifests.

Pros:
- Easy to explain for one maintainer.
- Little classification work.

Cons:
- Public pack quality collapses.
- Too many one-off or overlapping skills become “official.”
- Makes the repo less useful to outsiders.

### Option C: Recommended — Public profiles + private overlay

Split the model into:

- **Public catalog**: reusable skills suitable for distribution.
- **Public profiles**: scenario-based install bundles built from that catalog.
- **Private overlay**: local-only additions kept outside the public product surface.

Pros:
- Clear public positioning.
- Easy onboarding for new users.
- Scales better than a single monolithic pack.
- Lets the maintainer keep a larger private workspace without polluting the public product.

Cons:
- Requires profile design and installer changes.
- Requires more explicit curation policy.

## Recommendation

Adopt **Option C**.

This repository should be positioned as:

> A public, multi-agent, curated skills distribution repo with a small default baseline, optional scenario-based profiles, and support for private local overlays.

The public repo is the product. The local workspace is an operator environment. They should overlap, but they should not be identical.

## Information Architecture

### 1. Public Catalog

Keep `skills_manifest.csv` as the canonical public catalog.

Meaning:
- every row is a skill that is eligible for public distribution
- catalog rows are not all “default install”
- catalog rows must pass public curation rules

### 2. Public Profiles

Add a `profiles/` directory with small text manifests per use case.

Initial profile set:

- `core-meta`
- `development-core`
- `writing-blog`
- `resume-job-search`
- `docs-office`
- `cloud-platform`
- `design-ui`
- `database-data`

Derived aliases:

- `public-default = core-meta + development-core`
- `all-public = union of all public profiles`

### 3. Compatibility Export

Keep `skills_selected.txt`, but redefine it as a **compatibility export of `all-public`** rather than “the one true default pack.”

This preserves existing scripts and docs while allowing the product to evolve toward profiles.

### 4. Private Overlay

Support a git-ignored local layer, for example:

- `profiles.local/*.txt`
- or equivalent local-only manifest files

Rules:
- local overlay never changes public counts by default
- local overlay can be installed and synced locally
- promotion into public catalog requires explicit review

## Public Profile Principles

Profiles should be:

- small enough to understand in one glance
- additive rather than mutually exclusive
- organized by real user jobs, not by repo source
- stable enough to document publicly

Profiles are not:

- a dump of everything related to a theme
- a strict taxonomy of all skills on the market
- automatically derived from `skills.sh`

## Initial Profile Intent

### `core-meta`

Must-have workflow and discovery layer for most users.

Expected examples:
- Context7 lookup
- skills discovery
- verification / review checkpoints
- session continuity utilities

### `development-core`

Default software development workflow pack.

Expected examples:
- architecture / backend / frontend / testing baseline
- git workflow
- planning / debugging
- common framework essentials

### `writing-blog`

Blogging and public technical writing.

Expected examples:
- technical blog writing
- long-form post writing
- content strategy
- writing workflow support

### `resume-job-search`

Resume and job-market packaging.

Expected examples:
- resume builder
- tailored resume generation
- ATS optimization
- bullet writing

### `docs-office`

Document handling and deliverables.

Expected examples:
- pdf
- docx
- pptx
- markitdown

### `cloud-platform`

Cloud deployment and platform operations for public-friendly stacks.

Expected examples:
- deploy-to-vercel
- github-actions-templates
- wrangler
- selected AWS / Azure starter skills
- Hugging Face / Supabase skills where they fit platform workflows

### `design-ui`

UI implementation and design-heavy work.

### `database-data`

Database, query, and data workflow support.

## Promotion Rules from Local Workspace

When deciding whether a local-only skill should move into the public catalog:

Promote if it is:
- reusable by outsiders
- low-conflict
- clearly scoped
- backed by a credible source
- useful in at least one public profile

Keep local-only if it is:
- experimental
- highly personal
- too meta
- too broad
- too tightly coupled to one agent ecosystem

Reject if it causes:
- trigger conflict with a stronger existing skill
- major workflow overlap without clearer scope
- poor source quality

## Installer UX

Move from “single pack install” to “target + profiles”.

Recommended public UX:

```bash
python scripts/install_curated.py claude --profiles public-default
python scripts/install_curated.py claude --profiles core-meta+writing-blog
python scripts/install_curated.py all --profiles public-default+cloud-platform
python scripts/install_curated.py codex --profiles resume-job-search
```

This keeps:
- agent target selection
- profile selection

as separate concepts.

## Documentation Impact

README and site should answer these questions immediately:

1. What is this repo for?
2. Which profile should I install first?
3. Which profile fits my task?
4. How is the public repo different from the maintainer's local workspace?

## Migration Strategy

### Phase 1

- keep current catalog intact
- introduce profiles without breaking existing installer behavior
- define `public-default`

### Phase 2

- reframe README and site around profiles
- treat `skills_selected.txt` as compatibility export

### Phase 3

- gradually promote selected local-only skills into public profiles
- keep private overlay outside the public contract

## Decision

Proceed with:

- public repo as the primary product
- public profiles as the primary install model
- small default baseline plus optional add-on profiles
- private local overlay as a separate, non-public layer
