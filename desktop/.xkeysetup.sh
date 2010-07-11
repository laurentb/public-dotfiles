# clear options
setxkbmap -option

# bépo
setxkbmap fr bepo

# enable zapping (not enabled by default anymore)
setxkbmap -option terminate:ctrl_alt_bksp

# swap caps lock and esc
setxkbmap -option caps:swapescape

# remap keys
xmodmap ~/.Xmodmap

# reload xbindkeys or start it
killall -HUP xbindkeys||xbindkeys

# make the center button acts as a third button to avoid using the wheel
xinput set-button-map "Kingsis Peripherals  Evoluent VerticalMouse 3" 1 2 2 4 5 6 7 3 8

# disable the touchpad on laptops
xinput set-int-prop "SynPS/2 Synaptics TouchPad" "Device Enabled" 8 0
