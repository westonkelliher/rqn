#!/bin/bash

set -e

base="/home/requin"
dest="$base/rqn"

# lost permissions
chmod +x $dest/control_pad_target.so
chmod +x $dest/cp_server
chmod +x $dest/codewords
chmod +x $dest/configure.sh
chmod +x $dest/launcher.sh
chmod +x $dest/ota.sh

# set the desktop background
gsettings set org.gnome.desktop.background picture-uri file:///$dest/requin.png

# save local ip address into a file
ip addr | grep 192.168 | sed 's/^[^0-9]*\([0-9\.]*\).*/\1/' > $dest/localip

# change our package sources to a source that actually has standard packages
cp $dest/debian11_sources.list /etc/apt/sources.list
apt update

# install necessary packages for launcher.py
apt install -y python3-pip
pip3 install pygame

# install lightdm and set it to autologin
apt install -y lightdm
apt remove gdm3

# install tools
apt install -y curl git

# set github as known host and file permission for pulling
ssh-keyscan github.com >> $base/.ssh/known_hosts
chown requin $dest/.git/FETCH_HEAD

if ! [ $(getent group autologin) ]; then
    /sbin/groupadd -r autologin
    gpasswd -a requin autologin
fi
cp $dest/lightdm.conf /etc/lightdm/

# create directory to put service logs in to get info about the two services below
if ! [ -d "$base/logs" ]; then
    mkdir $base/logs
    chgrp requin $base/logs
fi

if ! [ -d "$base/rqnio" ]; then
    mkdir $base/rqnio
    chgrp requin $base/rqnio
    chown requin $base/rqnio
fi

# have the requin app launcher run on startup
cp $dest/launcher.service /usr/lib/systemd/system/
systemctl enable launcher

# have the control server for the touch mouse run on startup
cp $dest/cp_server.service /usr/lib/systemd/system/
systemctl enable cp_server

# done with setup
echo "Done."
sleep 3

#reboot the system
/sbin/reboot
