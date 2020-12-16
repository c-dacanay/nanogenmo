#!/bin/bash -e

# Make the html folder if it doesnt exist
mkdir -p html;
python3 main.py > out
python3 split_html.py < out
