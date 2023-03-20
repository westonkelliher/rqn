#!/bin/bash

set -e

# move from westonkelliher/rqn to RecBox-Games/rqn
cd /home/requin
git clone https://github.com/RecBox-Games/rqn.git newrqndir
mv rqn oldrqndir
mv newrqndir rqn
reboot
