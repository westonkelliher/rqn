#!/bin/bash

cd /home/requin/rqn

last=$(cat last_version)
new=$(cat version)

if [[ "$new" -eq "$last" ]]; then
    exit
fi

base="/home/requin"
dest="$base/rqn"

cp $dest/.bashrc $base/
cp $dest/.xinitrc $base/

if [[ -z "$last" || "$last" -lt "16" ]]; then
    sudo apt install node
    cd $dest/webcp
    npm install express
    npm install net
    npm install socketio
    npm install socket.io
fi

if [[ -z "$last" || "$last" -lt "34" ]]; then
    cp $base/xorg.conf /etc/X11/
fi
