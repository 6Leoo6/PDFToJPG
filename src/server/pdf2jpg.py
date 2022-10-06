from shutil import rmtree
from os import mkdir
from zipfile import ZipFile

import fitz


async def convertPDF(file):
    #Reseting the temp folder
    rmtree('./server/temp/')
    mkdir('./server/temp/')

    #Defineing basic names
    name = file.filename[:-4]
    pdf_name = f'./server/temp/{name}.pdf'
    zip_name = f'./server/temp/{name}.zip'

    #Writing the pdf into a temporary file so we can open it later
    with open(pdf_name, 'wb') as pdf:
        pdf.write(await file.read())

    #Openin the pdf file
    doc = fitz.open(pdf_name)
    with ZipFile(zip_name, 'w') as zipObj:
        #Looping through the pages of the pdf
        for i in range(doc.page_count):
            #Saving the pages as jpeg files
            doc.load_page(i).get_pixmap().save(
                f'./server/temp/{name}_{str(i)}.jpeg')
            #Adding the pages to a zip archive
            zipObj.write(
                f'./server/temp/{name}_{str(i)}.jpeg', f'{name}_{str(i)}.jpeg')
    #Getting the zip in a byte form
    with open(zip_name, 'rb') as z:
        zip_bytes = z.read()

    return zip_bytes
