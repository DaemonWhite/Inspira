#!/usr/bin/bash

path="$(dirname "$0")/.."
path="$(realpath $path)"

echo "----- COMPILE -----"
echo

meson compile -C _build
rm -r $path/_install/share/applications
meson install -C _build

echo
echo
echo "----- START -----"
echo
echo

SCHEMAS=$path/_install/share/glib-2.0/schemas
RESOURCES=$path/_install/share/inspira
EXEC=$path/_install/bin/inspira

echo "EXEC: $EXEC"
echo "RESOURCES: $RESOURCES"
echo "SCHEMAS: $SCHEMAS"
echo
echo "----- LOG Inspira -----"
echo

GSETTINGS_SCHEMA_DIR=$SCHEMAS G_RESOURCE_ROOT=$RESOURCES $EXEC