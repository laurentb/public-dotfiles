#!/bin/bash -eu
cd $(dirname $0)
eselect --brief modules|grep -q '^fontconfig$' && ./fontconfig.py
eselect --brief modules|grep -q '^infinality$' && eselect infinality set nyx && eselect lcdfilter set nyx
exit 0
