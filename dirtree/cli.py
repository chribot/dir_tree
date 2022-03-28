import os
import sys

def get_path_from_args():
    arg_count = len(sys.argv) - 1
    if arg_count == 1:
        path = sys.argv[1]
        if os.access(path, os.R_OK):
            return path
    return os.getcwd()

def get_abspath_from_args():
    return os.path.abspath( get_path_from_args() )


if __name__ == "__main__":
    path = get_path_from_args()
    print( path )