#!/usr/bin/env python3.4

import sys
import os
import re
import glob
from pathlib import Path
import argparse

debug_p = False

def gen_depline(fortfile):
    global debug_p

    usemodpat = re.compile(r'^\s*USE\s+([a-zA-Z]+)')

    if debug_p:
        print('gen_depline: working on {}'.format(fortfile))
        if usemodpat.search('       USE vaspxml'):
            print("hello")
        else:
            print("goodbye")

        if usemodpat.search('USE vaspxml'):
            print("foo")
        else:
            print("bar")

    with fortfile.open(mode='r') as ff:
        modules_used = set()
        for l in ff:
            m = usemodpat.match(l)
            if m:
                modules_used.add(''.join([m.group(1), '.mod']))

    return "{}: {}".format(re.sub('\.F$', '.o', fortfile.parts[-1]), ' '.join(modules_used))


def main(directory):
    global debug_p

    p = Path(directory)
    fortfiles = list(p.glob('**/*.F'))
    for f in fortfiles:
        print(gen_depline(f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", default=".", help="Directory containing .F files")
    args = parser.parse_args()
    
    main(args.directory)

