#!/usr/bin/env python3
import os
import sys
from glob import glob

TAGS = sorted(os.listdir("/etc/dotfiles/tags"))
TAGS.insert(0, 'common')

BASEDIR = os.path.join(os.path.dirname(__file__), 'checkpkg')


def shorten(pkg):
    return pkg.split('/')[-1]


def needed(pkgs):
    for pkg in pkgs:
        if pkg not in INSTALLED \
           and shorten(pkg) not in INSTALLED_SHORT:
            yield pkg


def cmd(pkgs):
    return 'emerge -av --select --noreplace %s' % ' '.join(sorted(pkgs))


def wanted(filename):
    with open(os.path.join(BASEDIR, filename)) as f:
        return f.read().strip().split('\n')


def bonus(pkg):
    return pkg not in WANTED and shorten(pkg) not in WANTED


with open('/var/lib/portage/world') as f:
    INSTALLED = set(f.read().strip().split('\n'))

INSTALLED_SHORT = set([shorten(pkg) for pkg in INSTALLED])

WANTED = set()

for tag in TAGS:
    print("# Tag: %s" % tag)
    config_files = [os.path.basename(c)
                    for c
                    in glob(os.path.join(BASEDIR, '%s.*' % tag))]
    for config_file in config_files:
        pkgs = wanted(config_file)
        WANTED.update(pkgs)
        needed_pkgs = list(needed(pkgs))
        if needed_pkgs:
            group = config_file.split('.')[1]
            print("## Group: %s" % group)
            print(cmd(needed_pkgs))

pkgs = [shorten(pkg) for pkg in INSTALLED if bonus(pkg)]
if '-b' in sys.argv[1:]:
    print('Bonus packages: %s' % ' '.join(sorted(pkgs)))
