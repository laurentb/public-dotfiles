#!/bin/bash -ue
# fail on pyflakes errors
flake8 --select=E9,F "$@"
# if no pyflakes errors, run pep8
flake8 "$@"
