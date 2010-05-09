import os

tag_dirs = [
    "/etc/dotfiles/tags",
    os.path.expanduser("~/dotfiles/tags"),
];
tags = set()
for tag_dir in tag_dirs:
    if os.path.isdir(tag_dir):
        tags.update(os.listdir(tag_dir))

is_gentoo = os.path.exists("/etc/gentoo-release")
is_root = os.getuid() == 0

# Clean up the namespace
del os, tag_dirs, tag_dir

