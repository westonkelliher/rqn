
log="/home/requin/logs"
dest="/home/requin/rqn"

# run game launcher
echo "python3 $dest/launcher.py"
echo "$(date)" > $log/launcher.out
python3 $dest/launcher.py 1>> $log/launcher.out 2>> $log/launcher.out


