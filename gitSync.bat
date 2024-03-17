@echo off
git checout main
git pull
git checkout dev
git merge main
git push