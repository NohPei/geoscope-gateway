#!/bin/sh

set -e

if [ -z $PIGNET_DIR ]; then
	PIGNET_DIR="/mnt/hdd/PigNet/"
fi

archive_folder() {
	zipfile="${1%/}.zip"
	if [ -f "$zipfile" ] && ! 7z t "$zipfile" -stl; then
		# if there's an existing archive, check it
		rm -f "$zipfile"
		# remove invalid old archives
	fi

	7z u "$zipfile" -stl -mx1 "$1"
	if 7z t "$zipfile" -stl;  then
		# verify the archive file
		find "$1" -mtime +1 -delete
		# if everything's fine, clear out old files (> 1 day) in the original directory
	fi
}

while read origdir; do
	archive_folder "$origdir" &
done < <( find "$PIGNET_DIR/data" -maxdepth 1 -mindepth 1 -type d )

wait

