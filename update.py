#!/usr/local/bin/python3
import csv
import re
# keep the spaces here cuz it looks nicer in the HTML
# also keep the last empty line.
MARKER_BEGIN = "        <!--MARKER_BEGIN-->\n"
MARKER_END = "        <!--MARKER_END-->\n"
TEMPLATE = """
        <!-- %s -->
        <div class="row">
          <div class="col s8">
            <p class="quote">
            %s
            </p>
            <p class="author">%s</p>
          </div>
        </div>

"""

output = ""
with open('google-form.csv', 'r') as f:
    f.readline() # skip the header
    output = "".join([MARKER_BEGIN] + [
        TEMPLATE % (t,fact,author)
        for (t,author,fact) in csv.reader(f)
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
            print(line)

    html = "".join(lines)

with open('index.html', 'w') as f:
    f.write(html)
