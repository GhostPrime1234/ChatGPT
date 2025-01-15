from pypdf import PdfReader
from pandas.io.clipboard import copy

user_input = input("Enter pdf file name: ")

reader = PdfReader("pdf/{0}.pdf".format(user_input))

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"

copy(text)
