#!/bin/sh

BASEDIR="$(dirname "`realpath "$0"`")"

source "$BASEDIR/../bin/activate"
exec python "$BASEDIR/../src/main.py"
