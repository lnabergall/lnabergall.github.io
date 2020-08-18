#!/usr/local/bin/python3

# Keep the spaces here cuz it looks nicer in the HTML.
URL = r"https://docs.google.com/spreadsheets/d/1gug657PzPp4B8tfHHsZ9BEcAFihkFIBDBHtJ-O_pWdQ/export?format=csv"

from urllib.request import urlopen
from ssl import SSLContext
google_form = [l.decode('utf-8', 'replace') for l in urlopen(URL,context=SSLContext()).readlines()]

# Use the above template to turn them into HTML.
import csv
import json
with open('truest_facts.json', 'w') as f:
    f.write(json.dumps([
      (i+1,t,author,fact)
      for i,(t,author,fact) in enumerate(csv.reader(google_form[1:]))
    ]))
