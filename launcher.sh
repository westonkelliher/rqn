#!/bin/bash

dest="/home/requin/rqn"

# OTA update
$dest/ota.sh

# placeholder in case we need to run something here without changing ota.sh
$dest/configure.sh

# run game launcher
python3 $dest/launcher.py
