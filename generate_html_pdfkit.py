from email import header
from jinja2 import Template
from dateutil import parser
import json
import pdfkit
from PyPDF2 import PdfFileReader, PdfFileWriter

def generate_pdf_from_html(source, target):
    options = {'--enable-local-file-access':'--enable-local-file-access'} # , '--header-html': 'generated_header.html'
    pdfkit.from_file(source, target, options=options, verbose=True)

def generate_pdf_from_template(template_name):
    file_name = 'templates/' + template_name + '.html'
    html_file_name = f'tmp/{template_name}' + '.html'
    pdf_file_name = f'tmp/{template_name}' + '.pdf'
    with open(file_name) as file_:
        template = file_.read()
    template = Template(template)
    html = template.render(data)

    Func = open(html_file_name, "w")
    Func.write(html)
    Func.close()
    generate_pdf_from_html(html_file_name, pdf_file_name)

def pdf_cat(input_files, output_stream):
    input_streams = []
    try:
        for input_file in input_files:
            input_streams.append(open(input_file, 'rb'))
        writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(output_stream)
    finally:
        for f in input_streams:
            f.close()

# Convert data for convenience in rendering
data = json.load(open('data/pdf_report_data.json'))
date = parser.parse(data['date'])
if 'date' in data:
    data['date'] = date.strftime('%D, %M %d, %Y')
if 'start' in data:
    data['start'] = date.strftime('%H:%M:%S')
if 'endTime' in data:
    end = parser.parse(data['endTime'])
if 'end' in data:
    data['end'] = end.strftime('%H:%M:%S')
if 'dateCreated' in data:
    dateCreated = parser.parse(data['dateCreated'])
    data['dateCreated'] = dateCreated.strftime('%d/%m/%Y - %H:%M:%S')
if 'dateModified' in data:
    dateModified = parser.parse(data['dateModified'])
    data['dateModified'] = dateModified.strftime('%d/%m/%Y - %H:%M:%S')
if 'description' in data:
    data['description'] = data['description'].replace('\n', '<br>')
if 'review' in data:
    if 'reviewStarted' in data['review']:
        data['review']['reviewStarted'] = data['review']['reviewStarted'].replace('\n', '<br>')

# Join component templates
template = ''
generate_pdf_from_template('first_page')
generate_pdf_from_template('second_page')
generate_pdf_from_template('third_page')

pdf_cat(['tmp/first_page.pdf', 'tmp/second_page.pdf', 'tmp/third_page.pdf'], 'tmp/result.pdf')
