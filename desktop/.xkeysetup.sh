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
