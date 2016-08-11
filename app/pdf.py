from flask import render_template
from weasyprint import HTML


def export_pdf(template, data):
    html = render_template(template, **data)
    return HTML(string=html).write_pdf()
