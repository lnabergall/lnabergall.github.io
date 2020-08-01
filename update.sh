#!/bin/sh

curl -L "https://docs.google.com/spreadsheets/d/1gug657PzPp4B8tfHHsZ9BEcAFihkFIBDBHtJ-O_pWdQ/export?format=csv" -o google-form.csv
python3 update.py
rm google-form.csv
git add index.html
git commit -m "ran update.sh @ $(date)"
