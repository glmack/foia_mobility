import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import tabula

filepath = '/Users/lee/Documents/code/foia_mobility/TRip_Relocation.pdf'
# doc = convert_from_path(filepath)
# path, filename = os.path.split(filepath)
# filebasename, filextension = os.path.splitext(filename)

# for page_number, page_data in enumerate(doc):
#     txt = pytesseract.image_to_string(Image.fromarray(page_data)) #.encode("utf-8")
#     print("Page # {} - {}".format(str(page_number),txt))

#--------
# response = requests.get()

dfs = tabula.read_pdf(filepath, multiple_tables=True, pages='all') # stream=True
dfs2 = tabula.read_pdf(filepath, multiple_tables=True, pages='all', stream='True')
x = dfs[16].T