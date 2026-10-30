# Cleanup Worktree

Close one merged task without losing pending work, useful ignored files or another
agent's environment. A portable [Agent Skill](https://agentskills.io/specification)
for local Git workflows.

The skill verifies the exact integrated revision, checks the temporary checkout,
and uses Git or the host's supported worktree lifecycle when retirement is
authorized. It leaves branches and unrelated resources in place.

## Repository contents

```text
skills/cleanup-worktree/     Canonical portable skill, references and license
skills/cleanup-worktree/agents/  Optional Codex UI metadata
scripts/                    Package and temporary-installation checks
tests/                      Disposable validator regression fixtures
docs/                       Validation scenarios and release process
.github/                    CI, release template and versioned release notes
CHANGELOG.md                Version history
CONTRIBUTING.md             Contribution scope and required checks
```

## Install

From the project where you want to use it:

```sh
npx skills add rgmez/cleanup-worktree --skill cleanup-worktree
```

Select an agent with `-a claude-code`, `-a github-copilot`, `-a cursor` or `-a codex`.
Add `-g` only for a personal global installation. Manual installs must copy the
entire `skills/cleanup-worktree` directory, including references and license.
Node.js is required for the installer; the skill's ordinary workflow requires
local filesystem access and Git on macOS or Linux. Cloud environments do not
gain access to your Mac by installing it.

The `rgmez/cleanup-worktree@cleanup-worktree` shorthand is also supported. To pin
the initial release, use:

```sh
npx skills add https://github.com/rgmez/cleanup-worktree/tree/v0.1.0 --skill cleanup-worktree
```

## Example requests

> Check whether this merged task's temporary worktree can be retired. Report only.

For an authorized retirement:

> Retire this task's temporary worktree after verifying the merge. Preserve test
> evidence and any pending work. Leave its branch intact.

Existing authorization or standing preferences can apply to a specific task.
Installation alone does not authorize retirement or create a post-merge hook.

## How it fits with the other tools

| Tool | Purpose | Limits |
| --- | --- | --- |
| cleanup-worktree | Close one merged task and retire its eligible temporary checkout | Requires integration, ownership, content and activity evidence |
| [dev-artifact-cleanup](https://github.com/rgmez/dev-artifact-cleanup) | Audit development artifacts and execute only its supported, approved candidates | Its separate manifests and execution contract apply |
| [simslim](https://github.com/MobAI-App/simslim) | Reduce simulator memory use by disabling selected services | Changes test capabilities; does not manage task ownership |

The companion skill and simslim are optional. This skill does not duplicate their
execution machinery. Simulators remain diagnostic-only in version 0.1.0. There
is no simulator pool, concurrency controller or automatic disk cleaner here.

## Safety and validation

A clean Git status is insufficient: ignored files, unpushed work and nested
repositories can still matter. Squash merges require exact hosting evidence;
matching a branch name to an old PR is insufficient. Shared or active worktrees
are retained. The primary checkout is never retired.

The instructions guide agent behavior; they do not enforce a sandbox or eliminate
concurrent-write risks. Unsupported host-managed worktrees are retained rather
than removed manually. No force removal, branch deletion or simulator mutation
is part of the default workflow.

Run `python3 scripts/validate_distribution.py` for packaging and local references.
Install `requirements-dev.txt` first. Run
`python3 -B -m unittest discover -s tests -v` for validator regression coverage.
Run `python3 scripts/smoke_install.py` for pinned CLI discovery and installation
into a disposable project, with telemetry disabled and all package files compared.
Behavioral validation scenarios are in [docs/validation.md](docs/validation.md).
Installer checks demonstrate resource packaging, not behavior in every agent.
An installable GitHub repository does not imply confirmed skills.sh indexing.

## Releases

- Current version: **0.1.1**.
- [Changelog](CHANGELOG.md).
- [Release notes](.github/RELEASE_NOTES_0.1.1.md).
- [Release process](docs/releasing.md) and [release template](.github/RELEASE_TEMPLATE.md).
- [GitHub Releases](https://github.com/rgmez/cleanup-worktree/releases).

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing the skill's scope or checks.

## License

MIT. See [LICENSE](LICENSE).
