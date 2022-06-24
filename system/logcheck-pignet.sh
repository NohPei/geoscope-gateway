#!/bin/sh

FROM="`id -un`@`uname -n`"
TO="PigNetErrors@umich.edu"
SUBJECT="[logcheck-pignet@Home-Server] PigNet-USMARC Error Notice"

rclone ls --max-age 6h usda:Geophone\ Data/data/ --fast-list | grep -q zip && exit 0
# check the remote folder, and exit if there are files within the last 8 hours

mail -s "$SUBJECT" -r "$FROM" "$TO" << EOF
Latest Uploaded Geophone data is more than 6 hours old. There's probably a problem.

<<THIS IS SENT FROM AN AUTOMATED SCRIPT>>
EOF
