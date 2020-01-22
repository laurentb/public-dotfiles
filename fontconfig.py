#!/usr/bin/env python3
import re
import sys
from os import path
from subprocess import check_call, check_output

interactive = sys.stdin.isatty()
BRIGHT = '\x1b[1m' if interactive else ''
NORMAL = '\x1b[22m' if interactive else ''

config_file = path.join(path.dirname(__file__), "fontconfig.wanted")

REGEXP = re.compile(r'^ +\[\d+\] +(?P<name>[^ ]+)\.conf(?P<enabled> \*)?$')
NUMRE = re.compile(r'\d+-(?P<name>[^ ]+)')

eselect = [REGEXP.match(line)
           for line
           in check_output("eselect fontconfig list", shell=True).decode('utf-8').strip().splitlines()
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
            if NUMRE.match(font) and NUMRE.match(font).groupdict()['name'] == wanted_font:
                yield font


wanted_fonts = set()
for fonts in raw_wanted_fonts:
    for font in full(fonts):
        wanted_fonts.add(font)

for font in available_fonts:
    if font in wanted_fonts \
            and font not in active_fonts:
        print("%s+%s%s" % (BRIGHT, NORMAL, font))
        check_call("eselect fontconfig enable %s.conf" % font, shell=True)
    if font not in wanted_fonts \
            and font in active_fonts:
        print("%s-%s%s" % (BRIGHT, NORMAL, font))
