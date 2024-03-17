@echo off
git checkout main
git pull
git checkout dev
git merge main
git push