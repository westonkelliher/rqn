#!/bin/bash


base="/home/requin"

cd $base/rqn

v_old=$(cat version)
v_new=$(curl -s https://github.com/westonkelliher/rqn-scripts/blob/main/version)

if [ -z "$v_new" ]; then
    echo "CURL FAILURE"
fi


if [[ "$v_old" == "$v_new" ]]; then
    echo "no rqn update"
    exit
fi


#rm -r $base/old_rqn
#cp -r $base/rqn $base/old_rqn

cd $base/rqn

git pull origin main
