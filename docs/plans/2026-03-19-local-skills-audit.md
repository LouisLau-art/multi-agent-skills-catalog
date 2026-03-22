# Local Skills Audit

**Scope:** `/home/louis/.codex/skills`

**Current local count:** `92` (excluding `.system`)

**Goal:** Reduce local skill overload by applying the current curation rules derived from recent skill-selection research and our repo policy:

- prefer focused, procedural skills
- avoid broad trigger overlap
- avoid multiple skills competing for the same request surface
- treat installs and name similarity as weak signals
- prefer skills that reduce verification and execution failure

## Why This Audit Exists

The local workspace grew to nearly 200 skills. That creates three problems:

1. more descriptions loaded into context
2. more trigger conflicts between similar skills
3. more “meta noise” relative to real task execution

The objective is not to minimize the count blindly. The objective is to keep the **right** skills.

## Audit Method

This first pass focuses on high-overlap clusters:

- `shadcn`
- `context7`
- `testing`
- `review/git`

This document started as a pre-deletion audit. The first wave has now been executed.

## Execution Status

**Completed first wave on:** `2026-03-19`

Removed from `~/.codex/skills` and synced with `--prune` to all managed agent directories:

- `shadcn-ui`
- `documentation-lookup`
- `playwright-best-practices`
- `code-review`

Post-sync directories now align at `182` user skills:

- `~/.codex/skills`
- `~/.claude/skills`
- `~/.gemini/skills`
- `~/.qwen/skills`
- `~/.config/opencode/skills`
- `~/.config/agents/skills`
- `~/.codebuddy/skills`

**Completed second wave on:** `2026-03-19`

Removed from `~/.codex/skills` and synced with `--prune` to all managed agent directories:

- `context7`
- `context7-mcp`

Rationale:

- `context7-docs-lookup` remains the best Codex-native docs lookup path
- `find-docs` remains the best cross-agent CLI fallback
- `context7` was only a lower-level curl fallback with weaker marginal value
- local `context7-mcp` content was effectively a renamed duplicate of `context7-docs-lookup`, not a distinct MCP setup workflow

Post-sync directories now align at `180` user skills:

- `~/.codex/skills`
- `~/.claude/skills`
- `~/.gemini/skills`
- `~/.qwen/skills`
- `~/.config/opencode/skills`
- `~/.config/agents/skills`
- `~/.codebuddy/skills`

**Recount correction on:** `2026-03-20`

- A direct recount before wave 10 showed the pre-wave-10 local baseline after wave 9 was `158`, not `159`.
- The off-by-one started in wave 7: wave 6 ended at `170`, and removing two skills should have produced `168`.
- Current downstream counts are now verified directly instead of inferred from the earlier running totals.

---

## Cluster 1: shadcn

### Skills found

- `shadcn`
- `shadcn-ui`
- `tailwind-v4-shadcn`

### Assessment

- `shadcn` is the strongest default choice.
  It is focused around the real CLI and project context, and it aligns with current component-registry workflows.
- `shadcn-ui` is broader and overlaps heavily with `shadcn`.
- `tailwind-v4-shadcn` still has value, but only when the repo is explicitly using Tailwind v4 and shadcn together.

### Recommendation

- **Keep:** `shadcn`
- **Conditional keep:** `tailwind-v4-shadcn`
- **First-wave removal candidate:** `shadcn-ui`

---

## Cluster 2: Context7

### Skills found

- `context7`
- `context7-docs-lookup`
- `context7-mcp`
- `find-docs`
- `documentation-lookup`

### Assessment

- `context7-mcp` is not a query skill; it is an integration/setup skill. It should be evaluated separately from docs-query skills.
- `context7-docs-lookup` is the best fit for Codex-native Context7 tool usage.
- `find-docs` is still useful as a cross-agent CLI fallback.
- `documentation-lookup` overlaps almost completely with `context7-docs-lookup`.
- `context7` (direct HTTP API via curl) is a pragmatic fallback, but its role becomes weaker once MCP is installed and stable everywhere.

### Recommendation

- **Keep:** `context7-mcp`
- **Keep:** `context7-docs-lookup`
- **Conditional keep:** `find-docs` if cross-agent CLI fallback is still desired
- **First-wave removal candidate:** `documentation-lookup`
- **Second-wave review candidate:** `context7`

---

## Cluster 3: testing

### Skills found

- `e2e-testing-patterns`
- `playwright-best-practices`
- `webapp-testing`

### Assessment

- `e2e-testing-patterns` provides general testing principles and standards.
- `webapp-testing` is execution-oriented and useful for actually interacting with local apps.
- `playwright-best-practices` is extremely broad and overlaps with both of the above.

### Recommendation

- **Keep:** `e2e-testing-patterns`
- **Keep:** `webapp-testing`
- **First-wave removal candidate:** `playwright-best-practices`

---

## Cluster 4: review and git workflow

### Skills found

- `code-review`
- `code-reviewer`
- `gh-cli`
- `git-commit`
- `github-actions-templates`
- `using-git-worktrees`
- `requesting-code-review`
- `receiving-code-review`
- `finishing-a-development-branch`

### Assessment

- The workflow-oriented set is good and relatively well-separated:
  - `git-commit`
  - `using-git-worktrees`
  - `requesting-code-review`
  - `receiving-code-review`
  - `finishing-a-development-branch`
- `gh-cli` and `github-actions-templates` remain useful as targeted GitHub skills.
- `code-reviewer` is the better automated review skill.
- `code-review` is weak, generic, and redundant.

### Recommendation

- **Keep:** `gh-cli`, `git-commit`, `github-actions-templates`, `using-git-worktrees`, `requesting-code-review`, `receiving-code-review`, `finishing-a-development-branch`, `code-reviewer`
- **First-wave removal candidate:** `code-review`

---

## First-Wave Removal Candidates

These are the strongest current candidates for safe pruning:

- `shadcn-ui`
- `documentation-lookup`
- `playwright-best-practices`
- `code-review`

**Status:** completed

## Second-Wave Review Candidates

These were the follow-up review items after the first wave:

- `context7`
- `tailwind-v4-shadcn`

### Second-wave outcome

- `context7`: removed
- `tailwind-v4-shadcn`: kept

Reason for keeping `tailwind-v4-shadcn`:

- `scholar-flow/frontend` currently uses `tailwindcss@4.2.1`
- the project also uses shadcn
- this makes the skill a real project-specific asset rather than a theoretical duplicate

## Suggested Next Step

The next pass should focus on narrower local-only cleanup:

1. inspect whether any still-installed generic advisor or toolkit skills have weak trigger discipline
2. re-check writing/blog clusters only after current blogging work is further along
3. avoid touching repo public catalog unless a local-only decision clearly generalizes

---

## Wave 3: Generic / Toolkit / Advisor / Senior

**Completed third wave on:** `2026-03-19`

Removed from `~/.codex/skills` and synced with `--prune` to all managed agent directories:

- `template-skill`
- `content-creator`
- `social-media-analyzer`

Post-sync directories now align at `177` user skills:

- `~/.codex/skills`
- `~/.claude/skills`
- `~/.gemini/skills`
- `~/.qwen/skills`
- `~/.config/opencode/skills`
- `~/.config/agents/skills`
- `~/.codebuddy/skills`

