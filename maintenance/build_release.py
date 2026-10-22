#!/usr/bin/env python3
"""Build and verify release ZIPs from committed Git objects, without dependencies."""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from check import ROOT, check, require


def git(*args):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout


def tree_files(ref):
    return git("ls-tree", "-r", "--name-only", "-z", ref).decode("utf-8").strip("\0").split("\0")


def archive(ref, prefix):
    return git("archive", "--format=zip", f"--prefix={prefix}/", ref)


def subset_archive(full_data, full_prefix, folder, prefix, license_data):
    # Reuse verified archive bytes and timestamps. Archiving a subtree directly
    # loses root attributes and can trigger Windows CRLF conversion.
    data = BytesIO()
    source_prefix = f"{full_prefix}/{folder}/"
    with ZipFile(BytesIO(full_data)) as source, ZipFile(data, "w", compression=ZIP_DEFLATED) as bundle:
        selected = [entry for entry in source.infolist()
                    if not entry.is_dir() and entry.filename.startswith(source_prefix)]
        require(selected, f"No files to package: {folder}")
        for original in selected:
            name = original.filename[len(source_prefix):]
            entry = ZipInfo(f"{prefix}/{name}", date_time=original.date_time)
            entry.external_attr = original.external_attr
            entry.compress_type = ZIP_DEFLATED
            bundle.writestr(entry, source.read(original))
        entry = ZipInfo(f"{prefix}/LICENSE", date_time=selected[0].date_time)
        entry.external_attr = 0o100644 << 16
        entry.compress_type = ZIP_DEFLATED
        bundle.writestr(entry, license_data)
    return data.getvalue()


def verify(data, prefix, expected):
    with ZipFile(BytesIO(data)) as bundle:
        infos = bundle.infolist()
        names = [entry.filename for entry in infos]
        require(len(names) == len(set(names)), "Duplicate ZIP member")
        require(bundle.testzip() is None, "ZIP CRC check failed")
        for name in names:
            path = PurePosixPath(name)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in name,
                    f"Unsafe ZIP path: {name}")
            require(path.parts and path.parts[0] == prefix, f"Unexpected ZIP prefix: {name}")
        actual = {entry.filename[len(prefix) + 1:]: bundle.read(entry) for entry in infos if not entry.is_dir()}
        require(set(actual) == set(expected), "ZIP file manifest differs from Git tree")
        for name, content in expected.items():
            require(actual[name] == content, f"ZIP content differs from Git blob: {name}")
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="Version tag, such as v1.0.0")
    parser.add_argument("--output", type=Path, help="Defaults to dist/<tag>")
    args = parser.parse_args()
    require(re.fullmatch(r"v\d+\.\d+\.\d+", args.ref), "--ref must be a version tag")
    commit = git("rev-parse", "--verify", f"refs/tags/{args.ref}^{{commit}}").decode().strip()
    version = git("show", f"{commit}:VERSION").decode("utf-8").strip()
    require(args.ref == f"v{version}", "Tag and committed VERSION differ")
    files = tree_files(commit)
    require(all(name and not any(part in {".git", "dist", ".venv", "__pycache__"} for part in PurePosixPath(name).parts)
                and not PurePosixPath(name).name.startswith(".env") for name in files), "Unexpected private or generated path")
    blobs = {name: git("show", f"{commit}:{name}") for name in files}

    full_prefix = f"Delicious-Study-{args.ref}"
    full_data = archive(commit, full_prefix)
    verify(full_data, full_prefix, blobs)
    with tempfile.TemporaryDirectory(prefix="delicious-study-release-") as temp:
        # Paths were checked above; do not extract unverified external archives.
        with ZipFile(BytesIO(full_data)) as bundle:
            bundle.extractall(temp)
        result = check(Path(temp) / full_prefix)

    license_data = blobs["LICENSE"]
    skill_files = {name.removeprefix("skills/delicious-study/"): data for name, data in blobs.items()
                   if name.startswith("skills/delicious-study/")}
    skill_files["LICENSE"] = license_data
    example_files = {name.removeprefix("examples/"): data for name, data in blobs.items() if name.startswith("examples/")}
    example_files["LICENSE"] = license_data
    require("SKILL.md" in skill_files and "agents/openai.yaml" in skill_files, "Skill entry files missing")
    require("README.md" in example_files, "Example entry missing")
    example_prefix = f"Delicious-Study-examples-{args.ref}"
    skill_data = subset_archive(full_data, full_prefix, "skills/delicious-study", "delicious-study", license_data)
    example_data = subset_archive(full_data, full_prefix, "examples", example_prefix, license_data)
    verify(skill_data, "delicious-study", skill_files)
    verify(example_data, example_prefix, example_files)

    output = (args.output or ROOT / "dist" / args.ref).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bundles = {
        f"Delicious-Study-{args.ref}.zip": full_data,
        f"Delicious-Study-skill-{args.ref}.zip": skill_data,
        f"Delicious-Study-examples-{args.ref}.zip": example_data,
    }
    sums = []
    for name, data in sorted(bundles.items()):
        (output / name).write_bytes(data)
        sums.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
    (output / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "commit": commit, "checks": result,
                      "output": str(output), "assets": {name: len(data) for name, data in bundles.items()}}, ensure_ascii=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"BUILD FAILED: {error}", file=sys.stderr)
        sys.exit(1)
