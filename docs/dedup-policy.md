# De-dup Policy

We de-duplicate only for high-overlap skills and keep the winner by:

1. Higher installs (log-normalized)
2. Higher trust score
3. Preferred official/maintained source
4. Verified proxy (`trust >= 9`)

This repo keeps manifests and installer scripts only (no third-party SKILL content).
