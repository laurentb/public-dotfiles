#!/bin/bash -ue
# fail on pyflakes errors
flake8 --select=E9 --ignore=E "$@"
# if no pyflakes errors, run pep8
flake8 "$@"