### Keep

| Skill | Bucket | Why keep it |
|---|---|---|
| `claude-automation-recommender` | advisor/meta | Distinct value for Claude Code automation planning; not redundant with architecture or docs skills. |
| `senior-architect` | senior | Broad, but still the clearest umbrella for system design and dependency trade-offs. |
| `senior-backend` | senior | Useful fallback for API/database work when the narrower backend skills do not fully cover a case. |
| `senior-security` | senior | Distinct security domain; the overlap cost is lower than the risk of losing a dedicated security umbrella. |
| `senior-prompt-engineer` | senior | Still useful for prompt design, token budgeting, and agent workflow tuning. |

### Delete

| Skill | Bucket | Why it is a low-risk delete candidate |
|---|---|---|
| `template-skill` | generic | Placeholder scaffold rather than a real skill; no unique workflow value. |
| `content-creator` | toolkit | Broad marketing-content umbrella that overlaps heavily with `content-strategy`, `technical-blog-writing`, and `blog-post`. |
| `social-media-analyzer` | toolkit | Narrow marketing analytics skill with weak relevance to the current workstreams and no strong trigger advantage. |

**Status:** completed

---

## Wave 4: Umbrella / Meta / Wide-Trigger

**Completed fourth wave on:** `2026-03-19`

Removed from `~/.codex/skills` and synced with `--prune` to all managed agent directories:

- `senior-frontend`
- `senior-fullstack`
- `senior-qa`

Post-sync directories now align at `174` user skills:

- `~/.codex/skills`
- `~/.claude/skills`
- `~/.gemini/skills`
- `~/.qwen/skills`
- `~/.config/opencode/skills`
- `~/.config/agents/skills`
- `~/.codebuddy/skills`

### Keep

| Skill | Bucket | Why keep it |
|---|---|---|
| `claude-automation-recommender` | advisor/meta | Still useful for Claude Code automation planning; it is opinionated but not redundant with architecture or docs helpers. |
| `dispatching-parallel-agents` | process | Narrow orchestration helper for parallel independent work; operationally distinct from the umbrella skills under review. |
| `subagent-driven-development` | process | Useful for independent implementation plans with review gates; helps coordinate work without being a generic umbrella. |
| `systematic-debugging` | process | Strong root-cause discipline and a good guardrail before fixes. |
| `test-driven-development` | process | Keeps implementation disciplined; narrower and more actionable than the senior QA umbrella. |
| `verification-before-completion` | process | Directly reduces false-completion risk and stays useful across every repo. |
| `requesting-code-review` | process | A clear workflow checkpoint, not a broad umbrella. |
| `receiving-code-review` | process | Complements review requests and avoids blind agreement. |
| `writing-plans` | process | Keeps multi-step work structured; useful despite being broad because it creates execution clarity. |
| `frontend-patterns` | frontend | Specific enough to keep as a practical frontend reference. |
| `react-dev` | frontend | Focused on typed React work and narrower than `senior-frontend`. |
| `react-web` | frontend | Good for common React web patterns without the width of the senior umbrella. |
| `webapp-testing` | testing | Practical browser-level test helper with a concrete execution surface. |

### Delete

| Skill | Bucket | Why it is a low-risk delete candidate |
|---|---|---|
| `senior-frontend` | senior | Broad frontend umbrella that overlaps heavily with `frontend-patterns`, `react-dev`, `react-web`, `webapp-testing`, `web-design-guidelines`, `responsive-design`, and the Vercel-specific skills. |
| `senior-fullstack` | senior | Very wide fullstack umbrella; most of its daily value is already covered by narrower frontend, backend, QA, and workflow skills. |
| `senior-qa` | senior | Broad QA umbrella with substantial overlap against `test-driven-development`, `webapp-testing`, `frontend-testing`, `react-testing`, and `verification-before-completion`. |

**Status:** completed

### Observe

| Skill | Bucket | Why observe instead of deleting now |
|---|---|---|
| `using-superpowers` | meta | It is more of a global trigger policy than a task skill; noisy, but still serving as a front-door reminder until the loading story is simplified. |
| `tech-stack-evaluator` | evaluation | Useful for cloud/provider/TCO decisions, but it overlaps with `senior-architect` and is not a daily driver. |
| `monorepo-management` | tooling | Redundant with `turborepo` for most of the current workflow, but still useful if monorepo work expands again. |
| `web-component-design` | frontend | Good reusable-pattern reference, but it competes with narrower React and design-system helpers. |
| `vercel-react-best-practices` | frontend | Strong guidance, but broad enough to overlap with multiple narrower React and Next helpers. |
| `next-best-practices` | frontend | Valuable, but the repository already has narrower Next/React skills that handle most day-to-day cases. |
| `ui-dev` | frontend | Practical UI helper, but broad enough to compete with other frontend composition skills. |
| `ui-web` | frontend | Same issue as `ui-dev`; useful, but not clearly indispensable. |
| `react-state-management` | frontend | Helpful for store decisions, but it overlaps with React query/state guidance already present. |
| `frontend-testing` | testing | Project-specific testing helper that is useful when the target repo matches its conventions, but not a universal default. |

### Execution Recommendation

- This batch has now removed `senior-frontend`, `senior-fullstack`, and `senior-qa` together.
- Keep `using-superpowers` and `tech-stack-evaluator` in observe until we verify whether the remaining process skills already cover their useful edge cases.
- Do not delete the narrower frontend/testing process skills yet; they are more focused than the umbrella skills and still earn their keep.
- The parity sync across `~/.codex/skills`, `~/.claude/skills`, `~/.gemini/skills`, `~/.qwen/skills`, `~/.config/opencode/skills`, `~/.config/agents/skills`, and `~/.codebuddy/skills` has also been completed.

---

## Wave 5: Metadata / UI Umbrella / Context-Noise

**Completed fifth wave on:** `2026-03-19`

Removed from `~/.codex/skills` only. Per current user preference, this wave has **not** been synced yet to the other managed agent directories:

- `using-superpowers`
- `ui-dev`
- `ui-web`

Current local counts:

- `~/.codex/skills`: `171`
- `~/.claude/skills`: `174`
- `~/.gemini/skills`: `174`
- `~/.qwen/skills`: `174`
- `~/.config/opencode/skills`: `174`
- `~/.config/agents/skills`: `174`
- `~/.codebuddy/skills`: `174`

### Keep

| Skill | Why keep it |
|---|---|
| `tech-stack-evaluator` | Still useful for current cloud/provider evaluation work. It overlaps with `senior-architect`, but it remains more explicit on TCO, migration, and ecosystem comparison. |
| `monorepo-management` | Broader than `turborepo`, but still useful if the task is monorepo-wide and not strictly Turbo-specific. |

### Delete

