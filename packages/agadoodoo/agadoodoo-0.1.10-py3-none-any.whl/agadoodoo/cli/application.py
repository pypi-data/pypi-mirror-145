import os, sys, subprocess


__BASE_DIR__ = os.path.dirname(os.path.abspath(__file__))


def get_cli_args():
    return sys.argv


def get_execution_for(path):
    cmd = [path]

    if sys.platform in ['win32', 'cygwin']:
        cmd.insert(0, sys.executable)
    return cmd


def main():
    args = get_cli_args()
    script_path = os.path.join(__BASE_DIR__, 'scripts', 'foo.py')

    print("sys.argv:", args)

    try:
        child = subprocess.Popen(
            get_execution_for(script_path)
        )
    except Exception as e:
        print(type(e), ":", str(e))
        return -1
    code = child.wait()

    print("execution finished")
    print(f"({script_path}): {code}")
    return 0