#!/usr/bin/env bash

echo "----- INSTALL Package -----"

pacman -S mingw-w64-ucrt-x86_64-gtk4 mingw-w64-ucrt-x86_64-libadwaita \
    mingw-w64-ucrt-x86_64-python-pip mingw-w64-ucrt-x86_64-python-gobject \
    mingw-w64-ucrt-x86_64-python-yaml mingw-w64-ucrt-x86_64-python-requests \
    mingw-w64-ucrt-x86_64-python-pillow mingw-w64-ucrt-x86_64-desktop-file-utils\
    mingw-w64-ucrt-x86_64-ca-certificates mingw-w64-ucrt-x86_64-meson\
    git mingw-w64-ucrt-x86_64-gettext mingw-w64-ucrt-x86_64-gettext\
    mingw-w64-ucrt-x86_64-gettext --needed

echo "----- CONFIGURING Inspira -----"

meson setup _build --prefix=$(pwd)/_install