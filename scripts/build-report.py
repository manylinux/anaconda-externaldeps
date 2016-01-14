import os
import argparse
import json
import functools
from conda.utils import memoized
from subprocess import check_output
from pprint import pprint
from collections import OrderedDict


def main():
    p = argparse.ArgumentParser()
    p.add_argument('unmet_depends', help='unmet-depends.json file')
    args = p.parse_args()

    with open(args.unmet_depends) as f:
        data = json.load(f)

    unmet_depends = set()
    for pkg_fn in data:
        unmet_depends.update(data[pkg_fn]['unmet_depends'])

    dep2pkgs = {}
    for dep in unmet_depends:
        pkgs = [pkg_fn for (pkg_fn, record) in data.items() if dep in record['unmet_depends']]
        dep2pkgs[dep] = pkgs

    # pprint(dep2pkgs)
    sorted_deps = sorted(dep2pkgs.keys(), key=lambda k: len(dep2pkgs[k]), reverse=True)
    odeps = OrderedDict()
    for dep in sorted_deps:
        n = len(dep2pkgs[dep])
        odeps[dep] = sorted([fn[:-8] for fn in dep2pkgs[dep]])

    print(json.dumps(odeps, indent=4))
        

if __name__ == '__main__':
    main()
