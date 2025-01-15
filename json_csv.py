import json
import logging
from os import getenv
import csv

# Constant
PDF_DIRECTORY = "pdf"
DATABASE_FILE = "database/data.json"


def write_csv(data, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for question in data:
            writer.writerow([question["question"], question["answer"]])


def main():
    quiz_name = input("Quiz name: ")

    with open(DATABASE_FILE, "r") as database:
        try:
            data = json.load(database)
        except json.decoder.JSONDecodeError:
            with open("database/data.json", "w") as database:
                data = {'api_key': getenv('OPENAI_API_KEY'), 'quiz': {}}
                json.dump(data, database)

        if data['api_key'] == "":
            pass
        else:
            api_key = data['api_key']

    user_input = {
        "quiz_name": quiz_name,
        "questions": [
            {"question": "What is the primary role of project managers in project integration management?",
             "answer": "To coordinate all other knowledge areas throughout a project's life cycle."},
            {"question": "What are the main processes in project integration management?",
             "answer": "Developing the project charter, developing the project management plan, directing and "
                       "managing project work, monitoring and controlling project work, performing integrated change "
                       "control, and closing the project or phase."},
            {"question": "What are the methods for selecting projects?",
             "answer": "Focusing on broad organizational needs, categorizing information technology projects, "
                       "performing net present value or other financial analyses, using a weighted scoring model, "
                       "and implementing a balanced scorecard."},
            {"question": "What is the purpose of net present value (NPV) analysis in project selection?",
             "answer": "To calculate the expected net monetary gain or loss from a project by discounting all "
                       "expected future cash inflows and outflows to the present point in time."},
            {"question": "What is a key consideration in categorizing IT projects?",
             "answer": "Project's impetus, time window, and priority."},
            {"question": "What are the criteria for selecting projects based on broad organizational needs?",
             "answer": "Need, funding, and will."},
            {"question": "What is the role of a weighted scoring model in project selection?",
             "answer": "To provide a systematic process for selecting projects based on many criteria by assigning "
                       "weights to each criterion and multiplying them by the scores for each project."},
            {"question": "What is the purpose of implementing a balanced scorecard in project management?",
             "answer": "To help select and manage projects that align with business strategy by aligning business activities to strategy, improving communications, and monitoring performance against strategic goals."},
            {"question": "What are the inputs for developing a project charter?",
             "answer": "Business case, benefits management plan, agreements, enterprise environmental factors, and organizational process assets."},
            {"question": "What are the main elements of a project management plan?",
             "answer": "Introduction/overview, project organization, management and technical processes, work to be done, schedule and budget information, and references to other project planning documents."},
            {"question": "What is the purpose of monitoring and controlling project work?",
             "answer": "To collect, measure, and disseminate performance information and to manage and control changes to the project."},
            {"question": "What is the main function of a project management plan?",
             "answer": "To guide project execution by coordinating all project planning documents."},
            {"question": "What are the main inputs for closing a project or phase?",
             "answer": "Project charter, project management plan, project documents, accepted deliverables, business documents, agreements, procurement documentation, and organizational process assets."},
            {"question": "What are the main tools and techniques for monitoring and controlling project work?",
             "answer": "Expert judgment, data analysis, and meetings."},
            {"question": "What is the primary objective of project integration management?",
             "answer": "To ensure that all the elements of a project are properly coordinated and integrated."}
        ]

    }

    new_quiz = {'quiz_name': quiz_name, "questions": user_input["questions"]}
    with open(DATABASE_FILE, "r") as database:
        data = json.load(database)
        data['quiz'] = new_quiz
        with open(DATABASE_FILE, "w") as database:
            json.dump(data, database)

    user_input = user_input
    csv_data = user_input['questions']
    write_csv(csv_data, 'data.csv')

    logging.info("Finished generating csv file")


if __name__ == "__main__":
    main()
