import argparse

from ur_py_ctl.send_script import send_script as send_script_func

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Send program to UR")
    # parser.add_argument("path", type=pathlib.Path, help="script file")

    # args = parser.parse_args()

    # if not args.path.exists():
    #    raise FileNotFoundError()

    send_script_func()
