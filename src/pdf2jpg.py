from io import BytesIO
from zipfile import ZipFile
import fitz


async def convertPDF(file):
    file_bytes = await file.read()
    zip_bytes = BytesIO()

    #Loading the bytes into the pdf handler
    doc = fitz.open('pdf', file_bytes)

    #Providing the variable for the zip to be created in
    with ZipFile(zip_bytes, 'w') as zip:
        # Looping through the pages of the pdf
        for i in range(doc.page_count):
            #Getting the page as an img
            page_bytes = doc.load_page(i).get_pixmap().tobytes('jpg')

            #Adding the current page to the zip
            zip.writestr(f'{file.filename}_{i}.jpg', page_bytes)
    return zip_bytes.getvalue()


def testConvertPDF(fname):
    with open(fname, 'rb') as f:
        file_bytes = f.read()

    zip_bytes = BytesIO()

    #Loading the bytes into the pdf handler
    doc = fitz.open('pdf', file_bytes)

    #Providing the variable for the zip to be created in
    with ZipFile(zip_bytes, 'w') as zip:
        # Looping through the pages of the pdf
        for i in range(doc.page_count):
            #Getting the page as an img
            page_bytes = doc.load_page(i).get_pixmap().tobytes('jpg')

            #Adding the current page to the zip
            zip.writestr(f'test_{i}.jpg', page_bytes)
    print(zip.filelist)
    with open(fname.replace('.pdf', '.zip'), 'wb') as f:
        f.write(zip_bytes.getbuffer())

if __name__ == '__main__':
    testConvertPDF(r"")