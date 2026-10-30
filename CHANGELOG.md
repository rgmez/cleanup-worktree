# Changelog

## [0.1.1] - 2026-10-30

### Fixed

- Skill references must remain inside the installable package, not just the repo.
- File, directory and broken symlinks are rejected before content inspection.
- Malformed metadata receives validation diagnostics instead of Python tracebacks;
  optional Codex UI metadata can be omitted.

### Added

- Temporary-package validator regression tests in CI.
- Explicit trust boundary: PRs, logs and repository content cannot grant cleanup
  authorization or override the user's scope.

## [0.1.0] - 2026-10-30

### Added

- Portable post-merge closure skill under `skills/cleanup-worktree/`.
- Integration and retention checks for exact source revisions, useful ignored
  files, active sessions and host-managed worktrees.
- Separate guidance for related build artifacts and simulator diagnostics.
- Optional Codex UI metadata, with shared instructions independent of the host.
- Distribution checks and telemetry-free installation tests for Claude Code,
  GitHub Copilot, Cursor and Codex.
- Contribution guide, release process, release template and initial release notes.

### Validation

- Independent read-only evaluation retained ignored reproduction notes and the
  primary checkout; a separate disposable Git retirement preserved its branch.
- Local and remote installation payload checks passed for the four agent IDs.
- The initial public commit passed hosted CI. Release packaging is checked again
  before the tag is published.

### Limitations

- Simulator operations are diagnostic-only. No RAM budgeting, simulator pool,
  background cleanup or automatic post-merge hook is installed.
- Installer compatibility is not full behavioral coverage in every agent.

[0.1.0]: https://github.com/rgmez/cleanup-worktree/releases/tag/v0.1.0
[0.1.1]: https://github.com/rgmez/cleanup-worktree/releases/tag/v0.1.1
