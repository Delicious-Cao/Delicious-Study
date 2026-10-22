#!/usr/bin/env python3
"""Check release metadata and local document links; Python standard library only."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def quoted_scalar(text, key):
    match = re.search(rf'^\s*{re.escape(key)}: ("[^\n]*")\s*$', text, re.MULTILINE)
    require(match is not None, f"Missing quoted scalar: {key}")
    return json.loads(match.group(1))


def check(root=ROOT):
    root = Path(root).resolve()
    required = [
        "VERSION", "LICENSE", "README.md", "CHANGELOG.md", "CONTRIBUTING.md",
        "skills/delicious-study/SKILL.md", "skills/delicious-study/agents/openai.yaml",
        "docs/QUICKSTART.md", "docs/RUNTIME.md", "docs/RELEASING.md",
        "examples/README.md", "examples/colligative-properties.md", "examples/derivatives.md",
        "maintenance/check.py", "maintenance/build_release.py",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml", ".github/ISSUE_TEMPLATE/config.yml",
    ]
    for name in required:
        require((root / name).is_file(), f"Missing required file: {name}")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    require(re.fullmatch(r"\d+\.\d+\.\d+", version), "VERSION must be x.y.z")
    require((root / f"docs/RELEASE-v{version}.md").is_file(), "Missing release notes")

    skill = (root / "skills/delicious-study/SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    require(match is not None, "Missing Skill frontmatter")
    frontmatter = match.group(1)
    require(re.search(r"^name: delicious-study$", frontmatter, re.MULTILINE), "Unexpected Skill name")
    require(quoted_scalar(frontmatter, "version") == version, "Skill version differs from VERSION")
    description = quoted_scalar(frontmatter, "description")
    require(0 < len(description) <= 1024, "Invalid Skill description length")
    require("[TODO:" not in skill, "Unfinished Skill scaffold")

    ui = (root / "skills/delicious-study/agents/openai.yaml").read_text(encoding="utf-8")
    require(quoted_scalar(ui, "display_name") == "Delicious-Study", "Unexpected display name")
    require(25 <= len(quoted_scalar(ui, "short_description")) <= 64, "UI description must be 25-64 characters")
    if re.search(r"^\s*default_prompt:", ui, re.MULTILINE):
        require("$delicious-study" in quoted_scalar(ui, "default_prompt"), "Default prompt must name the Skill")

    link_count = 0
    files = [p for p in root.rglob("*") if p.is_file() and not any(
        part in {".git", "dist", "__pycache__", ".venv"} for part in p.relative_to(root).parts
    )]
    for path in files:
        if path.suffix.lower() not in {".md", ".yml", ".yaml", ".py", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8")
        require("\ufffd" not in content, f"Invalid text replacement character: {path.relative_to(root)}")
        if path.suffix.lower() != ".md":
            continue
        # Remove fenced code before finding ordinary Markdown links.
        prose = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", content, flags=re.MULTILINE | re.DOTALL)
        for target in re.findall(r"\]\(([^)\n]+)\)", prose):
            target = target.strip().split(' "', 1)[0].strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            require(resolved.is_relative_to(root), f"Link escapes repository: {path.name}: {target}")
            require(resolved.exists(), f"Broken local link: {path.relative_to(root)}: {target}")
            link_count += 1

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    require(f"## [{version}]" in changelog, "CHANGELOG does not contain current version")
    return {"version": version, "files_checked": len(files), "local_links_checked": link_count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = check(args.root)
    except (ValueError, OSError, UnicodeError) as error:
        print(f"CHECK FAILED: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "passed", **result}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
