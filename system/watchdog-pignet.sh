#!/bin/bash

SENSOR_COUNT=15
PIGNET_PID=`pgrep pignet.sh | head -n1`

overrun_check() {
	threads=`pstree -c $PIGNET_PID | wc -l`
	if [ $threads -gt $((SENSOR_COUNT * 3)) ]; then
		return $threads
	fi
}

pignet_reset() {
	kill $PIGNET_PID
	while ps $PIGNET_PID > /dev/null; do
		sleep 2
	done
	overrun_check
}

if [ -z $PIGNET_PID ]; then
	exit 0
fi

case $1 in
	test)
		overrun_check
		exit
		;;
	repair)
		pignet_reset
		exit
		;;

	*)
		exit 1
esac

