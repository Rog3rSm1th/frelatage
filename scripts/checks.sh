#!/usr/bin/env bash

# Reformating the code using black
black --check $(git ls-files './frelatage/*.py')
# Check for unused imports
pylint --disable=all --enable=unused-import $(git ls-files './frelatage/*.py')
# Validate types using mymy
mypy ./frelatage