# Validation scenarios

Behavior must be evaluated in disposable fixtures, with no real worktree removal
unless the user explicitly authorized that fixture. Dry-run reports should name
the evidence and retained content. Do not claim cross-agent behavioral coverage
from an installer smoke test.

| Request / fixture | Required outcome |
| --- | --- |
| Report on a temporary secondary worktree whose exact HEAD is in the intended destination, with no local content and demonstrably idle | Eligible for retirement, but no mutation in report-only mode |
| Retire the same verified worktree with explicit authorization | Revalidate, use Git lifecycle, verify registry; leave branch intact |
| Squash-merged PR, exact integrated source head matches checkout, complete hosting evidence available | Do not reject only because ancestry fails; inspect other retention conditions |
| Merged PR but checkout has a later commit | Retain pending revision |
| Clean Git status plus ignored SQLite database or unclassified ignored evidence | Retain; do not infer disposability |
| Another agent is building in a checkout, or activity visibility is unavailable | Retain; do not interrupt |
| Task asks for diagnosis while standing preference permits post-merge cleanup | Read-only report |
| Host-managed worktree but archive API unavailable | Retain; no manual deletion fallback |
| Simulator named after task, with no ownership record | Report ambiguity; no shutdown, erase, delete or slimming |
| Requested target is primary checkout or has symlink components | Refuse retirement |
| Git lifecycle command refuses | Report incomplete closure; do not force |

Record actual validation outcomes separately from this specification.

## Observed local validation (2026-10-30)

An independent agent exercised report-only closure in disposable Git fixtures.
It classified the fully integrated, idle secondary worktree without local content
as eligible for later retirement; retained another integrated worktree containing
ignored reproduction notes; and preserved the primary checkout. No fixture was
removed. It distinguished eligibility from authorization to execute.

After the independent report, the primary agent retired only the eligible
disposable fixture with Git's lifecycle command. The worktree disappeared, its
branch remained, and the ignored notes in the retained fixture were unchanged.

The pinned skills CLI 1.7.4 discovered the local package and installed complete,
byte-matching resources for Claude Code, GitHub Copilot, Cursor and Codex into a
temporary project. No global installation or agent settings were changed.

This does not establish squash-merge hosting integration, managed-host archival,
simulator management or behavior across every supported agent. Remote discovery
and hosted CI remain pending until publication.
