#!/bin/bash

echo "rqn-start as $(whoami)"
echo "....................."
echo "Start $(date)"
echo "....................."



log="/home/requin/logs"
dest="/home/requin/rqn"

# run recbox system applications (AppSwitcher)
echo "$dest/loader"
echo "$(date)" > $log/loader.out
$dest/loader.out 1> $log/loader.out 2> $log/loader.out &

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
