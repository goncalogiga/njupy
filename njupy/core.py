import os
import sys
import shutil
from shutil import copyfile
from njupy.process_runner import launch_process

DAEMON_PATH = "/tmp/njupy_daemon_on"

class Core():
    def __init__(self, notebook_name, notebook_path_str, verbose):
        self.notebook_name = notebook_name
        self.notebook_path_str = notebook_path_str
        self.verbose = verbose

    def create_sync_files(self):
        # renaming the notebook
        filename, file_extension = os.path.splitext(self.notebook_path_str)
        file_extension = file_extension[1:]

        if file_extension != "ipynb":
            raise Exception("File extension should be 'ipynb', not '%s'."
                            % file_extension)

        os.rename(self.notebook_path_str, filename + ".sync.ipynb")

        self.notebook_path_str = filename + ".sync.ipynb"

        synced_notebook = filename + ".sync.py"

        stdout_str = launch_process(['jupytext', '--sync', self.notebook_path_str,
                                     '-o', synced_notebook],
                                     verbose=self.verbose)

        if not os.path.exists(synced_notebook):
            print("[njupy] Aborted since no python file was dumped by jupytext.")
            print("[njupy] Please make sure the notebook is compatible with jupytext.")
            retrieve_notebook(self.notebook_path_str)
            sys.exit(1)

        print("[njupy] Added a python file '%s' linked to the notebook."
              % synced_notebook)

    def launch_jupyter(self):
        launch_process(['jupyter', 'notebook', self.notebook_path_str],
                       path=self.notebook_path_str,
                       detatch=True)

        print("[njupy] Launched detached process running the notebook")


def retrieve_notebook(notebook_path_str):
    filename, _ = os.path.splitext(notebook_path_str)
    filename, _ = os.path.splitext(filename)

    os.rename(notebook_path_str, filename + ".ipynb")

    new_name = filename + ".ipynb"

    print(f"[njupy] Renamed notebook back to '{new_name}'")
