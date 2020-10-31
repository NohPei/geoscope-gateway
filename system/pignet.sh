#!/bin/sh

BASEDIR="$(dirname "`realpath "$0"`")"

source $BASEDIR/../bin/activate
python $BASEDIR/../src/main.py &
python $BASEDIR/../src/monitoring.py &

wait

trap 'jobs -p | xargs kill' EXIT INT QUIT TERM
