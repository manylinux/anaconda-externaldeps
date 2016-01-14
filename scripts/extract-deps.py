import os
import json
import shutil
import tempfile
import argparse
from subprocess import check_output, Popen, PIPE

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def find_so_depinfo(package_dir):
    with open(os.path.join(package_dir, 'info', 'files')) as f:
        files = '\n'.join(os.path.join(package_dir, f.strip()) for f in f.readlines())

    with tempfile.SpooledTemporaryFile() as f:
        f.write(files.encode('utf-8'))

        for scriptname in ('find-requires', 'find-provides'):
            f.seek(0)
            stdout = Popen([os.path.join(THIS_DIR, scriptname)], stdin=f, stdout=PIPE).stdout.read()
            yield [fn.strip() for fn in stdout.decode('utf-8').splitlines()]


def analyze_package(package_fn):
    unpack_to = tempfile.mkdtemp()
    try:
        os.system('tar -xjf %s -C %s' % (package_fn, unpack_to))

        requires, provides = find_so_depinfo(unpack_to)
        return {
            'pkg_fn': os.path.basename(package_fn),
            'requires': requires,
            'provides': provides,
        }
    finally:
        shutil.rmtree(unpack_to)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('package')
    p.add_argument('output_fn')
    args = p.parse_args()

    with open(args.output_fn, 'w') as f:
        json.dump(analyze_package(args.package), f)


if __name__ == '__main__':
    main()
