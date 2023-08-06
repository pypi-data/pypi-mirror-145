import logging
import shutil
import venv
from subprocess import PIPE, Popen
from threading import Thread

logger = logging.getLogger(__name__)


class EnvBuilderWithReqs(venv.EnvBuilder):
    def __init__(self, *args, **kwargs):
        self.project_dir = kwargs["project_dir"]
        self.spinner = kwargs["spinner"]
        del kwargs["project_dir"]
        del kwargs["spinner"]

        super().__init__(*args, **kwargs)

    def install_reader(self, stream):
        if self.spinner:
            self.spinner.text = "Installing packages"

        # Get the terminal width, so our output doesn't spill onto another line
        terminal_columns = shutil.get_terminal_size((80, 20)).columns - 25

        while True:
            s = stream.readline()
            if not s:
                break

            proc_output = s.decode("utf-8").strip()[:terminal_columns]
            if self.spinner:
                self.spinner.text = f"Installing packages [{proc_output}]"

        stream.close()

    def post_setup(self, context):
        pip_install_requirements = [
            context.env_exe,
            "-m",
            "pip",
            "install",
            "-e",
            ".",
        ]
        p = Popen(
            pip_install_requirements, stdout=PIPE, stderr=PIPE, cwd=self.project_dir
        )
        t1 = Thread(target=self.install_reader, args=(p.stdout,))
        t1.start()
        p.wait()
        t1.join()
        if p.returncode != 0:
            logger.error("Error when install python packages")
