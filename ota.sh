#!/bin/bash



base="/home/requin"

branch="main"

if [[ -f "$base/testing" ]]; then
    branch="testing"
fi

if [[ -f "$base/development" ]]; then
    branch="development"
fi

git pull origin $branch
git checkout $branch

