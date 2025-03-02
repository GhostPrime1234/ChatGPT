from pypdf import PdfReader
from pandas.io.clipboard import copy

user_input = input("Enter pdf file name: ")

reader = PdfReader("pdf/{0}.pdf".format(user_input))

text = ""

start_page = int(input("Enter start page number: "))
end_page = int(input("Enter end page number: "))

for index in range(start_page - 1, end_page):
    text += reader.pages[index].extract_text() + "\n"

copy(text)
