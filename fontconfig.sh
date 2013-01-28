#!/bin/bash -xeu
[[ -f /usr/share/eselect/modules/fontconfig.eselect ]] && ./fontconfig.py
[[ -f /usr/share/eselect/modules/infinality.eselect ]] && eselect infinality set nyx && eselect lcdfilter set nyx
