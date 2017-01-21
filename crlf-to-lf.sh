#!/bin/bash
#
# If you see this error msg:
# bash: ./create-venv.sh: /bin/bash^M: bad interpreter: No such file or directory
# 
# How to prevent:
# core.autocrlf true (Windows <--> repo)
# core.autocrlf input (Linux <--> repo)
#
# How to Fix: (.gitattributes)
# *.sh        eol=lf
# *.py        eol=lf
#
# Create the .gitattributes file and then run the following commands twice!
# 1 round -- clean up and commit all changed (crlf --> lf) files to repo
# 2 round -- clean up and reset local files to that commit
#
# Again, this is because git handles your files as:
# 	clear local files & cache (1st)
# 	local files <-- (1st) local repo checkout upon reset but with new .gitattributes
#	commit (detected file attributes change)
#	local files --> remote repo accepts push with auto change-upon-commit according to .gitattributes
#	clear local files & cache (2nd) since local file contents have not changed
#	local files* <-- (2nd) local repo
# 	

git config --global core.autocrlf input
git rm --cached -r .
git reset --hard # run this line out of this file