| Skill | Why it was removed |
|---|---|
| `using-superpowers` | This is a global meta-trigger rule, not a task skill. Its instruction style is maximally broad and effectively says “trigger skills for nearly everything,” which increases activation noise. Since the environment already has a concrete skill inventory, agent-level instructions, and a more deliberate curation policy, its marginal value is now lower than its context/trigger cost. |
| `ui-dev` | Too broad and overlaps heavily with `shadcn`, `tailwind-v4-shadcn`, `frontend-design`, and `responsive-design`. It mixes dark theme, animations, responsive layout, and shadcn guidance into one wide trigger surface instead of staying narrowly procedural. |
| `ui-web` | Another broad UI guidance skill that overlaps with `web-design-guidelines`, `responsive-design`, and `frontend-design`. It is heavy on general design rules and accessibility reminders, but not specific enough to justify its own activation surface alongside the narrower UI skills already kept. |

### Observe

| Skill | Why observe instead of deleting now |
|---|---|
| `tech-stack-evaluator` | Active relevance because current work still includes cloud choice, ecosystem trade-offs, and cost questions. |
| `monorepo-management` | Some overlap with `turborepo`, but it remains the only generic monorepo umbrella left if the workflow expands beyond Turbo conventions. |

### Execution Note

- This wave intentionally stopped at Codex-only pruning.
- Cross-agent sync is deferred until a larger stable batch is complete.

---

## Wave 6: Monorepo / Tooling Specificity

**Completed sixth wave on:** `2026-03-19`

Removed from `~/.codex/skills` only. Per current user preference, this wave has **not** been synced yet to the other managed agent directories:

- `monorepo-management`

Current local counts:

- `~/.codex/skills`: `170`
- `~/.claude/skills`: `175`
- `~/.gemini/skills`: `175`
- `~/.qwen/skills`: `174`
- `~/.config/opencode/skills`: `175`
- `~/.config/agents/skills`: `174`
- `~/.codebuddy/skills`: `174`

### Keep

| Skill | Why keep it |
|---|---|
| `turborepo` | It is the narrower, more procedural version of the monorepo/tooling space. If monorepo work ever becomes real, this is the one that gives concrete `turbo` task, cache, and filter guidance rather than generic umbrella advice. |
| `tech-stack-evaluator` | Still relevant to current cloud/provider comparison work and broader than pure repo tooling. |

### Delete

| Skill | Why it was removed |
|---|---|
| `monorepo-management` | The active repos (`scholar-flow`, `multi-cloud-email-sender`, `LouisLau-art.github.io`) are not currently monorepos and do not contain `turbo.json`, `pnpm-workspace.yaml`, `nx.json`, or similar markers. The skill is broad, overlaps with `turborepo`, and has no immediate execution value in the current workspace. |

### Execution Note

- This was a low-risk delete because no current repo is using monorepo tooling.
- `turborepo` was kept as the narrower future-facing option.

---

## Wave 7: React / Next Overlap and Duplicate Guidance

**Completed seventh wave on:** `2026-03-19`

Removed from `~/.codex/skills` only. Per current user preference, this wave has **not** been synced yet to the other managed agent directories:

- `react-best-practices`
- `react-state-management`

Current local counts:

- `~/.codex/skills`: `168`
- `~/.claude/skills`: `175`
- `~/.gemini/skills`: `175`
- `~/.qwen/skills`: `174`
- `~/.config/opencode/skills`: `175`
- `~/.config/agents/skills`: `174`
- `~/.codebuddy/skills`: `174`

### Keep

| Skill | Why keep it |
|---|---|
| `vercel-react-best-practices` | This is the stronger and newer Vercel React/Next performance package. It keeps the same trigger surface as the removed duplicate but with a larger rule set and clearer metadata. |
| `next-best-practices` | Still useful because current active work includes real Next.js App Router code. |
| `nextjs-app-router-patterns` | More implementation-oriented App Router guidance than the broader best-practices package. |
| `tanstack-query` | Current active frontend work already uses `@tanstack/react-query`, so the dedicated query skill has direct execution value. |
| `tanstack-query-best-practices` | It complements the concrete TanStack Query skill with narrower cache/query-key/mutation guidance. |
| `react-dev` | Focused on typed React component and hook work; narrower than the removed state umbrella. |
| `react-web` | Still covers practical React web implementation patterns not limited to state tools. |

### Delete

| Skill | Why it was removed |
|---|---|
| `react-best-practices` | It is effectively an older duplicate of `vercel-react-best-practices`: same skill name in frontmatter, same trigger surface, same Vercel React/Next performance theme, but with a smaller 45-rule set compared with the kept 58-rule variant. Keeping both would create duplicate activation without adding a distinct workflow. |
| `react-state-management` | Too broad for the current workspace. It mixes Redux Toolkit, Zustand, Jotai, and React Query guidance into one umbrella skill, while the active frontend repo usage is specifically TanStack Query. That concrete need is already covered by `tanstack-query` and `tanstack-query-best-practices`, making this broader state package low-yield context overhead. |

### Execution Note

- This wave prioritized overlap and active usage over popularity.
- The current repos use Next.js and TanStack Query, but do not show real Redux/Zustand/Jotai usage, which is why the state umbrella was cut while the narrower query and Next skills stayed.

---

## Wave 8: Regulated / Mobile-Market / Compliance Outliers

**Completed eighth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. Per current user preference, this wave has **not** been synced yet to the other managed agent directories:

- `app-store-optimization`
- `capa-officer`
- `gdpr-dsgvo-expert`
- `information-security-manager-iso27001`
- `isms-audit-expert`
- `quality-documentation-manager`
- `risk-management-specialist`

Current local counts after this wave:

- `~/.codex/skills`: `161`
- `~/.claude/skills`: `169`
- `~/.gemini/skills`: `169`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `169`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `app-store-optimization` | This is a mobile growth/ASO skill for Apple App Store and Google Play metadata. It is far outside the current workspace, which is centered on web apps, backend engineering, cloud/runtime debugging, blogs, and resumes. |
| `capa-officer` | A medical-device CAPA/QMS workflow skill. It is highly domain-specific, unrelated to the user’s current engineering and job-search tasks, and brings a large specialized trigger surface with near-zero daily activation value. |
| `gdpr-dsgvo-expert` | A compliance automation package for GDPR/BDSG privacy programs. Useful in a privacy-consulting workflow, but not in the current day-to-day development/tooling/resume workflow, so its context cost outweighed its practical value. |
| `information-security-manager-iso27001` | An ISO 27001 healthcare/MedTech governance skill. It overlaps with broader security/architecture capabilities while pulling the local skill set toward audit/compliance work that the user is not actively doing. |
| `isms-audit-expert` | Another ISO 27001-focused audit skill. It is even narrower than `information-security-manager-iso27001`, making it a strong low-risk delete once the workspace is no longer centered on formal compliance operations. |
| `quality-documentation-manager` | Medical-device document-control/QMS workflow guidance. It is process-heavy and domain-heavy, but the current work already has more relevant doc skills (`doc-coauthoring`, `docx`, `internal-comms`) for actual writing tasks. |
| `risk-management-specialist` | ISO 14971 medical-device risk management. This is far removed from the current engineering repos and job-search focus, and it does not reduce any common failure mode in the current workload. |

### Execution Note

- This wave removed seven clearly off-track skills that were mostly coming from regulated-medical or mobile-market domains.
- The key principle was not “different domain means delete”; it was that these skills had weak relevance, high metadata noise, and no clear overlap with the user’s current active tasks.

---

## Wave 9: Executive / Strategy Umbrella Cleanup

