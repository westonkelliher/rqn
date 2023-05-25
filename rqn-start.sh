#!/bin/bash

echo "rqn-start as $(whoami)"
echo "....................."
echo "Start $(date)"
echo "....................."



log="/home/requin/logs"
dest="/home/requin/rqn"

# kill any existing control pad servers
pid=$(ps aux | grep cp_server | grep -v "grep" | sed 's/^[^[:space:]]\+[[:space:]]\+\([0-9]\+\).*/\1/')
for x in $pid; do
    kill -9 $x
done

# run recbox system applications (Loader which runs Launcher)
echo "$dest/loader"
echo "$(date)" > $log/loader.out
$dest/loader 1> $log/loader.out 2> $log/loader.out

sleep infinity
