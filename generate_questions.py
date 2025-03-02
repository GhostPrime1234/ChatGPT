from csv import QUOTE_MINIMAL
import pandas as pd
import logging
from os import getenv, path
import openai
import tiktoken


class Logger:
    @staticmethod
    def setup(log_file: str = None) -> None:
        logging.basicConfig(level=logging.INFO, filename=log_file, filemode='a',
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.getLogger('openai').setLevel(logging.WARNING)


class MarkdownScraper:
    @staticmethod
    def scrape(markdown_path: str, max_tokens: int = 16000) -> str:
        enc = tiktoken.get_encoding("cl100k_base")
        text, token_total = "", 0
        try:
            with open(markdown_path, 'r', encoding='utf-8') as file:
                for line in file:
                    tokens = enc.encode(line)
                    token_total += len(tokens)
                    if token_total > max_tokens:
                        break
                    text += line
        except FileNotFoundError:
            logging.error(f"File not found: {markdown_path}")
        return text


class QuizGenerator:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate(self, num_questions: int, facts: str) -> str:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content":   f"You are a quiz creator. Please create up to {num_questions} hard quiz questions based on the concepts from the following lecture slides.\n"
                                                    "Respond in CSV format with two columns: 'question' and 'answer'. "
                                                    "Ensure that all punctuation, including apostrophes, is correctly formatted. For any code snippets or syntax, use single backticks ( ` ) for clarity. "
                                                    "Do **not** include a header row, column names, or extra punctuation in your response. "
                                                    "Each question and answer pair should be on a new line, properly separated.\n\n"
                                                    "Example:\n"
                                                    "How many countries are in the world?|95 countries\n"
                                                    "How many planets are in the solar system?|8 planets\n"},
                    {"role": "user", "content": f"Lecture slides: {facts}"},
                ],
                temperature=0.6
            )
            logging.info(f"Total tokens used: {response.usage.total_tokens}")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Failed to generate quiz: {e}")
            return ""


class FileManager:
    def __init__(self, filename: str):
        self.filename = filename

    def write_csv(self, content: str) -> None:
        try:
            # Parse the content and split into rows and columns
            lines = content.strip().split('\n')
            data = [line.split('|', 1) for line in lines]
            
            # Create a DataFrame
            df = pd.DataFrame(data, columns=['question', 'answer'])
            
            # Save DataFrame to CSV
            df.to_csv(self.filename, index=False, quoting=QUOTE_MINIMAL, header=False, escapechar='\\', encoding='utf-8')
            logging.info(f"Data written to {self.filename} successfully.")
        except Exception as e:
            logging.error(f"Failed to write CSV with pandas: {e}")

    def truncate(self) -> None:
        try:
            open(self.filename, mode='w').close()
        except Exception as e:
            logging.error(f"Failed to truncate file: {e}")


class InputHandler:
    @staticmethod
    def get_valid_directory(prompt: str, base_path: str = "./notes/") -> str:
        while True:
            user_input = input(prompt)
            file_path = path.join(base_path, user_input)
            if path.exists(file_path):
                return file_path
            logging.error(f"{file_path} does not exist.")

    @staticmethod
    def get_numeric_function(prompt: str, default: int = None) -> int:
        while True:
            user_input = input(prompt).strip()
            if user_input == "":
                return default
            if user_input.isdigit():
                return int(user_input)
            logging.error(f"{user_input} is not a valid number.")

    @staticmethod
    def get_string_argument(prompt: str, default: str = None) -> str:
        user_input = input(prompt).strip()
        return user_input if user_input else default


class QuizApp:
    DATABASE_FILE = "data.csv"

    def __init__(self):
        Logger.setup()
        self.api_key = getenv("OPENAI_API_KEY") #or input("Enter your OpenAI API key: ")
        self.file_manager = FileManager(self.DATABASE_FILE)

    def run(self):
        source = InputHandler.get_valid_directory("Enter the markdown file name (e.g., notes.md): ")
        text = MarkdownScraper.scrape(source)

        num_questions = InputHandler.get_numeric_function("How many questions do you want? (default: 20): ", 20)

        generator = QuizGenerator(self.api_key)
        quiz = generator.generate(num_questions, text)

        self.file_manager.truncate()
        self.file_manager.write_csv(quiz)
        logging.info(f"Finished generating {self.DATABASE_FILE}")


if __name__ == "__main__":
    app = QuizApp()
    app.run()
