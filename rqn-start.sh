#!/bin/bash

echo "rqn-start as $(whoami)"
echo "....................."
echo "Start $(date)"
echo "....................."



log="/home/requin/logs"
dest="/home/requin/rqn"

# run loader
echo "python3 $dest/loader.py"
echo "$(date)" > $log/loader.out
python3 $dest/loader.py 1>> $log/loader.out 2>> $log/loader.out

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

# run web server
echo "node $dest/webcp/index.js"
node $dest/webcp/index.js 1> $log/node.out 2> $log/node.out &

# run game launcher
echo "$dest/launcher"
echo "$(date)" > $log/launcher.out
$dest/launcher 1>> $log/launcher.out 2>> $log/launcher.out
