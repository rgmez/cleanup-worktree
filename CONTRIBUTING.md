# Contributing

Keep this skill focused on closing one verified merged task. General artifact
audits belong in the companion project; simulator allocation and optimization
are separate workflows.

## Changes

- Keep one canonical package in `skills/cleanup-worktree/`.
- Preserve the distinction between eligibility and authorization.
- Add retention cases when a real failure exposes missing ownership, integration
  or preservation evidence. Do not add broad deletion shortcuts.
- Keep host-specific metadata optional and references skill-relative.
- Write concise guidance and separate verified behavior from planned scenarios.
- Do not include personal paths, credentials, private logs or user data.

## Checks

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_distribution.py
python3 -B -m unittest discover -s tests -v
python3 scripts/smoke_install.py
npx --yes markdownlint-cli@0.45.0 '**/*.md'
```

The installer runs in a temporary project with telemetry disabled. Never use real
user checkouts or simulators for destructive tests. For behavior changes, exercise
the relevant cases in [docs/validation.md](docs/validation.md), including a case
that must retain the worktree. Installation tests alone do not validate decisions.

All package resources must be regular files and all local references from inside
the skill must remain within its package. Repository documents may link into the
package; installed skill files cannot depend on repository-only documents.
Symbolic links, including internal or broken links, are rejected before reading
their contents. Add validator regression fixtures for changes to these boundaries.

Use English commit messages with `New:`, `Fix:` or `Update:`. For releases, follow
[docs/releasing.md](docs/releasing.md) and update the metadata, body version,
changelog and release notes together.
