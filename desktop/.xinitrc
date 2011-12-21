#!/bin/bash

# run all system xinitrc shell scripts.
if [ -d /etc/X11/xinit/xinitrc.d ]; then
    for i in /etc/X11/xinit/xinitrc.d/* ; do
        if [ -x "$i" ]; then
            . "$i"
        fi
    done
fi

# start pulseaudio in the background
if [ -x /usr/bin/start-pulseaudio-x11 ]; then
    /usr/bin/start-pulseaudio-x11
else
    if [ -x /usr/bin/pulseaudio ]; then
        /usr/bin/pulseaudio --start
    fi
fi

source ~/.urxvt/xrdb.sh

# urxvt daemon − use urxvtc instead of urxvt
urxvtd -q -o -f

. ~/.xkeysetup.sh

# prevent GTK and QT from using their own input systems
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim

xsetroot -solid "#323232"

xset s off
xset dpms 10800 10800 10800
xscreensaver &

(sleep 1 && stalonetray -w -p) &

(sleep 2 && kmix --keepvisibility) &
(sleep 2 && klipper) &
(sleep 3 && nice rsibreak) &

(sleep 4 && nice lal) &

which wicd-gtk && /etc/init.d/wicd status && (sleep 3 && nice wicd-gtk) &
which gnome-power-manager && (sleep 4 && nice gnome-power-manager) &

[ -f ~/.xinitrc.local ] && . ~/.xinitrc.local

# check /usr/libexec/openbox-xdg-autostart --list for more stuff we should launch

which ck-launch-session && exec ck-launch-session openbox
exec openbox
