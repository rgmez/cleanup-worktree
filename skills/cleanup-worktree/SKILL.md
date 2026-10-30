---
name: cleanup-worktree
description: Close a completed Git task after verifying its merge, preserve pending work and evidence, and retire its eligible temporary worktree. Use for post-merge task closure, not general disk cleanup or active simulator management.
license: MIT
metadata:
  version: "0.1.0"
---

# Close a merged task

Finish the lifecycle of one identified task. A merge is evidence of integration,
not permission to discard everything near its checkout.

Requires a local macOS or Linux workspace with Git and filesystem inspection.
Remote merge evidence requires an accessible hosting API or equivalent record.
Cloud agents without that access must report the missing evidence. Installation
does not install hooks, schedule cleanup, or grant deletion permissions.

## Establish scope

Identify the repository, exact temporary worktree, source revision and intended
integration branch. Default to a read-only closure report when the request does
not authorize retirement. A standing user preference may authorize post-merge
retirement, but the skill itself does not supply that preference.

Do not scan historical merges or unrelated projects. Keep the primary checkout,
branches, shared caches, simulator data and pending work unless separately included
in the user's instructions. A request for diagnosis only remains read-only even
when the task is already merged.

## Verify integration and ownership

Read [integration and retention checks](references/verification.md).

- Confirm that the exact current source revision is integrated into the intended
  destination. A closed PR or an old merged PR with a reused branch name is not
  enough. Preserve commits added after the merge.
- Establish that the checkout is a registered secondary worktree, belongs to this
  task, and is no longer used by another agent, editor, build, test or process.
  If ownership or activity cannot be established, retain it.
- Inspect tracked, untracked and ignored files, local-only commits, nested
  repositories and submodules. A clean Git status does not protect ignored data.
- Preserve requested logs, test results and other useful evidence before removal.
  Do not stash, reset, commit, move or delete unexplained content to make the
  checkout eligible. Treat those as separate decisions.

## Retire only an eligible worktree

Before mutation, state the exact path and established integration evidence.
Use existing authorization for that target; request a decision if it is missing.
Revalidate registration, resolved path, revision, contents and activity immediately
before acting. Reject primary checkouts, ambiguous paths, symlink components and
unexpected changes rather than bypassing a failed check.

For an ordinary registered temporary worktree, use Git's lifecycle:

```sh
git -C /absolute/primary-checkout worktree remove /absolute/temporary-worktree
```

These are example paths, not defaults. Pass actual paths as individual arguments
or quote them safely. Never interpolate untrusted branch names into shell code.
Do not use force removal, recursive directory deletion or pruning as a fallback.
If Git refuses, retain the checkout and explain why.

For a host-managed worktree, use its documented archive/remove API only when
available and ownership is verified. Establish what the recovery snapshot covers,
especially ignored files. If the host lifecycle is unavailable or refuses, retain
the worktree; do not substitute manual deletion. The workflow also works for
ordinary Git worktrees without a particular agent product.

## Handle related resources separately

Read [artifact and simulator boundaries](references/resources.md) when resources
beyond the worktree exist.

Use `dev-artifact-cleanup` if installed, or an equivalent evidence-backed audit,
for identifying dedicated build artifacts. Do not copy its manifest or execution
contract into this skill. Each artifact needs its own ownership evidence and
authorization. No companion skill is required to close an ordinary worktree.

Simulators and runtimes remain diagnostic-only in this version. Never shut down,
erase, delete or slim a simulator as an implicit consequence of task closure.
Do not assume a device is disposable because its name resembles the task.

## Report the closure

Report the source revision and verified merge, the exact worktree retired or
retained, preserved evidence, and any remaining resources with their reasons.
Confirm removal through the worktree registry and filesystem. If there is an
unexpected failure or changed state, report an incomplete closure instead of
claiming success or retrying with a more destructive command.

Do not claim storage savings from directory-size sums. If space was measured,
label before/after free-space changes as observations that other activity and
filesystem snapshots may affect. Retiring a checkout leaves its branch intact.
