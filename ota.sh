#!/bin/bash

base="/home/requin"

branch="main"

if [[ -f "$base/branch" ]]; then
    branch=$(cat $base/branch)
fi

cd $base/rqn
git fetch
git checkout $branch
git pull origin $branch

cp $base/rqn/.xinitrc $base/
