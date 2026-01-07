# Foundral Custom GPT YAML Pack — v1.0.0

This ZIP contains a **single Custom GPT spec in YAML**, plus versioning guidance and sample requests.
It is designed to reproduce the Foundral workflow you used in-session:

- **OPS Track** outputs (playbooks, checklists, cross-post copy, Magic HTML mirrors)
- **Book Track** outputs (manuscript + references + KDP/Heyzine/Gumroad assets)

## What's inside

- `gpt/foundral_book_review_architect.yaml` — the Custom GPT definition (YAML)
- `gpt/prompt_sequence_registry.yaml` — prompt sequencing + reusable blocks
- `templates/` — reusable text blocks (disclaimers, brief template)
- `samples/INTC/` — sample request + output manifest for the Intel book flow
- `samples/BEAM/` — sample request + output manifest for the BEAM vs peers flow
- `GUIDE_VERSIONING.md` — how to increment versions cleanly
- `CHANGELOG.md` — release log (start here)
- `LICENSE.txt` — permissive internal license note

## How to use (fast)

1) Copy the YAML into your Custom GPT system config:
- Start with `gpt/foundral_book_review_architect.yaml`
- Add `gpt/prompt_sequence_registry.yaml` as a companion “policy + prompt blocks” reference

2) Start a new project using `templates/PROJECT_BRIEF_TEMPLATE.md`.

3) Follow the phase order in the prompt registry. Don’t skip phases.

## Output discipline (important)

- Book files go to: `foundral_<topic>_book_vX.Y.Z.zip`
- Ops files go to:  `foundral_org_ops_index_vX.Y.Z.zip`

Never mix raw manuscript drafts into the OPS track.

**Created:** 2026-01-07
