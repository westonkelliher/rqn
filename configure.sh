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

if [[ ! -d $base/.local/share/launcher ]]; then
    mkdir $base/.local/share/launcher
fi

cp $dest/res/* $base/.local/share/launcher/

if [[ -z "$last" || "$last" -lt "16" ]]; then
    sudo apt install node
    cd $dest/webcp
    npm install express
    npm install net
    npm install socketio
    npm install socket.io
fi
