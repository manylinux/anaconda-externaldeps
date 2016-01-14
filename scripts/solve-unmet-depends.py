import os
import json
import logging
import functools
import argparse
import conda.config
from pprint import pprint
from conda.api import get_index, _fn2fullspec
from conda.resolve import Resolve, MatchSpec
logging.disable(logging.CRITICAL)


def loadjsonl(fn):
    with open(fn) as f:
        for line in f:
            yield json.loads(line)


def loadlogfile(fn):
    return {rec['pkg_fn']: rec for rec in loadjsonl(fn)}


def setreduce(sets):
    return functools.reduce(set.union, sets, set())


def load_index(cachefn):
    if os.path.exists(cachefn):
        with open(cachefn) as f:
            return json.load(f)
    else:
        index = get_index()
        with open(cachefn, 'w') as f:
            json.dump(index, f)
        return index


def main():
    p = argparse.ArgumentParser()
    p.add_argument('pkg_fn', type=os.path.basename)
    p.add_argument('output_fn')
    p.add_argument('--dependsdata')
    p.add_argument('--index-cache', default='.index-cache.json')
    
    args = p.parse_args()
    
    r = Resolve(load_index(args.index_cache))
    with open(args.dependsdata) as f:
        dependsdata = json.load(f)
    
    try:
        plan = r.solve([_fn2fullspec(args.pkg_fn)],
                       features=set(),
                       installed=['anaconda 2.4.1'],
                       update_deps=False)
        # print(plan)
    except SystemExit:
        print('\n\n========wtf is this!\n\n')
        with open(args.output_fn, 'w') as f:
            json.dump({'pkg_fn': args.pkg_fn, 'unmet_depends': []}, f)
            return

    depends_provides = setreduce(dependsdata[fn]['provides'] for fn in plan)
    # requires = set(dependsdata[args.pkg_fn]['requires'])
    requires = setreduce(dependsdata[fn]['requires'] for fn in plan)

    output = {'pkg_fn': args.pkg_fn, 'unmet_depends': list(requires - depends_provides)}
    with open(args.output_fn, 'w') as f:
        json.dump(output, f)             
    

if __name__ == '__main__':
    main()
