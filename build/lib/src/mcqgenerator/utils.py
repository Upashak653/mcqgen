import os 
import json
import traceback
import PyPDF2

def read_file(file):
    if file.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ""   
    elif file.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception("Unsupported file format. Please provide a .pdf or .txt file.")

def get_data(quiz_str):
    try:
        quiz_dict= json.loads(quiz_str)
        quiz_table_data=[]

        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options = " || ".join(
                [
                    f"{option}:-> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            correct=value["correct"]
            quiz_table_data.append(
                {
                    "mcq": mcq,
                    "options": options,
                    "correct": correct
                }
            )
    except Exception as e:
        print(f"Error parsing quiz data: {e}")
        return False
    