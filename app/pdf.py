from flask import render_template
from xhtml2pdf import pisa
from StringIO import StringIO

def export_pdf(template, data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(render_template(template, **data)), pdf)
    return pdf.getvalue()
