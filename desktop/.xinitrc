#!/bin/bash

# run all system xinitrc shell scripts.
if [ -d /etc/X11/xinit/xinitrc.d ]; then
    for i in /etc/X11/xinit/xinitrc.d/* ; do
        if [ -x "$i" ]; then
            . "$i"
        fi
    done
fi

if [ -n $DBUS_SESSION_BUS_ADDRESS ]; then
    export $(dbus-launch)
fi

# start pulseaudio in the background
if hash pulseaudio 2>/dev/null; then
    pulseaudio --start
fi
# register pulseaudio
if hash /usr/bin/start-pulseaudio-x11 2>/dev/null; then
    start-pulseaudio-x11
fi


xrdb -merge ~/.Xdefaults
source ~/.urxvt/xrdb.sh

. ~/.xinitrc.input

# prevent GTK and QT from using their own input systems
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim

# Qt5 theme trough qt5ct
export QT_QPA_PLATFORMTHEME="qt5ct"
# Qt5 theme through KDE
## export KDE_SESSION_VERSION=5 KDE_FULL_SESSION=true

hash kdeinit4 2>/dev/null && kdeinit4 +kded4 &
hash kdeinit5 2>/dev/null && kdeinit5 +kded5 &

# Chromium options
[ -f /etc/chromium/pepper-flash ] && . /etc/chromium/pepper-flash
export CHROMIUM_USER_FLAGS="${CHROMIUM_FLAGS} ${CHROMIUM_USER_FLAGS} --disable-sync --disable-manager-for-sync-signin --disallow-autofill-sync-credential --disallow-autofill-sync-credential-for-reauth --remember-cert-error-decisions=7257600 --disable-metrics --disable-metrics-reporting --disable-smooth-scrolling"

# force to use a keyring
hash gnome-keyring 2>/dev/null && export CHROMIUM_USER_FLAGS="$CHROMIUM_USER_FLAGS --password-store=gnome"
hash gnome-keyring-daemon 2>/dev/null && eval $(gnome-keyring-daemon --start --components=pkcs11,secrets)

xsetroot -solid "#323232"

xset s off
xset dpms 10800 10800 10800
xscreensaver &

(sleep 1 && stalonetray --dockapp-mode -p --kludges force_icons_size) &

(sleep 2 && gpaste-client start && gpaste-client applet) &
(sleep 3 && nice rsibreak --autostart) &

(sleep 4 && nice lal) &

(sleep 5 && nice redshift-gtk) &

hash wicd-gtk 2>/dev/null && /etc/init.d/wicd status && (sleep 3 && nice wicd-gtk --tray) &
hash xfce4-power-manager 2>/dev/null && (sleep 4 && nice xfce4-power-manager) &

[ -f ~/.xinitrc.local ] && . ~/.xinitrc.local

# check /usr/libexec/openbox-xdg-autostart --list for more stuff we should launch

exec openbox
