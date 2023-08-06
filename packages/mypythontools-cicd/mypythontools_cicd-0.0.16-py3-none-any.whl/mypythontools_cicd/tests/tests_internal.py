"""Module with functions for 'tests' subpackage."""

from __future__ import annotations
from typing import Sequence, cast
from pathlib import Path
import sys
import warnings
import os

from typing_extensions import Literal
import numpy as np
import mylogging

from mypythontools.paths import validate_path, PathLike
from mypythontools.system import get_console_str_with_quotes, terminal_do_command
from mypythontools.misc import delete_files, GLOBAL_VARS
import mypythontools.system.system_internal

from .. import venvs
from ..misc import get_requirements_files
from mypythontools_cicd.project_paths import PROJECT_PATHS


def setup_tests(
    generate_readme_tests: bool = True,
    matplotlib_test_backend: bool = False,
    set_numpy_random_seed: int | None = 2,
) -> None:
    """Add paths to be able to import local version of library as well as other test files.

    Value Mylogging.config.colorize = 0 changed globally.

    Note:
        Function expect `tests` folder on root. If not, test folder will not be added to sys path and
        imports from tests will not work.

    Args:
        generate_readme_tests (bool, optional): If True, generete new tests from readme if there are
            new changes. Defaults to True.
        matplotlib_test_backend (bool, optional): If using matlplotlib, it need to be
            closed to continue tests. Change backend to agg. Defaults to False.
        set_numpy_random_seed (int | None): If using numpy random numbers, it will be each time the same.
            Defaults to 2.

    """
    mylogging.config.colorize = False

    PROJECT_PATHS.add_root_to_sys_path()

    # Find paths and add to sys.path to be able to import local modules
    test_dir_path = PROJECT_PATHS.tests

    if test_dir_path.as_posix() not in sys.path:
        sys.path.insert(0, test_dir_path.as_posix())

    if matplotlib_test_backend:
        import matplotlib

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            matplotlib.use("agg")

    if generate_readme_tests:
        add_readme_tests()

    if set_numpy_random_seed:
        np.random.seed(2)


def run_tests(
    tested_path: None | PathLike = None,
    tests_path: None | PathLike = None,
    test_coverage: bool = True,
    stop_on_first_error: bool = True,
    virtualenvs: None | Sequence[PathLike] = sys.prefix,
    wsl_virtualenvs: None | Sequence[PathLike] = None,
    sync_requirements: None | Literal["infer"] | PathLike | Sequence[PathLike] = "infer",
    verbosity: Literal[0, 1, 2] = 1,
    extra_args: None | list = None,
) -> None:
    """Run tests. If any test fails, raise an error.

    This is not supposed for normal testing during development. It's usually part of pipeline an runs just
    before pushing code. It usually runs on more python versions and it's syncing dependencies, so takes much
    more time than testing in IDE.

    Args:
        tested_path (PathLike, optional): If None, root is used. root is necessary if using doctest, 'tests'
            folder not works for doctests in modules. Defaults to None.
        tests_path (PathLike, optional): If None, tests is used. It means where venv will be stored etc.
            Defaults to None.
        test_coverage (bool, optional): Whether run test coverage plugin. If True, pytest-cov must
            be installed. Defaults to True.
        stop_on_first_error (bool, optional): Whether stop on first error. Defaults to True.
        virtualenvs (None | Sequence[PathLike], optional): Virtualenvs used to testing. It's used to be able
            to test more python versions at once. Example: ``["venv/37", "venv/310"]``. If you want to use
            current venv, use `sys.prefix`. If there is no venv, it's created with default virtualenv version.
            Defaults to sys.prefix.
        wsl_virtualenvs (None | Sequence[PathLike], optional): If want to test Linux python from windows,
            it's possible with wsl. Just define path to venvs. It has to be relative paths. Defaults to None
        sync_requirements (None | Literal["infer"] | PathLike | Sequence[PathLike], optional): If using
            `virtualenvs` define what libraries will be installed by path to requirements.txt. Can also be a
            list of more files e.g ``["requirements.txt", "requirements_dev.txt"]``. If "infer", autodetected
            (all requirements). Defaults to "infer".
        verbosity (Literal[0, 1, 2], optional): Whether print details on errors or keep silent. If 0, no
            details, parameters `-q and `--tb=no` are added. if 1, some details are added --tb=short. If 2,
            more details are printed (default --tb=auto) Defaults to 1.
        extra_args (None | list, optional): List of args passed to pytest. Defaults to None

    Raises:
        Exception: If any test fail, it will raise exception (git hook do not continue...).

    Note:
        By default args to quiet mode and no traceback are passed. Usually this just runs automatic tests.
        If some of them fail, it's further analyzed in some other tool in IDE.

    Example:
        ``run_tests(verbosity=2)``
    """
    settings = {
        "tested_path": tested_path,
        "tests_path": tests_path,
        "test_coverage": test_coverage,
        "stop_on_first_error": stop_on_first_error,
        "sync_requirements": sync_requirements,
        "extra_args": extra_args,
    }

    tested_path = validate_path(tested_path) if tested_path else PROJECT_PATHS.root
    tests_path = validate_path(tests_path) if tests_path else PROJECT_PATHS.tests
    tested_path_str = get_console_str_with_quotes(tested_path)

    verbose = True if verbosity == 2 else False

    if not extra_args:
        extra_args = []

    if not test_coverage:
        pytest_args = [tested_path_str]
    else:
        pytest_args = [
            tested_path_str,
            "--cov",
            get_console_str_with_quotes(PROJECT_PATHS.app),
            "--cov-report",
            get_console_str_with_quotes(f"xml:{tests_path / 'coverage.xml'}"),
        ]

    if stop_on_first_error:
        extra_args.append("-x")

    if verbosity == 0:
        extra_args.append("-q")
        extra_args.append("--tb=no")
    elif verbosity == 1:
        extra_args.append("--tb=short")

    complete_args = [
        "pytest",
        *pytest_args,
        *extra_args,
    ]

    test_command = " ".join(complete_args)

    if (
        sync_requirements
        and sync_requirements != "infer"
        and isinstance(sync_requirements, (Path, str, os.PathLike))
    ):
        sync_requirements = [sync_requirements]
    sync_requirements = cast(list, sync_requirements)

    if virtualenvs:
        test_commands = []
        virtualenvs = [virtualenvs] if isinstance(virtualenvs, (str, Path)) else virtualenvs
        for i in virtualenvs:
            my_venv = venvs.Venv(i)
            my_venv.create()
            if sync_requirements:
                if verbosity:
                    print(f"\tSyncing requirements in venv '{my_venv.venv_path.name}' for tests")
                my_venv.sync_requirements(sync_requirements, verbose)
            # To be able to not install dev requirements in older python venv, pytest is installed.
            # Usually just respond with Requirements already satisfied.
            my_venv.install_library("pytest")
            test_commands.append(f"{my_venv.activate_command} && {test_command}")
    else:
        test_commands = [test_command]

    for i, command in enumerate(test_commands):
        if verbosity and virtualenvs:
            print(f"\tStarting tests with venv `{virtualenvs[i]}`")

        terminal_do_command(
            command, cwd=tested_path.as_posix(), verbose=verbose, error_header="Tests failed."
        )

    if test_coverage:
        delete_files(".coverage")

    if wsl_virtualenvs:
        wsl_virtualenvs = [wsl_virtualenvs] if isinstance(wsl_virtualenvs, (str, Path)) else wsl_virtualenvs

        for i in wsl_virtualenvs:
            settings["virtualenvs"] = [i]

            terminal_do_command(
                f"wsl {i}/bin/python -m pip install mypythontools_cicd",
                verbose=verbose,
                error_header=f"Installing pytest to wsl venv {i} failed.",
            )
            if verbosity:
                print(f"\tPreparing wsl environment.")

            terminal_do_command(
                f'wsl {i}/bin/python -m mypythontools_cicd --do_only test --test_options "{settings}"',
                cwd=tested_path.as_posix(),
                verbose=verbose,
                error_header="Tests failed.",
            )


