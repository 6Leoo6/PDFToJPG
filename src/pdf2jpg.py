from io import BytesIO
from zipfile import ZipFile
import fitz

import boto3
from random import choice
from string import ascii_letters, digits


async def convertPDF(file):
    file_bytes = await file.read()
    zip_bytes = BytesIO()

    # Loading the bytes into the pdf handler
    doc = fitz.open('pdf', file_bytes)

    # Providing the variable for the zip to be created in
    with ZipFile(zip_bytes, 'w') as zip:
        # Looping through the pages of the pdf
        for i in range(doc.page_count):
            # Getting the page as an img
            page_bytes = doc.load_page(i).get_pixmap(dpi=96).tobytes('jpg')

            # Adding the current page to the zip
            zip.writestr(f'{file.filename}_{i}.jpg', page_bytes)
    zip_bytes.seek(0)
    return zip_bytes.getvalue()