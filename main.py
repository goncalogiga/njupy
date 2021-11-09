import os
import sys
import click
import process_runner
from core import Core

def list_of_kernels(show=True):
    if not os.path.exists(process_runner.PROC_LOG_PATH):
        if show:
            print("[njupy] No kernels running.")
        return None

    kernels = []

    if show:
        print("[njupy] List of running kernels:")
    with open(process_runner.PROC_LOG_PATH, "r") as f:
        kernels = f.readlines()

        for kernel in kernels:
            kernel = kernel.split(" ")
            path, pid = kernel[0], kernel[2]
            if show:
                print(f"> {path} [pid={pid}]")
            kernels.append(pid)

    return kernels


@click.command()
@click.argument('notebook', nargs=-1, type=click.File('r'))
@click.option('--liston', is_flag=True, default=False, metavar='<liston>',
              help='Show the list of running jupter kernels.')
@click.option('--kill', default=None, metavar='<kill>',
              help='A PID of a kernel you wish to kill')
@click.option('--verbose', is_flag=True, default=False, metavar='<verbose>',
              help='Print stdout for each sub process executed.')
def main(notebook, liston, kill, verbose):
    if liston:
        list_of_kernels()

    if kill:
        if kill not in list_of_kernels(show=False):
            print(f"[njupy] PID {kill} is not in the list of kernels.")
            list_of_kernels()
        else:
            if len(list_of_kernels(show=False)) == 1:
                os.remove(core.DAEMON_PATH)
            process_runner.kill_pid(kill)
            print(f"[njupy] Killed jupyter kernel of id '{kill}'")

    if notebook:
        notebook_path = os.path.join(os.getcwd(), notebook[0].name)
        notebook_name = notebook[0].name.split("/")[-1].split(".")[0]

        njupy_core = Core(notebook_name, notebook_path, verbose)

        njupy_core.create_tmp_files()

        njupy_core.launch_jupyter()

        njupy_core.launch_njupy_daemon()


if __name__ == '__main__':
    main()
