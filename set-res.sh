#!/bin/bash

xrandr --option $(xrandr -q | grep " connected" | cut -f1 -d" " | head -1) --mode 1920x1080
