import os
import sys
import subprocess

PROC_LOG_PATH = "/tmp/njupy_proc_log.txt"

def add_pid_to_njupy_table(paths, pid):
    opening_flag = "a" if os.path.exists(PROC_LOG_PATH) else "w"

    with open(PROC_LOG_PATH, opening_flag) as f:
        f.write(paths[0] + " " + paths[1] + " " + str(pid) + "\n")


def kill_pid(pid):
    pass


def launch_detatched_process(args, paths, log_path):
    stderr = open(log_path, "a") if log_path else open("/dev/null", "w")

    process = subprocess.Popen(args, stdout=open('/dev/null', 'w'),
                               stderr=stderr,
                               preexec_fn=os.setpgrp,
                               shell=False)

    if paths is not None:
        add_pid_to_njupy_table(paths, process.pid)


def launch_and_wait_for_process(args, verbose):
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    return_code = process.poll()

    if return_code == 1:
        print(stderr.decode(sys.stderr.encoding))
        sys.exit(1)

    if verbose:
        print(stdout.decode(sys.stdin.encoding))


def launch_process(args, paths=None, log_path=None, detatch=False,
                   verbose=False):
    if detatch:
        launch_detatched_process(args, paths, log_path)
    else:
        launch_and_wait_for_process(args, verbose)
