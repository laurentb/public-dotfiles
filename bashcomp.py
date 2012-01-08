#!/usr/bin/env python
from __future__ import with_statement
from os import path, popen, system
import re

config_file = path.join(path.dirname(__file__), "bashcomp.wanted")

REGEXP = re.compile('^ +\[\d+\] +(?P<name>[^ ]+)(?P<enabled> \*)?$')

eselect = [REGEXP.match(line) \
        for line \
        in popen("eselect bashcomp list").read().strip().split('\n') \
        if REGEXP.match(line)]

available_completions = [line.groupdict()['name'] \
        for line \
        in eselect]

active_completions = [line.groupdict()['name'] \
        for line \
        in eselect \
        if line.groupdict().get('enabled')]

with open(config_file, "r") as f:
    wanted_completions = f.read().strip().split("\n")

completions = set(wanted_completions) - set(active_completions)
for completion in completions:
    if completion in available_completions:
        print "+%s" % completion
        system("eselect bashcomp enable %s" % completion)
    else:
        print "-%s" % completion
