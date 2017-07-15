#!/bin/bash -eu
cd $(dirname $0)
eselect --brief modules|grep -q '^fontconfig$' && ./fontconfig.py
exit 0