**Completed ninth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave8/`

Removed skills:

- `ceo-advisor`
- `cto-advisor`
- `marketing-strategy-pmm`

Current local counts after this wave:

- `~/.codex/skills`: `158`
- `~/.claude/skills`: `169`
- `~/.gemini/skills`: `169`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `169`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `senior-architect` | Still the strongest general architecture/design fallback despite being broad. It remains closer to real engineering work than executive or PMM strategy skills. |
| `architecture-decision-records` | A narrow documentation skill with a very clear execution surface for technical decisions. |
| `tech-stack-evaluator` | Still relevant when comparing providers, frameworks, and cloud stacks; narrower and more directly useful than CTO/CEO strategy playbooks. |
| `product-manager-toolkit` | Broad, but still closer to practical feature framing, requirements, and discovery than executive-board or GTM strategy guidance. |
| `data-storytelling` | Still useful for turning real project evidence into blog, portfolio, or interview narratives. |

### Delete

| Skill | Why it was removed |
|---|---|
| `ceo-advisor` | This is a high-level executive management package for board governance, investor relations, and organizational strategy. It is far from the user’s current coding, debugging, and job-search workflow, and it has a very wide trigger surface for discussions that should not be routed through an executive-playbook skill. |
| `cto-advisor` | Although more technical than `ceo-advisor`, it still overlaps heavily with `senior-architect`, `architecture-decision-records`, and `tech-stack-evaluator`. It is a broad leadership umbrella covering team scaling, tech debt, and engineering metrics, while the kept skills provide narrower, more actionable guidance. |
| `marketing-strategy-pmm` | This is a go-to-market and positioning skill. It overlaps with `content-strategy` on the content side, but is much more sales/GTM oriented than the user’s current priorities of engineering delivery, blog writing, and resume packaging. |

### Execution Note

- This wave targeted skills that felt “senior-sounding” and impressive, but did not materially improve execution in the current workflow.
- The threshold was: if a skill mostly helps run a company, manage investors, or plan go-to-market, it should not stay in the default Codex local set unless the user is actively doing that work.

---

## Wave 10: Data / ML Umbrella and Creative Outlier Cleanup

**Completed tenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave10/`

Removed skills:

- `algorithmic-art`
- `nano-banana-prompting`
- `senior-data-scientist`
- `senior-ml-engineer`
- `slack-gif-creator`

Current local counts after this wave:

- `~/.codex/skills`: `153`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `senior-data-engineer` | It is still more procedural and narrower than the other data/ML umbrella skills. The trigger surface is tied to ETL/data-pipeline work rather than generic “world-class AI” positioning, so it is an observe/keep candidate rather than a default delete. |
| `rag-implementation` | This remains the narrower RAG-specific workflow for the user’s real LLM/app work and avoids the broad MLOps umbrella of `senior-ml-engineer`. |
| `langchain` | This is still a concrete framework skill with direct execution value for LLM application work, unlike the removed generic data/ML senior umbrella. |
| `langchain-architecture` | Keeps the agent/workflow architecture surface covered without needing the broader ML-engineering package. |
| `ai-sdk` | This is a more relevant day-to-day AI application skill for the current workspace than full model-serving or feature-store guidance. |
| `gemini-api-dev` | Keeps current Gemini integration guidance available without carrying unrelated image-prompt orchestration or MLOps overhead. |

### Delete

| Skill | Why it was removed |
|---|---|
| `senior-data-scientist` | It is another broad “senior” umbrella with generic analytics/ML/leadership coverage. The current local set already has narrower AI/LLM skills for actual execution, while the active repos do not center on experimentation platforms, causal inference programs, or production data-science org workflows. |
| `senior-ml-engineer` | It overlaps with narrower kept skills such as `rag-implementation`, `langchain`, `langchain-architecture`, `ai-sdk`, and `gemini-api-dev`, while also pulling in model serving, feature stores, and full MLOps concerns that are not part of the current day-to-day repos. |
| `algorithmic-art` | It is a highly specialized creative-artifact workflow with a large instruction body, Anthropic-specific viewer/template assumptions, and minimal relevance to the user’s current coding, tooling, transcript, and interview-packaging work. |
| `nano-banana-prompting` | This skill is both low-frequency and environment-misaligned: it explicitly depends on an `AskUserQuestion` tool and a `nano-banana` follow-up skill that are not present in the current local skill/tool inventory. |
| `slack-gif-creator` | This is a narrow media-asset utility for Slack GIF production. It has a low trigger rate in the current workflow and does not reduce any common engineering failure mode across the active repos. |

### Execution Note

- This wave intentionally removed only the strongest candidates from the reviewed cluster and left `senior-data-engineer` in place for now because it is narrower and more procedural than the deleted senior data/ML skills.
- After wave 10, the live local-vs-downstream drift is now the 15-skill set from waves 8, 9, and 10. Earlier wave-5-to-wave-7 drift is no longer present in the current downstream directories.

---

## Wave 11: Quant / Computer Vision Outlier Cleanup

**Completed eleventh wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave11/`

Removed skills:

- `backtesting-frameworks`
- `senior-computer-vision`

Current local counts after this wave:

- `~/.codex/skills`: `151`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `senior-data-engineer` | Even after removing the quant/CV outliers, this one still maps more plausibly to real ETL/data-pipeline work and remains narrower than the deleted “senior” AI/vision packages. |
| `polars` | This is a concrete data-manipulation skill with direct implementation value and much lower trigger breadth than `backtesting-frameworks`. |
| `python-performance-optimization` | It stays relevant to real Python debugging work across the current repos without pulling in trading-specific assumptions. |
| `ai-sdk` | This is still a stronger match for the user’s current LLM/app work than specialized model-training or vision-deployment skills. |
| `gemini-api-dev` | Keeps current model/API integration coverage without the much broader computer-vision training/deployment surface. |

### Delete

| Skill | Why it was removed |
|---|---|
| `backtesting-frameworks` | This is a quantitative-trading skill focused on backtests, market-data bias, and strategy validation. The current active repos and recent workstreams do not involve trading systems, OHLCV pipelines, or market-strategy evaluation, so it is a clear domain outlier. |
| `senior-computer-vision` | This is a specialized visual-AI package for YOLO/segmentation/model deployment. The current workspace has no active object-detection, segmentation, or CV deployment repo, making it another high-specialization, low-activation outlier. |

### Execution Note

- This wave stayed conservative: it removed only two highly specialized domains that showed no live repo signal in the current worktree set.
- Immediately after wave 11, the live local-vs-downstream drift reached 17 skills, coming from waves 8 through 11.

---

## Post-Wave-11 Correction: Restore Narrow Creative Utilities

**Completed correction on:** `2026-03-20`

Restored to `~/.codex/skills` from `~/.codex/pruned-skills/2026-03-20-wave10/`:

- `algorithmic-art`
- `slack-gif-creator`

Current local counts after this correction:

- `~/.codex/skills`: `153`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Why restore

| Skill | Why it was restored |
|---|---|
| `algorithmic-art` | This is a specialized but narrow creative workflow. It is not a broad umbrella skill competing for common engineering requests, so it should not have been prioritized for deletion ahead of noisier overlap-heavy skills. |
| `slack-gif-creator` | This is also narrow and low-trigger: a specific utility for animated Slack GIF production. Low frequency alone is not enough reason to remove a skill when its trigger surface is small and unlikely to create routing noise. |

### Keep Removed

| Skill | Why it stays removed |
|---|---|
| `senior-ml-engineer` | It is still a broad MLOps/LLM umbrella with significant overlap against narrower kept skills such as `rag-implementation`, `langchain`, `ai-sdk`, and `gemini-api-dev`. |
| `nano-banana-prompting` | It remains environment-misaligned because it depends on an unavailable `AskUserQuestion` tool and a missing `nano-banana` follow-up skill. |

### Correction Note

- This was a principles correction, not a popularity correction. Public downloads can matter for catalog selection, but local default-skill pruning should prioritize trigger breadth, overlap, and execution value.
- After this correction, the live local-vs-downstream drift is back to 15 skills.

---

## Wave 12: PM / UX Broad Toolkit Cleanup

**Completed twelfth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave12/`

