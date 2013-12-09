#!/bin/bash -ue
# fail on pyflakes errors
flake8 --select=E9,F "$@"
# if no pyflakes errors, run isort + pep8
set +e
EXIT_STATUS=0
isort -c "$@" || EXIT_STATUS=$?
flake8 "$@" || EXIT_STATUS=$?
exit $EXIT_STATUS
