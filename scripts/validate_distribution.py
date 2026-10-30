"""Validate an installable skill package and its repository release metadata."""
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = "cleanup-worktree"
IGNORED_DIRECTORIES = {".git", ".venv", "__pycache__"}


def markdown_targets(content):
    """Read inline/image links and reference definitions, including angle targets."""
    inline = r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))"
    definitions = r"(?m)^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|([^\s]+))"
    for pattern in (inline, definitions):
        for match in re.finditer(pattern, content):
            yield match.group(1) or match.group(2)


def check_distribution(root):
    root = Path(root).absolute()
    errors = []
    files = []
    if root.is_symlink():
        return ["Repository root must not be a symbolic link"]
    root = root.resolve()
    package = root / "skills" / SKILL
    # Reject links before reading their contents, including directory links that
    # pathlib traversal might otherwise omit and broken links that look absent.
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if name not in IGNORED_DIRECTORIES]
        for name in dirs + names:
            path = Path(directory) / name
            if path.is_symlink():
                errors.append(f"Symbolic link is not distributable: {path.relative_to(root)}")
            elif path.is_file():
                files.append(path)
    if errors:
        return errors

    def read(path):
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read {path.relative_to(root)}: {exc.__class__.__name__}")
            return ""

    def mapping(raw, label):
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError:
            errors.append(f"Invalid YAML: {label}")
            return {}
        if not isinstance(data, dict):
            errors.append(f"Expected YAML mapping: {label}")
            return {}
        return data

    text = read(package / "SKILL.md")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.DOTALL)
    metadata = {}
    if frontmatter is None:
        errors.append("Invalid frontmatter boundaries")
    else:
        metadata = mapping(frontmatter.group(1), "SKILL.md frontmatter")
    if metadata.get("name") != SKILL or metadata.get("license") != "MIT":
        errors.append("Incorrect canonical name or license")
    description = metadata.get("description", "")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append("Invalid description")
    details = metadata.get("metadata", {})
    if not isinstance(details, dict):
        errors.append("Expected metadata mapping")
        details = {}
    version = details.get("version")
    valid_version = isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version)
    if not valid_version:
        errors.append("Version must be a semantic-version string")
    else:
        if f"## Version\n\n{version}." not in text:
            errors.append("Body version differs from metadata")
        if f"Current version: **{version}**" not in read(root / "README.md"):
            errors.append("README version differs from metadata")
        if f"## [{version}]" not in read(root / "CHANGELOG.md"):
            errors.append("Version has no changelog entry")
        if not (root / ".github" / f"RELEASE_NOTES_{version}.md").is_file():
            errors.append("Versioned release notes missing")
    # This metadata is optional for other hosts. If present, validate its shape.
    ui_path = package / "agents" / "openai.yaml"
    if ui_path.exists():
        ui = mapping(read(ui_path), "agents/openai.yaml")
        interface = ui.get("interface", {})
        if not isinstance(interface, dict):
            interface = {}
        short_description = interface.get("short_description")
        if not isinstance(short_description, str) or not 25 <= len(short_description) <= 64:
            errors.append("Invalid UI short description length")
    if not (package / "LICENSE").is_file():
        errors.append("Package license missing")
    for path in files:
        if path.suffix != ".md":
            continue
        content = read(path)
        if re.search(r"/Users/|/home/[^ /]+/|gh[pousr]_[A-Za-z0-9]{20,}", content):
            errors.append(f"Personal path or token-like content: {path.relative_to(root)}")
        boundary = package if path.is_relative_to(package) else root
        for target in markdown_targets(content):
            parsed = urlsplit(target)
            if parsed.scheme in {"http", "https", "mailto"}:
                continue
            if parsed.scheme or parsed.netloc:
                errors.append(f"Unsupported link: {path.relative_to(root)} -> {target}")
                continue
            if not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(boundary) or not resolved.is_file():
                errors.append(f"Invalid relative link: {path.relative_to(root)} -> {target}")
    return errors


def validate():
    errors = check_distribution(ROOT)
    if errors:
        raise SystemExit("\n".join(errors))
    print("Distribution checks passed")


if __name__ == "__main__":
    validate()
