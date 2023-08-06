"""Module with functions for 'project_utils' subpackage."""

from __future__ import annotations
from typing import Sequence, Any
import os
import sys

from typing_extensions import Literal

from .. import tests
from .. import venvs
from mypythontools.config import ConfigBase, MyProperty
from mypythontools.misc import GLOBAL_VARS, EMOJIS, print_progress
from mypythontools.paths import PathLike
from mypythontools.types import validate_sequence
from ..deploy import deploy_to_pypi
from .project_utils_functions import (
    get_version,
    git_push,
    reformat_with_black,
    set_version,
    docs_regenerate,
)

# Lazy loaded
# from git import Repo

from mypythontools_cicd.project_paths import PROJECT_PATHS


class PipelineConfig(ConfigBase):
    """Allow to setup CICD pipeline."""

    @MyProperty
    def do_only() -> Literal[
        None, "reformat", "test", "docs", "sync_requirements", "commit_and_push_git", "deploy"
    ]:
        """Run just single function from pipeline, ignore the others.

        Type:
            Literal[
                None, "reformat", "test", "docs", "sync_requirements", "commit_and_push_git", "deploy"
            ]

        Default:
            None

        Reason for why to call it form here and not directly is to be able to use sys args or single command
        line entrypoint.
        """
        return None

    @MyProperty
    @staticmethod
    def reformat() -> bool:
        """Reformat all python files with black. Setup parameters in pyproject.toml.

        Type:
            bool

        Default:
            True.
        """
        return True

    @MyProperty
    @staticmethod
    def test() -> bool:
        """Run pytest tests.

        Type:
            bool

        Default:
            True
        """
        return True

    @MyProperty
    @staticmethod
    def test_options() -> None | dict:
        """Check tests module and function run_tests for what parameters you can use.

        Type:
            None | dict

        Default:
            None

        For example:
            >>> {"virtualenvs": ["venv/37", "venv/310], "test_coverage": True, "verbose": False}
        """
        return None

    @MyProperty
    @staticmethod
    def version() -> None | str:
        """Overwrite __version__ in __init__.py.

        Type:
            str

        Default:
            'increment'.

        Version has to be in format like '1.0.3' three digits and two dots. If 'None', nothing will happen. If
        'increment', than it will be updated by 0.0.1..
        """
        return "increment"

    @MyProperty
    @staticmethod
    def docs() -> bool:
        """Whether generate sphinx apidoc and generate rst files for documentation. Some files in docs source
        can be deleted - check `docs` docstrings for details.

        Type:
            bool

        Default:
            True
        """
        return True

    @MyProperty
    @staticmethod
    def sync_requirements() -> None | Literal["infer"] | PathLike | Sequence[PathLike]:
        """Check requirements.txt and update all the libraries.

        Type:
            None | Literal["infer"] | PathLike | Sequence[PathLike]

        Default:
            None

        You can use path to requirements, list of paths or bool value. If True, then path is inferred.
        """
        return None

    @MyProperty
    @staticmethod
    def commit_and_push_git() -> bool:
        """Whether push to github or not.

        Type:
            bool

        Default:
            True
        """
        return True

    @MyProperty
    @staticmethod
    def commit_message() -> str:
        """Commit message.

        Type:
            str

        Default:
            'New commit'
        """
        return "New commit"

    @MyProperty
    @staticmethod
    def tag() -> str:
        """Tag. E.g 'v1.1.2'. If '__version__', get the version.

        Type:
            str

        Default:
            '__version__'
        """
        return "__version__"

    @MyProperty
    @staticmethod
    def tag_message() -> str:
        """Tag message.

        Type:
            bool

        Default:
            'New version'
        """
        return "New version"

    @MyProperty
    @staticmethod
    def deploy() -> bool:
        """Deploy to PYPI.

        `TWINE_USERNAME` and `TWINE_PASSWORD` are used for authorization.

        Type:
            bool

        Default:
            False
        """
        return False

    @MyProperty
    @staticmethod
    def allowed_branches() -> None | Sequence[str]:
        """Pipeline runs only on defined branches.

        Type:
            None | Sequence[str]

        Default:
            ["master", "main"]
        """
        return ["master", "main"]

    @MyProperty
    @staticmethod
    def verbosity() -> Literal[0, 1, 2]:
        """Pipeline runs only on defined branches.

        Type:
            Literal[0, 1, 2]

        Default:
            1
        """
        return 1


