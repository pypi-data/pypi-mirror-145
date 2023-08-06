import pathlib
import shutil
import typing
from unittest import mock

import pytest

from pipenv_freeze.cli import get_project_dir, main


@pytest.fixture(autouse=True)
def mock_freeze() -> typing.Generator[mock.MagicMock, None, None]:
    with mock.patch("pipenv_freeze.cli.freeze_pipfile") as mocked:
        yield mocked


@pytest.fixture(autouse=True)
def tmp_project_dir(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def mock_project_dir(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> typing.Generator[mock.MagicMock, None, None]:
    with mock.patch("pipenv_freeze.cli.get_project_dir") as mocked:
        mocked.return_value = tmp_path
        yield mocked


@pytest.fixture
def requires_pipenv() -> None:
    if not shutil.which("pipenv"):
        raise pytest.skip("`pipenv` is not installed")


def test_get_project_dir(
    requires_pipenv: None,
    tmp_path: pathlib.Path,
) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.touch()
    assert get_project_dir() == tmp_path


def test_get_project_subdir(
    requires_pipenv: None,
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.touch()

    sub = tmp_path / "sub"
    sub.mkdir()

    monkeypatch.chdir(sub)

    assert get_project_dir() == tmp_path


def test_get_project_dir_without_pipfile(
    requires_pipenv: None,
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(Exception, match="No Pipfile found"):
        get_project_dir()


def test_main_calls_freeze(
    mock_freeze: mock.MagicMock,
    mock_project_dir: mock.MagicMock,
) -> None:
    with mock.patch("sys.argv", new=["pipenv-freeze"]):
        main()
    mock_freeze.assert_called_once_with(pathlib.Path.cwd(), False)


def test_main_dry_run(
    mock_freeze: mock.MagicMock,
    mock_project_dir: mock.MagicMock,
) -> None:
    with mock.patch("sys.argv", new=["pipenv-freeze", "--dry-run"]):
        main()
    mock_freeze.assert_called_once_with(pathlib.Path.cwd(), True)


def test_main_pipfile_exists(
    tmp_path: pathlib.Path,
    mock_freeze: mock.MagicMock,
    mock_project_dir: mock.MagicMock,
) -> None:
    pipfile = tmp_path / "Pipfile"
    pipfile.touch()

    with mock.patch("sys.argv", new=["pipenv-freeze"]):
        main()
    mock_freeze.assert_called_once_with(pathlib.Path.cwd(), False)
    mock_project_dir.assert_not_called()
