import logging
import os
import pathlib
from shutil import rmtree

from git import Repo
from yaspin import yaspin

from .envbuild_withreqs import EnvBuilderWithReqs

logger = logging.getLogger(__name__)


def new_project(project_dir: str, dont_create_venv: bool) -> None:
    if os.path.isdir(project_dir):
        logger.error("Directory already exists, please choose a new directory path")
        return False

    project_name = pathlib.Path(project_dir).name

    with yaspin(text="Cloning repo").dots10:
        Repo.clone_from("https://github.com/ryanlinnit-sky/mite-demo.git", project_dir)

    write_setup(os.path.join(project_dir, "setup.cfg"), project_name)

    rmtree(os.path.join(project_dir, ".git"))

    r = Repo.init(project_dir)
    r.index.add(["*", ".*"])
    r.index.commit("initial commit")

    if not dont_create_venv:
        new_venv(project_name, project_dir)


def write_setup(setup_cfg_filepath: str, project_name: str) -> None:
    with open(setup_cfg_filepath, "r") as fp:
        setup_cfg = fp.readlines()

    for index, line in enumerate(setup_cfg):
        if "mite-demo" in line:
            setup_cfg[index] = line.replace("mite-demo", project_name)

    with open(setup_cfg_filepath, "w") as fp:
        fp.writelines(setup_cfg)


def new_venv(project_name: str, project_dir: str):
    with yaspin(text="Creating virtual environment").dots10 as spinner:
        new_venv = EnvBuilderWithReqs(
            system_site_packages=False,
            clear=False,
            symlinks=False,
            upgrade=False,
            with_pip=True,
            prompt=None,
            project_dir=project_dir,
            spinner=spinner,
        )

        venv_dir = os.path.join(pathlib.Path.home(), ".virtualenvs", project_name)
        new_venv.create(venv_dir)

    logging.info(
        f"New virtual environment created. Activate with the command: source {venv_dir}/bin/activate"
    )
