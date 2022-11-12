#!/bin/bash


base="/home/requin"

cd $base/rqn

v_old=$(cat version)
v_new=$(curl -s https://github.com/westonkelliher/rqn-scripts/blob/main/version)

if [ -z "$v_new" ]; then
    echo "CURL FAILURE"
fi


cd $base/rqn
cp version last_version # last_version informs configure.sh if certain configurations need to occur

if [[ "$v_old" == "$v_new" ]]; then
    echo "no rqn update"
    exit
fi


cp version old_version # old version tells us what version the user had the last time they got an OTA update

git pull origin main
