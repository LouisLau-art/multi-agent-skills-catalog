# `session-handoff` validator rejects valid `###` headings in required sections

## Summary

`skills/session-handoff/scripts/validate_handoff.py` currently treats required sections as present only when their headings use `#` or `##`.

That causes valid handoff documents using deeper Markdown headings such as:

- `### Immediate Next Steps`
- `### Important Context`

to be reported as incomplete, even though the section names and content are correct.

## Reproduction

Minimal handoff fragment:

```md
# Handoff: Example

## Current State Summary

This is a valid summary with enough content to pass the completeness check.

### Immediate Next Steps

1. Do the first thing.
2. Do the second thing.
3. Do the third thing.

### Important Context

This is the critical context the next agent must know before resuming work.
```

Current validator result:

- marks `Immediate Next Steps` as missing
- marks `Important Context` as missing

Expected result:

- both sections should be recognized as valid required sections

## Root Cause

The validator currently matches headings with a regex equivalent to:

```python
pattern = rf'(?:^|\\n)##?\\s*{re.escape(section)}'
```

That only accepts one or two `#` characters.

## Proposed Fix

Allow any Markdown heading depth:

```python
pattern = rf'(?:^|\\n)#+\\s*{re.escape(section)}'
```

The same adjustment should be applied consistently to:

- required section detection
- recommended section detection

## Why This Matters

The current behavior creates false negatives in otherwise valid handoffs and forces users/agents to rewrite heading levels just to satisfy the validator.

This is especially confusing because the semantic structure is correct; only the heading depth differs.

## Scope

This should be a small, low-risk bugfix:

- expand heading-level matching
- add a regression test for `###` headings
- keep the rest of validation logic unchanged
