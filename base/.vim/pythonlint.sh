#!/bin/bash -ue
# fail on pyflakes errors
flake8 --ignore=E,W "$@"
# if no pyflakes errors, run pep8
flake8 --max-line-length=120 "$@"
