import os
import argparse
import glob
from . import read_compile_write

def find_pbats(path):
    paths = []
    for n in os.listdir(path):
        if os.path.splitext(n)[1] != '.pbat':
            continue
        p = os.path.join(path, n)
        paths.append(p)
    return paths

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs='*', help='file, directory or glob')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    paths = []
    for path in args.path:
        if glob.has_magic(path):
            for path_ in glob.glob(path):
                paths.append(path_)
        else:
            if os.path.isdir(path):
                paths += find_pbats(path)
            else:
                paths.append(path)

    if len(args.path) == 0:
        paths = find_pbats('.')

    if len(paths) > 1 and args.output is not None:
        print("--output argument requires one input")
        exit(1)

    for path in paths:
        src = path
        if args.output is not None:
            dst = args.output
        else:
            dirname = os.path.dirname(path)
            basename = os.path.splitext(os.path.basename(path))[0]
            dst = os.path.join(dirname, basename + '.bat')
        if src == dst:
            print("src == dst", src)
            exit(1)

        try:
            read_compile_write(src, dst)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
    