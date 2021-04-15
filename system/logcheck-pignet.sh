#!/bin/sh

STORAGE=/media/hdd/
SENDMAIL=/usr/bin/sendmail
SENDMAIL_OPTS=""

FROM="`id -un`@`uname -n`"
TO="nobody@andrew.cmu.edu"
SUBJECT="[logcheck-pignet@`uname -n`] PigNet Error Notice"

if [ ! -d "$STORAGE" ]; then
	mail -S mta="$SENDMAIL" -S mta-arguments="$SENDMAIL_OPTS" -a "$STATUS_LOG" -s "$SUBJECT" "$TO" << EOF
From: $FROM

Storage Device is not Mounted. No data can be logged.

<<THIS IS SENT FROM AN AUTOMATED SCRIPT>>
EOF
	exit 0
fi

if [ `find $STORAGE/data -type f -mmin -360 | wc -l` -gt 0 ]; then
	exit 0
fi

# find most recent logfiles to send
DEVICE_LOG="`ls $STORAGE/log/GEOSCOPE* -t | head -n1`"
DEVICE_LOG_LAST="`ls $STORAGE/log/GEOSCOPE* -t | tail -n+2 | head -n1`"

if [ -z $DEVICE_LOG_LAST ]; then # for when the log hasn't been rotated yet
	DEVICE_LOG_LAST="$DEVICE_LOG"
fi




mail -S mta="$SENDMAIL" -S mta-arguments="$SENDMAIL_OPTS" -a "$DEVICE_LOG" -a "$DEVICE_LOG_LAST" -s "$SUBJECT" "$TO" << EOF
From: $FROM

Latest Geophone data is more than 6 hours old. There's probably a problem.
Check attached logs and system status.

<<THIS IS SENT FROM AN AUTOMATED SCRIPT>>
EOF
