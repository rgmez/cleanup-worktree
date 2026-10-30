"""Check the package's references, metadata and privacy-sensitive path leaks."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "cleanup-worktree"


def validate():
    errors = []
    source = PACKAGE / "SKILL.md"
    text = source.read_text()
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0]:
        raise SystemExit("Invalid frontmatter boundaries")
    metadata = yaml.safe_load(parts[1])
    if metadata.get("name") != PACKAGE.name or metadata.get("license") != "MIT":
        errors.append("Incorrect canonical name or license")
    description = metadata.get("description", "")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append("Invalid description")
    version = metadata.get("metadata", {}).get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit("Version must be a semantic-version string")
    if f"## Version\n\n{version}." not in text:
        errors.append("Body version differs from metadata")
    if f"Current version: **{version}**" not in (ROOT / "README.md").read_text():
        errors.append("README version differs from metadata")
    if f"## [{version}]" not in (ROOT / "CHANGELOG.md").read_text():
        errors.append("Version has no changelog entry")
    notes = ROOT / ".github" / f"RELEASE_NOTES_{version}.md"
    if not notes.is_file():
        errors.append("Versioned release notes missing")
    ui = yaml.safe_load((PACKAGE / "agents" / "openai.yaml").read_text())
    if not 25 <= len(ui["interface"]["short_description"]) <= 64:
        errors.append("Invalid UI short description length")
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
