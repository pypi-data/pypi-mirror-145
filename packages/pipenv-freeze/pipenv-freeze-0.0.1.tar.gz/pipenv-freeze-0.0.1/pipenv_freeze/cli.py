import argparse
import os
import pathlib
import subprocess

from pipenv_freeze import freeze_pipfile


def get_project_dir() -> pathlib.Path:
    output = subprocess.check_output(["pipenv", "--where"], encoding="utf-8").strip()
    if not output:
        raise Exception("No Pipfile found")
    return pathlib.Path(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if os.path.exists("Pipfile"):
        project = pathlib.Path.cwd()
    else:
        project = get_project_dir()

    freeze_pipfile(project, args.dry_run)
