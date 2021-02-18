#!/bin/sh

BASEDIR="$(dirname "`realpath "$0"`")"

mosquitto -c $BASEDIR/mosquitto.conf -d
