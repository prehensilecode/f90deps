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
                if debug_p:
                    print("AHA! {}: {}".format(fortfile, m.group(1)))
                modules_used.add(m.group(1))

    return "{}: {}".format(re.sub('\.F$', '.o', fortfile.parts[-1]), ' '.join(modules_used))


def main(directory):
    global debug_p


    if debug_p:
        print("directory = {}".format(directory))
        if os.path.isdir(directory):
            print("YAY {} is a directory".format(directory))


    p = Path(directory)
    fortfiles = list(p.glob('**/*.F'))
    for f in fortfiles:
        print(gen_depline(f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", default=".", help="Directory containing .F files")
    args = parser.parse_args()
    
    main(args.directory)

