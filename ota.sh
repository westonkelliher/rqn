#!/bin/bash

base="/home/requin"

if [[ -f "$base/no_ota" ]]; then
    exit
fi

branch="production"

if [[ -f "$base/branch" ]]; then
    branch=$(cat $base/branch)
fi

cd $base/rqn
git fetch
git checkout $branch
git pull origin $branch

sudo cp -p $base/rqn/.xinitrc $base/
