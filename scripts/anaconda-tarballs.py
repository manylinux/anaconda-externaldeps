import os
import logging
from conda.api import get_index
from conda.resolve import Resolve, MatchSpec
logging.disable(logging.CRITICAL)


def main():
    r = Resolve(get_index())
    plan = r.solve(['anaconda 2.4.1'],
                   features=set(),
                   installed=set(),
                   update_deps=True)
    for fn in plan:
        print(os.path.join('tarballs', fn))

    
if __name__ == '__main__':
    main()
