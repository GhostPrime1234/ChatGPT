import logging
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from pyperclip import copy
from time import sleep

import httpx
import ollama
import psutil
from pdf2image import convert_from_path
from pytesseract import image_to_string


class PDFProcessor:
    def __init__(self):
        self.SUMMARY_FILE_PATH = Path("summary.md")
        self.PDF_DIRECTORY = Path("pdf")
        self.pdf_name = ""
        self.MAX_CONCURRENT_TASKS = os.cpu_count()
        self.RETRY_ATTEMPTS = 3
        self.setup_logging()
        self.port = 11434
        self.start_ollama_serve()

    def setup_logging(self):
        with open(self.SUMMARY_FILE_PATH, "w") as file:
            file.truncate(0)

        logging.basicConfig(level=logging.INFO)
        logging.getLogger('pdf2image').setLevel(logging.WARNING)

    def start_ollama_serve(self) -> bool | None:
        def __is_port_in_use(port):
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    return True
            return False

        try:
            if __is_port_in_use(self.port):
                # logging.error(f"Port {self.port} is already in use.")
                return

            process = subprocess.Popen(["ollama", "serve", "--port", str(self.port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sleep(1)  # Allow some time for the subprocess to start
            if process.poll() is None:
                logging.info("ollama serve started successfully.")
            else:
                stdout, stderr = process.communicate()
                logging.error(f"Failed to start ollama serve: {stderr.decode()}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while starting ollama serve: {e}")

    @staticmethod
    def ocr_image(image) -> str:
        return image_to_string(image, lang='eng')

    def process_pdf(self, pdf_file: Path) -> str:
        try:
            images = convert_from_path(pdf_file)
            text = ""

            with ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_TASKS) as executor:
                batch_size = self.MAX_CONCURRENT_TASKS + 1
                for index in range(0, len(images), batch_size):
                    batch_images = images[index:index + batch_size]
                    batch_futures = [executor.submit(self.ocr_image, image) for image in batch_images]

                    for future in as_completed(batch_futures, timeout=60):  # Add a timeout
                        try:
                            extracted_text = future.result()
                            text += extracted_text + "\n"
                        except TimeoutError:
                            logging.error("OCR task timed out.")

            return text

        except FileNotFoundError as error:
            logging.error(f"Error processing PDF {pdf_file}: {error}.")
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}.")

    @staticmethod
    def chunk_text(text: str, max_words: int) -> list[str]:
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(' '.join(current_chunk + [word])) <= max_words:
                current_chunk.append(word)
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def generate_notes(self, facts: str) -> str:
        try:
            user_headings = input(
                "Please enter the headings that you want the notes to be created under separated by a comma: "
            ).split(",")
            headings_list = [heading.strip() for heading in user_headings]
            print(headings_list)
            gpt_input = (
                "You are a note-taking assistant. Create comprehensive notes that thoroughly explain all the "
                "content taught from the lecture slides under each heading using the headings given here: "
                f"{headings_list} If headings aren't included just select headings from lectures that will explain "
                f"all of the topics. Include detailed explanations, code examples, formulas, and diagrams"
                "where necessary. Ensure the notes cover all the material presented in the lecture and are clear and "
                "easy to understand. Respond only in markdown format."
            )

            for attempt in range(1, self.RETRY_ATTEMPTS + 1):
                try:
                    with ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_TASKS) as executor:
                        future = executor.submit(
                            ollama.chat,
                            model='llama3',
                            messages=[
                                dict(role='system', content=gpt_input),
                                dict(role='user', content=f'Lecture slides: {facts}')
                            ]
                        )
                    response = future.result(timeout=60)  # Add a timeout
                    logging.info(response["message"]["content"])
                    return response['message']['content']
                except httpx.ConnectError as ce:
                    logging.error(f"Connection error (attempt {attempt}/{self.RETRY_ATTEMPTS}): {ce}")
                    if attempt < self.RETRY_ATTEMPTS:
                        logging.info("Retrying in 5 seconds...")
                        sleep(5)
                    else:
                        raise ValueError("Failed to connect after retrying") from ce
                except TimeoutError:
                    logging.error(f"Ollama chat task timed out on attempt {attempt}.")
                except Exception as e:
                    logging.error(f"Error in generating notes: {e}")
                    raise ValueError("Error in generating notes")

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise ValueError("Error in generating notes")

    def process_pdf_files(self):
        try:
            self.pdf_name = self.prompt_user_for_pdf_name()
            pdf_path: Path = self.PDF_DIRECTORY / self.pdf_name

            ocr_text = self.process_pdf(pdf_path)
            notes = self.generate_notes(ocr_text)

            with open(self.SUMMARY_FILE_PATH, mode='a', encoding='utf-8') as file:
                file.write(notes)

            copy(notes)

        except KeyboardInterrupt:
            logging.info("\nExiting program due to user interruption.")
        except FileNotFoundError as error:
            logging.error(f"PDF file '{self.pdf_name}' not found: {error}")
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}, error type: {type(error)}")

    def prompt_user_for_pdf_name(self):
        while True:
            sleep(0.1)
            self.pdf_name = input("Enter the name of the PDF file (CSIT121.pdf): ")
            pdf_path = self.PDF_DIRECTORY / self.pdf_name
            if pdf_path.exists():
                return self.pdf_name
            else:
                logging.error(f"The file '{self.pdf_name}' does not exist. Please try again.")
                sleep(0.1)


if __name__ == '__main__':
    try:
        processor = PDFProcessor()
        processor.process_pdf_files()
    except ValueError:
        print("An unexpected error occurred")
