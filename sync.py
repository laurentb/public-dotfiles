#!/usr/bin/env python3
from os import path

import sync_options as options
from confman import ConfigSource

base_path = path.join(path.dirname(__file__), '..')


def privpub(dir):
    return [path.join("private", dir), path.join("public", dir)]


dirs = privpub("base")
if "desktop" in options.tags and not options.is_root:
    dirs += privpub("desktop")

for dir in dirs:
    base_dir = path.normpath(path.join(base_path, dir))
    ConfigSource(base_dir, "~", None, options).sync()

if options.is_root and options.is_gentoo:
    dirs = privpub("gentoo")
    for dir in dirs:
        base_dir = path.normpath(path.join(base_path, dir))
        ConfigSource(base_dir, "/etc", None, options).sync()
