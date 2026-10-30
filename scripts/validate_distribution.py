"""Check the package's references, metadata and privacy-sensitive path leaks."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "cleanup-worktree"


def validate():
    errors = []
    source = PACKAGE / "SKILL.md"
    text = source.read_text()
    if not text.startswith("---\nname: cleanup-worktree\n"):
        errors.append("Missing canonical frontmatter/name")
    if 'version: "0.1.0"' not in text or "license: MIT" not in text:
        errors.append("Missing version or license")
    if not (PACKAGE / "LICENSE").is_file():
        errors.append("Package license missing")
    for path in ROOT.rglob("*.md"):
        content = path.read_text()
        if re.search(r"/Users/|/home/[^ /]+/|gh[pousr]_[A-Za-z0-9]{20,}", content):
            errors.append(f"Personal path or token-like content: {path.relative_to(ROOT)}")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.is_file() or ROOT not in resolved.parents:
                errors.append(f"Invalid relative link: {path.relative_to(ROOT)} -> {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Distribution checks passed")


if __name__ == "__main__":
    validate()