Removed skills:

- `product-manager-toolkit`
- `ux-researcher-designer`

Current local counts after this wave:

- `~/.codex/skills`: `151`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `writing-plans` | This remains the narrower planning/process skill for multi-step execution without pulling in product-role frameworks like RICE, PRDs, and customer discovery. |
| `doc-coauthoring` | It covers structured documentation work more directly than the PM/UX roleplay-style toolkits. |
| `data-storytelling` | Still relevant for turning project evidence into interview/blog narratives; narrower than a full PM or UX research toolkit. |
| `frontend-design` | Keeps practical UI work covered without carrying the broader research/persona/journey-map package. |
| `content-strategy` | Retains topic/content planning value without bringing in the much wider PM toolkit surface. |

### Delete

| Skill | Why it was removed |
|---|---|
| `product-manager-toolkit` | This is a broad PM umbrella spanning RICE prioritization, customer interviews, PRD writing, discovery, and product strategy. That is a large trigger surface with partial overlap against the narrower planning, documentation, and storytelling skills already kept. |
| `ux-researcher-designer` | This is another role-oriented umbrella covering personas, journey maps, usability testing, and research synthesis. It is broader than the current need and overlaps with narrower design and documentation skills without mapping to a frequent live repo workflow. |

### Execution Note

- This wave follows the corrected pruning rule: remove broad role/toolkit umbrellas before touching narrow niche utilities.
- After wave 12, the live local-vs-downstream drift is back up to 17 skills, now spanning waves 8 through 12.

---

## Post-Wave-12 Correction: Restore Solo-Founder PM Layer

**Completed correction on:** `2026-03-20`

Restored to `~/.codex/skills` from `~/.codex/pruned-skills/2026-03-20-wave12/`:

- `product-manager-toolkit`

Current local counts after this correction:

- `~/.codex/skills`: `152`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Why restore

| Skill | Why it was restored |
|---|---|
| `product-manager-toolkit` | For a solo-founder or independent full-stack workflow, this is not just a generic PM roleplay package. It covers discovery, prioritization, and requirement-shaping work that the user may need to own directly when building products alone. |

### Keep Removed

| Skill | Why it stays removed |
|---|---|
| `ux-researcher-designer` | This remains a conditional keep. It becomes valuable when the user is actively running research interviews, usability tests, and journey-mapping work, but it is not yet a default keep based on the current direction. |

### Correction Note

- This correction reflects a workflow change: independent product ownership makes some cross-functional skills more valuable than they would be in a narrower pure-engineering setup.

---

## Wave 13: Azure Specialist Cleanup

**Completed thirteenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave13/`

Removed skills:

- `azure-compute`
- `azure-cost-optimization`
- `azure-deploy`
- `azure-prepare`
- `azure-resource-lookup`

Current local counts after this wave:

- `~/.codex/skills`: `147`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `tech-stack-evaluator` | Keeps general cloud/provider comparison available without locking the default skill set to one vendor's operational workflows. |
| `deploy-to-vercel` | This is a more directly relevant deployment path for current independent full-stack work than the Azure deployment chain. |
| `wrangler` | Keeps Cloudflare deployment/ops coverage that is closer to current and likely future workflows than the Azure specialist stack. |

### Delete

| Skill | Why it was removed |
|---|---|
| `azure-compute` | This is a narrow Azure VM/VMSS sizing and pricing skill. It is vendor-specific and tied to Azure infrastructure planning that is not part of the current active repos. |
| `azure-cost-optimization` | This requires Azure auth, Azure CLI extensions, and subscription-level cost analysis. It is highly environment-specific and not useful as a default local skill without active Azure operations. |
| `azure-deploy` | This is operationally heavy and depends on an Azure prepare/validate workflow with `.azure/plan.md` and validated deployment state. That is too specialized for the current default skill set. |
| `azure-prepare` | This is another deep Azure-specific preparation workflow. It is useful when actively building for Azure, but not worth keeping in the always-on local default set right now. |
| `azure-resource-lookup` | This is a strong Azure inventory skill, but it still assumes active Azure estate management. Without current Azure operations, it is a vendor-specific outlier. |

### Execution Note

- This wave removed the Azure specialist cluster as a group because the skills are both vendor-bound and workflow-bound.
- After wave 13, the live local-vs-downstream drift is 21 skills, spanning waves 8 through 13 with later corrections applied.

---

## Wave 14: Remove Remaining Vendor-Specific AWS Specialist

**Completed fourteenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directory was moved to:

- `~/.codex/pruned-skills/2026-03-20-wave14/`

Removed skill:

- `aws-solution-architect`

Current local counts after this wave:

- `~/.codex/skills`: `146`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `find-skills` | This stays as the recovery path for on-demand capability expansion. Vendor-specific cloud skills can be reinstalled later instead of occupying the default local set permanently. |
| `tech-stack-evaluator` | Keeps general cloud/provider comparison ability without pinning the local default set to AWS or Azure specialist workflows. |
| `deploy-to-vercel` | Remains more directly relevant to current independent full-stack deployment needs than cloud-vendor architecture packs. |
| `wrangler` | Still aligns more closely with current and likely future Cloudflare-centric workflows. |

### Delete

| Skill | Why it was removed |
|---|---|
| `aws-solution-architect` | This is a vendor-specific cloud architecture skill for AWS serverless and IaC planning. Given the user's stated preference to re-add cloud-specialist skills later through `find-skills` when needed, it no longer needs to remain in the default local set. |

### Execution Note

- This wave completes the current cloud-specialist pruning pass by removing the last retained AWS-specific specialist.
- After wave 14, the live local-vs-downstream drift is 22 skills.

---

## Wave 15: Remove Low-Risk Aggregators and Creative Outliers

**Completed fifteenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave15/`

Removed skills:

- `senior-data-engineer`
- `algorithmic-art`
- `slack-gif-creator`

Current local counts after this wave:

- `~/.codex/skills`: `143`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `senior-data-engineer` | Broad role-playing aggregator skill. Competes with narrower, more procedural backend and database skills without adding specific executable tools. |
| `algorithmic-art` | Creative outlier. Unlikely to be used in standard engineering workflows and takes up context window. |
| `slack-gif-creator` | Niche media generation skill that drifts from core engineering and documentation goals. |

