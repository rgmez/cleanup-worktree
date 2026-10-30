# Cleanup Worktree 0.1.1

## Summary

- Reject skill references that escape the installed package, even when their
  targets exist elsewhere in the repository.
- Reject file and directory symlinks before reading their contents.
- Report malformed metadata as validation errors and clarify that retrieved
  evidence cannot grant cleanup authorization.

## Why this release

The previous validator accepted a package reference to the repository README and
a symlink to an external fixture. Those cases were reproduced in temporary copies;
neither defect was present in the published 0.1.0 package. This patch prevents
future packages from relying on files that are not part of the installed payload.

## Compatibility notes

- No change to the installation name, ordinary cleanup scope or permissions.
- Symbolic links are deliberately unsupported, including links within the repo.
- Optional Codex UI metadata remains optional; if provided, it is validated.
- Simulators remain diagnostic-only.

## Validation

- All 24 regression fixtures passed, covering valid package links, escaping/encoded/reference-style
  links, file and directory symlinks, broken links, malformed YAML and mismatched
  release metadata. Fixtures are temporary and do not remove user worktrees.
- Package validation, skill-creator checks, Markdown lint and pinned installer
  checks passed locally. The exact release commit must also pass hosted CI.
- The added trust-boundary instructions have not undergone a new independent
  model evaluation; unit tests validate packaging, not model behavior.