def project_utils_pipeline(
    config: None | PipelineConfig = None,
    do_only: Literal[
        None,
        "reformat",
        "test",
        "docs",
        "sync_requirements",
        "commit_and_push_git",
        "deploy",
    ] = None,
    reformat: bool = True,
    test: bool = True,
    test_options: None | dict[str, Sequence[PathLike]] | dict[str, Any] = None,
    version: None | str = "increment",
    docs: bool = True,
    sync_requirements: None | Literal["infer"] | PathLike | Sequence[PathLike] = None,
    commit_and_push_git: bool = True,
    commit_message: str = "New commit",
    tag: str = "__version__",
    tag_message: str = "New version",
    deploy: bool = False,
    allowed_branches: None | Sequence[str] = ("master", "main"),
    verbosity: Literal[0, 1, 2] = 1,
) -> None:
    """Run pipeline for pushing and deploying app.

    Can run tests, generate rst files for sphinx docs, push to github and deploy to pypi. All params can be
    configured not only with function params, but also from command line with params and therefore callable
    from terminal and optimal to run from IDE (for example with creating simple VS Code task).

    Some function suppose some project structure (where are the docs, where is __init__.py etc.).
    If you are issuing some error, try functions directly, find necessary paths in parameters
    and set paths that are necessary in paths module.

    Note:
        Beware that pushing to git create a commit and add all the changes, not only the staged ones.

    When using sys args for boolean values, always define True or False.

    There is command line entrypoint called `mypythontools_cicd`. After mypythontools is installed, you can
    use it in terminal like::

        mypythontools_cicd --do_only reformat

    Args:
        config (None | PipelineConfig, optional): It is possible to configure all the params with CLI args
            from terminal. Just create script, where create config, use 'config.with_argparse()' and call
            project_utils_pipeline(config=config). Example usage 'python your_script.py --deploy True'
        do_only (Literal[None, "reformat", "test", "docs", "sync_requirements", "commit_and_push_git", "deploy"], optional):
            Run just single function from pipeline, ignore the others. Reason for why to call it form here and
            not directly is to be able to use sys args or single command line entrypoint. Defaults to None.
        reformat (bool, optional): Reformat all python files with black. Setup parameters in
            `pyproject.toml`, especially setup `line-length`. Defaults to True.
        test (bool, optional): Whether run pytest tests. Defaults to True.
        test_options (None | dict, optional): Parameters of tests function e.g.
            ``{"virtualenvs": ["venv/37", "venv/310], "test_coverage": True, "verbose": False}``.
            Defaults to None.
        version (None | str, optional): New version. E.g. '1.2.5'. If 'increment', than it's auto
            incremented. E.g from '1.0.2' to 'v1.0.3'. If empty string "" or not value arg in CLI,
            then version is not changed. 'Defaults to "increment".
        docs(bool, optional): Whether generate sphinx apidoc and generate rst files for documentation.
            Some files in docs source can be deleted - check `docs` docstrings for details.
            Defaults to True.
        sync_requirements(None | Literal["infer"] | PathLike | Sequence[PathLike], optional): Check
            requirements.txt and update all the libraries. Defaults to False.
        commit_and_push_git (bool, optional): Whether push repository on git with commit_message, tag and tag
            message. Defaults to True.
        commit_message (str, optional): Git message. Defaults to 'New commit'.
        tag (str, optional): Used tag. If tag is '__version__', than updated version from __init__
            is used.  If empty string "" or not value arg in CLI, then tag is not created.
            Defaults to __version__.
        tag_message (str, optional): Tag message. Defaults to New version.
        deploy (bool, optional): Whether deploy to PYPI. `TWINE_USERNAME` and `TWINE_PASSWORD`
            are used for authorization. Defaults to False.
        allowed_branches (None | Sequence[str], optional): As there are stages like pushing to git or to PyPi,
            it's better to secure it to not to be triggered on some feature branch. If not one of
            defined branches, error is raised. Defaults to ("master", "main").
        verbosity (Literal[0, 1, 2], optional): How much information print to console. 0 prints just errors,
            1 prints when starting new step, 2 prints every stdout to console. Defaults to 1.

    Example:
        Recommended use is from IDE (for example with Tasks in VS Code). Check utils docs for how to use it.
        You can also use it from python... ::

            if __name__ == "__main__":
                project_utils_pipeline(commit_and_push_git=False, deploy=False, allowed_branches=None)

        It's also possible to use CLI and configure it via args. This example just push repo to PyPi. ::

            python path-to-project/utils/push_script.py --do_only deploy
    """
    if not config:
        config = PipelineConfig()
        config.update(
            {
                "do_only": do_only,
                "reformat": reformat,
                "test": test,
                "test_options": test_options,
                "version": version,
                "sync_requirements": sync_requirements,
                "docs": docs,
                "commit_and_push_git": commit_and_push_git,
                "commit_message": commit_message,
                "tag": tag,
                "tag_message": tag_message,
                "deploy": deploy,
                "allowed_branches": allowed_branches,
                "verbosity": verbosity,
            }
        )

    if not GLOBAL_VARS.is_tested:
        config.with_argparse()

    if config.do_only:
        config.update(
            {
                "reformat": False,
                "test": False,
                "docs": False,
                "sync_requirements": None,
                "commit_and_push_git": False,
                "deploy": False,
                "version": None,
            }
        )
        config.update({config.do_only: True})

        if config.verbosity == 1:
            config.verbosity = 0

    verbose = True if config.verbosity == 2 else False
    progress_is_printed = config.verbosity > 0

    if config.allowed_branches:
        import git.repo
        from git.exc import InvalidGitRepositoryError

        validate_sequence(allowed_branches, "allowed_branches")

        try:
            branch = git.repo.Repo(PROJECT_PATHS.root.as_posix()).active_branch.name
        except InvalidGitRepositoryError:
            raise RuntimeError(
                "Loading of git project failed. Verify whether running pipeline from correct path. If "
                "checks branch with `allowed_branches', there has to be `.git` folder available."
            ) from None

        if branch not in config.allowed_branches:
            raise RuntimeError(
                "Pipeline started on branch that is not allowed."
                "If you want to use it anyway, add it to allowed_branches parameter and "
                "turn off changing version and creating tag."
            )

    # Do some checks before run pipeline so not need to rollback eventually
    if config.deploy:
        usr = os.environ.get("TWINE_USERNAME")
        pas = os.environ.get("TWINE_PASSWORD")

        if not usr or not pas:
            raise KeyError("Setup env vars TWINE_USERNAME and TWINE_PASSWORD to use deploy.")

    if config.sync_requirements:
        print_progress("Syncing requirements", progress_is_printed)

        if not venvs.is_venv:
            raise RuntimeError("'sync_requirements' available only if using virtualenv.")
        my_venv = venvs.Venv(sys.prefix)
        my_venv.create()
        my_venv.sync_requirements(config.sync_requirements, verbose=verbose)

    if config.test:
        print_progress("Testing", progress_is_printed)

        if not config.test_options:
            config.test_options = {}

        tests.run_tests(**config.test_options, verbosity=verbosity)

    if config.reformat:
        print_progress("Reformatting", progress_is_printed)
        reformat_with_black()

    if config.version and config.version != "None":
        print_progress("Setting version", progress_is_printed)
        original_version = get_version()
        set_version(config.version)

    try:
        if config.docs:
            print_progress("Sphinx docs generation", progress_is_printed)
            docs_regenerate(verbose=verbose)

        if config.commit_and_push_git:
            print_progress("Pushing to github", progress_is_printed)
            git_push(
                commit_message=config.commit_message,
                tag=config.tag,
                tag_message=config.tag_message,
                verbose=verbose,
            )

    except Exception as err:  # pylint: disable=broad-except
        if config.version:
            set_version(original_version)  # type: ignore

        raise RuntimeError(
            f"{3 * EMOJIS.DISAPPOINTMENT} Utils pipeline failed {3 * EMOJIS.DISAPPOINTMENT} \n\n"
            "Original version restored. Nothing was pushed to repo, you can restart pipeline."
        ) from err

    try:
        if config.deploy:
            print_progress("Deploying to PyPi", progress_is_printed)
            deploy_to_pypi()

    except Exception as err:  # pylint: disable=broad-except
        raise RuntimeError(
            f"{3 * EMOJIS.DISAPPOINTMENT} Deploy failed {3 * EMOJIS.DISAPPOINTMENT} \n\n"
            "Already pushed to repository. Deploy manually. Version already changed.",
        ) from err

    print_progress(f"{3 * EMOJIS.PARTY} Finished {3 * EMOJIS.PARTY}", True)
