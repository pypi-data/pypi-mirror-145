__version__ = "0.1.3"

import click
import os
import re
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfreader import SimplePDFViewer


regexexample = "(?:Entnahmestelle)((.+)((?:\n.+)+))(?:Entnahmezeit)"
regexexample_customer_id = "K\/\d{5}\s"


def normalize_filename(filename):
    keepcharacters = ('.', '-', '_')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


@click.command()
@click.argument("input_file", nargs=1, type=click.File("rb"))
@click.argument("output_path", nargs=-1, type=click.Path(exists=True))
@click.option("-c", "--compact", default=False, is_flag=True, help="Uses compact file name, like <SPLITPDF_IDENTIFIER_REGEX>.pdf")
def split_pdf(input_file, output_path, compact):
    if output_path:
        output_path = output_path[0]
    else:
        output_path = os.path.dirname(input_file.name)
    identifier_regex = os.getenv("SPLITPDF_IDENTIFIER_REGEX")
    print(identifier_regex)
    if identifier_regex:
        identifier_regex = fr"{identifier_regex}"
        identifier_pattern = re.compile(identifier_regex, re.IGNORECASE)
    fname = os.path.splitext(os.path.basename(input_file.name))[0]
    pdf = PdfFileReader(input_file)
    pdfviewer = SimplePDFViewer(input_file)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        identifier = ""
        if identifier_regex:
            pdfviewer.navigate(page + 1)
            pdfviewer.render()
            canvas = pdfviewer.canvas
            canvas.text_content
            page_text = pdf.getPage(page).extractText()
            match = identifier_pattern.search(page_text)
            if match:
                identifier = "{}".format(match.group().strip())
        identifier = identifier.replace("/", "-")
        if compact:
            if not identifier:
                identifier = "page{0}".format(page + 1)
            output_filename = "{}.pdf".format(normalize_filename(identifier))
        else:
            output_filename = "{}_{}_p{}.pdf".format(fname, normalize_filename(identifier), page + 1)
        output_file_path = os.path.join(click.format_filename(output_path), output_filename)
        with open(output_file_path, "wb") as out:
            pdf_writer.write(out)
        print("Created: {}".format(output_file_path))


if __name__ == "__main__":
    split_pdf()
