#!/usr/bin/env bash
set -euo pipefail

TARGET=${1:-claude}   # claude | universal | global | auto
DRY_RUN=${DRY_RUN:-0}

case "$TARGET" in
  claude) FLAG="--claude" ;;
  universal) FLAG="--universal" ;;
  global) FLAG="--global" ;;
  auto) FLAG="" ;;
  *) echo "Usage: $0 [claude|universal|global|auto]"; exit 1 ;;
esac

run_install() {
  local source="$1"
  local skill_name="$2"
  local -a cmd=(npx ctx7 skills install)
  if [ -n "$FLAG" ]; then cmd+=("$FLAG"); fi
  cmd+=("$source" "$skill_name")
  if [ "$DRY_RUN" = "1" ]; then
    printf "DRY_RUN: "; printf "%q " "${cmd[@]}"; echo
  else
    "${cmd[@]}"
  fi
}

echo "Installing curated skills (target=$TARGET, count=163)..."
run_install /vercel-labs/agent-browser agent-browser
run_install /anthropics/claude-code 'Agent Development'
run_install /vercel/ai-elements ai-elements
run_install /jezweb/claude-skills ai-sdk-core
run_install /anthropics/skills algorithmic-art
run_install /wshobson/agents api-design-principles
run_install /alirezarezvani/claude-skills app-store-optimization
run_install /wshobson/agents architecture-decision-records
run_install /wshobson/agents architecture-patterns
run_install /wshobson/agents async-python-patterns
run_install /wshobson/agents auth-implementation-patterns
run_install /gocallum/nextjs16-agent-skills authjs-skills
run_install /alirezarezvani/claude-skills aws-solution-architect
run_install /affaan-m/everything-claude-code backend-patterns
run_install /wshobson/agents backtesting-frameworks
run_install /jezweb/claude-skills better-auth
run_install /better-auth/skills better-auth-best-practices
run_install /obra/superpowers brainstorming
run_install /expo/skills building-native-ui
run_install /secondsky/claude-skills 'Bun Next.js'
run_install /vercel/next.js cache-components
run_install /anthropics/skills canvas-design
run_install /anthropics/claude-plugins-official claude-automation-recommender
run_install /anthropics/claude-code claude-opus-4-5-migration
run_install /secondsky/claude-skills cloudflare-nextjs
run_install /agno-agi/agno code-review
run_install /alirezarezvani/claude-skills code-reviewer
run_install /affaan-m/everything-claude-code coding-standards
run_install /anthropics/claude-code 'Command Development'
run_install /intellectronica/agent-skills context7
run_install /upstash/context7 context7-docs-lookup
run_install /narumiruna/context7-skills-skill context7-skills
run_install /waynesutton/convexskills 'Convex Best Practices'
run_install /better-auth/skills create-auth-skill
run_install /anthropics/skills doc-coauthoring
run_install /upstash/context7 documentation-lookup
run_install /anthropics/skills docx
run_install /wshobson/agents dotnet-backend-patterns
run_install /wshobson/agents e2e-testing-patterns
run_install /wshobson/agents embedding-strategies
run_install /obra/superpowers executing-plans
run_install /expo/skills expo-api-routes
run_install /expo/skills expo-cicd-workflows
run_install /expo/skills expo-deployment
run_install /expo/skills expo-dev-client
run_install /expo/skills expo-tailwind-setup
run_install /wshobson/agents fastapi-templates
run_install /alinaqi/claude-bootstrap flutter
run_install /anthropics/skills frontend-design
run_install /affaan-m/everything-claude-code frontend-patterns
run_install /langgenius/dify frontend-testing
run_install /openclaw/openclaw gemini
run_install /google-gemini/gemini-skills gemini-api-dev
run_install /wshobson/agents github-actions-templates
run_install /wshobson/agents go-concurrency-patterns
run_install /martinholovsky/claude-skills-generator gsap
run_install /anthropics/claude-code 'Hook Development'
run_install /anthropics/skills internal-comms
run_install /davila7/claude-code-templates langchain
run_install /wshobson/agents langchain-architecture
run_install /rawveg/skillsforge-marketplace laravel
run_install /davila7/claude-code-templates markitdown
run_install /anthropics/skills mcp-builder
run_install /anthropics/claude-code 'MCP Integration'
run_install /wshobson/agents memory-safety-patterns
run_install /wshobson/agents mobile-android-design
run_install /wshobson/agents mobile-ios-design
run_install /wshobson/agents monorepo-management
run_install /jezweb/claude-skills motion
run_install /nikiforovall/claude-code-rules nano-banana-prompting
run_install /expo/skills native-data-fetching
run_install /vercel-labs/next-skills next-best-practices
run_install /jezweb/claude-skills nextjs
run_install /wshobson/agents nextjs-app-router-patterns
run_install /JosiahSiegel/claude-plugin-marketplace nextjs-modal-integration
run_install /wshobson/agents nodejs-backend-patterns
run_install /onmax/nuxt-skills nuxt
run_install /onmax/nuxt-skills nuxt-better-auth
run_install /onmax/nuxt-skills nuxt-ui
run_install /anthropics/skills pdf
run_install /anthropics/claude-code 'Plugin Settings'
run_install /anthropics/claude-code 'Plugin Structure'
run_install /davila7/claude-code-templates polars
run_install /wshobson/agents postgresql-table-design
run_install /anthropics/skills pptx
run_install /blencorp/claude-code-kit prisma
run_install /wshobson/agents python-performance-optimization
run_install /wshobson/agents rag-implementation
run_install /Gentleman-Programming/Gentleman-Skills react-19
run_install /davila7/claude-code-templates react-best-practices
run_install /google-labs-code/stitch-skills react:components
run_install /softaworks/agent-toolkit react-dev
run_install /resend/react-email react-email
run_install /wshobson/agents react-modernization
run_install /wshobson/agents react-native-architecture
run_install /callstackincubator/agent-skills react-native-best-practices
run_install /shipshitdev/library react-native-components
run_install /wshobson/agents react-native-design
run_install /wshobson/agents react-state-management
run_install /citypaul/dotfiles react-testing
run_install /alinaqi/claude-bootstrap react-web
run_install /upstash/redis-js redis-js
run_install /remotion-dev/skills remotion-best-practices
run_install /wshobson/agents responsive-design
run_install /wshobson/agents rust-async-patterns
run_install /davila7/claude-code-templates senior-architect
run_install /alirezarezvani/claude-skills senior-backend
run_install /alirezarezvani/claude-skills senior-computer-vision
run_install /alirezarezvani/claude-skills senior-data-engineer
run_install /alirezarezvani/claude-skills senior-data-scientist
run_install /alirezarezvani/claude-skills senior-devops
run_install /alirezarezvani/claude-skills senior-frontend
run_install /davila7/claude-code-templates senior-fullstack
run_install /alirezarezvani/claude-skills senior-ml-engineer
run_install /alirezarezvani/claude-skills senior-prompt-engineer
run_install /davila7/claude-code-templates senior-qa
run_install /alirezarezvani/claude-skills senior-security
run_install /giuseppe-trisciuoglio/developer-kit shadcn-ui
run_install /anthropics/skills skill-creator
run_install /anthropics/claude-code 'Skill Development'
run_install /anthropics/skills slack-gif-creator
run_install /wshobson/agents sql-optimization-patterns
run_install /stripe/ai stripe-best-practices
run_install /wshobson/agents stripe-integration
run_install /alinaqi/claude-bootstrap supabase-nextjs
run_install /sveltejs/mcp svelte-code-writer
run_install /obra/superpowers systematic-debugging
run_install /wshobson/agents tailwind-design-system
run_install /jezweb/claude-skills tailwind-v4-shadcn
run_install /jezweb/claude-skills tanstack-query
run_install /DeckardGer/tanstack-agent-skills tanstack-query-best-practices
run_install /jezweb/claude-skills 'TanStack Table'
run_install /alirezarezvani/claude-skills tdd-guide
run_install /alirezarezvani/claude-skills tech-stack-evaluator
run_install /anthropics/skills template-skill
run_install /wshobson/agents terraform-module-library
run_install /obra/superpowers test-driven-development
run_install /wshobson/agents typescript-advanced-types
run_install /alirezarezvani/claude-skills ui-design-system
run_install /gabrielantonyxaviour/Velox ui-dev
run_install /alinaqi/claude-bootstrap ui-web
run_install /vercel/next.js update-docs
run_install /expo/skills upgrading-expo
run_install /expo/skills use-dom
run_install /obra/superpowers using-superpowers
run_install /wshobson/agents uv-package-manager
run_install /alirezarezvani/claude-skills ux-researcher-designer
run_install /itsjavi/vani vani-async-client-only
run_install /vercel-labs/agent-skills vercel-composition-patterns
run_install /vercel-labs/agent-skills vercel-deploy
run_install /vercel-labs/agent-skills vercel-react-best-practices
run_install /vercel-labs/agent-skills vercel-react-native-skills
run_install /antfu/skills vite
run_install /antfu/skills vitest
run_install /onmax/nuxt-skills vue
run_install /anthropics/skills web-artifacts-builder
run_install /wshobson/agents web-component-design
run_install /vercel-labs/agent-skills web-design-guidelines
run_install /cloudflare/skills web-perf
run_install /anthropics/skills webapp-testing
run_install /cloudflare/skills wrangler
run_install /obra/superpowers writing-plans
run_install /anthropics/skills xlsx
echo "Done."
echo "Note: For Codex folder sync, copy ~/.claude/skills to ~/.codex/skills if needed."
