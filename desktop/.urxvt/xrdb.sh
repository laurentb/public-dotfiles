#!/bin/sh -xeu
xrdb -merge <<END
URxvt*perl-lib: ${HOME}/.urxvt/perl
URxvt*perl-ext-common: default,$(ls -m ${HOME}/.urxvt/perl|sed 's/ //g')
END
