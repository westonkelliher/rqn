#!/bin/bash

echo "rqn-start as $(whoami)"
echo "....................."
echo "Start $(date)"
echo "....................."



log="/home/requin/logs"
dest="/home/requin/rqn"

# OTA update
echo "$dest/ota.sh"
echo "$(date)" > $log/ota.out
$dest/ota.sh 1>> $log/ota.out 2>> $log/ota.out

# placeholder in case we need to run something here without changing ota.sh
echo "$dest/configure.sh"
$dest/configure.sh 1> $log/configure.out 2> $log/configure.out

# kill any existing control pad servers
pid=$(ps aux | grep cp_server | grep -v "grep" | sed 's/^[^[:space:]]\+[[:space:]]\+\([0-9]\+\).*/\1/')
for x in $pid; do
    kill -9 $x
done

# run control pad server
echo "$dest/cp_server"
$dest/cp_server 1> $log/cp_server.out 2> $log/cp_server.out &

# initialize graphics and start the launcher
startx
