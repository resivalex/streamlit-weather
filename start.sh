#!/bin/bash

pip install poetry
poetry config virtualenvs.in-project true
poetry update
poetry install
poetry run streamlit run app.py

echo "\nWait for Ctrl-C"
trap 'kill $(jobs -p)' INT
sleep infinity &
wait
