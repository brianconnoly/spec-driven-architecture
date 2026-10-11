#!/usr/bin/env python3
"""Check LikeC4 links and spec markers for a spec-driven repository.

The skill and the starter each carry this file. Keep the copies identical.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".next",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "tsp-output",
    "vendor",
}

SOURCE_SUFFIXES = {
    ".c",
    ".cc",
    ".cjs",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".lua",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".swift",
    ".ts",
    ".tsx",
}

MARKER_RE = re.compile(
    r"^\s*(?://!|///|//+|#|%%|\*|/\*)?\s*"
    r"(Architecture|Contract|Flow|Implementation):\s+(.+?)\s*$"
)
LINK_RE = re.compile(r"^\s*link\s+(\S+)\s*$")
ARROW_RE = re.compile(r"(\S+)\s+->\s+(\S+)")
FQN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")


def code_portion(line: str) -> str:
    """Drop a LikeC4 line comment without touching '//' inside quotes."""
    out: list[str] = []
    quote = None
    index = 0
    while index < len(line):
        char = line[index]
        if quote:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
            index += 1
            continue
        if char == "/" and index + 1 < len(line) and line[index + 1] == "/":
            break
        out.append(char)
        index += 1
    return "".join(out)


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def display(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def ident_declared(text: str, ident: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(ident)}\s*=", text) is not None


def fqn_problem(texts: list[str], fqn: str, required_text: str | None = None) -> str | None:
    if not FQN_RE.fullmatch(fqn):
        return f"not a LikeC4 id: {fqn}"
    blob = "\n".join(texts)
    missing = [part for part in fqn.split(".") if not ident_declared(blob, part)]
    if missing:
        return f"{fqn} is missing declarations for {', '.join(missing)}"
    if required_text is not None and not ident_declared(required_text, fqn.rsplit(".", 1)[-1]):
        return f"{fqn} is not declared in the linked model file"
    return None


def check(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    linked_files: set[Path] = set()
    c4_text: dict[Path, str] = {}

    for path in iter_files(root):
        if path.suffix != ".c4":
            continue
        text = path.read_text(encoding="utf-8")
        c4_text[path] = text
        for line_no, line in enumerate(text.splitlines(), 1):
            match = LINK_RE.match(code_portion(line).strip())
            if match is None:
                continue
            raw = match.group(1).strip("'\"")
            label = f"{display(root, path)}:{line_no}"
            if raw.startswith(("http://", "https://")):
                errors.append(f"{label}: link a file in the repo, not {raw}")
                continue
            candidate = (path.parent / raw).resolve()
            if not inside(root, candidate):
                errors.append(f"{label}: link escapes the repository: {raw}")
                continue
            if not candidate.exists():
                errors.append(f"{label}: missing link target {raw}")
                continue
            if candidate.is_file():
                linked_files.add(candidate)

    def read_lines(path: Path) -> list[str]:
        return path.read_text(encoding="utf-8").splitlines()

    def marker_errors(path: Path) -> None:
        require_arrow = path.suffix != ".tsp"
        for line_no, line in enumerate(read_lines(path), 1):
            match = MARKER_RE.match(line)
            if match is None:
                continue
            kind, value = match.group(1), match.group(2).strip()
            label = f"{display(root, path)}:{line_no}"
            if kind == "Architecture":
                arrow = ARROW_RE.fullmatch(value)
                if arrow:
                    raw_path, fqn = arrow.group(1), arrow.group(2)
                    target = resolve_repo_file(root, raw_path, label, errors)
                    if target is None:
                        continue
                    problem = fqn_problem(
                        list(c4_text.values()),
                        fqn,
                        target.read_text(encoding="utf-8"),
                    )
                    if problem:
                        errors.append(f"{label}: {problem}")
                    continue
                if require_arrow:
                    errors.append(
                        f"{label}: Architecture must be '<file>.c4 -> <fqn>', got {value}"
                    )
                    continue
                problem = fqn_problem(list(c4_text.values()), value)
                if problem:
                    errors.append(f"{label}: {problem}")
                continue
            target = resolve_repo_file(root, value.split()[0], label, errors)
            if target is None:
                continue

    def wants_markers(path: Path) -> bool:
        if path.suffix in SOURCE_SUFFIXES:
            return True
        if path.suffix == ".tsp":
            return True
        return path.suffix == ".mmd" and "specs" in path.parts

    for path in iter_files(root):
        if wants_markers(path):
            marker_errors(path)

    for path in iter_files(root):
        if path.suffix == ".tsp" and "@service" in path.read_text(encoding="utf-8"):
            if path not in linked_files:
                errors.append(
                    f"{display(root, path)}: @service contract has no LikeC4 link"
                )
        if path.suffix == ".mmd" and "specs" in path.parts and path not in linked_files:
            errors.append(f"{display(root, path)}: flow has no LikeC4 link")
        if path.suffix in SOURCE_SUFFIXES and path in linked_files:
            text = path.read_text(encoding="utf-8")
            if not any(
                MARKER_RE.match(line) and MARKER_RE.match(line).group(1) == "Architecture"
                for line in text.splitlines()
            ):
                errors.append(
                    f"{display(root, path)}: linked source file has no Architecture marker"
                )
    return errors


def resolve_repo_file(root: Path, raw: str, label: str, errors: list[str]) -> Path | None:
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append(f"{label}: path must be repository-relative: {raw}")
        return None
    target = (root / candidate).resolve()
    if not inside(root, target):
        errors.append(f"{label}: path escapes the repository: {raw}")
        return None
    if not target.is_file():
        errors.append(f"{label}: missing {raw}")
        return None
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current directory.",
    )
    args = parser.parse_args(argv)
    root = args.root
    if not root.is_dir():
        print(f"spec links failed: {root} is not a directory", file=sys.stderr)
        return 1
    errors = check(root)
    if errors:
        print("spec links failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("spec links ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
