# Integration and retention checks

Use read-only commands first. Discover the primary checkout from Git, not from
folder names or recency. Example inspection commands, with actual safely quoted
paths supplied by the agent:

```sh
git -C /absolute/repository worktree list --porcelain
git -C /absolute/temporary-worktree rev-parse --show-toplevel
git -C /absolute/temporary-worktree rev-parse HEAD
git -C /absolute/temporary-worktree status --porcelain=v1 --untracked-files=all
git -C /absolute/temporary-worktree ls-files --others --ignored --exclude-standard
git -C /absolute/temporary-worktree submodule status --recursive
```

## Integration evidence

Resolve the intended destination from the task, repository policy and hosting
record. Never silently assume `main`, `master` or `develop`.

For a merge that preserves ancestry, a successful `git merge-base --is-ancestor`
check can establish that the exact source revision is contained in a verified
destination revision. Confirm the destination is the intended one and that the
revision is current enough for the task; local refs may be stale. Network fetches
are not part of read-only diagnosis unless the user authorizes them.

For a squash or rebase merge, direct ancestry may fail even when the PR merged.
Use the hosting record for that exact PR: repository, destination branch, merged
status, last reviewed head revision and merge revision. Match the worktree's HEAD
to the integrated source head. If the branch has advanced, retain the worktree
unless the additional commits are independently verified as integrated. A PR
title, branch name, closed state or visually similar diff is insufficient.

Detached worktrees still need an identified task and exact integration evidence.
If hosting evidence is inaccessible, report the unresolved condition rather than
classifying the worktree as safe to remove.

## Content and activity

Git status excludes ignored content. Enumerate ignored paths and determine their
purpose before treating them as regenerated. Local databases, signing material,
environment files, screenshots, result bundles and notes can be ignored and still
valuable. Do not print secret contents while inspecting metadata.

Check nested repositories and submodules as independent work. If a nested
repository's pending or unpushed state is unknown, retain the parent checkout.
Do not force through submodule-related restrictions in Git or a host API.

Use available process inspection, job state and host session evidence to establish
that the checkout is idle. A process-name search alone cannot prove this for an
agent-managed or shared checkout. Missing visibility means retain, not idle.

Record preservation destinations without copying private data into a public
report. Verify preservation succeeded before relying on it. A host snapshot or
Git commit does not normally include ignored files.

Recheck the same evidence immediately before retirement. Ordinary lifecycle
commands are appropriate for a cooperative, quiescent workspace, not protection
against adversarial concurrent writers. If another session may mutate the
checkout, stop until the task has exclusive ownership.
