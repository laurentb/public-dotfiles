#!/usr/bin/env python
from os import path, popen, system

config_file = path.join(path.dirname(__file__), "bashcomp.wanted")

available_completions = popen("eselect --brief bashcomp list") \
            .read().strip().split("\n")

def is_enabled(name):
    return path.exists(path.join(path.expanduser("~/.bash_completion.d"), name))

active_completions = filter(is_enabled, available_completions)

with open(config_file, "r") as file:
    wanted_completions = file.read().strip().split("\n")

completions = set(wanted_completions) - set(active_completions)
for completion in completions:
  system("eselect bashcomp enable "+completion)

