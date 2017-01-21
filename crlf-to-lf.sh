#!/bin/bash
#
# If you see this error msg:
# bash: ./create-venv.sh: /bin/bash^M: bad interpreter: No such file or directory
# 
# core.autocrlf true (Windows <--> repo)
# core.autocrlf input (Linux <--> repo)

git config --global core.autocrlf input
git rm --cached -r .
git reset --hard