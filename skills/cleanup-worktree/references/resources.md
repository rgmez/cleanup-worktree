# Resource boundaries

Worktree retirement, branch deletion, build-cache cleanup and simulator lifecycle
are separate operations. One successful merge does not authorize all four.

## Build artifacts

Identify dedicated outputs through configuration, recorded paths or metadata.
For Xcode DerivedData, `info.plist` and its `WorkspacePath` may associate an output
with the task. Compare normalized paths with component boundaries; a textual
prefix is not containment. Missing metadata or a missing checkout does not prove
abandonment. Shared module caches must not be classified as task-owned output.

XcodeBuildMCP workspace names are clues, not ownership records. Inspect their
actual metadata and retain useful logs or result bundles. Dedicated build outputs
can be included in an artifact audit, but this skill does not authorize deleting
them or bypass a companion tool's eligibility checks.

Inside a worktree, preserve unexplained ignored files before retirement. Outside
it, report candidates without broad directory sweeps. For generic artifact audits
and bounded execution, use the separate `dev-artifact-cleanup` skill when available.

## Simulators

Read-only inventory is optional on macOS when relevant:

```sh
xcrun simctl list devices --json
xcrun simctl list runtimes --json
```

Devices and runtime images are different resources. Record exact UUIDs only when
the task records or configuration establish an association. A task-looking name,
age or shutdown state does not establish disposability. Device data can contain
apps, local databases and reproduction state. Do not delete CoreSimulator folders
or run global unavailable-device cleanup as part of closing a worktree.

This version does not allocate simulators, manage a concurrent pool, enforce RAM
budgets or reclaim devices. Report those needs without claiming to implement them.

## Optional memory optimization

[simslim](https://github.com/MobAI-App/simslim) is an independent tool that changes
which services run in a simulator. It complements resource lifecycle management;
it does not establish ownership or cap the number of active agents/devices.

Do not install or apply it during closure unless separately requested. Disabling
services changes the test environment: required capabilities must be preserved
and checked. Do not slim devices used by other tasks. Memory improvements need
local measurement and relevant behavior checks; never borrow the project's
benchmark as a result for the user's machine.
