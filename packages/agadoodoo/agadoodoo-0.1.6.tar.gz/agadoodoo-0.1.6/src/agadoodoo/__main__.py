import os, sys, subprocess
from re import sub


__BASE_DIR__ = os.path.dirname(os.path.abspath(__file__))


def get_execution_for(path):
    cmd = [path]

    if sys.platform in ['win32', 'cygwin']:
        cmd.insert(0, 'python')
    return cmd


def main(argv):
    script_path = os.path.join(__BASE_DIR__, 'scripts', 'foo.py')

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


if __name__ == '__main__':
    if(len(sys.argv) <= 1):
        exit(-1)
    exit(main(sys.argv))
