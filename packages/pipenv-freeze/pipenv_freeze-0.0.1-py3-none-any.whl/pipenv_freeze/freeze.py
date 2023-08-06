import json
import os
import pathlib
import sys
import typing

import tomlkit

Dict = typing.Dict[str, typing.Any]
Directory = typing.Union[str, "os.PathLike[str]"]


def freeze_table(pipfile: typing.Any, key: str, lock: Dict) -> None:
    try:
        table = pipfile[key]
    except KeyError:
        return

    if not isinstance(table, dict):
        print(
            f"Warning: '{key}' is {type(table).__name__} (expected Container)",
            file=sys.stderr,
        )
        return

    for package, entry in table.items():
        if package not in lock:
            print(f"Warning: '{package}' not found in lockfile", file=sys.stderr)
            continue

        if lock[package].get("editable"):
            continue

        locked_version = lock[package]["version"]
        if entry == "*":
            table[package] = locked_version
            print(f"Pinned '{package}' to {locked_version}", file=sys.stderr)
        elif isinstance(entry, dict) and entry.get("version", "*") == "*":
            entry["version"] = locked_version
            print(f"Pinned '{package}' to {locked_version}", file=sys.stderr)


def freeze_pipfile(project: Directory, dry_run: bool = False) -> None:
    project = pathlib.Path(project)

    pipfile_path = project / "Pipfile"
    original = pipfile_path.read_text()
    pipfile = tomlkit.parse(original)

    with (project / "Pipfile.lock").open() as fp:
        lock = json.load(fp)

    freeze_table(pipfile, "packages", lock.get("default", {}))
    freeze_table(pipfile, "dev-packages", lock.get("develop", {}))

    frozen = tomlkit.dumps(pipfile)
    if frozen != original and not dry_run:
        pipfile_path.write_text(frozen)
