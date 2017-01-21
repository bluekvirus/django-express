#!/bin/bash
#
# If you see this error msg:
# bash: ./create-venv.sh: /bin/bash^M: bad interpreter: No such file or directory
# 
# Prevent:
# core.autocrlf true (Windows <--> repo)
# core.autocrlf input (Linux <--> repo)
#
# Fix: (.gitattributes)
# *.sh        eol=lf
# *.py        eol=lf
#
# Create the .gitattributes file and then run the following commands:

git config --global core.autocrlf input
git rm --cached -r .
git reset --hard # run this line out of this file