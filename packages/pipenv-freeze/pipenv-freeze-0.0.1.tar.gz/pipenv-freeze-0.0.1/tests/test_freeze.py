import json
import pathlib

import pytest

from pipenv_freeze.freeze import freeze_pipfile

packages = """
[packages]
tomlkit = "*"
with-path = {path = "."}
locked = ">=0.1"
with-comment = "==1.0"  # comment
editable = {version = "*",editable = true}
missing = "==1.0"
"""

dev_packages = """
[dev-packages]
pytest = "*"
"""

lock_default = {
    "tomlkit": {
        "hashes": ["..."],
        "version": "==0.10.1",
    },
    "with-path": {
        "hashes": ["..."],
        "version": "==0.0.1",
    },
    "locked": {
        "hashes": ["..."],
        "version": "==0.2",
    },
    "with-comment": {
        "hashes": ["..."],
        "version": "==1.0",
    },
    "editable": {
        "editable": True,
    },
}

lock_develop = {
    "pytest": {
        "hashes": ["..."],
        "index": "pypi",
        "version": "==7.1.1",
    },
}


def test_freeze_packages(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.write_text(packages)

    lock = tmp_path / "Pipfile.lock"
    lock.write_text(json.dumps({"default": lock_default}))

    freeze_pipfile(tmp_path)

    locked = pipfile.read_text().splitlines(keepends=False)
    assert 'tomlkit = "==0.10.1"' in locked
    assert 'with-path = {path = ".",version = "==0.0.1"}' in locked
    assert 'locked = ">=0.1"' in locked
    assert 'with-comment = "==1.0"  # comment' in locked
    assert 'editable = {version = "*",editable = true}' in locked

    _, err = capsys.readouterr()
    assert "Warning: 'missing' not found in lockfile" in err
    assert "Pinned 'tomlkit' to ==0.10.1" in err
    assert "Pinned 'with-path' to ==0.0.1" in err


def test_freeze_dry_run(tmp_path: pathlib.Path) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.write_text(packages)
    ctime = pipfile.stat().st_ctime_ns

    lock = tmp_path / "Pipfile.lock"
    lock.write_text(json.dumps({"default": lock_default}))

    freeze_pipfile(tmp_path, dry_run=True)

    assert pipfile.read_text() == packages
    assert pipfile.stat().st_ctime_ns == ctime


def test_freeze_develop_packages(tmp_path: pathlib.Path) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.write_text(dev_packages)

    lock = tmp_path / "Pipfile.lock"
    lock.write_text(json.dumps({"develop": lock_develop}))

    freeze_pipfile(tmp_path)

    assert 'pytest = "==7.1.1"' in pipfile.read_text()


def test_freeze_unexpected_structure(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.write_text("packages = 1\n[[dev-packages]]\ntest = 1\n")

    lock = tmp_path / "Pipfile.lock"
    lock.write_text("{}")

    freeze_pipfile(tmp_path)

    _, err = capsys.readouterr()
    assert "Warning: 'packages' is Integer" in err
    assert "Warning: 'dev-packages' is AoT" in err
