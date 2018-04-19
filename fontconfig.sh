#!/bin/bash -eu
cd $(dirname $0)
eselect fontconfig version > /dev/null 2>&1 && ./fontconfig.py
exit 0
