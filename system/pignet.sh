#!/bin/sh

BASEDIR="$(dirname "`realpath "$0"`")"

source $BASEDIR/../bin/activate
python $BASEDIR/../src/main.py
