from jinja2 import Template
from dateutil import parser
import json

import os
import sys
import cgi
import logging
from io import StringIO
import xhtml2pdf.pisa as pisa

def dump_errors(pdf, show_log=True):
    if pdf.err:
        print("*** %d ERRORS OCCURED" % pdf.err)


# def generate_html_from_json(data):
data = json.load(open('data/pdf_report_data.json'))
date = parser.parse(data['date'])
data['date'] = date.strftime('%D, %M %d, %Y')
data['start'] = date.strftime('%H:%M:%S')
end = parser.parse(data['endTime'])
data['end'] = end.strftime('%H:%M:%S')
dateCreated = parser.parse(data['dateCreated'])
data['dateCreated'] = dateCreated.strftime('%d/%m/%Y - %H:%M:%S')
dateModified = parser.parse(data['dateModified'])
data['dateModified'] = dateModified.strftime('%d/%m/%Y - %H:%M:%S')
data['review']['reviewStarted'] = data['review']['reviewStarted'].replace('\n', '<br>')

with open('pdf_template.html') as file_:
    template = Template(file_.read())
html = template.render(data)

Func = open("generated.html", "w")
# Adding input data to the HTML file
Func.write(html)
# Saving the data into the HTML file
Func.close()
# return html

src="generated.html"
dest="generated.pdf"
pdf = pisa.CreatePDF(open(src, "r"), open(dest, "wb"))

if pdf.err:
    dump_errors(pdf)
else:
    pisa.startViewer(dest)
