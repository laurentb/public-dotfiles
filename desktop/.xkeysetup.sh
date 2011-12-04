# clear options
setxkbmap -option

# bépo
# enable zapping (not enabled by default anymore)
# swap caps lock and esc
setxkbmap fr bepo -option terminate:ctrl_alt_bksp -option caps:swapescape

# remap keys
xmodmap ~/.Xmodmap

# reload xbindkeys or start it
killall -HUP xbindkeys||xbindkeys
# same with keynav
killall -HUP keynav||keynav

# make the center button acts as a third button to avoid using the wheel
xinput set-button-map "Kingsis Peripherals  Evoluent VerticalMouse 3 " 1 2 2 4 5 6 7 3 8

# pointer: acceleration, threshold
xset mouse 3 3

# shorter delay, bigger rate
xset r rate 300 50
