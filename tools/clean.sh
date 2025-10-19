#!/usr/bin/env bash

echo "----- CLEANING -----"

path="$(dirname "$0")/.."
path="$(realpath $path)"

rm -r $path/_build
rm -r $path/_install

echo "----- END CLEANING -----"