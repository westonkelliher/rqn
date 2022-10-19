#!/bin/bash

set -e

# lost permissions
chmod +x /home/requin/rqn/control_pad_target.so
chmod +x /home/requin/rqn/cp_server
chmod +x /home/requin/rqn/codewords
chmod +x /home/requin/rqn/launcher.sh
chmod +x /home/requin/rqn/ota.sh

# set the desktop background
gsettings set org.gnome.desktop.background picture-uri file:////home/requin/rqn/requin.png

# save local ip address into a file
ip addr | grep 192.168 | sed 's/^[^0-9]*\([0-9\.]*\).*/\1/' > /home/requin/rqn/localip

# change our package sources to a source that actually has standard packages
cp /home/requin/rqn/debian11_sources.list /etc/apt/sources.list
apt update

# install necessary packages for launcher.py
apt install -y python3-pip
pip3 install pygame

# install lightdm and set it to autologin
apt install -y lightdm
apt remove gdm3

# install tools
apt install -y curl git

if ! [ $(getent group autologin) ]; then
    /sbin/groupadd -r autologin
    gpasswd -a requin autologin
fi
cp /home/requin/rqn/lightdm.conf /etc/lightdm/

# create directory to put service logs in to get info about the two services below
if ! [ -d "/home/requin/logs" ]; then
    mkdir /home/requin/logs
    chgrp requin /home/requin/logs
fi

if ! [ -d "/home/requin/rqnio" ]; then
    mkdir /home/requin/rqnio
    chgrp requin /home/requin/rqnio
fi

# have the requin app launcher run on startup
cp /home/requin/rqn/lc-launcher.service /usr/lib/systemd/system/
systemctl enable lc-launcher

# have the control server for the touch mouse run on startup
cp /home/requin/rqn/touch-mouse.service /usr/lib/systemd/system/
systemctl enable touch-mouse

# done with setup
echo "Done."
sleep 3

#reboot the system
/sbin/reboot
