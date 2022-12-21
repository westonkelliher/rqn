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

if [[ -z "$last" || "$last" -lt "16" ]]; then
    sudo apt install node
    cd $dest/webcp
    npm install express
    npm install net
    npm install socketio
    npm install socket.io
fi

if [[ "$new" -eq "33" ]]; then
    cd $base
    git clone https://github.com/RecBox-Games/rqn.git rqn_new
    mv rqn old_rqn
    mv rqn_new rqn
fi
