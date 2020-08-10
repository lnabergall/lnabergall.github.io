#!/usr/local/bin/python3

# Keep the spaces here cuz it looks nicer in the HTML.
URL = r"https://docs.google.com/spreadsheets/d/1gug657PzPp4B8tfHHsZ9BEcAFihkFIBDBHtJ-O_pWdQ/export?format=csv"
MARKER_BEGIN = "        <!--MARKER_BEGIN-->\n"
MARKER_END = "        <!--MARKER_END-->\n"
TEMPLATE = """
        <!-- %s -->
        <div class="row fact">
          <div class="col-sm-12 col-md-8 offset-md-2">
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

# -------
# WARNING
# -------
#
# After Kel's python upgrade to 3.7.3, the script now gives me some kinda of SSL
# validation error because of the https in the link. Chaning it to http doesn't
# help because Google redirects it to https.
#
# In true algebraic combinators style, we simply asks python to not validate SSL
# certificate for the https link. # What can possibly go wrong?
#
from urllib.request import urlopen
from ssl import SSLContext
google_form = [l.decode('utf-8', 'replace') for l in urlopen(URL,context=SSLContext()).readlines()]

# Read and turn stuff from CSV to arrays.
import csv
html_escape = lambda s: s.replace("'","&#39;").replace("\"","&quot;")
output = "".join([MARKER_BEGIN] + [
    TEMPLATE % (t,i+1,html_escape(fact),author)
    for i,(t,author,fact) in enumerate(csv.reader(google_form[1:]))
] + [MARKER_END])

# Use the above template to turn them into HTML.
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
