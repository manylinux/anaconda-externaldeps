import os
import glob
import json
import argparse
import itertools
from fnmatch import fnmatch
from conda.utils import memoize
from conda.resolve import MatchSpec, Package
from conda.api import get_index, _fn2fullspec, _fn2spec


def load_index(cachefn):
    if os.path.exists(cachefn):
        with open(cachefn) as f:
            return json.load(f)
    else:
        index = get_index()
        with open(cachefn, 'w') as f:
            json.dump(index, f)
        return index

class BuildNumberMatcher(object):
    def __init__(self, index):
        self.index = index

    @memoize
    def _matches(self, pattern):
        fns = [fn for fn in self.index.keys()
                if fnmatch(fn, pattern)]
        return sorted([Package(fn, self.index[fn]) for fn in fns])

    def is_latest_build_number(self, fn):
        pkg =  Package(fn, self.index[fn])
        if '_' not in pkg.build:
            return True

        pattern = pkg.name + '-' + pkg.version + '-' + \
                  pkg.build.split('_')[0] + \
                  '_*' + '.tar.bz2'
        return pkg == self._matches(pattern)[-1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('files_glob')
    p.add_argument('--index-cache', default='.index-cache.json')
    args = p.parse_args()
    index = load_index(args.index_cache)
    matcher = BuildNumberMatcher(index)

    for i, path in enumerate(glob.iglob(args.files_glob)):
        fn = os.path.basename(path)

        if matcher.is_latest_build_number(fn):
            print(path)


if __name__ == '__main__':
    main()
