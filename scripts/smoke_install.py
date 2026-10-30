"""Exercise pinned skills CLI installation without changing global settings."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = "cleanup-worktree"
AGENTS = {
    "claude-code": ".claude/skills",
    "github-copilot": ".agents/skills",
    "cursor": ".agents/skills",
    "codex": ".agents/skills",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(ROOT))
    args = parser.parse_args()
    env = dict(os.environ, DISABLE_TELEMETRY="1", DO_NOT_TRACK="1", CI="1", NO_COLOR="1")
    cli = ["npx", "--yes", "skills@1.7.4", "add", args.source]
    with tempfile.TemporaryDirectory(prefix="cleanup-worktree-install-") as temp:
        project = Path(temp)
        subprocess.run(["git", "init", "--quiet", str(project)], check=True)
        discovery = subprocess.run(
            cli + ["--list"], cwd=project, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=True,
        )
        if SKILL not in discovery.stdout:
            raise RuntimeError("Skill not discovered")
        subprocess.run(
            cli + ["--skill", SKILL, "--agent", *AGENTS, "--copy", "--yes"],
            cwd=project, env=env, timeout=120, check=True,
        )
        for agent, directory in AGENTS.items():
            installed = project / directory / SKILL
            for resource in (ROOT / "skills" / SKILL).rglob("*"):
                if not resource.is_file():
                    continue
                relative = resource.relative_to(ROOT / "skills" / SKILL)
                copy = installed / relative
                if not copy.is_file() or copy.read_bytes() != resource.read_bytes():
                    raise RuntimeError(f"Incorrect payload for {agent}: {relative}")
        print("Discovery and complete package verified for " + ", ".join(AGENTS))


if __name__ == "__main__":
    main()
