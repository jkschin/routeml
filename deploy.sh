#!/bin/bash

# Step 1: Deploy MkDocs documentation to GitHub Pages
mkdocs gh-deploy

# Step 2: Publish the package to PyPI
rm -rf build/ dist/

python setup.py sdist bdist_wheel
TWINE_USERNAME=$PYPI_USERNAME TWINE_PASSWORD=$PYPI_PASSWORD twine upload dist/*
