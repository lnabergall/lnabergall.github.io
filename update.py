#!/usr/local/bin/python3
import csv
from urllib.request import urlopen

# keep the spaces here cuz it looks nicer in the HTML
# also keep the last empty line.
URL = r"https://docs.google.com/spreadsheets/d/1gug657PzPp4B8tfHHsZ9BEcAFihkFIBDBHtJ-O_pWdQ/export?format=csv"
MARKER_BEGIN = "        <!--MARKER_BEGIN-->\n"
MARKER_END = "        <!--MARKER_END-->\n"
TEMPLATE = """
        <!-- %s -->
        <div class="row fact">
          <div class="col s8 push-s2">
            <div class="quote">
              <span class="label">%d. </span>
              <span>
                %s
              </span>
            </div>
            <div class="author">
              <span>%s</span>
            </div>
          </div>
        </div>
"""

google_form = [l.decode('utf-8') for l in urlopen(URL).readlines()]
output = "".join([MARKER_BEGIN] + [
    TEMPLATE % (t,i+1,fact,author)
    for i,(t,author,fact) in enumerate(csv.reader(google_form[1:]))
] + [MARKER_END])

html = ""
with open('index.html', 'r') as f:
    skip = False
    lines = []
    for line in f:
        if line == MARKER_BEGIN:
            skip = True
        elif line == MARKER_END:
            skip = False
            lines.append(output)
        elif not skip:
            lines.append(line)
        else:
            print(line, end="")

    html = "".join(lines)

with open('index.html', 'w') as f:
    f.write(html)
