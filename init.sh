#!/bin/sh

git reset HEAD --hard
git fetch --all
git checkout main
git pull origin main
pip3 install schedule
pip3 install termcolor
