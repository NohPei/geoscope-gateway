#!/bin/bash

BASEDIR="$(dirname "`realpath "$0"`")"

exec mosquitto -c "$BASEDIR/mosquitto.conf"
