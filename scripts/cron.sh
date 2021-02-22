#!/bin/bash
echo "Run this script from repository root!"
cd scripts

pipenv install
pipenv run python ../src/actions.py