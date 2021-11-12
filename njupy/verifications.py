import sys
import subprocess


test_cmds = [
    ["jupytext", "-h"],
    ["jupyter", "nbextension", "list"],
    ["jupyter", "serverextension", "list"]
]

find = [
    None,
    "jupyter_ascending",
    "jupyter_ascending"
]

err_msgs = [
    """Jupytext is not installed.""",
    """Could not find jupyter_ascending in jupyter extensions.
    Please install it with:
    $ jupyter nbextension install jupyter_ascending --sys-prefix --py

    and enable it with:
    $ jupyter nbextension enable jupyter_ascending --sys-prefix --py""",
    """Could not find jupyter_ascending in jupyter's server extension.
    Please enable it with:
    $ jupyter serverextension enable jupyter_ascending --sys-prefix --py"""
]


def verify_fn():

    for k, args in enumerate(test_cmds):
        cmd_as_str = ' '.join(args)
        print("[njupy diagnostic] Test (%d) - %s... " % (k, cmd_as_str), end="")

        process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        return_code = process.poll()

        if find[k] is not None and find[k] not in stdout.decode(sys.stdout.encoding):
            print("\033[91mfailed.\033[0m")
            print(err_msgs[k])
            sys.exit(1)

        if return_code == 1:
            print("\033[91mfailed.\033[0m")
            print(err_msgs[k])
            print("Traceback:")
            print(stderr.decode(sys.stderr.encoding))
            sys.exit(1)

        print("\033[92mOK.\033[0m")
