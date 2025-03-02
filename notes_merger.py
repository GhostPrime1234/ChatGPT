from os import listdir, path
from natsort import natsorted


def merge_notes(folder_path, output_file):
    markdown_files = [path.join(folder_path, file) for file in listdir(folder_path) if file.endswith(".md")]

    with open(output_file, "a") as output_file:
        output_file.truncate(0)
        for markdown_file in natsorted(markdown_files):
            with open(markdown_file, 'r') as file:
                file_content = file.read()
                output_file.write(file_content + "\n")

    if markdown_files:
        print(f"Markdown files merged into {folder_path}")
    else:
        print("No Markdown files found in the directory.")


if __name__ == "__main__":
    m_folder_path = "pdf/"
    m_output_file = "notes_summary.md"
    merge_notes(m_folder_path, m_output_file)
