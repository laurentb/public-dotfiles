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

xinput set-button-map "Kingsis Peripherals  Evoluent VerticalMouse 3" 1 2 2 4 5 6 7 3 8
