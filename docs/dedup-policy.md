# De-dup Policy

We de-duplicate only for high-overlap skills.

## Stage 1: Objective pre-score

For candidates that appear meaningfully overlapping, compute:

`0.60 * Installs(log-normalized) + 0.25 * TrustScore + 0.15 * Verified`

Where:

- `Installs(log-normalized)` is the primary signal
- `TrustScore` is normalized to the same 0-1 range
- `Verified` is `1` for verified skills/libraries, otherwise `0`

This keeps installs as the dominant factor, but gives meaningful credit to
Context7 trust and verification status.

## Stage 2: Content review for close calls

Do a manual content review when any of these are true:

1. Pre-score gap is less than `0.12`
2. Install ratio is less than `1.8x`
3. Skills share the same source or near-identical descriptions

In close calls, prefer the skill with:

1. Clearer trigger description
2. Better scope fit (general vs framework-specific)
3. More useful bundled material (`references/`, `scripts/`, `assets/`)
4. Better maintained or more canonical naming

## Stage 3: Final tie-break

If still tied, prefer:

1. Official or maintained source
2. Verified skill/library
3. More canonical slug/name

This repo keeps manifests and installer scripts only (no third-party SKILL content).
