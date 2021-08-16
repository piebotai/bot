#!/bin/sh

git reset HEAD --hard
git fetch --all
git checkout main
git pull origin main
