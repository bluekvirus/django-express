#!/bin/bash

# Note: You need pandoc installed system-wide, but twine installed through pip in venv.
sudo apt install pandoc
# pip install pypandoc
pip install twine

# trans .md to .rst
pandoc -f markdown -t rst -o README.rst README.md
#pandoc -f markdown -t rst -o CHANGELOG.rst CHANGELOG.md

# src and wheels dist
rm -rf dist/*
python setup.py sdist
python3 setup.py bdist_wheel

# register it
#twine register -r pypitest dist/*.whl
#twine register dist/*.whl

# upload it
#twine upload -r pypitest dist/*
twine upload dist/*