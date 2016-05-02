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

if [ -n $DBUS_SESSION_BUS_ADDRESS ]; then
    dbus-send --session \
        --dest=org.freedesktop.DBus \
        /org/freedesktop/DBus \
        org.freedesktop.DBus.StartServiceByName \
        string:org.gtk.vfs.Daemon uint32:0
fi

xrdb -merge ~/.Xdefaults
source ~/.urxvt/xrdb.sh

. ~/.xinitrc.input

# prevent GTK and QT from using their own input systems
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim

# Chromium options
[ -f /etc/chromium/pepper-flash ] && . /etc/chromium/pepper-flash
export CHROMIUM_USER_FLAGS="${CHROMIUM_FLAGS} ${CHROMIUM_USER_FLAGS} --disable-sync --disable-manager-for-sync-signin --disallow-autofill-sync-credential --disallow-autofill-sync-credential-for-reauth --remember-cert-error-decisions=7257600 --disable-metrics --disable-metrics-reporting"

# force to use a keyring
type -p gnome-keyring && export CHROMIUM_USER_FLAGS="$CHROMIUM_USER_FLAGS --password-store=gnome"

xsetroot -solid "#323232"

xset s off
xset dpms 10800 10800 10800
xscreensaver &

(sleep 1 && stalonetray --dockapp-mode -p --kludges force_icons_size) &

(sleep 2 && klipper) &
(sleep 3 && nice rsibreak) &

(sleep 4 && nice lal) &

type -p wicd-gtk && /etc/init.d/wicd status && (sleep 3 && nice wicd-gtk --tray) &
type -p gnome-power-manager && (sleep 4 && nice gnome-power-manager) &

[ -f ~/.xinitrc.local ] && . ~/.xinitrc.local

# check /usr/libexec/openbox-xdg-autostart --list for more stuff we should launch

type -p ck-launch-session && exec ck-launch-session openbox
exec openbox
