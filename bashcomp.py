#!/usr/bin/env python
import os

config_file = os.path.join(os.path.dirname(__file__), "bashcomp.wanted")

available_completions = os.popen("eselect --brief bashcomp list") \
            .read().strip().split("\n")

def is_enabled(name):
    path = os.path.expanduser("~/.bash_completion.d/"+name)
    return os.path.exists(path)

active_completions = filter(is_enabled, available_completions)

with open(config_file, "r") as file:
    wanted_completions = file.read().strip().split("\n")

completions = set(wanted_completions) - set(active_completions)
for completion in completions:
  os.system("eselect bashcomp enable "+completion)

