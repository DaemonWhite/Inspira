#!/usr/bin/env bash

echo "----- COMPILE -----"
echo

meson compile -C _build
rm -r _install
meson install -C _build

echo
echo
echo "----- START -----"
echo
echo

SCHEMAS=$(pwd)/_install/share/glib-2.0/schemas
RESOURCES=$(pwd)/_install/share/inspira
GSETTINGS_SCHEMA_DIR=$SCHEMAS G_RESOURCE_ROOT=$RESOURCES ./_install/bin/inspira