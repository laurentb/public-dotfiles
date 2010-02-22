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

# urxvt daemon − use urxvtc instead of urxvt
urxvtd -q -o -f

. ~/.xkeysetup.sh

# prevent GTK and QT from using their own input systems
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim
# pointer: acceleration, threshold
xset mouse 3 3
# keyboard repeat
xset r on
xset r rate 600 40

xsetroot -solid "#3A3A3A"

xset s off
xset dpms 10800 10800 10800
xscreensaver &

(sleep 1 && stalonetray -w -p) &

(sleep 2 && kmix --keepvisibility) &
(sleep 2 && klipper) &
(sleep 3 && rsibreak) &

(sleep 4 && lal) &

exec openbox

