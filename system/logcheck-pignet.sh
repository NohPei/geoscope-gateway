#!/bin/sh

STORAGE=/media/hdd/
SENDMAIL=/usr/bin/sendmail
SENDMAIL_OPTS=""

FROM="PigNet <lab@localhost>"
TO="nobody@andrew.cmu.edu"
SUBJECT="PigNet Error Notice"

if [ `find $STORAGE/data -type f -mmin -360 | wc -l` -gt 0 ]; then
	exit 0
fi

# find most recent logfiles to send
STATUS_LOG="`ls $STORAGE/log/STATUS* -t | head -n1`"
DEVICE_LOG="`ls $STORAGE/log/GEOSCOPE* -t | head -n1`"


mail -S mta="$SENDMAIL" -S mta-arguments="$SENDMAIL_OPTS" -a "$STATUS_LOG" -a "$DEVICE_LOG" -s "$SUBJECT" "$TO" << EOF
Latest Geophone data is more than 6 hours old. There's probably a problem.
Check attached logs and system status.
EOF
