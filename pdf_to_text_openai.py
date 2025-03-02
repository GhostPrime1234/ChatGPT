import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count, getenv
from pathlib import Path
from typing import List

import pytesseract
from openai import OpenAI, OpenAIError
from pdf2image import convert_from_path
from PIL import Image


class LoggerSetup:
    @staticmethod
    def setup_logging(summary_file_path: Path) -> None:
        """Configures logging for the program."""
        with open(summary_file_path, "w") as log_file:
            log_file.truncate(0)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.getLogger("pdf2image").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)

    @staticmethod
    def log_error(message: str) -> None:
        """Logs an error message."""
        logging.error(message)

    @staticmethod
    def log_info(message: str) -> None:
        """Logs an info message."""
        logging.info(message)


class OCRProcessor:
    def __init__(self, max_concurrent_tasks: int = None) -> None:
        """Initializes the OCRProcessor with a specified number of concurrent tasks."""
        self.max_concurrent_tasks = max_concurrent_tasks or cpu_count()
        self.logger_setup = LoggerSetup()

    @staticmethod
    def ocr_image(image: Image.Image) -> str:
        """Performs OCR (Optical Character Recognition) on the given image."""
        return pytesseract.image_to_string(image, lang="eng")

    def process_pdf(self, pdf_file: Path) -> str:
        """Processes OCR and generates text from a PDF file."""
        try:
            # Ask the user for an optional page range
            page_range = input(
                "Enter page range to process (e.g., 2-5) or press Enter to process the entire PDF: "
            ).strip()
            convert_kwargs = {}

            if page_range:
                try:
                    start_str, end_str = page_range.split("-")
                    convert_kwargs["first_page"] = int(start_str)
                    convert_kwargs["last_page"] = int(end_str)
                except Exception as error:
                    LoggerSetup.log_error(f"Invalid range entered ({error}). Processing entire PDF.")

            images = convert_from_path(pdf_file, **convert_kwargs)
            text = ""

            with ThreadPoolExecutor(max_workers=self.max_concurrent_tasks) as executor:
                batch_futures = [executor.submit(self.ocr_image, image) for image in images]

                for future in as_completed(batch_futures):
                    extracted_text = future.result()
                    text += extracted_text + "\n"

            return text

        except FileNotFoundError as error:
            LoggerSetup.log_error(f"Error processing PDF {pdf_file}: {error}.")
        except Exception as error:
            LoggerSetup.log_error(f"An unexpected error occurred: {error}.")
        return ""


class TextProcessor:
    def __init__(self) -> None:
        """Initializes the TextProcessor."""

    @staticmethod
    def generate_notes(client: OpenAI, facts: str) -> str:
        """Generates notes by interacting with a chat-based language model."""
        user_headings = input(
            "Please enter the headings that you want the notes to be created under separated by a comma: "
        ).split(",")
        user_headings = ""
        headings_list = [heading.strip() for heading in user_headings]

        # Modified prompt for detailed notes with subheadings
        gpt_input = (
            "You are a note-taking assistant. Create detailed notes under the following main headings: "
            f"{headings_list}. For each heading, generate subheadings where appropriate to ensure all key topics "
            "are covered in a structured manner. Provide thorough explanations, examples, code snippets, formulas, "
            "and diagrams as needed. Organize the content logically, ensuring that each subheading is relevant and "
            "elaborates on the topics mentioned in the lecture. Present the notes in markdown format."
        )

        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(
                    client.chat.completions.create,
                    model="gpt-4o-mini",
                    temperature=0.6,
                    messages=[
                        {"role": "system", "content": gpt_input},
                        {"role": "user", "content": f"Lecture slides: {facts}"},
                    ],
                )
                response = future.result()
            LoggerSetup.log_info(f"Total tokens used: {response.usage.total_tokens}")
            return response.choices[0].message.content
        except OpenAIError as error:
            LoggerSetup.log_error(f"OpenAI error: {error}")
            return "Error generating notes"


class PDFProcessor:
    SUMMARY_FILE_PATH = Path("summary.md")
    PDF_DIRECTORY = Path("pdf")
    SUMMARY_DIRECTORY = Path("summary")
    MAX_CONCURRENT_TASKS = cpu_count()  # Limit concurrent tasks to avoid overwhelming resources
    RETRY_ATTEMPTS = 3  # Number of retry attempts for API rate limiting

    def __init__(self) -> None:
        """Initializes the PDFProcessor."""
        LoggerSetup.setup_logging(self.SUMMARY_FILE_PATH)

    def list_pdf_files(self) -> List[Path]:
        """Lists all PDF files in the 'pdf' directory."""
        return [file for file in self.PDF_DIRECTORY.glob("*.pdf")]

    def process_pdf_files(self) -> None:
        """Processes PDF files by OCR and generates summaries."""
        try:
            # Ensure teh summary folder exists
            self.SUMMARY_DIRECTORY.mkdir(parents=True, exist_ok=True)

            pdf_files = self.list_pdf_files()
            if not pdf_files:
                LoggerSetup.log_error("No PDF files found in the 'pdf' directory.")
                return

            # Let the user select a file to process
            selected_pdf = self.prompt_user_for_pdf_selection(pdf_files)
            try:
                # Process PDF file
                client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
                ocr_processor = OCRProcessor(self.MAX_CONCURRENT_TASKS)
                # text = ocr_processor.process_pdf(pdf_path)
                text = ocr_processor.process_pdf(selected_pdf)

                # Generate notes
                text_processor = TextProcessor()
                notes = text_processor.generate_notes(client=client, facts=text)

                # Writing to summary file
                summary_file = self.SUMMARY_DIRECTORY / f"{selected_pdf.stem}_summary.md"
                summary_file.write_text(notes, encoding="utf-8")
                LoggerSetup.log_info(f"Summary written to: {summary_file}")
                # self.SUMMARY_FILE_PATH.write_text(notes, encoding='utf-8')
            except Exception as inner_error:
                LoggerSetup.log_error(f"Error processing PDF {selected_pdf}: {inner_error}.")

        except KeyboardInterrupt:
            LoggerSetup.log_info("\nExiting program due to user interruption.")
        except FileNotFoundError as error:
            LoggerSetup.log_error(f"PDF file '{selected_pdf}' not found: {error}")
        except Exception as error:
            LoggerSetup.log_error(f"An unexpected error occurred: {error}")

    def prompt_user_for_pdf_selection(self, pdf_files: List[str]) -> Path:
        """Prompts the user to select a PDF file from the list."""
        for idx, pdf_file in enumerate(pdf_files, 1):
            print(f"{idx}. {pdf_file.name}")

        while True:
            selection = int(input("Select the number of the file to process: "))
            if 1 <= selection <= len(pdf_files):
                return pdf_files[selection - 1]
            else:
                LoggerSetup.log_error(f"Invalid selection. Please enter a number between 1 and {len(pdf_files)}.")


if __name__ == "__main__":
    try:
        processor = PDFProcessor()
        processor.process_pdf_files()
    except ValueError:
        print("An unexpected error occurred")
