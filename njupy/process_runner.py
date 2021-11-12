import os
import signal
import sys
import subprocess

PROC_LOG_PATH = "/tmp/njupy_proc_log.txt"


def add_pid_to_njupy_table(path, pid):
    opening_flag = "a" if os.path.exists(PROC_LOG_PATH) else "w"

    with open(PROC_LOG_PATH, opening_flag) as f:
        f.write(path + " " + str(pid) + "\n")


def kill_pid(pid):
    os.kill(int(pid), signal.SIGTERM)


def launch_detatched_process(args, path, log_path):
    stderr = open(log_path, "a") if log_path else open("/dev/null", "w")

    process = subprocess.Popen(args, stdout=open('/dev/null', 'w'),
                               stderr=stderr,
                               preexec_fn=os.setpgrp,
                               shell=False)

    add_pid_to_njupy_table(path, process.pid)


def launch_and_wait_for_process(args, verbose):
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    return_code = process.poll()

    print("\033[93m" + stderr.decode(sys.stderr.encoding) + "\033[0m")

    if return_code == 1:
        sys.exit(1)

    if verbose:
        print(stdout.decode(sys.stdin.encoding))

    return stdout.decode(sys.stdin.encoding)


def launch_process(args, path=None, log_path=None, detatch=False,
                   verbose=False):
    if detatch:
        launch_detatched_process(args, path, log_path)
    else:
        launch_and_wait_for_process(args, verbose)
