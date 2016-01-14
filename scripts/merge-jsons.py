import os
import json
import glob
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_glob')
    p.add_argument('output_fn')
    args = p.parse_args()
    
    depdata = {}
    for fn in glob.glob(args.input_glob):
        with open(fn) as f:
            record = json.load(f)

        pkg_fn = record['pkg_fn']
        depdata[pkg_fn] = record

    with open(args.output_fn, 'w') as f:
        json.dump(depdata, f)
        

if __name__ == '__main__':
    main()
