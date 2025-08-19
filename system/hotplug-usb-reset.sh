#!/bin/sh

if [ "$ACTION" == "remove" ] && [ "$DEVNUM" -gt 1 ]; then
	# Anytime the device is removed

	rmmod xhci_plat_hcd
	modprobe xhci_plat_hcd
	# reset the USB controller
	# If the "removal" is a bug, it'll reinit. Otherwise this will do nothing
fi
