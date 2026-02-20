import json
import PyPDF2
import traceback


def read_file(file):
    """
    Reads an uploaded file and returns its text content.
    Supports PDF (.pdf) and plain text (.txt) files.
    """
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading PDF file: " + str(e))

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("Unsupported file format. Please upload a PDF or TXT file.")


def get_table_data(quiz_str):
    """
    Converts a quiz JSON string into a list of dicts suitable for a table.

    Each entry in the returned list contains:
        MCQ      - the question text
        a        - option a
        b        - option b
        c        - option c
        d        - option d
        Correct  - the correct answer key
    """
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for _key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = value["options"]
            correct = value["correct"]

            quiz_table_data.append(
                {
                    "MCQ": mcq,
                    "a": options.get("a"),
                    "b": options.get("b"),
                    "c": options.get("c"),
                    "d": options.get("d"),
                    "Correct": correct,
                }
            )

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
