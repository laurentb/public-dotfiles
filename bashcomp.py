#!/usr/bin/env python
from __future__ import with_statement

import re
import sys
from os import listdir, path, popen, readlink, system, unlink

interactive = sys.stdin.isatty()
BRIGHT = '\x1b[1m' if interactive else ''
NORMAL = '\x1b[22m' if interactive else ''

config_file = path.join(path.dirname(__file__), "bashcomp.wanted")

REGEXP = re.compile('^ +\[\d+\] +(?P<name>[^ ]+)(?P<enabled> \*)?$')

eselect = [REGEXP.match(line)
           for line
           in popen("eselect bashcomp list").read().strip().splitlines()
           if REGEXP.match(line)]

available_completions = [line.groupdict()['name']
                         for line
                         in eselect]

active_completions = [line.groupdict()['name']
                      for line
                      in eselect
                      if line.groupdict().get('enabled')]

with open(config_file, "r") as f:
    wanted_completions = f.read().strip().splitlines()

for completion in available_completions:
    if completion in wanted_completions \
            and completion not in active_completions:
        print "%s+%s%s" % (BRIGHT, NORMAL, completion),
        system("eselect bashcomp enable %s" % completion)
    if completion not in wanted_completions \
            and completion in active_completions:
        print "%s-%s%s" % (BRIGHT, NORMAL, completion),


BCPATH = path.expanduser('~/.bash_completion.d')
for completion in listdir(BCPATH):
    try:
        if not path.exists(path.join(BCPATH, readlink(path.join(BCPATH, completion)))):
            print "%s_%s%s" % (BRIGHT, NORMAL, completion),
            unlink(path.join(BCPATH, completion))
    except OSError:
        pass
