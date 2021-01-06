#!/bin/bash -e

# Make the html folder if it doesnt exist
mkdir -p html;
python3 main.py -n 100 > out
python3 split_html.py < out
echo "100 chapters"
echo "$(grep -r "<tt>meeting" html/ | wc -l) reached MEETING"
echo "$(grep -r "<tt>courting" html/ | wc -l) reached COURTING"
echo "$(grep -r "<tt>dating" html/ | wc -l) reached DATING"
echo "$(grep -r "<tt>committed" html/ | wc -l) reached COMMITTED"
