import os
import sys
import shutil
import config
from shutil import copyfile
from process_runner import launch_process

DAEMON_PATH = "/tmp/njupy_daemon_on"

class Core():
    def __init__(self, notebook_name, notebook_path_str, verbose):
        self.notebook_name = notebook_name
        self.notebook_path_str = notebook_path_str
        self.verbose = verbose

    def create_tmp_files(self):
        clean_name = self.notebook_path_str.replace("/", "_").replace(".", "_")

        self.path_in_tmp = os.path.join("/tmp/", "njupy_" + clean_name)

        if os.path.exists(self.path_in_tmp):
            raise Exception("njupy is already running for directory '%s'"
                            % self.notebook_path_str)

        os.mkdir(self.path_in_tmp)

        self.ipynb_path = os.path.join(self.path_in_tmp,
                                       self.notebook_name + ".sync.ipynb")
        self.py_path = os.path.join(self.path_in_tmp,
                                    self.notebook_name + ".sync.py")

        copyfile(self.notebook_path_str, self.ipynb_path)

        launch_process(['jupytext', '--sync', self.ipynb_path],
                       verbose=self.verbose)

        link = self.notebook_name + ".sync.py"

        try:
            os.symlink(self.py_path, link)
        except FileExistsError:
            shutil.rmtree(self.path_in_tmp)
            raise Exception(f"A file named '{link}' already exists. Please remove it and try again.")

        print("[njupy] Added a python file '%s' linked to the notebook."
              % self.notebook_name + ".sync.py")


    def launch_jupyter(self):
        if self.verbose:
            log_path = os.path.join(self.path_in_tmp, "log.log")
        else:
            log_path = None

        launch_process(['jupyter', 'notebook', self.ipynb_path],
                       paths=[self.notebook_path_str, self.ipynb_path],
                       log_path=log_path,
                       detatch=True)

        print("[njupy] Launched detached process running the notebook")


    def launch_njupy_daemon(self):
        if os.path.exists(DAEMON_PATH):
            return

        launch_process(
            ["python3", os.path.join(config.NJUPY_PATH, "njupy_daemon.py")],
            detatch=True
        )

        with open(DAEMON_PATH, 'w'):
            pass