### Execution Note

- This wave removes residual role-playing aggregator skills and highly specific media/creative outliers.
- After wave 15, the live local-vs-downstream drift is 25 skills.

---

## Wave 16: Remove Senior Role-Playing Aggregators

**Completed sixteenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave16/`

Removed skills:

- `senior-architect`
- `senior-backend`
- `senior-prompt-engineer`
- `senior-security`

Current local counts after this wave:

- `~/.codex/skills`: `139`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `168`
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `senior-architect` | Broad role-playing aggregator skill. Competes with more specific architecture frameworks (like `architecture-patterns`). |
| `senior-backend` | Broad role-playing aggregator. Generates redundant metadata instead of specific procedural execution. |
| `senior-prompt-engineer` | Broad role-playing aggregator. We already have `prompt-engineering-patterns` which provides procedural workflow over persona roleplay. |
| `senior-security` | Broad role-playing aggregator. Duplicates narrower, more useful skills without offering precise verification paths. |

### Execution Note

- This wave removes the remaining "senior-*" persona skills, adhering to the principle of prioritizing focused procedural skills over generic roleplay prompts.
- After wave 16, the live local-vs-downstream drift is 29 skills.

---

## Wave 17: Design/Content Umbrellas and Outliers

**Completed seventeenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave17/`

Removed skills:

- `ui-design-system`
- `content-strategy`
- `canvas-design`
- `data-storytelling`

Current local counts after this wave:

- `~/.codex/skills`: `135`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `139` (synced to 139 via sync_from_codex.py prior to Wave 17)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `ui-design-system` | A broad toolkit umbrella that overlaps heavily with the more procedural `tailwind-design-system`, `web-component-design`, and `frontend-design`. |
| `content-strategy` | A broad role-playing persona (Content Strategist). We already have procedural writing tools (`blog-post`, `technical-blog-writing`). |
| `canvas-design` | An outlier tool for generating visual aesthetics and PDFs. Like `algorithmic-art`, it deviates from standard coding workflows and adds trigger noise. |
| `data-storytelling` | A broad umbrella for crafting executive analytics presentations. Similar to `marketing-strategy-pmm` and `senior-data-scientist`, it falls outside focused engineering/documentation tasks. |

### Execution Note

- This wave removes overly broad toolkits in the design/content space and purges non-standard media generation tools to reduce context competition.
- After wave 17, the live local count is 135.

---

## Post-Wave-17 Correction: Reliance on `find-skills` for Niche Use Cases

**Completed correction on:** `2026-03-20`

*Initial thought was to restore `canvas-design` and `data-storytelling` for occasional executive reporting and PDF/PPT visual enhancements. However, these are fundamentally low-frequency, niche use cases that pollute the everyday coding context window.*

Instead of keeping them pre-installed, we rely on the **`find-skills`** fallback. When a specific reporting or visual design task arises, the agent can use `find-skills` to fetch the *absolute best and most up-to-date* skill for that exact situation, rather than hoarding a potentially suboptimal or overly broad skill in the default local set.

Current local counts remain reflecting their deletion:

- `~/.codex/skills`: `131` (Accounting for Wave 18 as well)

---

## Wave 18: Vue/Nuxt Ecosystem Cleanup

**Completed eighteenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave18/`

Removed skills:

- `vue`
- `nuxt`
- `nuxt-better-auth`
- `nuxt-ui`

Current local counts after this wave:

- `~/.codex/skills`: `131`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `131` (synced to 131 via sync_from_codex.py)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `vue` | The primary frontend stack is React/Next.js. Vue is an alternative ecosystem that clutters the context window with unused patterns. |
| `nuxt` | Same as Vue. Nuxt competes directly with Next.js skills but isn't used in the active workflow. |
| `nuxt-better-auth` | Nuxt-specific authentication plugin. Useless without Nuxt. |
| `nuxt-ui` | Nuxt-specific UI component library. Clashes with Shadcn and Tailwind skills used in React. |

### Execution Note

- This wave eliminates framework noise from the Vue/Nuxt ecosystem since the current primary target is React/Next.js.
- After wave 18, the live local count is 131.

---

## Wave 19: Alternative Frameworks and Languages

**Completed nineteenth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave19/`

Removed skills:

- `svelte-code-writer`
- `laravel`
- `dotnet-backend-patterns`

Current local counts after this wave:

- `~/.codex/skills`: `128`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `128` (synced to 128 via sync_from_codex.py)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `svelte-code-writer` | The primary frontend stack is React/Next.js. Svelte is an alternative framework that takes up space and trigger logic unneeded by the current default workflow. |
| `laravel` | PHP framework. Out of scope given the Node.js/Python backend focus. |
| `dotnet-backend-patterns` | C# framework. Out of scope given the Node.js/Python backend focus. |

### Execution Note

- This wave continues the philosophy of picking "one version of truth" for frameworks and relying on `find-skills` if the user occasionally needs to jump into a C#, PHP, or Svelte codebase.
- After wave 19, the live local count is 128.

---

## Wave 20: Office/PDF Formats and Animation Libraries

**Completed twentieth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave20/`

Removed skills:

- `gsap`
- `motion`

*(Note: `docx`, `pptx`, `xlsx`, and `pdf` were initially removed but immediately restored. They are high-frequency needs for academic workflows and internship resume preparation.)*

Current local counts after this wave:

- `~/.codex/skills`: `126`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `126` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `gsap`, `motion` | Specialized animation libraries (GSAP for JS, Framer Motion for React). These are UI polish tools rather than architectural cores. They add trigger noise for standard components. When complex animations are required, `find-skills` can load them on demand. |

### Execution Note

- This wave removes narrow animation libraries, trusting `find-skills` to provide on-demand capability when these niche UI polish requirements arise. Office document parsers are retained to support immediate academic and resume needs.
- After wave 20, the live local count is 126.

---

## Wave 21: Niche Third-Party SDKs and SaaS APIs

**Completed twenty-first wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave21/`

Removed skills:

- `stripe-integration`
- `stripe-best-practices`
- `convex-best-practices`
- `remotion-best-practices`
- `redis-js`
- `polars`

*(Note: `hf-cli` was initially removed but restored because Hugging Face Spaces offers highly valuable free backend deployment capabilities.)*

Current local counts after this wave:

- `~/.codex/skills`: `120`
- `~/.claude/skills`: `168`
- `~/.gemini/skills`: `120` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `stripe-integration`, `stripe-best-practices` | Stripe payment integration is a highly specific SaaS API workflow. Most React/Node developers don't touch payment flows daily. When needed, `find-skills` can grab it. |
| `convex-best-practices` | Convex is a specialized backend-as-a-service (BaaS). Not part of the default Node.js/Python core. |
| `remotion-best-practices` | Remotion is for programmatic video generation in React. A very specific edge case, not a standard web development requirement. |
| `redis-js` | Upstash Redis JS SDK. While caching is common, dedicating a full skill to a specific Redis provider's SDK in JS is too granular for the default set. |
| `polars` | Fast DataFrame library for Python/Rust. It's a specific data science tool, disconnected from the core web/backend engineering focus. |

### Execution Note

