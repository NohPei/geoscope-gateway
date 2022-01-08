#!/bin/sh

BASEDIR="$(dirname "`realpath "$0"`")"

cd "$BASEDIR/.."
source "bin/activate"
exec python -m geoscope_gateway
