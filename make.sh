#!/bin/bash -e

mkdir -p docs
python3 main.py -n 100 > out
python3 split_docs.py < out
echo "100 chapters"
echo "$(grep -r "<tt>meeting" docs/ | wc -l) reached MEETING"
echo "$(grep -r "<tt>courting" docs/ | wc -l) reached COURTING"
echo "$(grep -r "<tt>dating" docs/ | wc -l) reached DATING"
echo "$(grep -r "<tt>committed" docs/ | wc -l) reached COMMITTED"
echo "$(grep -rl "<tt>committed" docs | sed 's/.*/            &/')"