- This wave targets third-party SDKs, niche API platforms, and highly specialized libraries. These represent classic "on-demand" capabilities perfectly suited for `find-skills` rather than cluttering the default context.
- After wave 21, the live local count is 120.

---

## Wave 22: Third-Party Integrations and Legacy Claude Tooling

**Completed twenty-second wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave22/`

Removed skills:

- `figma`
- `figma-implement-design`
- `send-email`
- `audit-website`
- `claude-opus-4-5-migration`
- `claude-automation-recommender`

*(Note: `markitdown` was initially removed but restored because converting various file formats (PDFs, PPTs, images) to Markdown is a highly valuable and frequent pre-processing step for passing complex documents into LLM context windows.)*

Current local counts after this wave:

- `~/.codex/skills`: `114`
- `~/.claude/skills`: `115` (synced to codex + `claude-automation-recommender` retained)
- `~/.gemini/skills`: `114` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `figma`, `figma-implement-design` | Figma integration requires specific MCP setups and is a highly specialized UX-to-code pipeline. For general web development, this is an on-demand skill (`find-skills`) rather than a default. |
| `send-email` | Resend API integration. Same logic as Stripe - third-party SaaS APIs should be fetched via `find-skills` when actually building notification flows. |
| `audit-website` | A specific CLI wrapper (`squirrelscan`) for SEO/Performance audits. `web-perf` already covers Chrome DevTools MCP profiling which is more standard. |
| `claude-opus-4-5-migration` | A highly specific, one-time migration script for Claude models. Outdated context noise for daily Gemini/Codex usage. |
| `claude-automation-recommender` | Meta-skill specifically for configuring Claude Code automations. Irrelevant when using Gemini CLI. |

### Execution Note

- This wave removes third-party SaaS integrations (Figma, Resend), one-off utilities, and legacy Claude-specific configuration skills.
- After wave 22, the live local count is 114.

---

## Wave 23: React Ecosystem Deduplication

**Completed twenty-third wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave23/`

Removed skills:

- `react-web`
- `react-modernization`
- `react-components`

Current local counts after this wave:

- `~/.codex/skills`: `111`
- `~/.claude/skills`: `115`
- `~/.gemini/skills`: `111` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `react-web` | A generic umbrella for React development. We already have the more specific and up-to-date `react-dev` (TypeScript focused) and `react-19`. |
| `react-modernization` | A very specific one-time workflow (migrating class components to hooks). If encountering legacy code, this can be handled via `find-skills` instead of permanently loading migration instructions into every chat. |
| `react-components` | This was specifically tied to a proprietary "Stitch" design-to-code workflow (`stitch*:*` tools), which you don't use. For standard component building, `frontend-design` and `web-component-design` are better. |

### Execution Note

- This wave targets duplicate, legacy, and proprietary-tool-bound React skills, ensuring only the core modern React/Next.js procedural guides remain.
- After wave 23, the live local count is 111.

---

## Wave 24: Better Auth Umbrella Deduplication

**Completed twenty-fourth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave24/`

Removed skills:

- `better-auth-best-practices`
- `create-auth-skill`
- `email-and-password-best-practices`

Current local counts after this wave:

- `~/.codex/skills`: `108`
- `~/.claude/skills`: `115`
- `~/.gemini/skills`: `108` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `better-auth-best-practices`, `create-auth-skill`, `email-and-password-best-practices` | These three skills are highly fragmented, partial sub-skills for the "Better Auth" library. They create immense trigger noise when the user asks for authentication. We retain the single comprehensive `better-auth` skill to act as the canonical source for this library. |

### Execution Note

- This wave removes redundant, highly granular sub-skills for a specific auth library, ensuring the AI relies on a single comprehensive entry point rather than guessing between four overlapping tools.
- After wave 24, the live local count successfully drops below 110, settling at 108.

---

## Post-Wave-25 Correction: Retain Resume Ecosystem for Active Job Hunt

**Completed correction on:** `2026-03-20`

*(Initial thought was to remove `resume-ats-optimizer`, `resume-bullet-writer`, and `tailored-resume-generator` to avoid trigger overlap with `resume-builder`.)*

However, upon reviewing the core principles—"prefer focused, procedural skills" and the user's immediate context (an active job hunt)—these skills actually serve very distinct procedural roles in a pipeline, rather than just being text wrappers:
1. `resume-builder`: Generates the base JSON structure.
2. `resume-bullet-writer`: Applies the STAR/XYZ method specifically to the content.
3. `resume-ats-optimizer`: Runs a keyword diff against a specific Job Description.
4. `tailored-resume-generator`: Handles the final generation.

Given the extreme high-frequency need during the current sprint, they are kept in the active set.

Current local counts remain reflecting their retention:

- `~/.codex/skills`: `108`

---

## Wave 26: General Best Practices & Coding Standards

**Completed twenty-sixth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave26/`

Removed skills:

- `coding-standards`
- `backend-patterns`
- `frontend-patterns`

Current local counts after this wave:

- `~/.codex/skills`: `105`
- `~/.claude/skills`: `115`
- `~/.gemini/skills`: `105` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Delete

| Skill | Why it was removed |
|---|---|
| `coding-standards` | Extremely generic ("Universal coding standards"). Replaced by narrower, framework-specific skills and global instructions. |
| `backend-patterns` | Generic backend architecture advice. Overlaps with the much more specific and procedural `nodejs-backend-patterns` and `architecture-patterns`. |
| `frontend-patterns` | Generic frontend guidance. Duplicates the core logic found in `react-dev`, `next-best-practices`, and `frontend-design`. |

### Execution Note

- This wave removes broad "best practice" umbrellas that fail to provide procedural value and only contribute to trigger overlap.
- After wave 26, the live local count is 105.

---

## Wave 27: Database and SQL Deduplication

**Completed twenty-seventh wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave27/`

Removed skills:

- `postgresql-table-design`
- `sql-optimization-patterns`

Current local counts after this wave:

- `~/.codex/skills`: `103`
- `~/.claude/skills`: `115`
- `~/.gemini/skills`: `103` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `supabase-postgres-best-practices` | Represents the strongest, most up-to-date, and highly structured (8 categories of performance rules) guide for PostgreSQL. It fully supersedes generic table design or SQL optimization skills. |
| `prisma` | Provides specific procedural ORM logic, which is the primary layer at which most Next.js/Node.js backend developers interact with the database. |

### Delete

| Skill | Why it was removed |
|---|---|
| `postgresql-table-design` | Overlaps heavily with `supabase-postgres-best-practices` which is the superior, more modern alternative for Postgres schema architecture. |
| `sql-optimization-patterns` | Generic SQL optimization. Covered better by the comprehensive Postgres-specific rules in the Supabase package, avoiding trigger overlap. |

### Execution Note

- This wave strictly applies the "avoid multiple skills competing for the same request surface" rule by declaring the Supabase Postgres package as the absolute version of truth for database design and optimization.
- After wave 27, the live local count is 103.

---

## Wave 28: Testing Framework Deduplication

**Completed twenty-eighth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave28/`

Removed skills:

- `e2e-testing-patterns`
- `frontend-testing`
- `react-testing`

Current local counts after this wave:

