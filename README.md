# [GeoMCU](https://github.com/NohPei/GeoMCU) Gateway

This repo provides software for working with networks of [GeoMCU](https://github.com/NohPei/GeoMCU) vibration sensors, consisting primarily of:

 - A Python module for logging/aggregating geophone data
 - Some configurations and scripts to quickly set up a combined MQTT broker and data logger for a network of GeoMCU boards

   - In that spirit, there are some device tree overlay sources that have been needed for some of the SBCs we've used for the combined broker and logger

In-depth documentation is included with the [GeoMCU Documentation](https://geomcu.readthedocs.io)

## Installation

## Python Module

The python module can be installed with the normal `pip install .`, preferably from a virtual environment of some sort.
You can then run main data logger with default settings with `python -m geoscope_gateway`

## System Scripts

There are several types of useful configuration files under `system/`, each used differently depending on their function:

 - [systemd](https://github.com/systemd/systemd) unit files (having `.service` or `.timer` extensions) can be linked into the appropriate folder manually or with `systemctl --user link <file>`
 - Configuration files (`.conf` or `.rules`) can be symlinked or copied to the configuration folder for that tool (e.g., `/etc/udev/rules.d/` for `systemd/gpio.rules`). Some  (such as `system/mosquitto.conf`) can be used in-place by specifying the configuration location for the relevant program.
 - Shell scripts (`.sh`) can be run with their absolute path or symlinked into your `$PATH`, for example in `~/bin/`

## Timenode Firmware

The `timenode-firmware/` folder contains Arduino® firmware for synchronizing time between the system clock an ESP-32 development board. Currently unused, but useful for future work on wireless sensor synchronization.

## Device Tree Overlays

The `dt-overlay/` folder contains the device tree overlays, which can be built into overlay files and loaded following [these instructions from U-Boot](https://docs.u-boot.org/en/v2023.04/usage/fdt_overlays.html).


Copyright © 2024 The Regents of the University of Michigan, [PEI Lab](https://peizhang.engin.umich.edu/)
