# Cleanup Worktree 0.1.0

## Summary

- Close one merged Git task with exact integration, ownership and retention checks.
- Retire an eligible temporary worktree through Git or the host's supported
  lifecycle, preserving pending work and leaving branches intact.
- Install the same portable package for Claude Code, GitHub Copilot, Cursor and
  Codex, with optional Codex UI metadata.

## Why this release

Temporary worktrees can outlive the task that created them. Removing a directory
because a PR merged risks discarding later commits, useful ignored files or
another session's work. This initial release makes closure an evidence-backed
workflow and distinguishes it from general artifact cleanup.

## Compatibility notes

- Initial version `0.1.0`; no breaking changes to the published package name or
  skill directory.
- Requires local filesystem access and Git on macOS or Linux. Host-managed
  retirement requires an available, verified lifecycle API.
- Simulators remain diagnostic-only. No automatic hook, scheduler, memory budget
  or simulator pool is installed.
- This public package does not overwrite an existing personal installation.

## Validation

- Skill-creator validation, package metadata/version checks, local Markdown links
  and Markdown lint passed.
- The pinned skills CLI 1.7.4 discovered and installed byte-matching resources for
  all four agent IDs in a temporary project, with telemetry disabled.
- An independent read-only evaluation retained useful ignored notes and the
  primary checkout. A separate disposable Git retirement left its branch intact.
- Remote installation checks and hosted CI passed before publishing the release.
- Squash-merge hosting integration, managed-host archival and full behavioral
  execution in every agent have not been independently exercised.