def add_readme_tests(readme_path: None | PathLike = None, test_folder_path: None | PathLike = None) -> None:
    """Generate pytest tests script file from README.md and save it to tests folder.

    Can be called from conftest.

    Args:
        readme_path (None | PathLike, optional): If None, autodetected (README.md, Readme.md or readme.md
            on root). Defaults to None.
        test_folder_path (None | PathLike, optional): If None, autodetected (if root / tests).
            Defaults to None.

    Raises:
        FileNotFoundError: If Readme not found.

    Example:
        >>> add_readme_tests()

        Readme tests found.

    Note:
        Only blocks with python defined syntax will be evaluated. Example::

            ```python
            import numpy
            ```

        If you want to import modules and use some global variables, add ``<!--phmdoctest-setup-->`` directive
        before block with setup code.
        If you want to skip some test, add ``<!--phmdoctest-mark.skip-->``
    """
    readme_path = validate_path(readme_path) if readme_path else PROJECT_PATHS.readme
    test_folder_path = validate_path(test_folder_path) if test_folder_path else PROJECT_PATHS.tests

    readme_date_modified = str(readme_path.stat().st_mtime).split(".", maxsplit=1)[0]  # Keep only seconds
    readme_tests_name = f"test_readme_generated-{readme_date_modified}.py"

    test_file_path = test_folder_path / readme_tests_name

    # File not changed from last tests
    if test_file_path.exists():
        return

    for i in test_folder_path.glob("*"):
        if i.name.startswith("test_readme_generated"):
            i.unlink()

    python_path = get_console_str_with_quotes(sys.executable)
    readme = get_console_str_with_quotes(readme_path)
    output = get_console_str_with_quotes(test_file_path)

    generate_readme_test_command = f"{python_path} -m phmdoctest {readme} --outfile {output}"

    terminal_do_command(generate_readme_test_command, error_header="Readme test creation failed")


def deactivate_test_settings() -> None:
    """Deactivate functionality from setup_tests.

    Sometimess you want to run test just in normal mode (enable plots etc.). Usually at the end of
    test file in ``if __name__ = "__main__":`` block.
    """
    mylogging.config.colorize = True

    if "matplotlib" in sys.modules:

        import matplotlib
        from importlib import reload

        reload(matplotlib)
