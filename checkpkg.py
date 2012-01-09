#!/usr/bin/env python
from glob import glob
import os


TAGS = sorted(os.listdir("/etc/dotfiles/tags"))
TAGS.insert(0, 'common')

BASEDIR = os.path.dirname(__file__)


def shorten(pkg):
    return pkg.split('/')[-1]


def needed(pkgs):
    for pkg in pkgs:
        if pkg not in INSTALLED \
        and shorten(pkg) not in INSTALLED_SHORT:
            yield pkg


def cmd(pkgs):
    return 'emerge -av --select --noreplace %s' % ' '.join(pkgs)


def wanted(filename):
    with open(os.path.join(BASEDIR, filename)) as f:
        return f.read().strip().split('\n')


with open('/var/lib/portage/world') as f:
    INSTALLED = set(f.read().strip().split('\n'))

INSTALLED_SHORT = set([shorten(pkg) for pkg in INSTALLED])


for tag in TAGS:
    print "# Tag: %s" % tag
    config_files = [os.path.basename(c) for c in \
        glob(os.path.join(BASEDIR, 'checkpkg.%s.*' % tag))]
    for config_file in config_files:
        group = config_file.split('.')[2]
        pkgs = list(needed(wanted(config_file)))
        print "## Group: %s" % group
        if pkgs:
            print cmd(pkgs)
