#!/usr/bin/env bash

# create virtual environment
python -m venv env
# activate env
source ./env/bin/activate
# install requirements
pip install --upgrade pip
python3 -m pip install -r requirements.txt
# close env
deactivate
