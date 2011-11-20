#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys
import os
import argparse
import re
from ConfigParser import ConfigParser

FF_PATH = os.path.expanduser('~/.mozilla/firefox')
UP_REGEX = re.compile(r'^user_pref\("(?P<key>[^"]+)", (?P<value>.+)\);$')


def scan_profiles():
    f = os.path.join(FF_PATH, 'profiles.ini')
    if not os.path.exists(f):
        return

    ini = ConfigParser()
    ini.read(f)
    for section in ini.sections():
        if section.startswith('Profile'):
            yield (ini.get(section, 'Name'), ini.get(section, 'Path'))


def read_prefs(profile):
    f = os.path.join(FF_PATH, profile, 'prefs.js')
    assert os.path.exists(f)
    prefs = dict()
    with open(f, 'r') as p:
        for line in p:
            match = UP_REGEX.match(line.strip())
            if match:
                prefs[match.groupdict()['key']] = match.groupdict()['value']
    return prefs


def diff(a, b):
    removed = dict()
    added = dict()
    changed = dict()
    for key, value in a.iteritems():
        if key not in b:
            removed[key] = value
        elif b[key] != value:
            changed[key] = b[key]
    for key, value in b.iteritems():
        if key not in a:
            added[key] = value
    return removed, added, changed


def pentadactylrc(removed, added, changed):
    def stripval(value):
        if value.startswith('"') and value.endswith('"'):
            svalue = value[1:-1]
            if '"' not in svalue and "=" not in svalue:
                return svalue
        return value

    print '" reset to default deleted values'
    for key, value in removed.iteritems():
        print 'set! %s&' % key
    print '" added'
    for key, value in added.iteritems():
        print 'set! %s=%s' % (key, stripval(value))
    print '" changed'
    for key, value in changed.iteritems():
        print 'set! %s=%s' % (key, stripval(value))


def main(argv):
    profiles = dict(scan_profiles())
    default_profile = profiles.get('default')
    if default_profile is None and len(profiles) == 1:
        default_profile = profiles.values()[0]

    parser = argparse.ArgumentParser(description="Live diff Firefox settings.")
    parser.add_argument('-p', '--profile', nargs=1,
        required=default_profile is None,
        default=default_profile, choices=profiles.values(),
        help="Profile name")

    args = parser.parse_args(argv[1:])

    print "Watching settings of %s." % args.profile
    oldprefs = read_prefs(args.profile)
    raw_input('Press enter when ready to show the differences.')
    newprefs = read_prefs(args.profile)

    removed, added, changed = diff(oldprefs, newprefs)

    # TODO Add support for other outputs
    pentadactylrc(removed, added, changed)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
