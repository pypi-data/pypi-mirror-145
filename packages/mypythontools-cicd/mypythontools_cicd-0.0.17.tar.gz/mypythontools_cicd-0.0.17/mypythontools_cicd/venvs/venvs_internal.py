"""Module with functions for 'venvs' subpackage."""

from __future__ import annotations
from typing import Sequence
import platform
import subprocess
import shutil
from pathlib import Path
from ast import literal_eval
import sys

from typing_extensions import Literal

from mypythontools.paths import PathLike
from mypythontools.system import (
    get_console_str_with_quotes,
    terminal_do_command,
    SHELL_AND,
    PYTHON,
)

from ..misc import get_requirements_files
from mypythontools_cicd.project_paths import PROJECT_PATHS


class Venv:
    """You can create new venv or sync it's dependencies.

    Example:
        >>> from pathlib import Path
        ...
        >>> path = "venv/310" if platform.system() == "Windows" else "venv/ubuntu"
        >>> venv = Venv(path)
        >>> venv.create()  # If already exists, it's skipped
        >>> venv.install_library("colorama==0.3.9")
        >>> "colorama==0.3.9" in venv.list_packages()
        True
        >>> venv.sync_requirements()  # There ia a 0.4.4 in requirements.txt
        >>> "colorama==0.4.4" in venv.list_packages()
        True
        >>> venv.remove()
        >>> Path(path).exists()
        False
    """

    def __init__(self, venv_path: PathLike) -> None:
        """Init the venv class. To create or update it, you can call extra functions.

        Args:
            venv_path(PathLike): Path of venv. E.g. `venv`

        Raises:
            FileNotFoundError: No folder found on defined path.
        """
        self.venv_path = Path(venv_path).resolve()
        """Path to venv prefix, e.g. .../venv"""

        if not self.venv_path.exists():
            self.venv_path.mkdir()

        self.venv_path_console_str = get_console_str_with_quotes(self.venv_path)

        if not self.venv_path.exists():
            self.venv_path.mkdir(parents=True, exist_ok=True)

        if platform.system() == "Windows":
            activate_path = self.venv_path / "Scripts" / "activate.bat"
            self.executable = self.venv_path / "Scripts" / "python.exe"
            self.executable_str = get_console_str_with_quotes(
                (self.venv_path / "Scripts" / "python.exe").as_posix()
            )
            self.create_command = f"python -m virtualenv {self.venv_path_console_str}"
            self.activate_command = get_console_str_with_quotes(activate_path.as_posix())
            scripts_path = self.venv_path / "Scripts"
        else:
            self.executable = self.venv_path / "bin" / "python"
            self.executable_str = get_console_str_with_quotes((self.venv_path / "bin" / "python").as_posix())
            self.create_command = f"python3 -m virtualenv {self.venv_path_console_str}"
            self.activate_command = f". {get_console_str_with_quotes(self.venv_path / 'bin' / 'activate')}"
            scripts_path = self.venv_path / "bin"

        self.installed = True if (self.executable).exists() else False

        self.scripts_path: Path = scripts_path
        """Path to the executables. Can be directly used in terminal. Some libraries cannot use
        ``python -m package`` syntax and therefore it can be called from scripts folder."""

        self.subprocess_prefix = f"{self.activate_command} {SHELL_AND} {self.executable_str} -m "
        """Run as module, so library can be directly call afterwards. Can be directly used in terminal. It can
        look like this for example::
        
            .../Scripts/activate.bat && .../venv/Scripts/python.exe -m
        """

    def create(self, verbose: bool = False) -> None:
        """Create virtual environment. If it already exists, it will be skipped and nothing happens.

        Args:
            verbose (bool, optional): If True, result of terminal command will be printed to console.
                Defaults to False.
        """
        if not self.installed:
            terminal_do_command(
                self.create_command,
                cwd=PROJECT_PATHS.root.as_posix(),
                shell=True,
                verbose=verbose,
                error_header="Venv creation failed",
            )

    def sync_requirements(
        self, requirements: Literal["infer"] | PathLike | Sequence[PathLike] = "infer", verbose: bool = False
    ) -> None:
        """Sync libraries based on requirements. Install missing, remove unnecessary.

        Args:
            requirements (Literal["infer"] | PathLike | Sequence[PathLike], optional): Define what libraries
                will be installed. If "infer", autodetected. Can also be a list of more files e.g
                `["requirements.txt", "requirements_dev.txt"]`. Defaults to "infer".
            verbose (bool, optional): If True, result of terminal command will be printed to console.
                Defaults to False.
        """
        self.install_library("pip-tools")
        requirements = get_requirements_files(requirements)

        requirements_content = ""

        for i in requirements:
            with open(i, "r") as req:
                requirements_content = requirements_content + "\n" + req.read()

        requirements_all_path = self.venv_path / "requirements_all.in"
        requirements_all_console_path_str = get_console_str_with_quotes(requirements_all_path)
        freezed_requirements_console_path_str = get_console_str_with_quotes(
            self.venv_path / "requirements.txt"
        )

        with open(requirements_all_path, "w") as requirement_libraries:
            requirement_libraries.write(requirements_content)

        pip_compile_command = (
            f"pip-compile {requirements_all_console_path_str} --output-file "
            f"{freezed_requirements_console_path_str} --quiet"
        )

        sync_commands = {
            pip_compile_command: "Creating joined requirements.txt file failed.",
            f"pip-sync {freezed_requirements_console_path_str} --quiet": "Requirements syncing failed.",
        }

        for i, j in sync_commands.items():
            terminal_do_command(f"{self.activate_command} {SHELL_AND} {i}", verbose=verbose, error_header=j)

    def list_packages(self) -> str:
        """Get list of installed libraries in the venv.

        The reason why it's meta coded via string parsing and not parsed directly is that it needs to be
        available from other venv as well.
        """
        result = subprocess.run(
            f"{self.activate_command} {SHELL_AND} {PYTHON} -m pip freeze",
            capture_output=True,
            check=True,
            shell=True,
        )
        output_str = result.stdout.decode().strip("\r\n")

        return output_str

    def install_library(self, name: str, verbose: bool = False) -> None:
        """Install package to venv with pip install.

        Args:
            verbose (bool, optional): If True, result of terminal command will be printed to console.
                Defaults to False.
        """
        command = f"{self.activate_command} {SHELL_AND} pip install {name}"
        terminal_do_command(command, shell=True, verbose=verbose, error_header="Library installation failed.")

    def uninstall_library(self, name: str, verbose: bool = False) -> None:
        """Uninstall package to venv with pip install.

        Args:
            verbose (bool, optional): If True, result of terminal command will be printed to console.
                Defaults to False.
        """
        command = f"{self.activate_command} {SHELL_AND} pip uninstall {name}"

        terminal_do_command(command, shell=True, verbose=verbose, error_header="Library removal failed")

    def remove(self) -> None:
        """Remove the folder with venv."""
        shutil.rmtree(self.venv_path.as_posix())

    def get_script_path(self, name: str) -> str:
        """Get script path such as pip for example."""
        if platform.system() == "Windows":
            return get_console_str_with_quotes(self.scripts_path / f"{name}.exe")
        else:
            return get_console_str_with_quotes(self.scripts_path / name)


def is_venv() -> bool:
    """True if run in venv, False if run in main interpreter directly."""
    return sys.base_prefix.startswith(sys.prefix)
