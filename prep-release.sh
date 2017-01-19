#!/bin/bash

# trans .md to .rst
pandoc -f markdown -t rst -o README.rst README.md
pandoc -f markdown -t rst -o CHANGELOG.rst CHANGELOG.md

# src and wheels dist
python setup.py sdist
python3 setup.py bdist_wheel