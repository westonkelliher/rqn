# turn off display power management services
xset -dpms
setterm -blank 0 -powerdown 0

# turn off black screensaver
xset s off

log="/home/requin/logs"
dest="/home/requin/rqn"

$dest/rqn-start.sh 1>> $log/rqn-start.out 2>> $log/rqn-start.out