- `~/.codex/skills`: `100`
- `~/.claude/skills`: `115`
- `~/.gemini/skills`: `100` (synced)
- `~/.qwen/skills`: `168`
- `~/.config/opencode/skills`: `168`
- `~/.config/agents/skills`: `168`
- `~/.codebuddy/skills`: `168`

### Keep

| Skill | Why keep it |
|---|---|
| `vitest` | The absolute version of truth for modern React/Next.js unit testing. |
| `webapp-testing` | A highly procedural toolkit containing actual Playwright scripts/helpers for testing local apps, far superior to generic E2E advice. |
| `test-driven-development` | Kept for workflow and procedural discipline rather than syntax guidance. |

### Delete

| Skill | Why it was removed |
|---|---|
| `e2e-testing-patterns` | Generic advice on E2E. Overlaps with `webapp-testing` which actually provides the scripts and tools to do the job. |
| `frontend-testing` | A highly specific skill built for the "Dify" project. It explicitly says "This skill enables Claude to generate tests for the Dify project". That is irrelevant noise for other repos. |
| `react-testing` | Generic React Testing Library advice. It's better to rely on `vitest` as the core testing runner, and standard React patterns are already covered by `react-dev`. |

### Execution Note

- This wave removes redundant testing advice and project-bound test skills (Dify), leaving exactly one procedural unit testing framework (`vitest`) and one procedural E2E toolkit (`webapp-testing`).
- After wave 28, the live local count perfectly hits 100.

---

## Wave 29: Content And Internal Comms Pruning

**Completed twenty-ninth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave29/`

Removed skills:

- `blog-post`
- `technical-blog-writing`
- `internal-comms`

Current local counts after this wave:

- `~/.codex/skills`: `97` (excluding `.system`; raw dir count is `98`)
- `~/.claude/skills`: `115` (excluding `.system`; unchanged)

### Keep

| Skill | Why keep it |
|---|---|
| `doc-coauthoring` | Still covers structured documentation and proposal/spec writing without assuming a blog publishing pipeline. |
| `writing-plans` | Remains the lightweight planning/spec workflow for multi-step technical work. |
| `product-manager-toolkit` | Preserves the solo-founder product-writing path without keeping heavier content-marketing or corporate-comms packages in the default set. |

### Delete

| Skill | Why it was removed |
|---|---|
| `blog-post` | Broad long-form content/SEO package that also depends on a `task` researcher flow and `generate_cover` workflow that are not part of the current Codex environment. |
| `technical-blog-writing` | Developer-blog workflow that explicitly depends on the unavailable `infsh` CLI, making it an environment-misaligned default skill. |
| `internal-comms` | Explicitly tuned for company-internal updates and newsletters ("my company likes to use"), which does not fit the current solo-founder/local-default skill set. |

### Execution Note

- Counting is now standardized to exclude the special `.system` directory from "local skill count" totals.
- No downstream sync was performed in this wave; this remains a Codex-local pruning step only.

---

## Wave 30: Auth Framework Deduplication

**Completed thirtieth wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave30/`

Removed skills:

- `authjs-skills`

Current local counts after this wave:

- `~/.codex/skills`: `96` (excluding `.system`; raw dir count is `97`)
- `~/.claude/skills`: `115` (excluding `.system`; unchanged)

### Keep

| Skill | Why keep it |
|---|---|
| `better-auth` | Already acts as the canonical authentication-library skill in the local set, covering concrete framework integration and preventing fragmented auth trigger overlap. |
| `auth-implementation-patterns` | Still preserves framework-agnostic auth/authorization design guidance without competing at the library-specific trigger surface. |

### Delete

| Skill | Why it was removed |
|---|---|
| `authjs-skills` | Competes directly with the retained `better-auth` package on the same authentication request surface, while the current local set already chose `better-auth` as the default auth-library truth. |

### Execution Note

- This wave removes the remaining competing auth-framework-specific package from the default local set.
- No downstream sync was performed in this wave; this remains a Codex-local pruning step only.

---

## Wave 31: Project-Bound UI And Artifact Skills

**Completed thirty-first wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave31/`

Removed skills:

- `ai-elements`
- `web-artifacts-builder`
- `vani-async-client-only`

Current local counts after this wave:

- `~/.codex/skills`: `93` (excluding `.system`; raw dir count is `94`)
- `~/.claude/skills`: `115` (excluding `.system`; unchanged)

### Keep

| Skill | Why keep it |
|---|---|
| `react-dev` | Still acts as the primary React implementation skill for typed components, hooks, and modern React patterns. |
| `nextjs-app-router-patterns` | Keeps the main Next.js App Router/RSC guidance without carrying project-specific UI libraries or custom artifact workflows. |
| `frontend-design` | Preserves general product/frontend design capability without binding the default set to Claude-artifact-only or library-specific component workflows. |

### Delete

| Skill | Why it was removed |
|---|---|
| `ai-elements` | Tied to the specific AI Elements component library and its install/customization workflow; too project-bound for the default local set. |
| `web-artifacts-builder` | Specialized for elaborate Claude HTML artifacts rather than normal app/product development, making it a niche workflow better restored on demand. |
| `vani-async-client-only` | Encodes a niche async/client-only component pattern (`fallback`, `clientOnly`) that does not align with the main React/Next.js guidance already kept in the default set. |

### Execution Note

- This wave removes UI/artifact specialists that are either library-bound or built around non-core rendering workflows.
- No downstream sync was performed in this wave; this remains a Codex-local pruning step only.

---

## Post-Wave Sync Snapshot

**Completed sync on:** `2026-03-20`

After pausing the pruning waves, the current Codex-local set was synced out to all managed agent directories using:

```bash
python scripts/sync_from_codex.py --targets claude,gemini,qwen,opencode,amp,codebuddy --mode copy --prune
```

Verified post-sync counts:

- `~/.codex/skills`: `93` (excluding `.system`; raw dir count is `94`)
- `~/.claude/skills`: `93`
- `~/.gemini/skills`: `93`
- `~/.qwen/skills`: `93`
- `~/.config/opencode/skills`: `93`
- `~/.config/agents/skills`: `93`
- `~/.codebuddy/skills`: `93`

Verification notes:

- all downstream directories now have `0` extra skills versus Codex
- `.system` directories were left untouched by the sync script

---

## Wave 31: Context7 Extension Conflict Resolution

**Completed thirty-first wave on:** `2026-03-20`

Removed from `~/.codex/skills` only. To keep this reversible, the directories were moved to:

- `~/.codex/pruned-skills/2026-03-20-wave31/`

Removed skills:

- `find-docs`

Current local counts after this wave:

- `~/.codex/skills`: `92`
- `~/.gemini/skills`: `92` (synced)

### Delete

| Skill | Why it was removed |
|---|---|
| `find-docs` | This skill is now natively bundled and installed by the `context7` Gemini extension (located in `~/.gemini/extensions/context7/skills/find-docs/`). Having it duplicated in the user-level `~/.codex/skills/` directory caused startup conflict warnings. Relying on the extension-managed version ensures it stays up-to-date with the context7 provider. |

### Execution Note

- This wave resolves startup warnings caused by extension-provided skills clashing with user-installed skills.
- After wave 31, the live local count is 92.
