from pytesseract import image_to_string, pytesseract
from pathlib import Path
import pyperclip
from pdf2image import exceptions, convert_from_path
from concurrent.futures import ThreadPoolExecutor, as_completed

pytesseract.tesseract_cmd = r"C:\Users\michael\AppData\Local\Programs\Tesseract-OCR"


def clear_summary_file():
    with open("summary.md", "w") as file:
        file.truncate()


def ocr_image(image):
    return image_to_string(image)


def process_images(pdf_file):
    """Split given pdf into specified chunks."""
    # Ask for optional page range
    page_range = input("Enter page range to process (e.g., 2-5) or press Enter to process the entire PDF: ").strip()
    if page_range:
        try:
            start_str, end_str = page_range.split("-")
            start_page = int(start_str)
            end_page = int(end_str)
        except Exception as e:
            print(f"Invalid range entered ({e}). Processing entire PDF.")
    # Open the PDF file
    images = convert_from_path(pdf_file, dpi=300, first_page=start_page, last_page=end_page)
    total_pages = len(images)
    print(f"PDF has {total_pages} pages.")

    # Ask for optional page range

    
    extracted_text_list = []

    with ThreadPoolExecutor() as executor:
        future_to_image = {executor.submit(ocr_image, image): image for image in images}
        for future in as_completed(future_to_image):
            image = future_to_image[future]
            try:
                extracted_text_list.append(future.result())
            except Exception as e:
                print(f"Error processing an image - {e}")

    extracted_text = "".join(extracted_text_list)
    print(extracted_text)

    user_headings = input("Please enter the headings that you want the notes to be created under separated by a comma: ").split(",")
    headings_list = [heading.strip() for heading in user_headings]

    chatgpt_input = ("You are a note-taking assistant. Create comprehensive notes that thoroughly explain all the "
                     "content taught from the lecture slides under each heading using the headings given here, "
                     f"ensuring all headings thoroughly explain all of the topics: {headings_list}. "
                     "If the headings are not included, select appropriate headings from the lecture slides that "
                     "will cover all of the topics. Include detailed explanations, code examples, formulas, "
                     "and diagrams where necessary. Ensure the notes cover all the material presented in the lecture "
                     f"and are clear and easy to understand. Respond only in markdown format.\ntext:\n\n{extracted_text}")
    pyperclip.copy(chatgpt_input)


def main():
    try:
        pdf_name = input("Name of pdf (CSIT121.pdf): ")
        current_directory = Path.cwd()
        relative_path = Path(f"./pdf/{pdf_name}")
        absolute_path = current_directory / relative_path
        process_images(absolute_path)
    except KeyboardInterrupt:
        print("Exiting program")
        raise SystemExit(0)
    except FileNotFoundError as error:
        print(f"File not found: {error}")
    except exceptions.PDFPageCountError:
        print("Please re-enter pdf name")


if __name__ == '__main__':
    main()
