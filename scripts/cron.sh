#!/bin/bash
echo "Run this script from repository root!"
cd scripts

python -m pipenv install
python -m pipenv run python ../actions.py