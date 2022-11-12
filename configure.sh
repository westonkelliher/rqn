#!/bin/bash

last=$(cat last_version)
new=$(cat version)

if [[ "$new" -eq "$last" ]]; then
    exit
fi

base="/home/requin"
dest="$base/rqn"

cp $dest/.bashrc $base/
cp $dest/.xinitrc $base/

if [[ "$last" -lt "16" ]]; then
    sudo apt install node
    cd $dest/webcp
    npm install
fi
