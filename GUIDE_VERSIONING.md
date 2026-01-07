# Versioning Guide (OPS + GPT YAML Pack)

This pack uses semantic versioning:

- **MAJOR**: breaking changes to workflow structure or required files
- **MINOR**: new features (new phases, new templates, new output types)
- **PATCH**: fixes, copy edits, small improvements that don’t change structure

## Recommended tags
- `v1.0.0` — initial stable YAML pack
- `v1.0.1` — typo fixes / better prompts / added examples
- `v1.1.0` — new use-case template (e.g., energy, healthcare providers)
- `v2.0.0` — restructure of phases or required outputs

## Folder naming (suggested)
Keep the pack in its own repo or folder:
- `foundral-custom-gpt/`
  - `gpt/`
  - `templates/`
  - `samples/`
  - `docs/` (optional)

## Updating workflow safely
1) Change YAML first (source of truth).
2) Update `prompt_sequence_registry.yaml` to match.
3) Add/refresh a sample under `samples/`.
4) Update `CHANGELOG.md`.
5) Zip and tag release.

## Sampling from our session
- INTC: used as a semiconductor crossroads narrative + comparative lens.
- BEAM: used as biotech (gene editing) comparative lens + signals-not-predictions framing.

Use the sample request files as your starting prompts.
