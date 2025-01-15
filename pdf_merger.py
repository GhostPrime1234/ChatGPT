from os import path, listdir
from pathlib import Path
from PyPDF2 import PdfMerger
from natsort import natsorted
import sys


def merge_pdfs(folder_path: str, output_file: str, subject_code: str):
    merger = PdfMerger()

    # Get a list of all PDF files in the folder
    folder_path = Path(folder_path)
    files_in_path = [
        path.join(folder_path, file) 
        for file in listdir(folder_path)
        if file.endswith(".pdf") and file.startswith(subject_code)
    ]
    # sort files in alphabetical order
    for file in natsorted(files_in_path):
        print(file)

        # join filename with folder path
        file_path = path.join(file)

        # append file path to merger list
        merger.append(file_path)

    # Redirect stderr to null to ignore errors
    # old_stderr = sys.stderr
    # sys.stderr = open("nul", 'w')

    # Write the merged PDF to the output file
    merger.write(output_file)
    merger.close()

    # Restore stderr
    # sys.stderr.close()
    # sys.stderr = old_stderr


if __name__ == "__main__":
    m_folder_path = "pdf_merge/"
    subject_name = input("What subject are you merging?")
    m_output_file = f"{subject_name}-Merged_pdf.pdf"
    try:
        merge_pdfs(m_folder_path, m_output_file, subject_name)
    except Exception as error:
        print(f"Error: {error}; Error type {error.__class__.__name__}")
    print("merged pdf been created.")
