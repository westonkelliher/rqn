#!/bin/bash



base="/home/requin"

branch="main"

if [[ -f "$base/testing" ]]; then
    branch="testing"
fi

if [[ -f "$base/development" ]]; then
    branch="development"
fi

cd $base/rqn
git checkout $branch
git pull origin $branch

