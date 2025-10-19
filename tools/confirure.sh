#!/usr/bin/bash

echo "----- INSTALL Package -----"

if [ -n "$(grep -qi msys2 /etc/os-release)" ]; then

pacman -S mingw-w64-ucrt-x86_64-gtk4 mingw-w64-ucrt-x86_64-libadwaita \
    mingw-w64-ucrt-x86_64-python-pip mingw-w64-ucrt-x86_64-python-gobject \
    mingw-w64-ucrt-x86_64-python-yaml mingw-w64-ucrt-x86_64-python-requests \
    mingw-w64-ucrt-x86_64-python-pillow mingw-w64-ucrt-x86_64-desktop-file-utils\
    mingw-w64-ucrt-x86_64-ca-certificates mingw-w64-ucrt-x86_64-meson\
    git mingw-w64-ucrt-x86_64-gettext mingw-w64-ucrt-x86_64-blueprint-compiler --needed

fi

echo "----- CONFIGURING Inspira -----"

path="$(dirname "$0")/.."
path="$(realpath $path)"

meson setup _build --prefix=$path/_install -Ddevel=true