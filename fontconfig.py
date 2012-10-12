#!/usr/bin/env python
from __future__ import with_statement
from os import path, popen, system
import re
import sys

interactive = sys.stdin.isatty()
BRIGHT = '\x1b[1m' if interactive else ''
NORMAL = '\x1b[22m' if interactive else ''

config_file = path.join(path.dirname(__file__), "fontconfig.wanted")

REGEXP = re.compile('^ +\[\d+\] +(?P<name>[^ ]+)\.conf(?P<enabled> \*)?$')
NUMRE = re.compile('\d+-(?P<name>[^ ]+)')

eselect = [REGEXP.match(line)
           for line
           in popen("eselect fontconfig list").read().strip().splitlines()
           if REGEXP.match(line)]

available_fonts = [line.groupdict()['name']
                   for line
                   in eselect]

active_fonts = [line.groupdict()['name']
                for line
                in eselect
                if line.groupdict().get('enabled')]

with open(config_file) as f:
    raw_wanted_fonts = f.read().strip().splitlines()


# translate non-numbered wants
def full(wanted_font):
    if wanted_font in available_fonts:
        yield wanted_font
    else:
        for font in available_fonts:
            if NUMRE.match(font).groupdict()['name'] == wanted_font:
                yield font

wanted_fonts = set()
for fonts in raw_wanted_fonts:
    for font in full(fonts):
        wanted_fonts.add(font)

for font in available_fonts:
    if font in wanted_fonts \
            and font not in active_fonts:
        print "%s+%s%s" % (BRIGHT, NORMAL, font),
        system("eselect fontconfig enable %s.conf" % font)
    if font not in wanted_fonts \
            and font in active_fonts:
        print "%s-%s%s" % (BRIGHT, NORMAL, font),
